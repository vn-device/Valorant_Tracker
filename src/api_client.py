import requests
from typing import List, Dict, Any
from config import Config

class HenrikAPIClient:
    BASE_URL = "https://api.henrikdev.xyz/valorant"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": Config.API_KEY,
            "User-Agent": "DeviceTacticalAnalyst/1.0"
        })

    def get_competitive_matches(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Fetches the last 'limit' COMPETITIVE matches."""
        endpoint = f"{self.BASE_URL}/v3/matches/{Config.REGION}/{Config.NAME}/{Config.TAG}"
        
        try:
            response = self.session.get(endpoint, params={
                "mode": "competitive", 
                "size": limit
            })
            response.raise_for_status()
            data = response.json()
            
            if not data.get('data'):
                print(f"No competitive matches found for {Config.NAME}#{Config.TAG}")
                return []
                
            return data['data'] # Returns the list of matches
            
        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")
            return []