from typing import List, Optional
import json
import logging
import random
import re
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class ParagraphRequest(BaseModel):
    paragraph: str

class SentenceComponents(BaseModel):
    sentence: str
    subject: str
    predicate: str
class CorrectOrderComponents(BaseModel):
    subject: str
    predicate: str
class QuizResponse(BaseModel):
    sentences: list[SentenceComponents]
    correctOrder: list[CorrectOrderComponents]

class QuizRequest(BaseModel):
    paragraph: str
    order: list[str]
    correctOrder: list[str]
    
class SubjectPredicate(BaseModel):
    sentence: str
    subject: str
    predicate: str

class GrammerElement:
    def __init__(self):
        logging.info("Initializing GrammerElement class")
        
        # Retrieve the API key from environment variables
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logging.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set. Please set it before running the script.")
        
        # Initialize the Groq client with the API key
        self.client = Groq(api_key=self.api_key)
        self.system_prompt = '''
            You are an advanced language model tasked with rephrasing sentences from a given paragraph, identifying the grammer 
            element of each rephrased sentence, and structuring the output in a specified format.
            The sentences must adhere strictly to the specified grade level, curriculum standard, and number of sentences required.

            Your output should strictly reflect the content of the original paragraph without introducing any new information (hallucination).
            Ensure that the sentences are accurate, relevant, and appropriate for the given grade level and curriculum standard. 
            The structured output must be in JSON format, following the specified schema."
        '''
    def get_quiz(self, paragraph: str, grade: int, standard: str, noQues: int, grammerPrompt:str, model:str, schema : str):
        try:
            # Define the user prompt
            user_prompt = f'''Please rephrase the sentences from the following paragraph/word/sentence/alphabet/symbol according to the specified grade level and curriculum standard. Identify the {grammerPrompt} for each rephrased sentence, and structure the output as specified below:

                                Paragraph: {paragraph}

                                Grade Level: {grade}

                                Curriculum Standard: {standard}

                                Number of Sentences Required: {noQues}
            
            
            
            ### Strictly Enforced Rules ###
            1. Strictly ensure to generate exactly {noQues} sentences in the output.
            2. Ensure that there should be no empty sentence , {grammerPrompt}.
            3. The sentences should be presented in a random order.
            4. For each sentence The JSON object must use the schema: {schema}.
            5. Store response for each sentence in dictionary format.
            6. ***Strictly ensure to respond only data like Example JSON and no other message in any case.
            7. Most Importantly : Only generate "Example JSON structure" without any message .

            Please generate a similar JSON structure for the given topic, grade level, standard, and number of questions.
            '''
            example_schema = '''
                    Example JSON:
                    {
                        "sentences": [
                            {
                                "sentence": "{Rephrased sentence 1}",
                                "subject": "{Subject of sentence 1}",
                                "predicate": "{Predicate of sentence 1}"
                            },
                            {
                                "sentence": "{Rephrased sentence 2}",
                                "subject": "{Subject of sentence 2}",
                                "predicate": "{Predicate of sentence 2}"
                            },
                            ...
                        ]
                    }
        '''
            # logging.info('User prompt:' + user_prompt);

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt + example_schema}
                ],
                model=model,
                temperature=0.2,
                # Streaming is not supported in JSON mode
                stream=False,
                # Enable JSON mode by setting the response format
                # response_format={"type": "json_object"},
            )
            
            response = chat_completion.choices[0].message.content
            logging.info(f"type of response : {type(response)}")
            logging.info(f"Received response from Groq: {response}")
            json_str =  re.search(r'(\{\s*"sentences"\s*:\s*\[.*?\}\s*\]\s*\})', response, re.DOTALL).group(0)
            logging.info(f"Received response from json_str: {json_str}")
    # Convert the string back to a JSON object (to ensure it's valid JSON)
            data = json.loads(json_str)
            # data = json.loads(response)

    # Extract the list of sentences
            sentences = data['sentences']
            quizVal = random.sample(sentences, min(noQues, len(sentences)))
            logging.info("quizVal ---------------: ",quizVal)   
            return quizVal
       

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            return f"Error occurred: {str(e)}"
   
def get_sub_predicate(paragraph: str, grade:int , model: str, standard : str, noQuestion: int):
    grammerPrompt = "subject and predicate"
    logging.info(f"paragraph : {paragraph} grade : {grade} model {model} standard : {standard} noQues : {noQuestion}")
    schema = json.dumps(SubjectPredicate.model_json_schema(), indent=2)
    SVP = GrammerElement()
    sentences = SVP.get_quiz(paragraph, grade, standard, noQuestion, grammerPrompt , model, schema)
    correctOrder = []
    for item in sentences:
        correctOrder.append({
            'subject': item['subject'],
            'predicate': item['predicate']
        })
    return QuizResponse(sentences=sentences, correctOrder=correctOrder)