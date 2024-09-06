import requests
import json

def get_word_info(word):
    # Define the API endpoint with the given word
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        # Send a GET request to the API
        response = requests.get(url)
        # Raise an exception if there was an HTTP error
        response.raise_for_status()  
    except requests.RequestException as e:
        # Return an error message if the request failed
        return f"Request failed: {e}"

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        # Return an error message if the status code is not 200
        return f"Error: {response.status_code}"
