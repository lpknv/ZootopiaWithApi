import json
import requests

import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL')
HEADERS = {
    "X-Api-Key": os.getenv('API_KEY')
}


def fetch_data(animal_name):
    """
    Fetches the animals data for the animal 'animal_name'.
    Returns: a list of animals, each animal is a dictionary:
    {
        'name': ...,
        'taxonomy': {
        ...
        },
        'locations': [
        ...
        ],
        'characteristics': {
        ...
        }
    },
    """

    try:
        response = requests.get(
            API_URL,
            headers=HEADERS,
            params={"name": animal_name}
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as request_exception:
        print("Error:", request_exception)
        return []