from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display the form
@app.route('/')
def index():
    return render_template('indexpage.html')  # This will render the HTML file

# Route to handle form submission
@app.route('/collect_data', methods=['POST'])
def collect_data():
    # Get data from the form
    name = request.form['name']
    city = request.form['city']

    # Check if the data is provided
    if not name or not city:
        return "Both name and city are required."

    # Process the data (you can add more logic here)
    return f"Data received. Name: {name}, City: {city}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
