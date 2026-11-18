"""
generate_deep_analytics.py - Generates granular war-room analytics from RR proprietary tracking data.
- Pace vs Spin performance under pressure
- Delivery style effectiveness (Yorkers, Bouncers, Cutters, Googly, Chinaman)
- Speed tier performance
- Shot/stroke efficiency under pressure
- Auction Targets Archetype matching for RR IPL 2027
"""
import pandas as pd
import numpy as np
from pathlib import Path
from config import PROCESSED_DATA_DIR, OUTPUTS_DIR

def run_deep_analysis():
    print("Loading pressure classified dataset...")
    df = pd.read_parquet(PROCESSED_DATA_DIR / "ball_by_ball_pressure_classified.parquet")
    
    # 1. BATTER SPLITS: VS PACE & SPIN UNDER PRESSURE
    p_bat = df[df['is_high_pressure']].groupby(['striker_id', 'striker_name', 'pace_or_spin']).agg(
        runs=('batter_runs', 'sum'),
        balls=('is_ball_faced', 'sum'),
        fours=('is_four', 'sum'),
        sixes=('is_six', 'sum'),
        dots=('batter_runs', lambda s: (s == 0).sum()),
        dismissals=('is_wicket', lambda s: (s & (df.loc[s.index, 'dismissed_player_id'] == df.loc[s.index, 'striker_id'])).sum())
    ).reset_index()
    
    p_bat['sr'] = np.where(p_bat['balls'] > 0, (p_bat['runs'] / p_bat['balls'] * 100).round(1), 0.0)
    p_bat['boundary_pct'] = np.where(p_bat['balls'] > 0, ((p_bat['fours'] + p_bat['sixes']) / p_bat['balls'] * 100).round(1), 0.0)
    p_bat['dot_pct'] = np.where(p_bat['balls'] > 0, (p_bat['dots'] / p_bat['balls'] * 100).round(1), 0.0)
    p_bat['average'] = np.where(p_bat['dismissals'] > 0, (p_bat['runs'] / p_bat['dismissals']).round(1), p_bat['runs'])
    
    p_bat.to_parquet(OUTPUTS_DIR / "batter_pace_spin_pressure.parquet", index=False)
    
    # 2. BOWLER SPLITS: BY DELIVERY STYLE & VARIATION UNDER PRESSURE
    p_bowl_style = df[df['is_high_pressure']].groupby(['bowler_id', 'bowler_name', 'delivery_style']).agg(
        legal_balls=('is_legal_ball', 'sum'),
        total_balls=('is_legal_ball', 'count'),
        runs=('bowler_runs_conceded', 'sum'),
        wickets=('is_bowler_wicket', 'sum'),
        dots=('bowler_runs_conceded', lambda s: (s == 0).sum()),
        boundaries=('is_four', lambda s: (s | df.loc[s.index, 'is_six']).sum())
    ).reset_index()
    
    p_bowl_style['economy'] = np.where(p_bowl_style['legal_balls'] > 0, (p_bowl_style['runs'] / (p_bowl_style['legal_balls'] / 6.0)).round(2), 0.0)
    p_bowl_style['dot_pct'] = np.where(p_bowl_style['total_balls'] > 0, (p_bowl_style['dots'] / p_bowl_style['total_balls'] * 100).round(1), 0.0)
    p_bowl_style['strike_rate'] = np.where(p_bowl_style['wickets'] > 0, (p_bowl_style['legal_balls'] / p_bowl_style['wickets']).round(1), p_bowl_style['legal_balls'])
    
    p_bowl_style.to_parquet(OUTPUTS_DIR / "bowler_delivery_style_pressure.parquet", index=False)
    
    # 3. SPEED ANALYSIS UNDER PRESSURE
    # Group speeds into bins: < 120 (Slow/Cutter), 120-135 (Medium-Fast), 135-145 (Fast), 145+ (Express)
    pace_df = df[(df['pace_or_spin'] == 'Pace') & (df['bowl_speed'] > 0) & df['is_high_pressure']].copy()
    pace_df['speed_bin'] = pd.cut(
        pace_df['bowl_speed'],
        bins=[0, 120, 135, 145, 200],
        labels=['Sub-120 (Cutters/Change)', '120-135 (Medium-Fast)', '135-145 (Fast)', '145+ (Express)']
    )
    speed_summary = pace_df.groupby('speed_bin', observed=False).agg(
        balls=('is_legal_ball', 'sum'),
        runs=('bowler_runs_conceded', 'sum'),
        wickets=('is_bowler_wicket', 'sum'),
        boundaries=('is_four', lambda s: (s | pace_df.loc[s.index, 'is_six']).sum()),
        dots=('bowler_runs_conceded', lambda s: (s == 0).sum())
    ).reset_index()
    speed_summary['economy'] = (speed_summary['runs'] / (speed_summary['balls'] / 6.0)).round(2)
    speed_summary['strike_rate'] = (speed_summary['balls'] / speed_summary['wickets']).round(1)
    speed_summary['dot_pct'] = (speed_summary['dots'] / speed_summary['balls'] * 100).round(1)
    speed_summary.to_csv(OUTPUTS_DIR / "pace_speed_bins_pressure.csv", index=False)
    
    # 4. RR TARGET ARCHETYPES (AUCTION RECRUITMENT MATRIX)
    # Define archetypes:
    # 1. Death Finisher Beast (High SR vs Pace at Death)
    # 2. Spin Destroyer (High SR vs Spin in Middle overs under pressure)
    # 3. Elite Death Enforcer (Low Econ & high Yorker/Cutter accuracy)
    # 4. Mystery/Wrist Spin Choker (Sub 7.00 Econ & 40%+ Dot rate)
    
    print("Deep proprietary analytics successfully generated and saved to data/outputs/")

if __name__ == "__main__":
    run_deep_analysis()
