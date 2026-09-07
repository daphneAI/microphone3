---
title: Microphone Spike Detector
emoji: 🎤
colorFrom: blue
colorTo: green
sdk: gradio
app_file: app.py
pinned: false
---

# Microphone Spike Detector

This Space runs a lightweight Gradio app that captures microphone input from the browser, analyzes short-time energy and spectrogram features, and shows a spike alert in the UI.

The app is designed to be easy to run in a free Hugging Face Space while still providing an interactive interface for real-time audio analysis.

## How it works

- Capture live microphone input in the browser
- Compute short-time energy and spectrogram-based signal details
- Display the waveform, energy trace, and alert status in the UI
- Log recent spike events for quick review

## Local preview

Run the app locally with:

```bash
python app.py
```

Then open the URL shown in the terminal, typically `http://localhost:7860`.

## Files of interest

- `app.py` — Gradio interface and audio analysis logic
- `index.html` — static browser-only version for local/demo testing
- `README.md` — Space metadata and app instructions

## Notes

This is a lightweight demo intended for free-hosted Spaces. It is not a production-grade acoustic monitoring system and depends on browser microphone permissions.
