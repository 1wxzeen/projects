# detecting temposhifts with madmom  – stable clustering version

import pathlib, numpy as np, matplotlib.pyplot as plt
from itertools import groupby
from scipy.signal import medfilt
from madmom.features.beats import RNNBeatProcessor, DBNBeatTrackingProcessor

AUDIO_FILE    = "kurai ms (katai mix).mp3"
BPM_MEDFILT   = 9
MIN_BPM_DELTA = 8
MIN_SEG_SEC   = 1.0

print("running madmom…")
proc_rnn = RNNBeatProcessor()
proc_dbn = DBNBeatTrackingProcessor(fps=100, online=False)
beats    = proc_dbn(proc_rnn(AUDIO_FILE))  

if len(beats) < 4:
    raise RuntimeError("Madmom found <4 beats – check the audio/ffmpeg.")

# 1. instantaneous BPM from successive beat intervals
inst_bpm = 60.0 / np.diff(beats)
inst_times = beats[:-1]

# median-filter to kill ping-pong jitter
if len(inst_bpm) >= BPM_MEDFILT:
    inst_bpm = medfilt(inst_bpm, kernel_size=BPM_MEDFILT)

# 2. cluster consecutive frames by rounded BPM
rounded = inst_bpm.round().astype(int)
segments = []          # (start_time, end_time, bpm)
for k, grp in groupby(range(len(rounded)), key=lambda i: rounded[i]):
    idx = list(grp)
    t0, t1 = inst_times[idx[0]], inst_times[idx[-1]]
    if (t1 - t0) >= MIN_SEG_SEC:
        segments.append((t0, t1, k))

# 3a. merge if adjacent bpm difference small
merged = [segments[0]]
for seg in segments[1:]:
    prev_bpm = merged[-1][2]
    if abs(prev_bpm - seg[2]) < MIN_BPM_DELTA:
        # extend previous
        merged[-1] = (merged[-1][0], seg[1], prev_bpm)
    else:
        merged.append(seg)

# 3b. fix 2x/.5x illusions “half-time / double-time” resolver
for i in range(1, len(merged)):
    prev_bpm = merged[i-1][2]
    cur_bpm  = merged[i][2]
    if abs(cur_bpm - 2*prev_bpm) < 3:          # 2x faster?
        merged[i] = (merged[i][0], merged[i][1], cur_bpm // 2)
    elif abs(2*cur_bpm - prev_bpm) < 3:        # .5x slower?
        merged[i] = (merged[i][0], merged[i][1], cur_bpm * 2)

# 4. tempo-shift times (skip first segment)
shift_times = [round(seg[0], 2) for seg in merged[1:]]
print("Detected tempo shifts (s):", shift_times)

# 5. plot
plt.figure(figsize=(12,4))
plt.plot(inst_times, inst_bpm, alpha=.4, label="Instant BPM")
for seg in merged:
    plt.hlines(seg[2], seg[0], seg[1], colors="darkorange", linewidth=3)
for t in shift_times:
    plt.axvline(t, color="red", ls="--", alpha=.7)
plt.title(f"{pathlib.Path(AUDIO_FILE).name} madmom BPM clusters using adjustedx1 new algorithm")
plt.xlabel("Time (s)"); plt.ylabel("Tempo (BPM)")
plt.legend(); plt.tight_layout(); plt.show()

# Ibrahim this model imo was only alright not super great just alright
# tbh i think we just need to go back to the drawing board 
# maybe some deepmodel integration can help ?