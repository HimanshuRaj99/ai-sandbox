from groq import Groq
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging with timestamp, log level, and message format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GroqModel:
    def __init__(self):
        logging.info("Initializing RevealMeaning class")
        
        # Retrieve the API key from environment variables
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logging.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set. Please set it before running the script.")
        
        # Initialize the Groq client with the API key
        self.client = Groq(api_key=self.api_key)
        logging.info("Groq client initialized successfully")
    
    def get_response(self, user_prompt, system_prompt):
        logging.info(f"Processing user query: {user_prompt}")
        try:
            # Define the chat completion request
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=800,
                top_p=1,
                stop=None,
                stream=False,
            )

            # Extract the response content
            response = chat_completion.choices[0].message.content
            logging.info(f"Received response from Groq: {response}")
            return response

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return f"Error occurred: {str(e)}"
