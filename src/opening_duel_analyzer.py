from typing import Dict, Any
from config import Config

class OpeningDuelAnalyzer:
    def __init__(self, match_data: Dict[str, Any]):
        self.match = match_data
        self.name = Config.NAME.lower()
        self.tag = Config.TAG.lower()

    def analyze(self) -> Dict[str, float]:
        """
        Scans all rounds to calculate:
        1. First Bloods (FB): You killed the first enemy.
        2. First Deaths (FD): You died first.
        3. Attempt Rate: How often you are involved in the first fight.
        """
        first_bloods = 0
        first_deaths = 0
        rounds_played = 0

        # The API structure for rounds contains 'player_stats' and 'kill_events'
        rounds = self.match.get('rounds', [])
        
        for round_data in rounds:
            rounds_played += 1
            kill_events = round_data.get('player_stats', []) 
            # Note: v3 API organizes kills inside 'kill_events' list usually, 
            # but sometimes we must look at the event log. 
            # Let's try the direct 'kill_events' array if available, or parse stats.
            
            # Robust extraction of the first kill in the round
            events = round_data.get('defuse_events', []) + round_data.get('plant_events', []) + round_data.get('kill_events', [])
            
            # Filter only kills and sort by time
            kills = [e for e in events if 'killer_display_name' in e]
            kills.sort(key=lambda x: x.get('kill_time_in_round', 999999))

            if not kills:
                continue

            first_kill = kills[0]
            
            # Check if user is involved
            # API names often include tag, or just name. We check strict containment or exact match.
            killer_name = first_kill.get('killer_display_name', '').lower()
            victim_name = first_kill.get('victim_display_name', '').lower()
            
            # We match against the Config name
            # Note: The API 'display_name' usually looks like "device#4102"
            user_full = f"{self.name}#{self.tag}"
            
            if user_full in killer_name or self.name in killer_name:
                first_bloods += 1
            elif user_full in victim_name or self.name in victim_name:
                first_deaths += 1

        total_duels = first_bloods + first_deaths
        win_rate = (first_bloods / total_duels * 100) if total_duels > 0 else 0.0
        fd_rate = (first_deaths / rounds_played * 100) if rounds_played > 0 else 0.0

        return {
            "fb": first_bloods,
            "fd": first_deaths,
            "win_rate": win_rate,
            "fd_rate": fd_rate,
            "attempts": total_duels
        }