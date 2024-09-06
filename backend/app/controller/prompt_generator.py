from groq import Groq
import os
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv()

# Configure logging with timestamp, log level, and message format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeneratePrompt:
    def __init__(self):
        logging.info("Initializing GeneratePrompt class")
        
        # Retrieve the API key from environment variables
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logging.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set. Please set it before running the script.")
        
        # Initialize the Groq client with the API key
        self.client = Groq(api_key=self.api_key)
        logging.info("Groq client initialized successfully")
        
        # Set model parameters
        self.model_name = "llama-3.1-70b-versatile"
        self.temperature = 0.3
        self.max_tokens = 2000
        self.top_p = 0.95
        self.stop = None
        self.stream = False

        # Define the system prompt
        self.system_prompt = '''
            You are a master prompt engineer who is expert in creating an immersive and educational 
            roleplay prompt for a historical character.
        '''
    
    def get_prompt(self, character, grade, student_age):
        logging.info(f"Generating Prompt for: {character}")
        try:
            # Define the user prompt
            user_prompt = f'''
                Your goal is to create a roleplay prompt for the {character} that will be passed to a roleplay bot.
                Follow these comprehensive guidelines:
                
                Engage with Grade {grade} students in an educational and fun manner by incorporating the following elements:
                Extensive Research: Use extensive research on the historical figure's life, including lesser-known facts and personal anecdotes. Identify pivotal moments in their life that shaped their worldview and decisions.

                **Nuanced Personality Profile: Develop a personality profile that includes:
                •	Core values and beliefs
                •	Quirks, habits, and idiosyncrasies
                •	Hopes, fears, and personal motivations
                •	Sense of humor and preferred types of jokes



                **Distinctive Voice: Create a distinctive voice that includes:
                •	Vocabulary range and complexity appropriate to their era and education
                •	Speech patterns, catchphrases, and colloquialisms of their time
                •	Accent or dialect considerations (e.g., regional influences)

                Adaptive Conversation Strategies: Implement strategies to:
                •	Adjust complexity based on perceived user understanding
                •	Incorporate storytelling techniques to make information more engaging
                •	Use Socratic questioning to encourage critical thinking

                Sensitive Historical Topics: Develop nuanced guidelines for addressing potentially sensitive historical topics.

                Encouraging Reflection: Create guidelines for encouraging the user to reflect on what they've learned.

                **Temporal Knowledge Limitation: If a question or user asks about any information or event that happened after the death of the character, respond with "I have no knowledge of this event."

               ** Response : **Important:** Provide concise initial responses around 70-80 characters. Offer to elaborate if student shows interest. If a detailed response is required, provide it in small chunks to keep the student curious. Continue providing more details as the student asks for them.
                    E.g : Student : What led to American Revolution?
                         Character: (eyes light up with excitement) The colonists' resentment towards Britain's taxes and control, without consent, sparked protests that led to the Revolutionary War and independence..Would you like to hear more about the key battles and events of this pivotal struggle? I have many stories to share if you're interested.
                    Continue providing more details in this format, gauging the user's interest and willingness to learn more with each response.Do not give response in more than 70-80 characters. 
                                You response should be easy to understand by {grade} student who is around {student_age}.

                Knowledge: Use the knowledge base of the historical character and their expertise in their domain.

                **Storytelling Techniques:
                •	Use In media res storytelling technique to grab the attention of the student.
                •	Use show, don't tell storytelling technique when describing your role or your story.
            '''

            # Define the chat completion request
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
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
            logging.info("Prompt generated successfully")
            return response

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return f"Error occurred: {str(e)}"
    
# Example usage
# Uncomment the following block to test the GeneratePrompt class
# def main():
#     bot = GeneratePrompt()
#     character = str(input('Enter the historical character: '))
#     response = bot.get_prompt(character)
#     print(response)

# if __name__ == "__main__":
#     main()
