"""
batting_metrics.py - Fixed batting averages with proper numeric player IDs.
"""
import pandas as pd
import numpy as np

def compute_batter_aggregates(df: pd.DataFrame, prefix: str = "") -> pd.DataFrame:
    """
    Computes batting aggregates for a subset of balls.
    Balls faced excludes wides.
    Dismissals match striker_id with dismissed_player_id accurately.
    """
    # Ensure numeric types for reliable joins and comparisons
    df_calc = df.copy()
    df_calc['striker_id'] = pd.to_numeric(df_calc['striker_id'], errors='coerce')
    df_calc['dismissed_player_id'] = pd.to_numeric(df_calc['dismissed_player_id'], errors='coerce')
    
    grouped = df_calc.groupby(['striker_id', 'striker_name'])
    
    balls_faced = grouped['is_ball_faced'].sum()
    runs = grouped['batter_runs'].sum()
    fours = grouped['is_four'].sum()
    sixes = grouped['is_six'].sum()
    
    # Dots: ball faced where batter scored 0
    dots = ((df_calc['batter_runs'] == 0) & df_calc['is_ball_faced']).groupby([df_calc['striker_id'], df_calc['striker_name']]).sum()
    
    matches = grouped['match_id'].nunique()
    innings = grouped.apply(lambda g: g[['match_id', 'innings']].drop_duplicates().shape[0])
    
    # Dismissals for this batter
    is_dismissed = df_calc['is_wicket'] & (df_calc['dismissed_player_id'] == df_calc['striker_id'])
    dismissals = is_dismissed.groupby([df_calc['striker_id'], df_calc['striker_name']]).sum()
    
    res = pd.DataFrame({
        f'{prefix}runs': runs,
        f'{prefix}balls_faced': balls_faced,
        f'{prefix}fours': fours,
        f'{prefix}sixes': sixes,
        f'{prefix}dots': dots,
        f'{prefix}dismissals': dismissals,
        f'{prefix}matches': matches,
        f'{prefix}innings': innings
    }).reset_index()
    
    # Strike rate
    res[f'{prefix}strike_rate'] = np.where(
        res[f'{prefix}balls_faced'] > 0,
        (res[f'{prefix}runs'] / res[f'{prefix}balls_faced']) * 100.0,
        0.0
    )
    
    # Batting average
    res[f'{prefix}average'] = np.where(
        res[f'{prefix}dismissals'] > 0,
        res[f'{prefix}runs'] / res[f'{prefix}dismissals'],
        res[f'{prefix}runs'].astype(float)
    )
    
    # Boundary %
    res[f'{prefix}boundary_pct'] = np.where(
        res[f'{prefix}balls_faced'] > 0,
        ((res[f'{prefix}fours'] + res[f'{prefix}sixes']) / res[f'{prefix}balls_faced']) * 100.0,
        0.0
    )
    
    # Dot ball %
    res[f'{prefix}dot_pct'] = np.where(
        res[f'{prefix}balls_faced'] > 0,
        (res[f'{prefix}dots'] / res[f'{prefix}balls_faced']) * 100.0,
        0.0
    )
    
    return res

def build_batting_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Computes baseline vs pressure metrics for batters."""
    normal_df = compute_batter_aggregates(df, prefix="norm_")
    
    pressure_data = df[df['is_high_pressure']]
    press_df = compute_batter_aggregates(pressure_data, prefix="press_")
    
    merged = normal_df.merge(press_df, on=['striker_id', 'striker_name'], how='left')
    
    for col in merged.columns:
        if col.startswith('press_'):
            merged[col] = merged[col].fillna(0)
            
    # Lift metrics
    merged['sr_lift'] = merged['press_strike_rate'] - merged['norm_strike_rate']
    merged['boundary_lift'] = merged['press_boundary_pct'] - merged['norm_boundary_pct']
    merged['dot_reduction'] = merged['norm_dot_pct'] - merged['press_dot_pct']
    
    merged = merged.rename(columns={'striker_id': 'player_id', 'striker_name': 'player_name'})
    return merged

if __name__ == "__main__":
    from config import PROCESSED_DATA_DIR
    df = pd.read_parquet(PROCESSED_DATA_DIR / "ball_by_ball_pressure_classified.parquet")
    bat_profile = build_batting_profile(df)
    
    print("\n--- SAMPLE BATTING PROFILE (TOP BY PRESSURE BALLS FACED) ---")
    sample = bat_profile.sort_values(by='press_balls_faced', ascending=False).head(10)
    cols_show = ['player_name', 'press_innings', 'press_balls_faced', 'norm_strike_rate', 'press_strike_rate', 'norm_average', 'press_average', 'press_boundary_pct']
    print(sample[cols_show].round(2).to_string(index=False))
