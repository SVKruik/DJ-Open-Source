import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sample_path = "/Users/mikkelobro/DJ-Open-Source/backend/MJ_song.mp3"
sample, sample_rate = librosa.load(sample_path, sr=None)
frame_size = 2048
hop_size = 1024
window = np.hamming(frame_size)

spectra_norm = []

for i in range(0, len(sample) - frame_size, hop_size):
    
    # Extract frame
    frame = sample[i : i + frame_size]
    frame = frame * window
    
    # Apply FFT
    fft_vals = np.fft.rfft(frame)
    
    magnitudes = np.abs(fft_vals) 
    magnitudes = 20 * np.log10(magnitudes+ 1e-7)
    magnitudes = np.clip(magnitudes, -80, 0)
    magnitudes = (magnitudes + 80) / 80

    
    # Store
    spectra_norm.append(magnitudes)

spectra_norm = np.array(spectra_norm)

# Putting data into groups of 32 bars per time step

num_bars = 32
num_bins = len(spectra_norm[0])  
bins_per_bar = num_bins // num_bars
remainder   = num_bins % num_bars

bar_frames = []  # this will become [ [32 bars], [32 bars], ..., ]

for spectrum in spectra_norm:            # outer loop: over time frames
    bars = []
    start_bin = 0

    for b in range(num_bars):         # inner loop: over bars
        end_bin = start_bin + bins_per_bar

        # put any leftover bins into the last bar
        if b == num_bars - 1:
            end_bin += remainder

        # group of FFT bins for this bar
        group = spectrum[start_bin:end_bin]

        # average
        bar_value = np.mean(group)

        bars.append(bar_value)
        start_bin = end_bin

    bar_frames.append(bars)

bar_frames = np.array(bar_frames)

# making video

num_frames, num_bars = bar_frames.shape

fig, ax = plt.subplots()
ax.set_ylim(0, 1)
ax.set_xlim(0, num_bars)

bars = ax.bar(range(num_bars), bar_frames[0])

def update(frame_idx):
    heights = bar_frames[frame_idx]
    for bar, h in zip(bars, heights):
        bar.set_height(h)
    return bars

ani = animation.FuncAnimation(
    fig,
    update,
    frames=num_frames,
    interval=1000 * hop_size / sample_rate,
    blit=True
)

fps = sample_rate / hop_size
ani.save("visualizer_no_audio.mp4", fps=fps, writer="ffmpeg")