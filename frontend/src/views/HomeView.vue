<script lang="ts" setup>
import { ref } from "vue";

const file = ref<File | null>(null);
const videoPlayer = ref<HTMLVideoElement | null>(null);

/**
 * Visualize the uploaded audio file.
 */
async function visualize(): Promise<void> {
    try {
        if (!file.value)
            return alert("Please select a file to upload.");

        // Check file extension
        const allowedExtensions = ["mp3"];
        const fileExtension = file.value.name.split('.').pop()?.toLowerCase();
        if (!fileExtension || !allowedExtensions.includes(fileExtension)) {
            return alert("Please select a valid audio file (mp3).");
        }

        const formData = new FormData();
        formData.append("audio", file.value);
        const response = await fetch("http://localhost:9102/visualize", {
            method: "POST",
            body: formData,
        });

        if (!response.ok)
            return alert("Failed to upload and visualize the audio file.");

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        if (videoPlayer.value) {
            videoPlayer.value.src = url;
            videoPlayer.value.load();
            videoPlayer.value.play();
        }
    } catch (error) {
        console.error("Error uploading file:", error);
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
</script>

<template>
    <div class="flex-col">
        <h1>DJ Open Source</h1>
        <p>GitHub link <a href="https://github.com/SVKruik/DJ-Open-Source" target="_blank">here</a>.</p>
        <form @submit.prevent="visualize()">
            <input type="file" @change="input($event)"></input>
            <button type="submit">Upload</button>
        </form>
        <video controls ref="videoPlayer">
            Your browser does not support the video tag.
        </video>
    </div>
</template>

<style scoped>
div {
    padding: 10px;
}
</style>
