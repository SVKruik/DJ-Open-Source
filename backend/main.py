#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from audio_visualizer import visualize_audio

app = Flask(__name__)
CORS(app)

# Default Endpoint
@app.route('/', methods=["GET"])
def default():
    return jsonify({
        "message": "Hello DJ Open Source!"
    }), 200
    
@app.route('/visualize', methods=["POST"])
def visualize():
    # Get the audio file from the formData request
    audio_file = request.files.get("audio")
    
    # Save the audio file temporarily
    audio_file.save(f"backend/audio_file.mp3")
    
    # Generate and return the video to the frontend
    visualize_audio() 
    return send_file("visualizer_with_audio.mp4", mimetype="video/mp4")

# Start
app.run(host="localhost", port=9102, debug=True)