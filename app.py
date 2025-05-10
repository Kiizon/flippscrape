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

def get_grocery_flyer_id():
    """ Return flyer id's for grocery stores that are labeled as "Groceries" to filter out non-grocery flyers"""
    response_data = get_flyers_by_postal_code()
    
    if "flyers" not in response_data:
        return None
        
    grocery_flyer_ids = []
    
    for flyer in response_data['flyers']:
        merchant = flyer.get('merchant')
        categories = flyer.get('categories', [])
        
        # Convert categories to list if it's a string
        if isinstance(categories, str):
            categories = [cat.strip() for cat in categories.split(',')]
        
        if merchant in GROCERY_STORES:
            if "Groceries" in categories:
                grocery_flyer_ids.append(flyer['id'])
    
    return grocery_flyer_ids if grocery_flyer_ids else None


flyer_ids = get_grocery_flyer_id()
print(flyer_ids)
