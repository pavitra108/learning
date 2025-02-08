from flask import Flask, render_template, request, send_file



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

        # Get currency exchange rates


        # Convert the amount
        converted_amount = amount * (currency_rates[to_currency] / currency_rates[from_currency])

        return render_template("converter-page.html", converted_amount=converted_amount,
                               from_currency=from_currency, to_currency=to_currency, amount=amount)


if __name__ == "__main__":
    app.run(debug=True)