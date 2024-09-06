from gtts import gTTS
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Pronounce:
    def __init__(self) -> None:
        pass

    def text_to_pronunciation(self, word):
        try:
            # Log the start of the pronunciation function
            logging.info("Pronunciation Function Triggered...")

            # Initialize gTTS object with the word and language
            tts = gTTS(text=word, lang='en')

            # Create a BytesIO object to store the audio content
            audio_buffer = io.BytesIO()

            # Save the audio content to the BytesIO buffer
            tts.write_to_fp(audio_buffer)

            # Get the audio content as bytes
            audio_content = audio_buffer.getvalue()

            logging.info("Audio content generated in memory")
            logging.info("Pronunciation Finished...")

            # Return success status and audio content
            return True, audio_content

        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"An error occurred: {e}")
            # Return failure status and error message
            return False, str(e)

# Example usage
# if __name__ == "__main__":
#     word = "favorite"
#     obj1 = Pronounce()
#     success, result = obj1.text_to_pronunciation(word)
#     if success:
#         logging.info(f"The pronunciation of the word '{word}' has been generated successfully")
#         logging.info(f"Audio content size: {len(result)} bytes")
#     else:
#         logging.error(f"Failed to generate pronunciation: {result}")