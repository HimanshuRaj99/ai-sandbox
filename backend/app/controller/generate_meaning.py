from groq import Groq
import os
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv()

from app.controller import get_dict_meaning

# Configure logging with timestamp, log level, and message format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RevealMeaning:
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
        self.temperature = 0.3
        self.max_tokens = 800
        self.top_p = 1
        self.stop = None
        self.stream = False

        # Define the system prompt
        self.system_prompt = '''
            You are a highly knowledgeable lexicographer and linguist, with an exceptional understanding of words, their meanings, and their morphological structures. 
            Your expertise extends to the origins and historical development of words, allowing you to provide detailed and precise explanations. 
            You take great pride in your ability to communicate this understanding effectively and help others appreciate the richness of the English language.
        '''
    
    def get_meaning(self, user_query, grade, model):
        logging.info(f"Processing user query: {user_query} and grade : {grade} model {model}")
        try:
            dictionary_data = get_dict_meaning.get_word_info(user_query)
            # Define the user prompt
            user_prompt = '''Your task is to provide the meaning and morphology of the word given by the user in a way that is understandable for a student with respect to their grade level. Age of Grade 3, Grade 4 and Grade 5 students are 8, 9 and 11 years respectively. The response should be in a JSON structure as shown in the example below. Additionally, include a translation link to the US version of the dictionary meaning json provided. Ensure the explanation is appropriate for the student's grade level.
                Make sure to add proper synonyms, antonyms phonetic and morphology, prefix, suffix and other required information.
                For reference i will also provide you the meaning and other data of word from a dictionary in form of json.
                Ensure that the meanings are accurate and appropriate, avoiding any false or hallucinated responses. 
                Strictly Output only the JSON structure and nothing else.
            
                Example JSON : 
                    {
                        "word": "euphoria",
                        "phonetic": "/juːˈfɔːɹi.ə/",
                        "details": {
                            "meaning": "A feeling of intense happiness or excitement",
                            "synonyms": ["elation", "exhilaration", "rapture"],
                            "antonyms": ["depression", "despair", "melancholy"],
                            "pronunciation": {
                                "link": "https://api.dictionaryapi.dev/media/pronunciations/en/euphoria-us.mp3"  // Placeholder translation link
                            }
                        },
                        "morphology": {
                            "root": "eu",
                            "prefix": "euph-",
                            "suffix": "-ia",
                            "part_of_speech": "noun"
                        }
                    }


            '''
            # Set model parameters
            self.model_name = model
            logging.info(f"Processing user query: {user_query} and grade : {grade} self model {self.model_name}")
            # Define the chat completion request
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt + f"Word: '{user_query}'"  + f"Grade: '{grade}'" + f'Dictionary Meaning Json: {dictionary_data}'},
                ],
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                stop=self.stop,
                stream=self.stream,
            )

            # Extract the response content
            response = chat_completion.choices[0].message.content
            logging.info(f"Received response from Groq: {response}")
            logging.info(type(response))
            return response.strip("'''")

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return f"Error occurred: {str(e)}"
    
# Example usage
# Uncomment the following block to test the RevealMeaning class
# def main():
#     bot = RevealMeaning()
#     user_query = str(input('Enter the word to search: '))
#     dictionary_data = freedictapi.get_word_info(user_query)
#     response = bot.get_meaning(user_query,dictionary_data)
#     # print(response)

# if __name__ == "__main__":
#     main()