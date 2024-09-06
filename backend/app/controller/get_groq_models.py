from dotenv import load_dotenv  # Importing the library to load environment variables from a .env file
import os  # Importing the os module to access environment variables
import requests  # Importing the requests library to make HTTP requests

# Load environment variables from a .env file
load_dotenv()

class GroqModelLists:
    def __init__(self) -> None:
        # Retrieve the API key from environment variables
        self.api_key = os.getenv('GROQ_API_KEY')
        
        # Ensure the API key is available
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")
        
    def get_models(self):
        # Define the API endpoint URL
        url = "https://api.groq.com/openai/v1/models"
        
        # Set up the headers with the authorization token
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            # Make a GET request to the API endpoint
            response = requests.get(url, headers=headers)
            
            # Raise an exception for HTTP error responses
            response.raise_for_status()
            
            # Return the JSON response
            return response.json()
        
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            # Handle connection errors
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            # Handle timeout errors
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            # Handle other request-related errors
            print(f"An error occurred: {req_err}")
        except Exception as e:
            # Handle any other exceptions
            print(f"An unexpected error occurred: {e}")

# Example usage
# if __name__ == "__main__":
#     groq_model_lists = GroqModelLists()
#     models = groq_model_lists.get_models()
#     if models:
#         print(models)
