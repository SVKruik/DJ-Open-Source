# DJ Open Source

Welcome to project DJ Open Source, a music player with audio visualization made for the term project of the SeoulTech Open Source Software class.

Made by:

- Mikkel Oebro, made the logic for converting an audio file to a mp4 visualization.
- Stefan Kruik, responsible for the frontend and backend API. Also hosts the website.

Below you can find a detailed description of each of the components at work.

#### Frontend

The frontend is a modern Vue 3 website that connects the user input to the backend logic.

Vue is a web framework that makes development easier and performant.

#### Features

The website itself is fairly simple in design and feature-set, but does contain the essentials.

It has the option to upload and convert mp3 files, which are sent to the backend for processing. Once the backend is finished, it sends the mp4 file back which the frontend automatically plays.

Finally, it also keeps track of your playback history so that you can view and download your previous submissions.

#### Backend

The backend is a Flask API with an endpoint the frontend uses to communicate the files.

##### Loading and FFT

After receiving the mp3 file from the frontend, the code loads and decomposes it into short, overlapping frame with a 50% frame-step to help with smoother visual appeal. Each frame is multiplied by a hamming windows with is a technique used in signal processing to make the frequency domain more accurate (reduce spectral leakage). Afterwards each frame is converted to the frequency domain using fast fourier transform (FFT).

##### Decibal conversiona and normalization

The frequency values gets converted into decibal values to mimic human hearing and normalized to get values between 0 and 1. Low values (below min_db) gets ignored to contribute to the visual appeal so only the most noticable sounds contribute to the spectrum.

##### Frequency bars

The frequencies are categories into 32 bars of different frequency range. The frequency interval is determined using log spacing. This creates more bars for lower frequencies as that is more visually appealing in terms of illustrating the music (low frequencies contains the "energy" of the song).

##### Creating the video

A bart chart is drawn an updated for each time frame. The animation gets exported into a silent mp4 where it finally gets combined with the uploaded mp3 file to create the final audio visualization as an mp4 file. This is sent back to the frontend where it is played.

#### Hosting

To make the website accessible during the demo, it is hosted on a privately owned server.

When both components are running, a Nginx reverse proxy binds the two localhost ports to our domain.

You can view the website when it is active at [djos.stefankruik.com](https://djos.stefankruik.com/). If it is not on, you will see a Cloudflare error page.

> WARNING: Not all browsers allow playing of the video's. It might give you a permission error after uploading. Check your browser permissions and policies if you get this error.
