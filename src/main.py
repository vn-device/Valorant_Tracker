from api_client import HenrikAPIClient
from device_engine import DeviceEngine
from config import Config

def main():
    print(f"Initializing Tactical Analysis for {Config.NAME}#{Config.TAG}...\n")
    
    # 1. Ingest (Last 3 Competitive Games)
    client = HenrikAPIClient()
    matches = client.get_competitive_matches(limit=3)
    
    if not matches:
        print("Aborting: Could not fetch match data.")
        return

    # Session Accumulators for "Consistency Score"
    total_rounds = 0
    total_survived = 0
    total_kills = 0
    total_deaths = 0

    # 2. Analyze & Loop
    for i, match_data in enumerate(matches, 1):
        engine = DeviceEngine(match_data)
        
        # We need to extract raw stats for the session summary
        # (This relies on the engine finding the player correctly)
        if engine.hero_stats:
            stats = engine.hero_stats['stats']
            match_rounds = match_data['metadata']['rounds_played']
            
            # Accumulate
            total_rounds += match_rounds
            total_deaths += stats['deaths']
            total_kills += stats['kills']
            
            # Print Individual Report
            # Uses .get() to safely fall back if the key is missing, preventing a crash
            print(f"--- Game {i}: {match_data['metadata']['map']} ({match_data['metadata'].get('game_start_patched', 'Unknown Date')}) ---")
            print(engine.analyze_untradeability())
            print("\n" + "="*40 + "\n")
        else:
            print(f"--- Game {i}: Player data not found ---\n")

    # 3. Session Insight (The Device Consistency Check)
    if total_rounds > 0:
        session_survival = ((total_rounds - total_deaths) / total_rounds) * 100
        session_kd = total_kills / total_deaths if total_deaths > 0 else total_kills
        
        print(f"📊 SESSION SUMMARY (Last {len(matches)} Games)")
        print(f"Avg Survival Rate: {session_survival:.1f}%")
        print(f"Avg K/D Ratio:     {session_kd:.2f}")
        
        if session_survival < 40:
            print(">> CONCLUSION: You are playing too aggressive. Device averages 45%+ survival.")
        else:
            print(">> CONCLUSION: Good systemic discipline.")

if __name__ == "__main__":
    main()