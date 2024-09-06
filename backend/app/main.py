from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pathlib import Path
from app.schema.schemas import *
from app.controller.chatbot import RolePlayerBot
from app.controller.config_llm import ConfigureModel
from app.controller.text_to_speech import Pronounce
from app.controller.generate_meaning import RevealMeaning
from app.controller.get_groq_models import GroqModelLists
from app.controller.read_ai import ReaderAI
from app.controller.request_feature import send_email, EmailSchema 
from app.controller.get_age import select_age
from app.controller import word_filter
from app.controller.wordplay import generate_wordplay_schema
from app.controller.generate_img import query
from app.controller.word_swap import WordSwapGenerator
from app.controller.grammar_elements import get_sub_predicate
from app.controller.story_sequence import get_sequence
import requests
import io
import os
from PIL import Image
from io import BytesIO
import logging
import json
import os
 
# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS settings
origins = [
    "https://ai-sandbox-quantum.vercel.app",
    "https://ai-sandbox.vercel.app",
    "http://localhost:3000",
    "http://localhost:8080"
]

# origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_memory = None
conversation_chain = None

# Path to the JSON file containing model information
# MODEL_JSON_PATH = Path(__file__).parent / "model_list.json"

@app.post("/configure")
async def configure(config_request: ConfigRequest):
    """
    Endpoint to handle configure llm model.

    Args:
        config_request (ConfigRequest): The configuration request data.

    Returns:
        bool: True if configuration is successful, otherwise False.
    """
    try:
        global conversation_memory, conversation_chain
        # Log the incoming request data for debugging
        logging.info(f"Incoming request data: {config_request}")

        llm_provider = config_request.provider
        llm_model = config_request.model
        character = config_request.character
        grade = config_request.grade
        version = config_request.version
        standard = config_request.standard

        student_age = select_age(grade)
        logging.info(f'AGE: {student_age}')
        # Initialize the role player bot
        bot = ConfigureModel(provider_name=llm_provider, model_name=llm_model, character=character, grade=grade, version=version, student_age=student_age, standard=standard)
        conversation_memory, conversation_chain = bot.llm_config()
            
        if conversation_memory is None or conversation_chain is None:
            return {"status": False}
        return {"status": True}
    except Exception as e:
        logging.error(f"Error in /configure endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    """
    Endpoint to handle chat requests.

    Args:
        chat_request (ChatRequest): The chat request data.

    Returns:
        ChatResponse: The chat response data.
    """
    try:
        global conversation_memory, conversation_chain
        # Log the incoming request data for debugging
        logging.info(f"Incoming request data: {chat_request}")

        # Extract details from the request
        user_message = chat_request.message

        # Use the RolePlayerBot to get a response
        bot = RolePlayerBot()
        response = bot.get_response(user_message, conversation_memory, conversation_chain)

        # Prepare the response
        # reply = ChatResponse(response=response)
        logging.info(f"Response Type: {type(response)}")
        logging.info("Response Sent")
        return response
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Create a security scheme for the passcode
PASSCODE_HEADER = APIKeyHeader(name="X-Passcode")

# Function to verify the passcode
def verify_passcode(request: Request, passcode: str = Depends(PASSCODE_HEADER)):
    referer = request.headers.get('referer')
    logger.info(f"Request referer: {referer}")

    if referer and referer.startswith('https://ai-sandbox-quantum.vercel.app'):
        logger.info("Passcode verification required")
        correct_passcode = os.getenv("APP_PASSCODE")
        
        if not passcode:
            raise HTTPException(status_code=403, detail="Passcode required")
        
        logger.info(f"Correct Passcode: {correct_passcode}, Input Passcode: {passcode}")
        
        if passcode != correct_passcode:
            raise HTTPException(status_code=403, detail="Invalid passcode")
        
        logger.info("Passcode verified successfully")
    else:
        logger.info("Passcode verification not required for this referer")
    
    return passcode

@app.post("/api/verify-passcode")
async def verify_passcode_endpoint(passcode: str = Depends(verify_passcode)):
    logger.info("Passcode verification endpoint called")
    return {"status": "success", "message": "Passcode verified"}

# Reader AI : Find Meaning API 
@app.post("/find-meaning")
async def get_meaning(find_meaning_request: FindMeaningRequest):
    """
    Endpoint to handle reader ai find meaning requests.

    Args:
        find_meaning_request (FindMeaningRequest): The reader ai request data.

    Returns:
        Response: Meaning in json format with key as 'meaning'
    """
    try:
        text = find_meaning_request.selected_characters
        context = find_meaning_request.context
        grade = find_meaning_request.grade

        reader = ReaderAI()
        meaning = reader.find_meaning(text, context, grade)
        if not meaning:
            return {'meaning': 'Failed to retrieve meaning'}
        return json.loads(meaning)
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/simplify-meaning")
async def simplify_meaning(simplify_meaning_request: SimplifyMeaningRequest):
    """
    Endpoint to handle reader ai simplify meaning requests.

    Args:
        find_meaning_request (SimplifyMeaningRequest): The reader ai request data.

    Returns:
        Response: Simplified Meaning in json format with key as 'simplified_meaning'
    """
    try:

        logging.info(f"Incoming request data: {simplify_meaning_request}")
        text = simplify_meaning_request.text
        context = simplify_meaning_request.context
        grade = simplify_meaning_request.grade
        generated_meaning = simplify_meaning_request.generated_meaning


        reader = ReaderAI()
        meaning = reader.simplify_meaning(text, context, grade, generated_meaning)
        if not meaning:
            return {'meaning': 'Failed to retrieve meaning'}
        return json.loads(meaning)
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/activities")
async def activities(activity_request: ActivityRequest):
    """
    Endpoint to handle activities requests.

    Args:
        clickpronounce_request (ActivityRequest): The activities request data.

    Returns:
        JSON: Wordplay Schema with three words with their prexi, root, suffix and word itself.
    """
    try:
        content = activity_request.content
        type = activity_request.type
        if type=='wordplay':
            wordplay_json = generate_wordplay_schema(content)
            if not wordplay_json:
                raise Exception("LLM Response Generation Failed.")
            return wordplay_json
        return {"Type of Activity is not defined or found."}
    except Exception as e:
        logging.error(f"Error in /click-to-pronounce endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/click-to-reveal")
async def click_to_reveal(request: Request, clickreveal_request: ClickRevealRequest):
    """
    Endpoint to handle click-to-reveal requests.

    Args:
        clickreveal_request (ClickRevealRequest): The click-to-reveal request data.

    Returns:
        JSON: The meaning and morphology of the word.
    """

    print(f"Received request from origin: {request.headers.get('origin')}")

    try:
        # Log the incoming request
        logging.info("Click to reveal initiated")
        logging.info(f"ClickRevealRequest object: {clickreveal_request}")

        # Extract the word from the request
        word = clickreveal_request.word
        grade = clickreveal_request.grade
        model = clickreveal_request.model
        
        #check if word is inappropriate
        isInAppropriate = word_filter.check_if_censored(word)
        logging.info(f'Checking if word is InAppropriate....')
        logging.info(f'isInappropriate: {isInAppropriate}')
        if isInAppropriate:
            logging.info(f'The word is inAppropriate, can not retireve meaning for such words.')
            return {'result' :'The word you searched for is considered inappropriate. Please try searching for another word.'}
        
        # Initialize the RevealMeaning instance
        reveal_meaning = RevealMeaning()

        # Get the meaning and morphology of the word
        meaning_morpho = reveal_meaning.get_meaning(word, grade, model)
        if not meaning_morpho:
            raise HTTPException(status_code=400, detail="Failed to retrieve meaning")

        logging.info("Process Completed")
        return json.loads(meaning_morpho)  # Return the response in JSON format
    except Exception as e:
        logging.error(f"Error in click-to-reveal endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Retrieving directly in Vue.js from Assets folder

# @app.get("/models")
# async def get_models():
#     """
#     Endpoint to fetch models from the Groq API.
#     """
#     try:
#         with open(MODEL_JSON_PATH, 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         logging.error(f"Model list JSON file not found at {MODEL_JSON_PATH}")
#         raise HTTPException(status_code=500, detail="Model list configuration not found")
#     except json.JSONDecodeError:
#         logging.error(f"Invalid JSON in model list file at {MODEL_JSON_PATH}")
#         raise HTTPException(status_code=500, detail="Invalid model list configuration")

# endpoint to send email
@app.post("/send-email")
async def send_email_endpoint(email_data: EmailSchema):
    logging.info("Email Process started")
    send_email(email_data.email, email_data.subject, email_data.message)
    return {"message": "Email has been sent successfully"}

@app.route('/request-feature', methods=['POST'])
def request_feature():
    data = request.json
    feature_name = data.get('featureName')
    use_cases = data.get('useCases')
    suggestions = data.get('suggestions')

    # Create email content
    subject = f"New Feature Request: {feature_name}"
    body = f"""
    New Feature Request:

    Feature Name: {feature_name}

    Use Cases:
    {use_cases}

    Suggestions:
    {suggestions}
    """

    # Send email
    try:
        send_feature_request_email(subject, body)
        return jsonify({"message": "Feature request submitted successfully!"}), 200
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({"message": "An error occurred while processing your request."}), 500

@app.post("/generate-synonym-swap")
async def synonym_swap(request: Request):
    data = await request.json()
    topic = data.get("topic")
    gradeLevel = data.get("gradeLevel")
    model = data.get("model")
    standard = data.get("standard")
    num_questions = data.get("num_questions")

    generator = WordSwapGenerator()
    result = generator.generate_synonym_swap(topic, gradeLevel, model, standard, num_questions)

    return JSONResponse(content=result)

# Uncomment and implement if needed
@app.post("/click-to-pronounce", response_model=ClickPronounceResponse)
async def click_to_pronounce(clickpronounce_request: ClickPronounceRequest):
    """
    Endpoint to handle click-to-pronounce requests.

    Args:
        clickpronounce_request (ClickPronounceRequest): The click-to-pronounce request data.

    Returns:
        StreamingResponse: The pronunciation audio content.
    """
    try:
        logging.info("Incoming request data for click-to-pronounce")
        logging.info(f"ClickPronounceRequest object: {clickpronounce_request}")

        selected_word = clickpronounce_request.word

        # Input Validation
        if not selected_word.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid input: word cannot be empty or whitespace."
            )

        # Initialize the Pronounce instance
        pronounce = Pronounce()
        status_success, audio_content = pronounce.text_to_pronunciation(selected_word)
        
        if not status_success:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail="Failed to process the word pronunciation."
            )
        
        if not audio_content:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT, 
                detail="No audio content generated."
            )

        # Use StreamingResponse to stream the audio content
        return StreamingResponse(
            BytesIO(audio_content), 
            media_type="audio/mp3", 
            headers={"Content-Disposition": "inline; filename=output1.mp3"}
        )
    
    except HTTPException as http_exc:
        logging.error(f"HTTPException in /click-to-pronounce endpoint: {http_exc.detail}")
        raise http_exc
    
    except Exception as e:
        logging.error(f"Unexpected error in /click-to-pronounce endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal Server Error"
        )
    
