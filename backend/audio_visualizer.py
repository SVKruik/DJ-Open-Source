import librosa
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

y, sample_rate = librosa.load("MJ_song.mp3", sr=None)
frame_size = 2048
hop_size = 1024
window = np.hamming(frame_size)

spectra_db = []

for i in range(0, len(y) - frame_size, hop_size):
    
    # Extract frame
    frame = y[i : i + frame_size]
    frame = frame * window
    
    # Apply FFT
    fft_vals = np.fft.rfft(frame)
    magnitudes = np.abs(fft_vals) 
    
    # DB conversion
    magnitude_db = 20 * np.log10(magnitudes+ 1e-7)
    
    # Store
    spectra_db.append(magnitude_db)

spectra_db = np.array(spectra_db)

# Putting data into groups of 32 bars per time step


print(len(spectra_db[0]))
num_bars = 32
num_bins = len(spectra_db[0])          # should be 1025

bins_per_bar = num_bins // num_bars    # 1025 // 32 = 32
remainder   = num_bins % num_bars      # 1025 % 32 = 1

bar_frames = []  # this will become [ [32 bars], [32 bars], ..., ]

for spectrum in spectra_db:            # outer loop: over time frames
    bars = []
    start_bin = 0

    for b in range(num_bars):         # inner loop: over bars
        end_bin = start_bin + bins_per_bar

        # put any leftover bins into the last bar
        if b == num_bars - 1:
            end_bin += remainder

        # group of FFT bins for this bar
        group = spectrum[start_bin:end_bin]

        # one bar value (average magnitude in dB for that band)
        bar_value = np.mean(group)

        bars.append(bar_value)
        start_bin = end_bin

    bar_frames.append(bars)

bar_frames = np.array(bar_frames)

t = 1000   # about 23 seconds into the song

plt.bar(range(32), bar_frames[t])
plt.title(f"32 bars at time frame {t}")
plt.xlabel("Bar index (0–31)")
plt.ylabel("Amplitude (dB)")
plt.show()