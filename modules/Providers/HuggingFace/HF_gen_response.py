# gui/HuggingFace/HF_gen_response.py

import json
import logging
import os
from dotenv import load_dotenv
import requests
from modules.speech_services.GglCldSvcs import tts

load_dotenv()

logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("HF_API_TOKEN")

HF_MODEL = "microsoft/DialoGPT-large"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def set_hf_model(model_name):
        global HF_MODEL
        HF_MODEL = model_name 

def get_hf_model():
    return HF_MODEL

def query(payload):
    API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

async def generate_response(current_persona, message, temperature_var, top_p_var=None, top_k_var=None):
    data = query(
        {
            "inputs": {
                "past_user_inputs": [msg['content'] for msg in message if msg['role'] == 'user'],
                "generated_responses": [msg['content'] for msg in message if msg['role'] == 'system'],
                "text": current_persona['content']
            },
            "parameters": {
                "temperature": temperature_var,
                "top_k": top_k_var,
                "top_p": top_p_var
            },
            "options": {
                "wait_for_model": True    
            }
        }
    )


    response_content = data.get('generated_text')

    if response_content is not None:
        if tts.get_tts():
            try:
                await tts.text_to_speech(response_content)
            except Exception as e:
                logger.error("Error during TTS: %s", e)

    print(data)

    return data

# THIS IS A VERY EARLY ATTEMPT AT HUGGINGFACE. I HAVE NOT RETURNED HERE FOR A LONG TIME. I ALSO DONT THINK IT WORKS.