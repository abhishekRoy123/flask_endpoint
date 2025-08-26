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
        time.sleep(10)


@app.route("/values", methods=["GET"])
def get_values():
    """API endpoint to get the latest temperature and humidity."""
    return jsonify(data)


if __name__ == "__main__":
    # Start the background thread
    thread = threading.Thread(target=update_values, daemon=True)
    thread.start()

    # Use Render's provided PORT environment variable (fallback: 5000 for local)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
