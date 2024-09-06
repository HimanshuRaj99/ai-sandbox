from typing import List, Optional
import json
import logging
import random
from pydantic import BaseModel
from groq import Groq
import re
import os
import json
from dotenv import load_dotenv
from app.controller.generate_img import query
from PIL import Image
import io
from io import BytesIO

load_dotenv()

class Sequence(BaseModel):
    sequenceNumber : int
    sequence : str
class Story(BaseModel):
    storyTitle: str
    story : str
    sequenceOrder : list[Sequence]


class StoryElements:
    def __init__(self):
        logging.info("Initializing Story Sequence class")

        # Retrieve the API key from environment variables
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logging.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set. Please set it before running the script.")

        # Initialize the Groq client with the API key
        self.client = Groq(api_key=self.api_key)
        self.system_prompt = '''
            You are a friendly and creative assistant helping young students in grades 3 to 5 create a story.
            The student will provide a word, sentence, or phrase, and your task is to help them craft a simple and engaging story.
            The story should have multiple events but must be condensed into four ordered sequences. Each sequence should be clear, concise, and easy for young readers to understand. 
            Ensure that the events flow logically and that the language is age-appropriate. Once the story is created, provide the story along with the four sequences in a JSON format.
                        
        '''
    def get_sequence_story(self, topic: str, grade: int, model: str, schema:str):
        try:
            # Define the user prompt
            user_prompt = f'''I have this [word/sentence/phrase]: {topic}.
            Can you help me create a fun and simple story with four ordered sequences using this? Please provide the story and the four sequences in JSON format.
            Please generate a JSON structure for the given topic, grade level.
                                [word/sentence/phrase]: {topic}
                                Grade Level: {grade}
            '''
            # Example schema to guide the model
            example_schema = '''
                        {
    "result": 
        {
        "storyTitle" : "The Picnic",
        "story": "Once upon a time, there was a little girl named Emma. She loved playing with her favorite toy, a small stuffed rabbit named Mr. Fluffers. One day, Emma decided to have a picnic in the park with Mr. Fluffers. She packed a basket with sandwiches, fruits, and cookies. As they sat under a big tree, Emma's dog, Max, came running towards them with a big smile on his face.",
        "sequenceOrder": [
            {
            "sequenceNumber": 1,
            "sequence": "Emma had a favorite toy named Mr. Fluffers, a small stuffed rabbit."
            },
            {
            "sequenceNumber": 2,
            "sequence": "Emma decided to have a picnic in the park with Mr. Fluffers."
            },
            {
            "sequenceNumber": 3,
            "sequence": "Emma packed a basket with sandwiches, fruits, and cookies for the picnic."
            },
            {
            "sequenceNumber": 4,
            "sequence": "Max, Emma's dog, joined them on the picnic under the big tree."
            }
        ]
        }
    }
            '''
            # Sending the prompt to the model
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt + example_schema}
                ],
                model=model,
                temperature=0.2,
                stream=False,
            )

            response = chat_completion.choices[0].message.content
            logging.info(f"Received response from Groq: {response}")
            json_str = re.search(r'(\{\s*"result"\s*:\s*\{\s*"storyTitle"\s*:\s*".*?"\s*,\s*"story"\s*:\s*".*?"\s*,\s*"sequenceOrder"\s*:\s*\[.*?\]\s*\}\s*\})', response, re.DOTALL).group(0)
            logging.info(f"Received response from json_str: {json_str}")

            # Convert the string back to a JSON object
            data = json.loads(json_str)
            logging.info(f"type of json_str : {type(json_str)}")
            logging.info("---------------start----------------")
            logging.info("---------------end----------------")

            # sentences = data['result']
            logging.info("type of data val after transforming : ",type(data))
            logging.info("data val after transforming : ",data)
            return data
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return f"Error occurred: {str(e)}"



def get_sequence(paragraph: str, grade:int, model: str):
    print(paragraph)
    logging.info(f"paragraph : {paragraph} grade : {grade} ")
    schema = json.dumps(Story.model_json_schema(), indent=4)
    StorySequence = StoryElements()
    # response = SVP.get_quiz(paragraph, grammerPrompt ,schema)
    result = StorySequence.get_sequence_story(paragraph, grade, model ,schema)
    logging.info("result story : ", result["result"]["story"])
    print("story data : ",result["result"]["story"])
    inputVal = result["result"]["story"]
    payload = {
    "inputs": inputVal,
    "seed":0,
    "randomize_seed": "True",
    "width":1024,
    "height": 1024,
    "num_inference_steps": 4
    }
    req = payload
    res = query(req)
    save_folder = "../frontend/src/assets"
# Load the image from the returned bytes
    image = Image.open(io.BytesIO(res))  
    image_path = os.path.join(save_folder, "flux_img.png")
    image.save(image_path)
    logging.info("saved file : ",image_path)
    # image.show() 
    return result