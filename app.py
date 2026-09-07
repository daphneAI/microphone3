import io
import datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scipy.signal as signal
import gradio as gr

EVENT_LOG = []


def analyze(audio):
    """Analyze a single captured audio clip from the microphone."""
    if audio is None:
        return None, "No audio captured", ""

    # Gradio may pass (sr, samples) or just ndarray depending on version.
    if isinstance(audio, tuple) and len(audio) == 2:
        sr, samples = audio
    else:
        samples = np.array(audio)
        sr = 44100

    if samples.size == 0:
        return None, "Empty audio", ""

    if samples.ndim > 1:
        samples = samples.mean(axis=1)

    samples = samples.astype(np.float32)
    if np.max(np.abs(samples)) > 0:
        samples = samples / (np.max(np.abs(samples)) + 1e-9)

    frame_len = int(0.02 * sr) or 1
    hop = max(1, frame_len // 2)
    squared = samples ** 2
    window = np.ones(frame_len)
    energy = np.convolve(squared, window, mode="valid") / frame_len
    times = np.arange(len(energy)) * (hop / sr)

    peak = float(np.max(energy))
    mean_e = float(np.mean(energy))
    std_e = float(np.std(energy))
    score = (peak - mean_e) / (std_e + 1e-9)
    threshold = mean_e + 2.5 * std_e
    is_spike = peak > threshold

    f, t, Sxx = signal.spectrogram(samples, fs=sr, nperseg=1024, noverlap=512)

    fig, axes = plt.subplots(3, 1, figsize=(6, 8))
    ax = axes[0]
    times_wave = np.arange(len(samples)) / sr
    ax.plot(times_wave, samples, color="C0")
    ax.set_ylabel("Amplitude")
    ax.set_xlim(0, times_wave[-1])

    ax = axes[1]
    ax.plot(times[: len(energy)], energy, color="C1")
    ax.axhline(threshold, color="r", linestyle="--", label="threshold")
    ax.set_ylabel("Energy")
    ax.legend()

    ax = axes[2]
    im = ax.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-12), shading="auto")
    fig.colorbar(im, ax=ax, format="%+2.0f dB")
    ax.set_ylabel("Freq [Hz]")
    ax.set_xlabel("Time [s]")

    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    alert = "SPIKE" if is_spike else "No spike"
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    event = f"{timestamp} | score={score:.2f} | peak={peak:.6f} | {alert}"

    global EVENT_LOG
    EVENT_LOG = [event] + EVENT_LOG[:199]
    log_text = "\n".join(EVENT_LOG)

    return buf.getvalue(), f"{alert} (score {score:.2f})", log_text


with gr.Blocks(title="Microphone Spike Detector") as demo:
    gr.Markdown("**Microphone Spike Detector — live audio analysis**")

    with gr.Row():
        audio_in = gr.Audio(type="numpy", label="Microphone (live)")
        with gr.Column():
            analyze_btn = gr.Button("Analyze latest chunk")
            alert_box = gr.Textbox(label="Alert", interactive=False)

    image_out = gr.Image(label="Analysis", type="pil")
    log_out = gr.Textbox(label="Event Log (newest first)", lines=8)

    analyze_btn.click(fn=analyze, inputs=[audio_in], outputs=[image_out, alert_box, log_out])
    audio_in.stream(fn=analyze, inputs=[audio_in], outputs=[image_out, alert_box, log_out])
    audio_in.change(fn=analyze, inputs=[audio_in], outputs=[image_out, alert_box, log_out])

    gr.Markdown("""
    **How it works**: listens to the microphone stream, computes short-time
    energy and a spectrogram on each captured chunk, and raises a spike alert
    when energy exceeds a simple statistical threshold. This is a signal-processing
    demo — it is *not* a robust production detector.
    """)

if __name__ == "__main__":
    demo.launch()
