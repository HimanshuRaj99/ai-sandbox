from groq import Groq
import os
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv()


# Configure logging with timestamp, log level, and message format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReaderAI:
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
        
        # Set model parameters
        self.model_name = "llama-3.1-8b-instant"
        self.temperature = 0.3
        self.max_tokens = 800
        self.top_p = 0.95
        self.stop = None
        self.stream = False

        # Define the system prompt
        self.system_prompt = '''
            You are a highly knowledgeable lexicographer and linguist, with an exceptional understanding of words, their meanings with respect to the context they are being used in. 
            Your expertise extends to the origins and historical development of words, allowing you to provide detailed and precise explanations. 
            You take great pride in your ability to communicate this understanding effectively and help others appreciate the richness of the English language.
        '''
    
    def find_meaning(self, text, context, grade):
        logging.info(f"Calling Reader Ai Find Meaning for : {text}")
        try:
            
            # Define the user prompt
            user_prompt = f'''Your task is to provide the meaning with reference to the given context for Grade {grade} level student under US Education System.
                **Give the response in json format with key as 'meaning'.
                For reference i will also provide you context in which the portion of text is being used.
                **Ensure that the meanings are accurate and appropriate, avoiding any false or hallucinated responses. 
                ** Ensure the meaning is easy to understand for Grade {grade} level student.
                Output only the JSON structure and nothing else.

                Selected Text: '{text}'
                Context: '{context}'
            '''

            example_schema = ''' Example JSON : 
                    {   
                        "meaning" : " the term "Extraordinary" means something that's far beyond what's normal or expected. It's used to describe things or people that are really special, unusual, or amazing."
                    }
'''

            # Define the chat completion request
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt + example_schema},
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
            return response

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return f"Error occurred: {str(e)}"
    

    def simplify_meaning(self, text, context, grade, generated_meaning):
        logging.info(f"Calling Reader Ai Find Meaning for : {text}")
        try:
            
            # Define the user prompt
            user_prompt = f'''Your task is to simplify the meaning of the given word so that a Grade {grade} level student can easily understand it. 
                            You will be given the word, its meaning in context, and the context in which it is used.

                                Output the simplified meaning in JSON format with the key 'simplified_meaning'.

                                Ensure the meaning is accurate and appropriate for a Grade {grade} level student. 
                                Do not include any additional text or explanations.

                                Input Details:

                                    Selected Text: '{text}'
                                    Context: '{context}'
                                    Generated Meaning: '{generated_meaning}'
                                '''

            example_schema =                 ''''   Response Example JSON : 

                                {
                                    "simplified_meaning": "Extraordinary means very special or amazing. It's something much better or different than normal."
                                }
                                '''

            # Define the chat completion request
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt + example_schema},
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
            return response

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return f"Error occurred: {str(e)}"