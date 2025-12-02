import time
import matplotlib
matplotlib.use("Agg")

import librosa
from numpy import hamming, fft, abs, log10, clip, array, median, linspace, copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import subprocess
from matplotlib.animation import FFMpegWriter

def visualize_audio(file_name: str) -> str:
    start_time = time.time()
    
    # values for fft=
    log_file_name = file_name.replace("backend/uploads/", "")
    sample, sample_rate = librosa.load(file_name, sr=None)
    frame_size          = 2048
    hop_size            = frame_size // 2
    window              = hamming(frame_size)
    
    print(f"[{log_file_name}] Received audio file. Sample rate: {sample_rate}, total samples: {len(sample)}")

    # values for db conversion and normalization
    min_db          = -20
    max_db          = 0
    spectra_norm    = []

    for i in range(0, len(sample) - frame_size, hop_size):
        
        # Extract frame
        frame = sample[i : i + frame_size]
        frame = frame * window
        
        # Apply FFT
        fft_vals = fft.rfft(frame)
        
        # Finding magnitudes in db and normalize
        magnitudes = abs(fft_vals) 
        magnitudes = 20 * log10(magnitudes+ 1e-7)
        magnitudes = clip(magnitudes, min_db, max_db)
        magnitudes = (magnitudes - min_db) / (max_db - min_db)

        # Store
        spectra_norm.append(magnitudes)

    #convert into array
    spectra_norm = array(spectra_norm)


    # Putting data into bar groups per time step using log spacing
    num_bars    = 32
    num_bins    = len(spectra_norm[0])
    power       = 3.0 #used for logarithmic spacing. larger make more low freq bars

    edges = ((linspace(0, 1, num_bars + 1)) ** power) * num_bins
    edges = edges.astype(int)

    bar_frames = []

    for spectrum in spectra_norm:
        bars = []
        for b in range(num_bars):
            start_bin = edges[b]
            end_bin   = edges[b + 1]
            group     = spectrum[start_bin:end_bin]

            if len(group) == 0:
                bar_value = 0.0
            else:
                bar_value = median(group)

            bars.append(bar_value)

        bar_frames.append(bars)

    bar_frames = array(bar_frames)

    # making video

    num_frames, num_bars = bar_frames.shape
    alpha                = 0.7
    smoothed             = copy(bar_frames)

    # smooth transistion using recursive formula

    for t in range(1, num_frames):
        smoothed[t] = alpha * smoothed[t-1] + (1 - alpha) * bar_frames[t]

    bar_frames = smoothed

    fig, ax = plt.subplots()
    ax.set_ylim(0, 3)
    ax.set_xlim(0, num_bars)
    ax.axis("off")

    bars = ax.bar(range(num_bars), bar_frames[0])

    def update(frame_idx):
        heights = bar_frames[frame_idx]
        for bar, h in zip(bars, heights):
            bar.set_height(h)
        return bars

    ani = animation.FuncAnimation(
        fig,
        update,
        frames   = num_frames,
        interval = 1000 * hop_size / sample_rate,
        blit     = True
    )

    video_file = file_name.replace(".mp3", "_visualizer_no_audio.mp4")
    print(f"[{log_file_name}] Saving video...")
    ani.save(video_file, writer=FFMpegWriter(fps=sample_rate / hop_size))

    input_video  = video_file
    input_audio  = file_name
    output_video = video_file.replace("_no_audio", "_with_audio")


    cmd = [
        "ffmpeg",
        "-loglevel", "quiet",
        "-y",                    # overwrite output if exists
        "-i", input_video,
        "-i", input_audio,
        "-c:v", "copy",          # no re-encode of video
        "-c:a", "aac",           # MP4 requires AAC audio
        "-shortest",             # stop when shortest stream ends
        output_video
    ]

    print(f"[{log_file_name}] Merging audio and video...")
    subprocess.run(cmd)
    
    end_time = time.time()
    print(f"[{log_file_name}] Generated video file: {output_video}")
    print(f"[{log_file_name}] Time taken: {end_time - start_time:.2f} seconds")
    
    return output_video

# Uncomment to test the function directly from this file
# visualize_audio("../assets/MJ_song.mp3")