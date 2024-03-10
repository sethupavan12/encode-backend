from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from PIL import Image
from dotenv import load_dotenv
from ai import DescribeImage, AiAgent, LiveAgent
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
    # The front end will send the image as a base64 encoded string
    data = request.json
    # print(data)
    image = data["image"]
    # if the data also has 'text' in it and it is not empty
    # 5 seconds we will use an (video) image, 5 seconds we will use the (audio) text
    if 'text' in data and len(data['text']) > 0:
        image_description = data['text']
    else:
        # Image is given as a base64 encoded string
        # convert the base64 string to a PIL image using PIL
        PIL_image = Image.open(io.BytesIO(base64.b64decode(image)))
        image_description = image_to_text_describer.get_description_of_(PIL_image)

    # Generate the comments
    fan_comment = fan_agent.generate_comment(image_description)
    hater_comment = hater_agent.generate_comment(image_description)
    curious_comment = curious_agent.generate_comment(image_description)
    comment_list = [fan_comment, hater_comment, curious_comment]

    return jsonify({"comments": comment_list})


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

    
