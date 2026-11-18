"""
bowling_metrics.py - Calculates bowling performance metrics across baseline and pressure contexts.
Computes overs, legal balls, runs conceded, wickets, economy, strike rate, average, and dot %.
"""
import pandas as pd
import numpy as np

def compute_bowler_aggregates(df: pd.DataFrame, prefix: str = "") -> pd.DataFrame:
    """
    Computes bowling aggregates for a subset of balls (e.g. all balls vs pressure balls).
    Note: Overs are computed from legal deliveries.
    Runs conceded exclude fielding extras (byes, leg-byes).
    Wickets count only bowler-credited dismissals (Bowled, Caught, LBW, Stumped, Hit Wicket).
    """
    grouped = df.groupby(['bowler_id', 'bowler_name'])
    
    # 1. Total deliveries and legal deliveries
    total_balls = grouped.size()
    legal_balls = grouped['is_legal_ball'].sum()
    
    # 2. Runs conceded (excluding byes / legbyes)
    runs_conceded = grouped['bowler_runs_conceded'].sum()
    
    # 3. Wickets credited to bowler
    wickets = grouped['is_bowler_wicket'].sum()
    
    # 4. Dot balls: deliveries where 0 runs were conceded off the bat and no extras conceded
    dots = (df['bowler_runs_conceded'] == 0).groupby([df['bowler_id'], df['bowler_name']]).sum()
    
    # 5. Boundaries conceded (fours and sixes)
    boundaries = (df['is_four'] | df['is_six']).groupby([df['bowler_id'], df['bowler_name']]).sum()
    
    # 6. Matches bowled in
    matches = grouped['match_id'].nunique()
    
    res = pd.DataFrame({
        f'{prefix}legal_balls': legal_balls,
        f'{prefix}total_balls': total_balls,
        f'{prefix}runs_conceded': runs_conceded,
        f'{prefix}wickets': wickets,
        f'{prefix}dots': dots,
        f'{prefix}boundaries_conceded': boundaries,
        f'{prefix}matches': matches
    }).reset_index()
    
    # Overs bowled (legal balls / 6.0)
    res[f'{prefix}overs'] = res[f'{prefix}legal_balls'] / 6.0
    
    # Economy rate = runs_conceded / overs
    res[f'{prefix}economy'] = np.where(
        res[f'{prefix}overs'] > 0,
        res[f'{prefix}runs_conceded'] / res[f'{prefix}overs'],
        0.0
    )
    
    # Bowling Strike Rate = legal_balls / wickets
    res[f'{prefix}strike_rate'] = np.where(
        res[f'{prefix}wickets'] > 0,
        res[f'{prefix}legal_balls'] / res[f'{prefix}wickets'],
        res[f'{prefix}legal_balls'].astype(float)
    )
    
    # Bowling Average = runs_conceded / wickets
    res[f'{prefix}average'] = np.where(
        res[f'{prefix}wickets'] > 0,
        res[f'{prefix}runs_conceded'] / res[f'{prefix}wickets'],
        res[f'{prefix}runs_conceded'].astype(float)
    )
    
    # Dot ball % = dots / total_balls * 100
    res[f'{prefix}dot_pct'] = np.where(
        res[f'{prefix}total_balls'] > 0,
        (res[f'{prefix}dots'] / res[f'{prefix}total_balls']) * 100.0,
        0.0
    )
    
    # Boundary conceded % = boundaries / total_balls * 100
    res[f'{prefix}boundary_conceded_pct'] = np.where(
        res[f'{prefix}total_balls'] > 0,
        (res[f'{prefix}boundaries_conceded'] / res[f'{prefix}total_balls']) * 100.0,
        0.0
    )
    
    return res

def build_bowling_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes both baseline (normal) and pressure metrics for all bowlers,
    and calculates comparative suppression / delta metrics.
    """
    # 1. Overall / Normal baseline
    normal_df = compute_bowler_aggregates(df, prefix="norm_")
    
    # 2. Pressure situations
    pressure_data = df[df['is_high_pressure']]
    press_df = compute_bowler_aggregates(pressure_data, prefix="press_")
    
    # 3. Merge profiles
    merged = normal_df.merge(press_df, on=['bowler_id', 'bowler_name'], how='left')
    
    for col in merged.columns:
        if col.startswith('press_'):
            merged[col] = merged[col].fillna(0)
            
    # 4. Comparative lift / Delta metrics
    # Economy suppression: norm_economy - press_economy (Positive is BETTER: bowler restricts runs under pressure!)
    merged['econ_suppression'] = merged['norm_economy'] - merged['press_economy']
    
    # Dot ball lift: press_dot_pct - norm_dot_pct (Positive is BETTER)
    merged['dot_lift'] = merged['press_dot_pct'] - merged['norm_dot_pct']
    
    # Boundary prevention: norm_boundary_conceded_pct - press_boundary_conceded_pct (Positive is BETTER)
    merged['boundary_prevention'] = merged['norm_boundary_conceded_pct'] - merged['press_boundary_conceded_pct']
    
    # Wicket rate lift (wickets per legal ball under pressure vs normal)
    press_wkt_rate = np.where(merged['press_legal_balls'] > 0, merged['press_wickets'] / merged['press_legal_balls'], 0.0)
    norm_wkt_rate = np.where(merged['norm_legal_balls'] > 0, merged['norm_wickets'] / merged['norm_legal_balls'], 0.0)
    merged['wkt_rate_lift'] = (press_wkt_rate - norm_wkt_rate) * 100.0
    
    # Standardize player identifiers
    merged = merged.rename(columns={'bowler_id': 'player_id', 'bowler_name': 'player_name'})
    return merged

if __name__ == "__main__":
    from config import PROCESSED_DATA_DIR
    df = pd.read_parquet(PROCESSED_DATA_DIR / "ball_by_ball_pressure_classified.parquet")
    bowl_profile = build_bowling_profile(df)
    
    print("\n--- SAMPLE BOWLING PROFILE (TOP BY PRESSURE BALLS BOWLED) ---")
    sample = bowl_profile.sort_values(by='press_legal_balls', ascending=False).head(10)
    cols_show = ['player_name', 'press_legal_balls', 'norm_economy', 'press_economy', 'norm_average', 'press_average', 'press_wickets', 'press_dot_pct']
    print(sample[cols_show].to_string(index=False))
