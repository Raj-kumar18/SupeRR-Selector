"""
data_cleaning.py - Cleans raw cricket data and engineers ball-by-ball match state.
Calculates state variables strictly at the START of each delivery.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from config import (
    BOWLER_CREDITED_DISMISSALS,
    ILLEGAL_BALL_EXTRAS,
    PROCESSED_DATA_DIR
)
from src.data_loader import load_raw_data

def prepare_matches_metadata(matches: pd.DataFrame, comps: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans matches data, joins competition metadata, and categorizes tournament tier (IPL vs T20I).
    """
    df = matches.copy()
    comps_clean = comps[['comp_id', 'comp_name', 'match_format', 'season']].copy()
    
    # Merge competition details
    df = df.merge(comps_clean, on='comp_id', how='left')
    
    # Tag competition type cleanly
    df['is_ipl'] = df['comp_name'].str.contains('IPL', case=False, na=False)
    df['comp_type'] = np.where(df['is_ipl'], 'IPL', np.where(df['match_format'] == 'T20I', 'T20I', 'Other T20'))
    
    # Date parsing
    df['match_date'] = pd.to_datetime(df['match_date'])
    df['match_year'] = df['match_date'].dt.year
    
    return df

def clean_and_engineer_ball_by_ball(bbb: pd.DataFrame, matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds the fundamental delivery-level analytical dataset.
    Ensures precise MCC cricket rules:
    - Identifies legal deliveries (no wide, no overstep/no-ball).
    - Accurately tracks batter runs vs extras.
    - Accurately computes bowler runs conceded (excluding byes and leg-byes).
    - Accurately attributes wickets (bowler wickets vs runouts).
    - Computes running match state (score, wickets, balls remaining, target, RRR) BEFORE each ball.
    """
    df = bbb.copy()
    
    # Merge essential match metadata
    match_cols = matches_df[['match_id', 'comp_id', 'comp_name', 'comp_type', 'season', 'match_date', 
                             'revised_target', 'first_inn_revised_overs', 'second_inn_revised_overs']].copy()
    df = df.merge(match_cols, on='match_id', how='left')
    
    # Sort strictly in chronological delivery order
    df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num']).reset_index(drop=True)
    
    # Clean boolean flags
    for col in ['is_four', 'is_six', 'is_wicket']:
        df[col] = df[col].astype(str).str.lower().isin(['true', '1'])
        
    # Standardize numerical types
    df['runs'] = pd.to_numeric(df['runs'], errors='coerce').fillna(0).astype(int)
    df['extras1_runs'] = pd.to_numeric(df['extras1_runs'], errors='coerce').fillna(0).astype(int)
    df['extras_2_runs'] = pd.to_numeric(df['extras_2_runs'], errors='coerce').fillna(0).astype(int)
    df['extras_type'] = df['extras_type'].fillna('None')
    
    # Cricket Rules Logic
    # 1. Legal delivery identification
    df['is_legal_ball'] = ~df['extras_type'].isin(ILLEGAL_BALL_EXTRAS)
    
    # 2. Batter runs and balls faced
    df['batter_runs'] = df['runs']
    # A batter faces a ball on all deliveries EXCEPT wides
    df['is_ball_faced'] = df['extras_type'] != 'wide'
    
    # 3. Extras distribution
    # Wides and no-balls contribute to total team score
    # Leg-byes and byes contribute to total team score
    df['extra_runs'] = df['extras1_runs'] + df['extras_2_runs']
    df['total_delivery_runs'] = df['batter_runs'] + df['extra_runs']
    
    # 4. Bowler runs conceded (MCC Rule: byes and leg-byes are NOT charged to bowler)
    # Wides and no-balls (Overstep / other) ARE charged to bowler
    df['bowler_runs_conceded'] = np.where(
        df['extras_type'].isin(['byes', 'legbyes', 'Penalty']),
        0,
        df['batter_runs'] + df['extra_runs']
    )
    
    # 5. Bowler credited wickets vs non-bowler dismissals
    df['is_bowler_wicket'] = df['is_wicket'] & df['dismissal_type'].isin(BOWLER_CREDITED_DISMISSALS)
    df['is_team_wicket'] = df['is_wicket']
    
    # 6. Innings Phase
    # Overs 1-6: Powerplay, 7-15: Middle, 16-20: Death
    df['phase'] = np.where(
        df['overid'] <= 6, 'Powerplay',
        np.where(df['overid'] <= 15, 'Middle', 'Death')
    )
    
    # --- CUMULATIVE MATCH STATE (BEFORE DELIVERY) ---
    # Group by match and innings to compute state variables
    grouped = df.groupby(['match_id', 'innings'], group_keys=False)
    
    # Cumulative runs and wickets BEFORE this ball:
    # shift(1).fillna(0) ensures the state is at the START of delivery
    df['current_team_score'] = grouped['total_delivery_runs'].cumsum() - df['total_delivery_runs']
    df['current_wickets_lost'] = grouped['is_team_wicket'].cumsum() - df['is_team_wicket'].astype(int)
    df['wickets_in_hand'] = 10 - df['current_wickets_lost']
    
    # Legal balls bowled and remaining
    df['legal_balls_bowled'] = grouped['is_legal_ball'].cumsum() - df['is_legal_ball'].astype(int)
    
    # Total scheduled balls in innings (usually 120 unless rain revised)
    max_overs = np.where(
        (df['innings'] == 1) & df['first_inn_revised_overs'].notna(),
        df['first_inn_revised_overs'],
        np.where(
            (df['innings'] == 2) & df['second_inn_revised_overs'].notna(),
            df['second_inn_revised_overs'],
            20.0
        )
    )
    df['total_scheduled_balls'] = (max_overs * 6).astype(int)
    df['balls_remaining'] = np.maximum(0, df['total_scheduled_balls'] - df['legal_balls_bowled'])
    
    # Current Run Rate (CRR)
    # CRR = current_score / (legal_balls_bowled / 6)
    overs_bowled = df['legal_balls_bowled'] / 6.0
    df['current_run_rate'] = np.where(overs_bowled > 0, df['current_team_score'] / overs_bowled, 0.0)
    
    # --- 1ST INNINGS TOTAL & 2ND INNINGS TARGET ---
    # Calculate final 1st innings total for each match
    inn1_totals = df[df['innings'] == 1].groupby('match_id')['total_delivery_runs'].sum().reset_index()
    inn1_totals.rename(columns={'total_delivery_runs': 'inn1_final_runs'}, inplace=True)
    df = df.merge(inn1_totals, on='match_id', how='left')
    
    # Target calculation for 2nd innings
    # If revised_target is specified (DLS), use it; otherwise inn1_final_runs + 1
    df['target'] = np.where(
        df['innings'] == 2,
        np.where(df['revised_target'].notna(), df['revised_target'], df['inn1_final_runs'] + 1),
        np.nan
    )
    
    # Runs required in chase
    df['runs_required'] = np.where(
        df['innings'] == 2,
        np.maximum(0, df['target'] - df['current_team_score']),
        np.nan
    )
    
    # Required Run Rate (RRR)
    overs_remaining = df['balls_remaining'] / 6.0
    df['required_run_rate'] = np.where(
        (df['innings'] == 2) & (overs_remaining > 0),
        df['runs_required'] / overs_remaining,
        np.where((df['innings'] == 2) & (df['runs_required'] > 0), 36.0, 0.0)
    )
    
    return df

def run_cleaning_pipeline() -> pd.DataFrame:
    """Executes end-to-end cleaning and saves processed dataset."""
    print("Loading raw data...")
    dfs = load_raw_data()
    
    print("Preparing matches metadata...")
    matches_clean = prepare_matches_metadata(dfs['matches'], dfs['competitions'])
    
    print("Engineering ball-by-ball match state...")
    bbb_processed = clean_and_engineer_ball_by_ball(dfs['ball_by_ball'], matches_clean)
    
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / "ball_by_ball_processed.parquet"
    print(f"Saving processed analytical dataset to {output_path}...")
    bbb_processed.to_parquet(output_path, index=False)
    print(f"Successfully processed {len(bbb_processed):,} deliveries with complete match context!")
    return bbb_processed

if __name__ == "__main__":
    run_cleaning_pipeline()
