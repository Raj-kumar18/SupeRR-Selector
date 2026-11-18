"""
reliability_model.py - Computes Batting and Bowling Pressure Reliability Scores.
Applies:
1. Multi-metric standardization (Z-scores / MinMax).
2. Performance under pressure + Lift over normal baseline.
3. Sample size Bayesian shrinkage / confidence weighting.
4. IPL vs T20I competition weighting.
"""
import pandas as pd
import numpy as np
from config import (
    MIN_PRESSURE_BALLS_FACED_BATTER,
    MIN_PRESSURE_BALLS_BOWLED_BOWLER,
    MIN_MATCHES_PLAYED,
    MIN_PRESSURE_INNINGS
)

def compute_sample_confidence(n: pd.Series, min_val: float, target_val: float) -> pd.Series:
    """
    Computes a smooth sigmoidal / logarithmic confidence adjustment factor between 0.50 and 1.0.
    Ensures players with small sample sizes have their score regressed towards median.
    """
    # Logistic confidence scaling
    factor = np.clip((n - min_val) / (target_val - min_val), 0.0, 1.0)
    # Smooth curve: 0.60 base + 0.40 * factor
    return 0.60 + 0.40 * np.sqrt(factor)

def score_batting_reliability(bat_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Batting Pressure Reliability Score (0 to 100):
    Components:
    1. Pressure Strike Rate (35%)
    2. Strike Rate Lift over baseline (20%)
    3. Pressure Batting Average (20%)
    4. Pressure Boundary Percentage (15%)
    5. Dot ball suppression / pressure dot % (10%)
    
    Adjusted by Sample Size Confidence.
    """
    df = bat_df.copy()
    
    # Filter minimum eligibility
    eligible = (
        (df['press_balls_faced'] >= MIN_PRESSURE_BALLS_FACED_BATTER) &
        (df['norm_matches'] >= MIN_MATCHES_PLAYED) &
        (df['press_innings'] >= MIN_PRESSURE_INNINGS)
    )
    df = df[eligible].copy()
    
    # Standardize individual components using percentiles / robust scaling
    def scale_col(s, higher_is_better=True):
        p10, p90 = s.quantile(0.05), s.quantile(0.95)
        clipped = np.clip(s, p10, p90)
        norm = (clipped - p10) / (p90 - p10 + 1e-6)
        return norm if higher_is_better else (1.0 - norm)
        
    s_press_sr = scale_col(df['press_strike_rate'], higher_is_better=True)
    s_sr_lift = scale_col(df['sr_lift'], higher_is_better=True)
    s_press_avg = scale_col(df['press_average'], higher_is_better=True)
    s_press_bound = scale_col(df['press_boundary_pct'], higher_is_better=True)
    s_press_dot = scale_col(df['press_dot_pct'], higher_is_better=False) # Lower dot % is better
    
    # Composite raw score (0 to 100)
    raw_bat_score = (
        0.35 * s_press_sr +
        0.20 * s_sr_lift +
        0.20 * s_press_avg +
        0.15 * s_press_bound +
        0.10 * s_press_dot
    ) * 100.0
    
    # Confidence weight based on pressure balls faced (target = 250 balls)
    conf = compute_sample_confidence(df['press_balls_faced'], min_val=MIN_PRESSURE_BALLS_FACED_BATTER, target_val=250.0)
    
    df['confidence_factor'] = conf
    # Regress to 50 for smaller samples
    df['reliability_score'] = (raw_bat_score * conf) + (50.0 * (1.0 - conf))
    df['reliability_score'] = df['reliability_score'].round(2)
    
    return df.sort_values(by='reliability_score', ascending=False).reset_index(drop=True)

def score_bowling_reliability(bowl_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Bowling Pressure Reliability Score (0 to 100):
    Components:
    1. Pressure Economy (30% - lower is better)
    2. Economy Suppression over baseline (20% - positive is better)
    3. Pressure Bowling Strike Rate / Wickets per ball (25% - lower SR is better)
    4. Pressure Dot Ball % (15% - higher is better)
    5. Pressure Boundary Conceded % (10% - lower is better)
    
    Adjusted by Sample Size Confidence.
    """
    df = bowl_df.copy()
    
    eligible = (
        (df['press_legal_balls'] >= MIN_PRESSURE_BALLS_BOWLED_BOWLER) &
        (df['norm_matches'] >= MIN_MATCHES_PLAYED)
    )
    df = df[eligible].copy()
    
    def scale_col(s, higher_is_better=True):
        p10, p90 = s.quantile(0.05), s.quantile(0.95)
        clipped = np.clip(s, p10, p90)
        norm = (clipped - p10) / (p90 - p10 + 1e-6)
        return norm if higher_is_better else (1.0 - norm)
        
    s_press_econ = scale_col(df['press_economy'], higher_is_better=False)
    s_econ_supp = scale_col(df['econ_suppression'], higher_is_better=True)
    s_press_sr = scale_col(df['press_strike_rate'], higher_is_better=False)
    s_press_dot = scale_col(df['press_dot_pct'], higher_is_better=True)
    s_press_bound = scale_col(df['press_boundary_conceded_pct'], higher_is_better=False)
    
    raw_bowl_score = (
        0.30 * s_press_econ +
        0.20 * s_econ_supp +
        0.25 * s_press_sr +
        0.15 * s_press_dot +
        0.10 * s_press_bound
    ) * 100.0
    
    # Confidence weight based on pressure legal balls (target = 250 balls)
    conf = compute_sample_confidence(df['press_legal_balls'], min_val=MIN_PRESSURE_BALLS_BOWLED_BOWLER, target_val=250.0)
    
    df['confidence_factor'] = conf
    df['reliability_score'] = (raw_bowl_score * conf) + (50.0 * (1.0 - conf))
    df['reliability_score'] = df['reliability_score'].round(2)
    
    return df.sort_values(by='reliability_score', ascending=False).reset_index(drop=True)
