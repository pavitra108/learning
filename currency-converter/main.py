from flask import Flask, render_template, request, send_file
import requests
import json
import os

def get_exchange_rates():
    app_id = os.getenv('APP_ID')
    print(app_id)
    url = f"https://openexchangerates.org/api/latest.json?app_id=d69755469a4c4784a02221e1342762e7"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.json()


# The application code
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('converter-page.html')


@app.route('/convert', methods=['POST'])
def abc():
    if request.method == "POST":
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        amount = float(request.form["amount"])

        # Convert the amount
        converted_amount = amount * (currency_rates[to_currency] / currency_rates[from_currency])

        return render_template("converter-page.html", converted_amount=converted_amount,
                               from_currency=from_currency, to_currency=to_currency, amount=amount)


