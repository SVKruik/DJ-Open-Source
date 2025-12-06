# DJ-Open-Source

Music player with audio visualization made for the Open Source Software class.

#### Backend

##### Loading and FFT
The code loads a given mp3 file and decomposes it into short, overlapping frame with a 50% frame-step to help with smoother visual appeal. Each frame is multiplied by a hamming windows with is a technique used in signal processing to make the frequency domain more accurate (reduce spectral leakage). Afterwards each frame is converted to the frequency domain using fast fourier transform (FFT). 

##### Decibal conversiona and normalization
The frequency values gets converted into decibal values to mimic human hearing and normalized to get values between 0 and 1. Low values (below min_db) gets ignored to contribute to the visual appeal so only the most noticable sounds contribute to the spectrum

##### Frequency bars
The frequencies are categories into 32 bars of different frequency range. The frequency interval is determined using log spacing. This creates more bars for lower frequencies as that is more visually appealing in terms of illustrating the music (low frequencies contains the "energy" of the song).

##### Creating the video
A bart chart is drawn an updated for each time frame. The animation gets exported into a silent mp4 where it finally gets combined with the uploaded mp3 file to create the final audio visualization as an mp4 file

#### Directories

- `frontend`: contains all the website source code.
- `backend`: has the MP3 to waveform converter.
- `server`: the server that hosts the frontend code.
- `.github`: CI/CD, GitHub Actions
