import logging
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

from app.controller.select_chatbot_prompt import SelectChatBotPrompt
from app.controller.prompt_generator import GeneratePrompt

# Load environment variables from a .env file
load_dotenv()

# Configure logging with timestamp, log level, and message format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConfigureModel:
    def __init__(self, provider_name: str, model_name: str, character: str, grade: int, version: str, student_age: str, standard: str):
        logging.info("Initializing ConfigureModel class")

        prompt_generator = GeneratePrompt()
        character_details = prompt_generator.get_prompt(character, grade, student_age)
        if not character_details:
            logging.error(f'Character Profile for {character} could not be generated')
        logging.info(f'Character Profile for {character} generated')

        # Choose prompt based on the version
        prompt_version = SelectChatBotPrompt()
        self.prompt = prompt_version.select_prompt(version, character, grade, character_details, standard)
        if not self.prompt:
            logging.error("Failed to select prompt, make sure you passed the correct version.")
            raise ValueError("Failed to select prompt, make sure you passed the correct version")
        logging.info(f"Version {version} prompt selected.")

        self.provider_name = provider_name
        self.model_name = model_name
        self.memory_length = 5
        self.character = character
        self.grade = grade
        logging.info(f"ConfigureModel initialized with model_name: {model_name}, character: {character}, grade: {grade}")

    def llm_config(self):
        logging.info("Configuring LLM and conversation memory")

        # Set up conversation memory with a buffer window
        self.memory = ConversationBufferWindowMemory(
            k=self.memory_length,
            memory_key="chat_history",
            return_messages=True
        )

        if self.provider_name == "OpenAI":
            logging.info(f"OPEN AI model name: {self.model_name}")
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set.")
            chat_model = ChatOpenAI(api_key=api_key, model_name=self.model_name)
        elif self.provider_name == "Google":
            logging.info("Google AI model: {self.model_name}")
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable is not set.")
            chat_model = ChatGoogleGenerativeAI(google_api_key=api_key, model=self.model_name)
        elif self.provider_name == "Anthropic":
            logging.info("Claude AI model: {self.model_name}")
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
            chat_model = ChatAnthropic(anthropic_api_key=api_key, model=self.model_name)
        # elif self.model_name.startswith("NVIDIA"):
        #     api_key = os.getenv('NVIDIA_API_KEY')
        #     api_url = os.getenv('NVIDIA_API_URL')
        #     if not api_key or not api_url:
        #         raise ValueError("NVIDIA_API_KEY or NVIDIA_API_URL environment variable is not set.")
        #     chat_model = ChatNVIDIA(model=self.model_name, nvidia_api_key=api_key, nvidia_api_url=api_url)
        elif self.provider_name in ["Mistral AI", "Meta"]:
            logging.info("GROQ AI model: {self.model_name}")
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                raise ValueError("GROQ_API_KEY environment variable is not set.")
            chat_model = ChatGroq(groq_api_key=api_key, model_name=self.model_name) 
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

        logging.info(f"{self.model_name} chat model initialized successfully")

        # Define the system prompt for the role-playing bot
        system_prompt = self.prompt
        logging.info("System prompt configured")

        # Create a prompt template using system messages and placeholders
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{human_input}")
            ]
        )
        logging.info("Prompt template created")

        # Create a chain that combines the prompt with the model
        model_chain = prompt | chat_model

        # Create the RunnableSequence with at least two steps
        self.conversation = RunnableSequence(
            model_chain,
            StrOutputParser()
        )

        logging.info("RunnableSequence conversation configured")

        return self.memory, self.conversation
    