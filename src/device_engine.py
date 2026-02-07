from typing import Dict, List, Any  # Added Any
from config import Config # Fixed Import Case

class DeviceEngine:
    def __init__(self, match_data: Dict[str, Any]):
        self.match = match_data
        # We don't need to store player_name here if we extract it dynamically
        self.hero_stats = self._extract_hero_stats()

    def _extract_hero_stats(self):
        """Finds the user's specific stats within the match data."""
        # Safety check for API structure
        all_players = self.match.get('players', {}).get('all_players', [])
        
        for player in all_players:
            # Case-insensitive comparison for robust matching
            if (player['name'].lower() == Config.NAME.lower() and 
                player['tag'].lower() == Config.TAG.lower()):
                return player
        return None

    def analyze_untradeability(self) -> str:
        if not self.hero_stats:
            return f"Error: Player {Config.NAME}#{Config.TAG} not found in match."

        stats = self.hero_stats['stats']
        total_rounds = self.match['metadata']['rounds_played']
        deaths = stats['deaths']
        
        # Safety Check: In weird edge cases, deaths > rounds implies bad data or non-standard mode
        survived_rounds = max(0, total_rounds - deaths)
        
        if total_rounds == 0:
            return "Error: Match data indicates 0 rounds played."

        survival_rate = (survived_rounds / total_rounds) * 100
        kd_ratio = stats['kills'] / deaths if deaths > 0 else stats['kills']

        analysis = [
            f"--- Device Alignment Report for {self.match['metadata']['map']} ---",
            f"Survival Rate: {survival_rate:.1f}% (Target: >45%)",
            f"K/D Ratio:     {kd_ratio:.2f} (Target: >1.2)",
        ]

        # Tactical Logic remains the same...
        if survival_rate < 35:
            analysis.append(">> CRITICAL: You are dying too often. Device prioritizes survival to anchor sites.")
            analysis.append(">> ACTION: Stop re-peeking angles after missing the first shot.")
        elif kd_ratio < 1.0:
            analysis.append(">> WARNING: Inefficient trading. You are taking 50/50 duels instead of 70/30s.")
        else:
            analysis.append(">> SUCCESS: High systemic impact. You are playing the numbers game correctly.")

        return "\n".join(analysis)