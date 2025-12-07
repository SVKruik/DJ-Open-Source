#!/usr/bin/env python
# encoding: utf-8
import random
import string
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from audio_visualizer import visualize_audio

app = Flask(__name__)
CORS(app)

# Default Endpoint
@app.route('/', methods=["GET"])
def default():
    return jsonify({
        "message": "DJ Open Source Backend is running!"
    }), 200
    
@app.route('/visualize', methods=["POST"])
def visualize():
    # Get the audio file from the formData request
    audio_file = request.files.get("audio")
    ticket = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    file_name = f"uploads/{ticket}_{audio_file.filename}"
    
    # Save and process the audio file
    audio_file.save(file_name)
    video_file = visualize_audio(file_name).replace("backend/", "", 2)
    
    # Return the video to the frontend
    print(f"[{file_name}] Sending video file back to client...")
    return send_file(video_file, mimetype="video/mp4")

# Start
if __name__ == "__main__":
    app.run(host="localhost", port=9102, debug=True)