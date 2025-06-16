This repo contains experimental tempo-shift detection and highlight extraction algorithms applied to underground music datasets.

## Components

- madmom_tempogram.py: Segment songs into tempo regions using Madmom and custom BPM clustering.
    - minor edge case issues with madmom tempogram generation need to be fixed via some form of optimization that dillutes these issues
- memorable_window.py: Identify the likely "highlight" portion of a song using onset + RMS analysis.
    - This feature in its current iteration has not given amazing results; need to implement a deep model like MusicCLIP/MERT/MVT to better identify the 30s segments most representative of each track.
- /outputs folder: example tempo plots + output data with annotations.

## Notes

This was part of a self-directed project that my friend and I started to design better music discovery algorithms for non-mainstream genres like hyperpop, maoricore, rage-rap, etc. I have hit a roadblock in analysis and am currently debugging, so my work right now probably doesn't look like a ChatGPT for music.

## AI-assisted development

Portions of this code were prototyped with assistance from large language models (Claude AI, ChatGPT), especially for:
- Translating signal processing concepts into initial Python code skeletons
- Debugging edge cases in tempo clustering logic
- Drafting the initial structure of the highlight extraction method

All model outputs were manually reviewed, tested, iterated, and integrated by me and my partner was we continue working on this project. 

This approach allowed me to rapidly experiment applied signal processing and music analysis pipelines that would have otherwise taken much longer, while still allowing me the opportunity understand the underlying algorithms and tune hyperparameters for my target genre dataset.
