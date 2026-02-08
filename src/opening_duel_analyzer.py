from typing import Dict, Any, List

class OpeningDuelAnalyzer:
    def __init__(self, match_data: Dict[str, Any], hero_puuid: str):
        self.match = match_data
        self.hero_puuid = hero_puuid

    def analyze(self) -> Dict[str, float]:
        if not self.hero_puuid:
            return {"fb": 0, "fd": 0, "win_rate": 0.0, "fd_rate": 0.0, "attempts": 0}

        first_bloods = 0
        first_deaths = 0
        rounds_played = 0

        rounds = self.match.get('rounds', [])
        
        for round_data in rounds:
            rounds_played += 1
            
            all_kills = []

            # --- STRATEGY 1: Global Event Log (Preferred) ---
            raw_kills = round_data.get('kill_events')
            if raw_kills and isinstance(raw_kills, list):
                all_kills = raw_kills
            
            # --- STRATEGY 2: Player Stats Fallback ---
            # Only run this if Strategy 1 failed
            elif not all_kills:
                stats = round_data.get('player_stats', [])
                for player in stats:
                    killer_id = player.get('player_puuid')
                    
                    # CRITICAL FIX: Check if 'kills' is a list or just a number
                    player_kills = player.get('kills', [])
                    
                    if isinstance(player_kills, (int, float)):
                        # Data is just a count (e.g. 2). No timestamps available. Skip.
                        continue
                    
                    if isinstance(player_kills, list):
                        for k in player_kills:
                            # Inject implicit killer ID
                            if isinstance(k, dict):
                                k['killer_puuid'] = killer_id
                                all_kills.append(k)

            # --- ANALYSIS LOGIC ---
            if not all_kills:
                # If no kill data exists for this round, we skip it without crashing.
                continue

            # Sort by time
            valid_kills = [k for k in all_kills if isinstance(k, dict) and k.get('kill_time_in_round') is not None]
            valid_kills.sort(key=lambda x: x.get('kill_time_in_round'))

            if not valid_kills:
                continue

            first_kill = valid_kills[0]
            
            k_id = first_kill.get('killer_puuid')
            v_id = first_kill.get('victim_puuid')

            if k_id == self.hero_puuid:
                first_bloods += 1
            elif v_id == self.hero_puuid:
                first_deaths += 1

        # --- FINAL CALCS ---
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