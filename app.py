import requests, json, random
import pandas as pd

FLYERS = 'https://flyers-ng.flippback.com/api/flipp/data?locale=en&postal_code={}&sid={}'
FLYER_ITEMS = 'https://flyers-ng.flippback.com/api/flipp/flyers/{}/flyer_items?locale=en&sid={}'
GROCERY_STORES = {'No Frills', 'FreshCo', 'Walmart', 'Loblaws'}


def generate_sid():
    """
    Generate a session ID for the Flipp API.
    """
    return ''.join(str(random.randint(0,9)) for _ in range(16))

def get_flyers_by_postal_code(postal_code: str):
    """
    Fetch flyer data from Flipp API given a postal code and a session ID.
    
    """
    sid = generate_sid()
    url = FLYERS.format(postal_code, sid)
    response = requests.get(url)
    response.raise_for_status() 
    return response.json()

def get_grocery_flyer_id(postal_code: str):
    """ 
    Return flyer id's for grocery stores applicable to given postal code that are labeled as "Groceries" to filter out non-grocery flyers
    
    """
    response_data = get_flyers_by_postal_code(postal_code)
    
    if 'flyers' not in response_data:
        return None
        
    grocery_flyers = []
    
    for flyer in response_data['flyers']:
        merchant = flyer.get('merchant')
        categories = flyer.get('categories', [])
        
        # Convert categories to list if it's a string
        if isinstance(categories, str):
            categories = [cat.strip() for cat in categories.split(',')]
        
        if merchant in GROCERY_STORES:
            if 'Groceries' in categories:
                grocery_flyers.append({
                    'id': flyer['id'],
                    'merchant': merchant
                })
    
    return grocery_flyers if grocery_flyers else None

def get_flyer_items(flyer_id: int):
    """ Return flyer items for a given flyer id"""
    sid = generate_sid()
    
    url = FLYER_ITEMS.format(flyer_id, sid)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def main():
    # Get postal code from user
    while True:
        postal_code = input('Enter your postal code (format: A1A1A1): ').strip().upper()
        if len(postal_code) == 6 and postal_code[0].isalpha() and postal_code[1].isdigit() and \
           postal_code[2].isalpha() and postal_code[3].isdigit() and postal_code[4].isalpha() and postal_code[5].isdigit():
            break
        print('Invalid postal code format. Please use format A1A1A1 (e.g., M5V2H1)')
    
    print(f'\nFetching flyers for postal code: {postal_code}')
    
    # Get grocery flyers with their merchant names
    grocery_flyers = get_grocery_flyer_id(postal_code)
    
    if not grocery_flyers:
        print('No grocery flyers found for this postal code.')
        return
    
    print(f'Found {len(grocery_flyers)} grocery flyers')
    
    csv_data = []
    for flyer in grocery_flyers:
        flyer_id = flyer['id']
        merchant = flyer['merchant']
        print(f'Processing {merchant} flyer...')
        
        items = get_flyer_items(flyer_id)
        
        for item in items:
            csv_data.append({
                'merchant': merchant,
                'flyer_id': flyer_id,
                'name': item.get('name', ''),
                'price': item.get('price', ''),
                'valid_from': item.get('valid_from', ''),
                'valid_to': item.get('valid_to', '')
            })
    
    if csv_data:
        df = pd.DataFrame(csv_data)
        filename = f'flyer_items_{postal_code}.csv'
        df.to_csv(filename, index=False)
        print(f'\nSuccessfully saved {len(csv_data)} items to {filename}')
    else:
        print('No items found to save.')

if __name__ == '__main__':
    main()
