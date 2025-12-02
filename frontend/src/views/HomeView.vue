<script lang="ts" setup>
import { ref } from "vue";

// State variables
const file = ref<File | null>(null);
const videoPlayer = ref<HTMLVideoElement | null>(null);
const history = ref<Array<HistoryItem>>([]);
const showVideo = ref<boolean>(false);
const isProcessing = ref<boolean>(false);
const timeElapsed = ref<number>(0);
let timer: number | null = null;

type HistoryItem = {
    id: number;
    url: string;
    title: string;
    timeUsed: number;
    length: string;
};

/**
 * Visualize the uploaded audio file.
 */
async function visualize(): Promise<void> {
    try {
        if (isProcessing.value)
            throw new Error("A file is already being processed. Please wait.");
        isProcessing.value = true;

        if (!file.value)
            throw new Error("Please select a file to upload.");

        // Check file extension
        const allowedExtensions = ["mp3"];
        const fileExtension = file.value.name.split('.').pop()?.toLowerCase();
        if (!fileExtension || !allowedExtensions.includes(fileExtension))
            throw new Error("Please select a valid audio file (mp3).");

        // Start timer
        timeElapsed.value = 0;
        timer = window.setInterval(() => {
            timeElapsed.value += 1;
        }, 1000);

        // Send payload
        const formData = new FormData();
        formData.append("audio", file.value);
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/visualize`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok)
            throw new Error("An error occurred while uploading the file. Please try again later.");
        showVideo.value = true;

        // Play video
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        if (videoPlayer.value) {
            videoPlayer.value.src = url;
            videoPlayer.value.load();
            await videoPlayer.value.play();

            // Add to history
            history.value.push({
                id: history.value.length + 1,
                url,
                title: file.value.name,
                timeUsed: timeElapsed.value,
                length: formatSeconds(videoPlayer.value.duration || 0),
            });
        }

        // Clear file input
        file.value = null;
    } catch (error) {
        alert((error as Error).message);
        showVideo.value = false;
    } finally {
        isProcessing.value = false;
        if (timer) {
            clearInterval(timer);
            timer = null;
        }
    }
}

/**
 * Listen for input changes.
 * @param event The input change event.
 */
function input(event: Event): void {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
        file.value = target.files[0];
    } else file.value = null;
}

/**
 * Format seconds into mm:ss format.
 * @param seconds The number of seconds.
 * @returns The formatted time string.
 */
function formatSeconds(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Remove an item from the history.
 * @param item The history item to remove.
 */
function removeFromHistory(item: HistoryItem): void {
    window.URL.revokeObjectURL(item.url);
    history.value = history.value.filter(i => i.id !== item.id);
}
</script>

<template>
    <div class="flex-col content-wrapper">
        <div class="flex-col content">
            <!-- Introduction -->
            <article class="flex-col">
                <h1>DJ Open Source</h1>
                <div class="flex-col">
                    <p>Seoul National University of Science and Technology</p>
                    <p>Open Source Software - Fall 2025 - <a href="https://github.com/SVKruik/DJ-Open-Source"
                            target="_blank">GitHub</a></p>
                </div>
                <div class="flex-col">
                    <p>Term project made by <strong>Mikkel Oebro</strong> and <strong>Stefan Kruik</strong>.</p>
                    <p>Upload a MP3 file to play it with a Pyplot visualizer.</p>
                </div>
            </article>
            <hr class="splitter">
            </hr>

            <!-- Uploading -->
            <form @submit.prevent="visualize()" v-if="!isProcessing" class="flex">
                <label for="file-input" class="flex pointer" title="Select an audio file to process.">
                    <p>{{ file ? file.name : "Select Audio File" }}</p>
                    <i class="fa-regular fa-file-audio"></i>
                </label>
                <input type="file" @change="input($event)" id="file-input"></input>
                <button type="submit" class="flex upload-button" :disabled="!file" title="Upload selected file."
                    :class="{ 'disabled': !file }">
                    <p>Upload</p>
                    <i class="fa-regular fa-upload"></i>
                </button>
            </form>
            <div class="flex-col processing-text" v-else>
                <div class="flex">
                    <p>Uploading and processing file...</p>
                    <i class="fa-regular fa-circle-notch fa-spin"></i>
                </div>
                <p>Time elapsed: {{ timeElapsed }} seconds</p>
            </div>

            <!-- Video -->
            <video controls ref="videoPlayer" width="640" height="480" v-if="showVideo">
                Your browser does not support the video tag.
            </video>
            <div v-else class="video-placeholder"></div>

            <!-- History -->
            <hr>
            </hr>
            <h3>Playback History</h3>
            <div class="flex-col history-container" v-if="history.length > 0">
                <div class="flex history-item" v-for="(item, index) in history" :key="index">
                    <div class="flex-col">
                        <p class="strong">{{ item.title.replace(".mp3", "") }}</p>
                        <div class="flex-col history-item-details">
                            <p class="font-light">Duration: {{ item.length }}</p>
                            <p class="font-light">Processing: {{ item.timeUsed }} seconds</p>
                        </div>
                    </div>
                    <div class="flex">
                        <a :href="item.url" target="_blank" class="flex button" title="Download the video file.">
                            <i class="fa-regular fa-download"></i>
                        </a>
                        <button type="button" class="delete-button" @click="removeFromHistory(item)"
                            title="Remove the video file.">
                            <i class="fa-regular fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div v-else class="history-placeholder-text disabled">
                <p>No playback history yet. Upload and process an audio file to see it here.</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.content-wrapper {
    padding: 10px;
    align-items: center;
    margin-top: 30px;
}

.content,
article,
form {
    gap: 15px;
}

.content {
    width: 640px;
    align-items: center;
}

.video-placeholder {
    width: 640px;
    height: 480px;
    margin-top: -250px;
}

h3,
article,
.history-placeholder-text {
    text-align: center;
}

article,
hr,
form,
.processing-text {
    z-index: 1;
}

article,
article h1,
article p {
    width: 100%;
}

video {
    margin-top: -250px;
}

button,
.button,
label {
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius-low);
    box-sizing: border-box;
    padding: 5px 10px;
    height: 40px;
    justify-content: space-between;
}

label {
    width: 200px;
}

input {
    display: none;
}

.upload-button {
    background-color: var(--color-accent);
}

.delete-button {
    background-color: var(--color-danger);
}

button p,
button i {
    color: white;
}

hr {
    width: 640px;
    border: 0;
    border-top: 1px solid var(--color-border-dark);
    margin: 0 30px;
    background-color: transparent;
}

h3,
.history-container {
    width: 100%;
    margin-top: 20px;
    gap: 15px;
}

.history-item {
    width: 100%;
    justify-content: space-evenly;
}

.history-item-details {
    gap: 0;
}

.history-placeholder-text {
    color: var(--color-text-light);
    width: 400px;
}
</style>
