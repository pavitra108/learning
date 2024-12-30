from flask import Flask, request, jsonify

app = Flask(__name__)

# Data storage (in-memory for simplicity)
data = {
    "name": None,
    "city": None
}

# Endpoint to collect name
@app.route('/collect_name', methods=['POST'])
def collect_name():
    try:
        name = request.json.get('name')  # Get the name from the JSON request body
        if not name:
            return jsonify({"error": "Name is required"}), 400

        data['name'] = name  # Save the name to the data store
        return jsonify({"message": "Name collected successfully", "name": name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to collect city
@app.route('/collect_city', methods=['POST'])
def collect_city():
    try:
        city = request.json.get('city')  # Get the city from the JSON request body
        if not city:
            return jsonify({"error": "City is required"}), 400

        data['city'] = city  # Save the city to the data store
        return jsonify({"message": "City collected successfully", "city": city}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve all data
@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
