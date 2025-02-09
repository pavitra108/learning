from flask import Flask, render_template, request, send_file
from rates import get_exchange_rates

# The application code
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('converter-page.html')


@app.route('/convert', methods=['POST'])
def convert_currency():
    # Convert given currency based on the latest exchange rates.
    f_currency = request.form["from_currency"]
    t_currency = request.form["to_currency"]
    amount = float(request.form["amount"])

    # Get currency exchange rates
    value = get_exchange_rates()

    from_currency_rates = value['rates'].get(f_currency, None)
    to_currency_rates = value['rates'].get(t_currency, None)

    # Convert the amount
    if from_currency_rates and to_currency_rates:
        converted_amount = amount * (to_currency_rates / from_currency_rates)
        converted_amount = round(converted_amount, 2) if converted_amount is not None else None
    else:
        converted_amount = None  # Handle invalid currency codes

    return render_template("converter-page.html", converted_amount=converted_amount,
                           from_currency=f_currency, to_currency=t_currency, amount=amount)

if __name__ == "__main__":
    app.run(debug=True)