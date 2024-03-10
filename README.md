# Project Echo
Echo is an interesting interactive app that not only makes experience what it's like to be famous but also have some audience to cheer you up, motivate you or maybe just be there to listen.💙

# Code Structure
This repo is backend and front end is [here](https://github.com/bilal-mustafa10/encode-ai-hackathon)

The code is basically 2 parts
1. AI classes: This is where majority of AI tasks like customising AI agents, extracting context from image takes place.
2. Flask/server: This is where React Native front end meets backend which then ties it up with AI classes.


## Tech Stack
1. We used OpenAI's API for LLM source and additionally, we are also proud of supporting local LLMs using Ollama, meaning faster, secure and cost-free inferencing.
2. We used Langchain as our AI middleware connecting all the dots to seemlessly intergrated

## What does the AI do?
1.  AI is the heart of our project. As you can see in demom, we utilise AI for comments, for understanding visual context using BLIP and converting audio to text using Whisper.
2.  Additionally, we also use AI to stimulate the live stream collaboration (i.e paired streaming) by finding relevant bits of video to use when asked certain question.

We are really proud of our inference timings as we used smart methods to virtually not notice the ACTUAL latency. For eg, noise comments.
