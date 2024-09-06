from app.utility.groq_model import GroqModel
import json
import logging
import re

def generate_wordplay_schema(content):
    system_prompt = '''
        You are a linguistic analysis system specialized in English morphology and semantics. Your task is to process given passages of text and extract word information according to specific criteria.
    '''

    user_prompt = '''
        Read the passage and extract any three words from the passage and divide the words in such a way that when joined together form a complete word.Divide the words in form of their prefix, root, suffix and meaning in a proper JSON Schema along with the word.
        Only generate the Json Schema and nothing else.Make sure there are no empty values in any associated keys.

        Important: Choose words which have all three prefix , root and suffix, do not choose word if they lack any of these three.
                    **Do not choose words if they dont have prefix, root and suffix. 
        
        Example JSON SCHEMA:
        [
            {
                "word": "Immortality",
                "root": "mortal",
                "prefix": "Im",
                "suffix": "ity",
                "meaning": "the ability to live forever; eternal life."
                },
                {
                    "word": "Indistinguishable",
                    "root": "distinguish",
                    "prefix": "In",
                    "suffix": "able",
                    "meaning": "not able to be identified as different or distinct."
                },
                {
                    "word": "Deconstruction",
                    "root": "construct",
                    "prefix": "De",
                    "suffix": "tion",
                    "meaning": "the act of breaking something down into its separate parts in order to understand its meaning, especially when this is different from how it was previously understood"
            }
        ]
        
    '''
    
    llm = GroqModel()
    response = llm.get_response(user_prompt + f"Passage : {content}", system_prompt)
    
    logging.info(f"JSON response: {response}")

    # Sanitize response to ensure it is valid JSON
    try:
        wordplay_schema = json.loads(response)
        return wordplay_schema
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON response: {response}")
        raise Exception("LLM Response Generation Failed.")
