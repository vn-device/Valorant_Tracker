from typing import Dict, List, Any
from config import Config
from opening_duel_analyzer import OpeningDuelAnalyzer

class DeviceEngine:
    def __init__(self, match_data: Dict[str, Any]):
        self.match = match_data
        
        # 1. Find the Player Object first
        self.hero_stats = self._extract_hero_stats()
        
        # 2. Extract PUUID (Safely)
        hero_puuid = self.hero_stats.get('puuid') if self.hero_stats else None
        
        # 3. Inject PUUID into the Analyzer
        self.duel_analyzer = OpeningDuelAnalyzer(match_data, hero_puuid) 

    def _extract_hero_stats(self):
        all_players = self.match.get('players', {}).get('all_players', [])
        for player in all_players:
            # We still use Name for the initial lookup, which works on the Match level
            if (player['name'].lower() == Config.NAME.lower() and 
                player['tag'].lower() == Config.TAG.lower()):
                return player
        return None

    def generate_report(self) -> str:
        if not self.hero_stats:
            return f"Error: Player {Config.NAME}#{Config.TAG} not found in match."

        # --- Metric 1: Survival & Efficiency ---
        stats = self.hero_stats['stats']
        total_rounds = self.match['metadata']['rounds_played']
        deaths = stats['deaths']
        survived_rounds = max(0, total_rounds - deaths)
        
        if total_rounds == 0: return "Error: 0 rounds played."

        survival_rate = (survived_rounds / total_rounds) * 100
        kd_ratio = stats['kills'] / deaths if deaths > 0 else stats['kills']

        # --- Metric 2: Opening Duels ---
        duel_stats = self.duel_analyzer.analyze()
        
        # --- Report Formatting ---
        analysis = [
            f"--- Device Alignment Report for {self.match['metadata']['map']} ---",
            f"Survival Rate:    {survival_rate:.1f}%  (Target: >45%)",
            f"K/D Ratio:        {kd_ratio:.2f}    (Target: >1.2)",
            f"First Duels:      {duel_stats['fb']}W - {duel_stats['fd']}L ({duel_stats['win_rate']:.0f}% WR)",
            f"First Death Rate: {duel_stats['fd_rate']:.1f}%   (Target: <10%)"
        ]

        # --- Tactical Logic ---
        if survival_rate < 35:
            analysis.append(">> CRITICAL: Survival too low. Stop re-peeking angles.")
        
        if duel_stats['fd_rate'] > 15.0:
            analysis.append(">> WARNING: First Death Rate is too high. You are taking 50/50 opening fights.")
            analysis.append(">> ACTION: Let your teammates make first contact, then trade them.")
        
        if kd_ratio >= 1.2 and survival_rate >= 40 and duel_stats['fd_rate'] < 12:
            analysis.append(">> SUCCESS: Perfect Device Alignment. High impact, low risk.")

        return "\n".join(analysis)