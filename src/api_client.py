import requests
import time
import functools
from typing import List, Dict, Any, Callable
from config import Config

def retry_with_backoff(retries: int = 3, backoff_in_seconds: int = 1):
    """
    Decorator that retries a function if it hits a Rate Limit (429) or Server Error (5xx).
    Uses exponential backoff: 1s -> 2s -> 4s.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.HTTPError as e:
                    # If we hit a Rate Limit (429) or Server Error (500+)
                    if e.response.status_code == 429 or 500 <= e.response.status_code < 600:
                        x += 1
                        if x > retries:
                            print(f"❌ Max retries exceeded after {retries} attempts.")
                            raise e
                        
                        sleep_time = backoff_in_seconds * (2 ** (x - 1))
                        print(f"⚠️ Rate Limit/Server Error {e.response.status_code}. Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                    else:
                        # If it's a 404 or 403, do not retry. Raise immediately.
                        raise e
        return wrapper
    return decorator

class HenrikAPIClient:
    BASE_URL = "https://api.henrikdev.xyz/valorant"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": Config.API_KEY,
            "User-Agent": "DeviceTacticalAnalyst/2.0"
        })

    @retry_with_backoff(retries=3)
    def get_competitive_matches(self, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Fetches the last 'limit' COMPETITIVE matches.
        Automatically handles Rate Limits via the decorator.
        """
        endpoint = f"{self.BASE_URL}/v3/matches/{Config.REGION}/{Config.NAME}/{Config.TAG}"
        
        try:
            # We explicitly raise_for_status() inside the try block so the decorator catches it
            response = self.session.get(endpoint, params={
                "mode": "competitive", 
                "size": limit
            })
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('data'):
                print(f"No competitive matches found for {Config.NAME}#{Config.TAG}")
                return []
                
            return data['data']
            
        except requests.exceptions.RequestException as e:
            # The decorator handles 429/5xx. This catches final failures.
            print(f"Network Error: {e}")
            return []