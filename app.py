from flask import Flask, jsonify
import threading
import time
import random
import os

app = Flask(__name__)

# Shared variables for temperature and humidity
data = {"temperature": None, "humidity": None}

def update_values():
    """Background thread to update values every 10 seconds."""
    while True:
        # Simulate sensor readings
        data["temperature"] = round(random.uniform(20.0, 30.0), 2)  # °C
        data["humidity"] = round(random.uniform(40.0, 60.0), 2)     # %
        print(f"Updated: {data}")
        time.sleep(10)  # update every 10s (change to 60 for 1 min)

@app.route("/")
def home():
    return jsonify({"message": "Flask API is running. Go to /values for data."})

@app.route("/values", methods=["GET"])
def get_values():
    """API endpoint to get the latest temperature and humidity."""
    return jsonify(data)

# Start the background thread
thread = threading.Thread(target=update_values, daemon=True)
thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT dynamically
    app.run(debug=False, host="0.0.0.0", port=port)