@app.post("/api/generate-SVP-quiz")
async def generate_SVP_quiz(request: GenerateSVPQuiz):
    try:
        paragraph = request.paragraph
        grade =request.gradeLevel
        model= request.model
        standard= request.standard
        noQuestion = request.numQuestions
        result = get_sub_predicate(paragraph, grade, model, standard, noQuestion)
        return result
    except Exception as e:
        # Log the exception
        logging.error("Error in generate_SVP_quiz: %s", e)
        
        # Return an HTTP 500 Internal Server Error response
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/sequence-story")
async def get_story_sequence(generate_sequence: GenerateSequenceStory):
    """
    Endpoint to fetch models from the Groq API.
    """
    logging.info("get_story_sequence initialized")
    try:
        paragraph = generate_sequence.topic
        grade =generate_sequence.gradeLevel
        model = generate_sequence.model
        result = get_sequence(paragraph, grade, model)
        # logging.info("sequence : ",result.sequenceOrder)
        return result
    except Exception as e:
        # Log the exception
        logging.error("Error in generate_SVP_quiz: %s", e)

        # Return an HTTP 500 Internal Server Error response
        raise HTTPException(status_code=500, detail="Internal Server Error")

# @app.get("/story-image")
# async def get_image(request: Request):
#     logging.info("initialized story image generation")
#     # logging.info("request img val : ",request.inputs)
#     logging.info("----------")
#     data = await request.json()
#     logging.info("data val : ",data)
#     result = query(data)
#     logging.info("response received from query : ")
#     save_folder = "../frontend/src/assets"
# # Load the image from the returned bytes
#     image = Image.open(io.BytesIO(result))  
#     image_path = os.path.join(save_folder, "flux_img.png")
#     image.save(image_path)
#     logging.info("saved file")

    
