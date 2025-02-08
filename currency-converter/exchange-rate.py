import requests
import json
import os

def get_exchange_rates():
    app_id = os.getenv('APP_ID')
    print(app_id)
    url = f"https://openexchangerates.org/api/latest.json?app_id=d69755469a4c4784a02221e1342762e7"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    data = response.json()
    return data

a = get_exchange_rates()
print(a)