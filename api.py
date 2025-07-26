from flask import Flask, jsonify, request
import threading
import time
import random

app = Flask(__name__)

is_running = False
loop_count = 0
total_sent = 0

# Simulated background thread
def request_sender():
    global is_running, loop_count, total_sent
    while is_running:
        loop_count += 1
        # Simulate sending 100 requests per loop
        for _ in range(100):
            total_sent += 1
            time.sleep(random.uniform(0.01, 0.02))  # simulate delay
        time.sleep(1)

@app.route('/start', methods=["POST"])
def start():
    global is_running
    if not is_running:
        is_running = True
        threading.Thread(target=request_sender, daemon=True).start()
        return jsonify({"status": "started", "running": is_running, "loop_count": loop_count, "total_sent": total_sent})
    return jsonify({"status": "already running", "running": is_running})

@app.route('/stop', methods=["POST"])
def stop():
    global is_running
    is_running = False
    return jsonify({"status": "stopped", "running": is_running})

@app.route('/status', methods=["GET"])
def status():
    return jsonify({
        "running": is_running,
        "loop_count": loop_count,
        "total_sent": total_sent
    })

if __name__ == "__main__":
    app.run(debug=True)
