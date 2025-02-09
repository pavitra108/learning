import requests
import json
import os

def get_exchange_rates():
    app_id = os.getenv('open_exchange_APP_ID')
    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    data = response.json()
    return data

a = get_exchange_rates()
print(a)
m = a['rates'].get("AED")
print(m)