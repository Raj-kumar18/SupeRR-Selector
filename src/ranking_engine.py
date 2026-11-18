"""
ranking_engine.py - Generates final Top 10 Batters and Bowlers Under Pressure.
Enriches with primary team, competition context, and outputs formatted tables.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from config import OUTPUTS_DIR, PROCESSED_DATA_DIR
from src.batting_metrics import build_batting_profile
from src.bowling_metrics import build_bowling_profile
from src.reliability_model import score_batting_reliability, score_bowling_reliability
from src.data_loader import load_raw_data

def get_player_team_context(raw_dfs: dict) -> pd.DataFrame:
    """Finds the most frequent / primary team for each player."""
    mapping = raw_dfs['mapping']
    p11 = raw_dfs['playing_eleven']
    teams = raw_dfs['teams'].drop_duplicates(subset=['team_id'])
    
    # Merge team names
    m_teams = mapping.groupby('player_id')['team_name'].agg(lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else x.iloc[0]).reset_index()
    return m_teams

def generate_official_rankings():
    """Generates official Top 10 Batters and Top 10 Bowlers Under Pressure."""
    print("Loading enriched ball-by-ball dataset...")
    df = pd.read_parquet(PROCESSED_DATA_DIR / "ball_by_ball_pressure_classified.parquet")
    raw_dfs = load_raw_data()
    team_context = get_player_team_context(raw_dfs)
    
    # 1. Batting Rankings
    print("Computing Batting Reliability Scores...")
    bat_profile = build_batting_profile(df)
    bat_scored = score_batting_reliability(bat_profile)
    bat_scored = bat_scored.merge(team_context, on='player_id', how='left')
    bat_scored['team_name'] = bat_scored['team_name'].fillna('Global T20')
    
    top10_batters = bat_scored.head(10).copy()
    top10_batters['Rank'] = range(1, 11)
    
    # 2. Bowling Rankings
    print("Computing Bowling Reliability Scores...")
    bowl_profile = build_bowling_profile(df)
    bowl_scored = score_bowling_reliability(bowl_profile)
    bowl_scored = bowl_scored.merge(team_context, on='player_id', how='left')
    bowl_scored['team_name'] = bowl_scored['team_name'].fillna('Global T20')
    
    top10_bowlers = bowl_scored.head(10).copy()
    top10_bowlers['Rank'] = range(1, 11)
    
    # Save outputs
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    top10_batters.to_csv(OUTPUTS_DIR / "top_10_batters_under_pressure.csv", index=False)
    top10_bowlers.to_csv(OUTPUTS_DIR / "top_10_bowlers_under_pressure.csv", index=False)
    bat_scored.to_csv(OUTPUTS_DIR / "all_eligible_batters.csv", index=False)
    bowl_scored.to_csv(OUTPUTS_DIR / "all_eligible_bowlers.csv", index=False)
    
    print("\n" + "="*80)
    print("🏏 TOP 10 BATTERS UNDER PRESSURE (RAJASTHAN ROYALS SUPE-RR SELECTOR)")
    print("="*80)
    bat_display = top10_batters[['Rank', 'player_name', 'team_name', 'press_innings', 'press_balls_faced', 
                                 'norm_strike_rate', 'press_strike_rate', 'norm_average', 'press_average', 
                                 'press_boundary_pct', 'sr_lift', 'reliability_score']]
    print(bat_display.round(2).to_string(index=False))
    
    print("\n" + "="*80)
    print("🎯 TOP 10 BOWLERS UNDER PRESSURE (RAJASTHAN ROYALS SUPE-RR SELECTOR)")
    print("="*80)
    bowl_display = top10_bowlers[['Rank', 'player_name', 'team_name', 'norm_matches', 'press_legal_balls', 
                                  'norm_economy', 'press_economy', 'norm_average', 'press_average', 
                                  'press_wickets', 'press_dot_pct', 'econ_suppression', 'reliability_score']]
    print(bowl_display.round(2).to_string(index=False))
    
    return top10_batters, top10_bowlers

if __name__ == "__main__":
    generate_official_rankings()
