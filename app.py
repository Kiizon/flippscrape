import requests
import json
import random

FLYERS = "https://flyers-ng.flippback.com/api/flipp/data?locale=en&postal_code={}&sid={}"
FLYER_ITEMS = "https://flyers-ng.flippback.com/api/flipp/flyers/{}/flyer_items?locale=en&sid={}"
GROCERY_STORES = { "No Frills", "FreshCo", "Walmart", "Loblaws"}


def generate_sid():
    """
    Generate a session ID for the Flipp API.
    """
    return "".join(str(random.randint(0,9)) for _ in range(16))

def get_flyers_by_postal_code():
    """
    Fetch flyer data from Flipp API given a postal code and a session ID.
    """
    sid = generate_sid()
    postal_code = "L6S2C6"
    url = FLYERS.format(postal_code, sid)
    response = requests.get(url)
    response.raise_for_status() 
    return response.json()
