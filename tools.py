import os 
import requests
import datetime

def grab(url, savename, name=''):
    # URL of the website
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Send a GET request to the website
    response = requests.get(url, headers=headers)
    print('Collected? HTML Length = '+str(len(response.text)))
    
    # Save the raw HTML with savename and timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"logs/{savename}__{name}__{timestamp}.txt"
    
    # Ensure "logs/" directory exists
    if not os.path.exists("logs/"):
        os.makedirs("logs/")
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)
    
    return response.text