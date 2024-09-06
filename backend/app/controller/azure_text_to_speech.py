import os
import logging
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='text_to_speech.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class TextToSpeech:
    def __init__(self):
        # Set up the subscription info for the Speech Service
        self.subscription_key = os.getenv('AZURE_API_KEY')
        self.region = os.getenv('AZURE_REGION')
        
        # Validate environment variables
        if not self.subscription_key or not self.region:
            logging.error("Azure API key or region not found in environment variables.")
            raise ValueError("Azure API key or region not found in environment variables.")
        
        # Create a speech configuration with the subscription info
        self.speech_config = speechsdk.SpeechConfig(subscription=self.subscription_key, region=self.region)

    def synthesize_speech(self, text, output_file="output_audio.wav"):
        try:
            # Create an audio configuration that points to an output file
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            
            # Create a speech synthesizer using the speech configuration and audio configuration
            speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)
            
            # Generate speech from the text
            result = speech_synthesizer.speak_text_async(text).get()
            
            # Check the result
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logging.info(f"Speech synthesized for text [{text}], and the audio was saved as {output_file}.")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logging.warning(f"Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logging.error(f"Error details: {cancellation_details.error_details}")
        
        except Exception as e:
            logging.error(f"An error occurred during speech synthesis: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    tts = TextToSpeech()
    tts.synthesize_speech("Hello, this is Sandbox AI")
