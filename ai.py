"""
This file contains the AI related stuff needed to generate comments for the live feed.
"""
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI,Ollama
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import json
import whisper

load_dotenv()


from prompts import FAN_PROMPT,HATER_PROMPT,CURIOUS_PROMPT, VIDEO_FIND_PROMPT

class Auscribe:
    """
    Converts the audio files from front end to text using Whispher.
    """
    
    def __init__(self,model_size="tiny"):
        self.model = whisper.load_model(model_size)

    def convert_to_text(self, file):
        """
        This method converts the audio to text.
        :param file: audio file
        :return: str (The text from the audio)
        """
        out = self.model.transcribe(file)
        return out["text"]



class LiveAgent:
    """
    This class is used to find the most relevant video to send to the frontend.
    The way we decide the most relevant video is by using the what user talked about in the audio.
    Then, the agent will find the most relevant video using the description of the video in a json file and
    send the path of that video from the json file to the frontend.

    The agent will always send welcome video when it is the first call. All the videos are from json file.
    """

    def __init__(self):
        self.video_path = ""
        self.welcome_video_path = "./videos/adele_saying_hi.mov"
        self.model = OpenAI()

    def get_video_path(self, audio_text, first_time=False):
        """
        This method finds the most relevant video using the audio text.
        :param first_time: bool first time or not
        :param audio_text: str (The audio text)
        :return: str (The path of the most relevant video)
        """
        if first_time:
            self.video_path = self.welcome_video_path
        else:
            # Find the most relevant video using the audio text
            self.video_path = self.use_ai_to_find_relevant_video(audio_text)
        return self.video_path
    
    def use_ai_to_find_relevant_video(self, audio_text):
        """
        This method uses AI to find the most relevant video using the audio text.
        :param audio_text: str (The audio text)
        :return: str (The path of the most relevant video)
        """
        prompt_template=VIDEO_FIND_PROMPT
        prompt = PromptTemplate(
            input_variables=["audio_text"], template=prompt_template
        )
        llm_chain = LLMChain(llm=self.model, prompt=prompt)
        output = llm_chain.invoke(audio_text)
        print(output)
        clean_path = output['text']
        return clean_path


        

class AiAgent:
    """
    AiAgents are agents who imitate humans and depending
    on the type of agent, they have different persona, interests and questions, comments

    Persona is given to an agent and affects the way the agent interacts with the world.
    :param persona: str (Can only be "fan", "hater", or "curious")
    """
    def __init__(self, persona, model=None):
        if persona not in ["fan", "hater", "curious"]:
            raise ValueError("Persona can only be 'fan', 'hater', or 'curious'")
        self.persona = persona
        self.prompt = None

        if model is None:
            self.model = OpenAI()
        else:
            self.model = Ollama(model=model)
        if persona == "fan":
            prompt_template = FAN_PROMPT
        elif persona == "hater":
            prompt_template = HATER_PROMPT
        elif persona == "curious":
            prompt_template = CURIOUS_PROMPT
        self.prompt = PromptTemplate(
            input_variables=["visual_description","audio_description"], template=prompt_template
        )
        self.llm_chain = LLMChain(llm=self.model, prompt=self.prompt) if model is None else self.model

    def generate_comment(self, context)->str:
        """
        This method generates a comment based on the visual description.
        :param context: str (The context of the live feed)
        """
        output = self.llm_chain.invoke(context)
        clean_comment = output['text']
        return clean_comment



class DescribeImage:
    """
    This class uses BLIP to describe the image.
    """
    def __init__(self,gpu=False):
        "Loads model"
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.gpu = gpu if gpu else False
        if gpu == True:
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base", torch_dtype=torch.float16).to("cuda")
        else:
            self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    def describe(self, image)->str:
        """
        This method describes the image using model.
        :param image: PIL image (<class 'PIL.Image.Image'>)
        """
        if self.gpu:
            inputs = self.processor(image, return_tensors="pt").to("cuda", torch.float16)
            out = self.model.generate(**inputs)
            image_description = self.processor.decode(out[0], skip_special_tokens=True)
        else:
            inputs = self.processor(image, return_tensors="pt")
            out = self.model.generate(**inputs)
            image_description = self.processor.decode(out[0], skip_special_tokens=True)

        return image_description

    def get_description_of_(self, image)->str:
        """
        Pass me a PIL image and I will describe it.
        """
        return self.describe(image)
