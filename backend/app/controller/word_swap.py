from groq import Groq
import os
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv()

# Configure logging with timestamp, log level, and message format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WordSwapGenerator:
    def __init__(self):
        logging.info("Initializing WordSwapGenerator class")
        
        # Retrieve the API key from environment variables
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logging.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set. Please set it before running the script.")
        
        # Initialize the Groq client with the API key
        self.client = Groq(api_key=self.api_key)
        logging.info("Groq client initialized successfully")
        
        # Set model parameters
        self.temperature = 0.3
        self.max_tokens = 800
        self.top_p = 1
        self.stop = None
        self.stream = False

        # Define the system prompt
        self.system_prompt = '''
            You are a highly knowledgeable educator and linguist with an exceptional understanding of vocabulary and synonyms. 
            Your expertise extends to creating engaging and educational synonym swap activities for young learners. 
            You take great pride in your ability to generate activities that are both fun and informative.
        '''
        
    def generate_synonym_swap(self, topic, grade, model_name, standard, num_questions):
        logging.info(f"Generating synonym swap activity for topic: '{topic}', grade: {grade}, standard: {standard}, num_questions: {num_questions}, model_name: {model_name}")
        try:
            # Define the user prompt
            user_prompt = f'''Your task is to generate a synonym swap activity suitable for Grade {grade} on the topic of "{topic}", 
            aligned with the education {standard} standards of US curriculum.
            Provide a word bank and sentences with bold highlighted words to be replaced by synonyms from the word bank.
            Use HTML <b> tags to bold the word that needs to be replaced.
            Ensure that the activity is appropriate for the grade level and engaging for students.
            
            Example JSON:
            {{
                "word_bank": ["captivating", "delightful", "frightening"],
                "sentences": [
                    {{"original": "During science class, we learned <b>fascinating</b> facts about the cell.", "originalWord": "fascinating", "synonym": "captivating"}},
                    {{"original": "Lunch was <b>wonderful</b> because my mom made me a delicious sandwich.", "originalWord": "wonderful", "synonym": "delightful"}},
                    {{"original": "For silent reading, I chose a <b>scary</b> story about spiders.", "originalWord": "scary", "synonym": "frightening"}}
                ]
            }}
            
            ### Strictly Enforced Rules ###
            1. Strictly ensure to generate exactly {num_questions} sentences in the output.
            2. Strictly ensure that each sentence contains only 1 selected bold word.
            3. The word_bank should contain exactly {num_questions} words, each being a synonym for the bolded word in the corresponding sentence.
            4. The word_bank should contain words that are different from the original words in the sentences.
            5. The word_bank should be presented in a random order.
            6. Do not add any additional words to the word_bank that are not used as synonyms in the sentences.
            7. Output only the JSON structure and nothing else.

            Please generate a similar JSON structure for the given topic, grade level, standard, and number of questions.
            '''
            
            # logging.info('User prompt:' + user_prompt);

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                stop=self.stop,
                stream=self.stream,
            )
            
            response = chat_completion.choices[0].message.content
            logging.info(f"Received response from Groq: {response}")
            return response
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return f"Error occurred: {str(e)}"

# Example usage
# if __name__ == "__main__":
#     generator = WordSwapGenerator()
#     activity = generator.generate_synonym_swap("Science", 3, "llama-3.1-8b-instant", "Common Core", 5)
#     print(activity)