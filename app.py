from flask import Flask, jsonify
import threading
import time
import random

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
        time.sleep(10)  # update interval


@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return jsonify(message="Flask API is running! Go to /values for data.")


@app.route("/values", methods=["GET"])
def get_values():
    """API endpoint to get the latest temperature and humidity."""
    return jsonify(data)


# Start background thread when the app starts
def start_background_thread():
    thread = threading.Thread(target=update_values, daemon=True)
    thread.start()


# Run only if executed directly (not when gunicorn imports it)
if __name__ == "__main__":
    start_background_thread()
    app.run(host="0.0.0.0", port=5000, debug=True)
else:
    # Start background thread when loaded by gunicorn
    start_background_thread()
