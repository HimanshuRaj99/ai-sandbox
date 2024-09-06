import logging
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnableSequence

import json
from typing import Dict, List, Union

class RolePlayerBot:
    def get_response(self, user_input: str, memory: ConversationBufferWindowMemory, conversation_chain: RunnableSequence) -> Dict[str, Union[str, List[str]]]:
        # logging.info(f"Current memory state: {memory.load_memory_variables({})}")

        if user_input == 'mcq':
            user_input = '''
                Generate only one MCQ question if the conversation so far contains enough factual information or historical details to form a meaningful question. 
                The question should be directly relevant to the discussed topics, with four answer options provided. 
                If the conversation lacks sufficient detail to create an MCQ, respond with a message advising to wait for more discussion.

                Output Format:

                        **IF there is enough context:
                            {
                                "character_message": "Question) ask the question",     
                                "suggestions": [
                                        "1) Option 1",
                                        "2) Option 2",
                                        "3) Option 3",
                                        "4) Option 4"
                                                ]
                            }


                        **IF there is not enough context:

                            {
                                "character_message": "Ah, young friend! It is not a right time to begin questioning your knowledge. Let's wait for some time.",     
                                "suggestions": []
                            }
            '''

        try:
            reply = conversation_chain.invoke({
                "human_input": user_input,
                "chat_history": memory.chat_memory.messages
            })

            # Update memory with the new message
            memory.chat_memory.add_user_message(user_input)
            memory.chat_memory.add_ai_message(reply)

            # logging.info(f"Updated memory state: {memory.load_memory_variables({})}")

            print("User:", user_input)
            print("Bot:", reply)
            
            json_response = json.loads(reply)
            logging.info(f"Response from Model: {json_response}")

            # Validate that the response has the correct structure
            if not isinstance(json_response, dict):
                raise ValueError("Response is not a JSON object")
            if "character_message" not in json_response or "suggestions" not in json_response:
                raise ValueError("Response is missing required fields")
            if not isinstance(json_response["suggestions"], list):
                raise ValueError("Suggestions must be a list")
            
            # For MCQ, we allow either 0 or 4 suggestions
            if user_input == 'mcq' and len(json_response["suggestions"]) not in [0, 4]:
                raise ValueError("MCQ suggestions must be either empty or contain exactly 4 items")
            # For non-MCQ responses, we require exactly 4 suggestions
            elif user_input != 'mcq' and len(json_response["suggestions"]) != 4:
                raise ValueError("Non-MCQ suggestions must contain exactly 4 items")

            return json_response

        except json.JSONDecodeError:
            logging.error("Failed to parse response as JSON")
        except ValueError as e:
            logging.error(f"Invalid response format: {str(e)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
        
        # If parsing fails or any other error occurs, create a default response
        return {
            "character_message": "I apologize, but I seem to have encountered an issue. Could you please repeat your question?",
            "suggestions": [
                "Can you rephrase that?",
                "Let's try a different topic.",
                "Would you like me to explain something else?",
                "Should we start over?"
            ]
        }