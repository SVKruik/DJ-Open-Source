#!/usr/bin/env python
# encoding: utf-8
from flask import Flask
app = Flask(__name__)

# Default Endpoint
@app.route('/', methods=["GET"])
def default():
    return {
        "message": "Hello DJ Open Source!"
    }, 200

# Start
app.run(debug=True)