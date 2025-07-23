# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata
# app/models.py

from datetime import datetime, timezone
import threading

url_store = {}
lock = threading.Lock()

def save_url_mapping(short_code, original_url):
    with lock:
        url_store[short_code] = {
            "url": original_url,
            "clicks": 0,
            "created_at": datetime.now(timezone.utc)  
        }

def get_original_url(short_code):
    with lock:
        return url_store.get(short_code)

def increment_clicks(short_code):
    with lock:
        if short_code in url_store:
            url_store[short_code]['clicks'] += 1

def get_url_stats(short_code):
    with lock:
        return url_store.get(short_code)
