from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from PIL import Image
from dotenv import load_dotenv
from ai import DescribeImage, AiAgent, LiveAgent, Auscribe
import librosa
# import speech_recognition as sr
import io
import random
import time
import base64
import json
load_dotenv()


app = Flask(__name__)
CORS(app, origins="*")


# Download the BLIP model 
# First time will be slow
image_to_text_describer = DescribeImage()

# Intialize the AI agents
fan_agent = AiAgent(persona="fan")
hater_agent = AiAgent(persona="hater")
curious_agent = AiAgent(persona="curious")


audio_transcriber = Auscribe(model_size="base")

# Load the random comments from the JSON file
with open('random_comments.json', 'r') as f:
    random_comments = json.load(f)


@app.route("/")
def index():
    return render_template("index.html")

# Recieve the image from the frontend 
# This image will trigger the AI to generate a comment
@app.route("/generate_comments", methods=["POST"])
def generate_comments():
    # import pdb;
    # pdb.set_trace()
    try:
        # The front end will send the image as a base64 encoded string
        image = request.form.get('image')
        PIL_image = Image.open(io.BytesIO(base64.b64decode(image)))
        image_description = image_to_text_describer.get_description_of_(PIL_image)

        # pdb.set_trace()

        # Audio
        file = request.files['file']
        if 'file' not in request.files:
            return jsonify({"error": "No audio file part"}), 400
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            filename = "audio.wav"  # Or use secure_filename(file.filename) to keep original name
            file.save(filename)
            audio_array, sample_rate = librosa.load(filename)
            audio_description = audio_transcriber.convert_to_text(file=audio_array)

        context = f"This is the description of what is seen in the live stream: {image_description} and this is what you hear in the live stream:{audio_description}"
        # Generate the comments
        fan_comment = fan_agent.generate_comment(context)
        hater_comment = hater_agent.generate_comment(context)
        curious_comment = curious_agent.generate_comment(context)
        comment_list = [fan_comment, hater_comment, curious_comment]

        return jsonify({"comments": comment_list})
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occured"}), 500

@app.route("/generate_audio_comments", methods=["POST"])
def generate_audio_comments():
    print(request)
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No audio file part"}), 400

    file = request.files['file']
    type(file)

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = "audio.wav"  # Or use secure_filename(file.filename) to keep original name
        print(file)
        file.save(filename)
        audio_array, sample_rate = librosa.load(filename)
        text = audio_transcriber.convert_to_text(file=audio_array)
        return jsonify({"comments": text})


# On front end, you click a button to add someone to the live stream
# This will trigger this route. I want it so that once, I user clicks
# the button first time, I wanna play the first time video, then aftewards
# I want to use the 'text' from the post request to find the most relevant video
# and send the path to it.
@app.route("/add_live", methods=["POST"])
def live():
    data = request.json
    agent = LiveAgent()
    audio_text = data["text"]
    first_time = data["first_time"]
    if first_time:
        video_path = agent.get_video_path(audio_text, first_time=True)
    else:
        video_path = agent.get_video_path(audio_text)
    return jsonify({"video_path": video_path})

if __name__ == '__main__':
    # app.run(port=8000, debug=True)
    app.run(host='0.0.0.0', port=8000, debug=True)

    
