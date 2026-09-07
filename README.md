---
title: Microphone Spike Detector
emoji: 🎤
colorFrom: blue
colorTo: green
sdk: static
pinned: false
---

# Microphone Spike Detector

This Space runs  as a browser-only static app. It does not start a Python server, so it stays within the free Hugging Face CPU quota and works with a free accounts.

The app uses the browser microphone API to monitor audio in real time, compute a simple energy spike signal, and show live waveform/energy updates without any server-side processing .

## Why this works for free Spaces

- No backend process is running in the Space
- No model, Python worker, or long-running CPU task is required
- The microphone and analysis happen in the user browser
- This avoids the `You've reached your CPU Basic quota limit` problem caused by persistent server-backed apps

## Local preview

Open the generated `index.html` in a browser, or serve the folder locally:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Files of interest

- `index.html` — complete browser app with microphone access and live visualization
- `README.md` — static Space instructions

## Notes

This is a lightweight demo intended for free-hosted Spaces. It is not a production-grade acoustic monitoring system and depends on browser permissions for microphone access.
