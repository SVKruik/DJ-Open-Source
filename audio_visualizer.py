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
    magnitude_db = 20 * np.log10(magnitudes) + 1e-7)
    
    # Store
    spectra_db spectra.append(magnitude_db)
    
