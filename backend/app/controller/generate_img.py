import requests
import io
import os
from PIL import Image
import logging

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

headers = {"Authorization": "Bearer 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"}

# Correcting the dictionary syntax with ':' instead of '=' for key-value pairs

def query(payload):
    logging.info("query method initiialized: ",payload)
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content
