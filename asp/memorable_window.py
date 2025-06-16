#  loudest_window_wide_embed + chromaCQT.py
#  ---------------------------------------------------------------
# 1. CLAP  (loudest-8 s → 7x2 s hop-avg)             512 D
# 2. Tempogram  (z-scored)                             384 D
# 3. Spectral-contrast  <μ,σ>                          14 D
# 4. Δ-MFCC  (coeff 1-13) <μ,σ>                       24 D
# 5. Chroma-CQT  <μ,σ>                                 24 D  
#    ---------------------------------------------------------------
#                final vector (L2-normed)              958 D
#   weight mix:  0.7*CLAP  |  0.2*tempo  |  1.2*shape
#   where shape = [contrast 14  +  Δ-MFCC 24  +  chroma 24]
#  ---------------------------------------------------------------

import sys
import torch, torchaudio, librosa, numpy as np, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import silhouette_score
from transformers import ClapModel, ClapProcessor
from collections import Counter

# Insert file names here
# "Classname_songnumber : .mp3"
FILES = {
    "KTM_1" : "easterpink---windowtestcut.mp3",
    "KTM_2" : "idky---windowtestcut.mp3",
    "RUM_3" : "inмyeyeззз---windowtestcut.mp3",
    "KHYPR" : "closer---windowtestcut.mp3",
    "3.5 freestyle" : "3.5K FREESTYLE.mp3"
}
AUDIO_DIR = Path(".")

# ─── sanity check if all the files are presetnt ─────────────
missing    = []
duplicates = set()
seen       = set()

for tag, fn in FILES.items():
    fp = AUDIO_DIR / fn
    if not fp.is_file():
        missing.append(fn)
    if fn in seen:
        duplicates.add(fn)
    seen.add(fn)

print("\n─── File-loading sanity check ──────────────────────────────")
print(f"✓  {len(FILES) - len(missing)} of {len(FILES)} unique files located.")
if missing:
    print("  The following files were NOT found:")
    for m in missing:
        print("   ", m)
if duplicates:
    print("\n  Duplicate filename(s) referenced by multiple tags:")
    for d in duplicates:
        print("   ", d)
print("─────────────────────────────────────────────────────────────")

resp = input("\nProceed with feature extraction? [y/N]: ").strip().lower()
if resp != "y":
    print("Aborting at user request — nothing computed.")
    sys.exit(0)

# ─── CLAP backbone ─────────────────────────────────────────────
model_id = "laion/clap-htsat-unfused"
proc  = ClapProcessor.from_pretrained(model_id)
clap  = ClapModel.from_pretrained(model_id).to("cpu").eval()      # GPU → .to("cuda")

# ─── helpers ───────────────────────────────────────────────────
def loudest_window(path: Path, sr_tgt=48_000, win_sec=8, hop_ms=50):
    wav, sr = torchaudio.load(path)
    if sr != sr_tgt:
        wav = torchaudio.transforms.Resample(sr, sr_tgt)(wav); sr = sr_tgt
    y = wav.mean(0).numpy()
    hop = int(sr * hop_ms / 1000);  win = int(sr * win_sec)
    rms = librosa.feature.rms(y=y, hop_length=hop, frame_length=win).squeeze()
    s   = rms.argmax() * hop
    seg = wav[:, s:s+win]
    if seg.shape[1] < win:
        seg = torch.nn.functional.pad(seg, (0, win - seg.shape[1]))
    start_sec = s / sr
    return seg, sr, start_sec  # 🆕 return the loudest window start time

def mean_std(mat: np.ndarray):
    return np.concatenate([mat.mean(1), mat.std(1)])             # <μ|σ>

# ─── main embedding loop ───────────────────────────────────────
vecs = {}
log_rows = []  #  store logs for CSV
for tag, fn in FILES.items():
    wav8, sr, loudest_start = loudest_window(AUDIO_DIR / fn)
    log_rows.append({'tag': tag, 'filename': fn, 'start_sec': loudest_start})
    print(f"🔍  {tag}: loudest 8s starts at {loudest_start:.2f} sec in “{fn}”")

    # 1) CLAP (7  2-s chunks, 1-s hop)
    chunks = []
    for st in np.arange(0, 6.001, 1):            # 0‥6
        seg = wav8[:, int(sr*st):int(sr*(st+2))].mean(0).numpy()
        inp = proc(audios=seg, sampling_rate=sr, return_tensors="pt", padding=True)
        with torch.no_grad():
            chunks.append(clap.get_audio_features(**inp)[0])
    v_clap = torch.stack(chunks).mean(0).cpu().numpy()
    v_clap /= np.linalg.norm(v_clap) + 1e-9       # 512-D

    # 2) Tempogram (384-D)
    tmp  = librosa.feature.tempogram(y=wav8.mean(0).numpy(), sr=sr, hop_length=512)
    tmp  = (tmp - tmp.mean()) / (tmp.std() + 1e-9)
    v_tmp = tmp.mean(1);  v_tmp /= np.linalg.norm(v_tmp) + 1e-9

    # 3) Mel-spec in dB for downstream features
    S_db = librosa.power_to_db(
        librosa.feature.melspectrogram(y=wav8.mean(0).numpy(),
                                       sr=sr, n_mels=128, hop_length=512)
    )

    # 3a) Spectral-contrast (14-D)
    v_sc = mean_std(librosa.feature.spectral_contrast(S=S_db, sr=sr))

    # 3b) Δ-MFCC (24-D; coeff 1-13)
    mf   = librosa.feature.mfcc(S=S_db, sr=sr, n_mfcc=13)
    v_mfcc = mean_std(librosa.feature.delta(mf)[1:])             # skip coeff 0

    # 3c) Chroma-CQT (24-D)
    v_chr = mean_std(librosa.feature.chroma_cqt(y=wav8.mean(0).numpy(),
                                                sr=sr, hop_length=512))

    # z-score each shape sub-block
    for v in (v_sc, v_mfcc, v_chr):
        v -= v.mean();  v /= v.std() + 1e-9
    v_shape = np.concatenate([v_sc, v_mfcc, v_chr])
    v_shape /= np.linalg.norm(v_shape) + 1e-9

    # 4) Weighted fusion 958-D
    combo = np.concatenate([
        0.7 * v_clap,     # 512
        0.2 * v_tmp,      # 384
        1.2 * v_shape     # 62
    ])
    combo /= np.linalg.norm(combo) + 1e-9
    vecs[tag] = combo

# ─── cosine matrix + silhouette score ─────────────────────────
tags   = list(vecs)
mat    = cosine_similarity(np.vstack([vecs[t] for t in tags]))
df     = pd.DataFrame(mat, index=tags, columns=tags).round(3)

print("Trial 4.5")

print("\n Cosine similarity\n", df)

# global silhouette (uses genre = text before “_” for track name in FILES)
labels = [t.split('_')[0] for t in tags] # 'KTM' | 'RUM' | 'UGemo' etc
sil    = silhouette_score(np.vstack([vecs[t] for t in tags]),
                          labels, metric="cosine")
print("Label counts:", Counter(labels))
print(f"\n  Global silhouette score (−1 … +1):  {sil:.3f}")

# global silhoutte scores for this algo were pretty bad ngl
# means there's still room for algorithm optimization before implementing MRT/deepmodels

