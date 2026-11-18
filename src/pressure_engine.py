"""
pressure_engine.py - Quantifies and labels match pressure dynamically.
Calculates continuous pressure index (0 to 1) and discrete pressure tiers (Low, Medium, High).
Accounts for distinct 1st innings setting and 2nd innings chasing dynamics.
"""
import pandas as pd
import numpy as np

def compute_chase_pressure_score(df: pd.DataFrame) -> pd.Series:
    """
    Computes continuous pressure score for 2nd innings chasing:
    Pressure increases with:
    1. Higher Required Run Rate (RRR) relative to par T20 run rate (8.5 rpo).
    2. Fewer balls remaining (urgency amplifier).
    3. Fewer wickets in hand (risk of getting bowled out).
    
    Formula components:
    - rrr_factor = clip((RRR - 6.0) / 10.0, 0, 1.5)
    - wicket_pressure = clip((10 - wickets_in_hand) / 7.0, 0, 1.2)
    - death_urgency = 1.3 if overs 16-20, 1.1 if overs 11-15, 1.0 otherwise
    """
    rrr = df['required_run_rate'].fillna(8.0)
    wih = df['wickets_in_hand']
    balls_rem = df['balls_remaining']
    phase = df['phase']
    
    # Baseline T20 RRR normalization (8.0 is average, 14.0 is extreme pressure)
    rrr_pressure = np.clip((rrr - 7.0) / 7.0, 0.0, 1.5)
    
    # Wicket risk: 10 wickets is 0 risk, <= 3 wickets in hand is critical risk
    wkt_risk = np.clip((10.0 - wih) / 6.0, 0.0, 1.5)
    
    # Time/balls decay: pressure rises steeply when balls remaining is small
    time_factor = np.where(balls_rem <= 30, 1.3, np.where(balls_rem <= 60, 1.1, 1.0))
    
    # Continuous composite score (0 to 1.0 scale)
    raw_score = (0.55 * rrr_pressure + 0.35 * wkt_risk + 0.10 * (phase == 'Death').astype(float)) * time_factor
    return np.clip(raw_score / 1.5, 0.0, 1.0)

def compute_setting_pressure_score(df: pd.DataFrame) -> pd.Series:
    """
    Computes continuous pressure score for 1st innings target setting:
    In the 1st innings, pressure is driven by:
    1. Early wicket collapse (Powerplay with >= 3 wickets down).
    2. Middle over crisis (Middle phase with >= 5 wickets down).
    3. Death overs acceleration pressure (Overs 16-20 where batting team must attack).
    4. Slog overs with tail/limited resources (Death phase with <= 5 wickets in hand).
    """
    phase = df['phase']
    wkt_lost = df['current_wickets_lost']
    wih = df['wickets_in_hand']
    crr = df['current_run_rate']
    over = df['overid']
    
    # 1. Collapse pressure
    # Early collapse: lost 3+ wickets in overs 1-6
    early_collapse = (phase == 'Powerplay') & (wkt_lost >= 3)
    # Middle collapse: lost 5+ wickets in overs 7-15
    mid_collapse = (phase == 'Middle') & (wkt_lost >= 5)
    
    collapse_factor = np.where(mid_collapse, 0.9, np.where(early_collapse, 0.85, (wkt_lost / 10.0) * 0.5))
    
    # 2. Death overs urgency
    death_factor = np.where((phase == 'Death') & (wih <= 4), 0.95,
                   np.where(phase == 'Death', 0.75, 0.2))
    
    # 3. Sluggish run rate pressure in late overs (overs > 10 and CRR < 7.0)
    sluggish_factor = np.where((over > 10) & (crr < 7.0), 0.3, 0.0)
    
    raw_score = np.maximum(collapse_factor, death_factor) + sluggish_factor
    return np.clip(raw_score, 0.0, 1.0)

def classify_pressure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies unified pressure index and assigns discrete tiers:
    - High Pressure (Index >= 0.65)
    - Medium Pressure (0.35 <= Index < 0.65)
    - Low / Normal (Index < 0.35)
    """
    out = df.copy()
    
    # Calculate continuous scores separately for innings 1 vs 2
    is_inn2 = out['innings'] == 2
    
    score_inn2 = compute_chase_pressure_score(out)
    score_inn1 = compute_setting_pressure_score(out)
    
    out['pressure_index'] = np.where(is_inn2, score_inn2, score_inn1)
    
    # Discrete category
    out['pressure_tier'] = pd.cut(
        out['pressure_index'],
        bins=[-np.inf, 0.35, 0.65, np.inf],
        labels=['Low', 'Medium', 'High']
    )
    
    # Flag for high pressure deliveries
    out['is_high_pressure'] = out['pressure_tier'] == 'High'
    out['is_medium_pressure'] = out['pressure_tier'] == 'Medium'
    out['is_pressure_ball'] = out['pressure_index'] >= 0.50 # General pressure definition
    
    return out

if __name__ == "__main__":
    from config import PROCESSED_DATA_DIR
    df = pd.read_parquet(PROCESSED_DATA_DIR / "ball_by_ball_processed.parquet")
    scored = classify_pressure(df)
    
    print("\n--- PRESSURE TIER DISTRIBUTION ---")
    print(scored['pressure_tier'].value_counts(normalize=True).apply(lambda x: f"{x*100:.2f}%"))
    print("\nBreakdown by Innings:")
    print(pd.crosstab(scored['innings'], scored['pressure_tier'], margins=True))
    
    # Save enriched dataset with pressure classifications
    scored.to_parquet(PROCESSED_DATA_DIR / "ball_by_ball_pressure_classified.parquet", index=False)
    print("\nSaved classified dataset successfully!")
