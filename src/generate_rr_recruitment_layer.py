"""
generate_rr_recruitment_layer.py - Builds the dedicated Layer 2: Rajasthan Royals Recruitment Intelligence.
Categorizes all eligible players into:
1. Historical Rajasthan Royals Players
2. Players from Other IPL Franchises
3. Players with International-Only Appearances
4. Potential Auction Recruitment Candidates (Target shortlist based on pressure reliability, squad needs, and verified availability)

Enriches every player with:
- Historical teams played for
- Actual playing appearances (matches from playing_eleven.csv)
- Batting position (median batting order & role category)
- Batting / bowling role
- Pressure reliability score
- IPL pressure performance (Balls, SR / Economy)
- T20I pressure performance (Balls, SR / Economy)
"""
import pandas as pd
import numpy as np
from pathlib import Path
from config import PROCESSED_DATA_DIR, OUTPUTS_DIR

def build_rr_recruitment_dataset():
    print("Loading datasets for Layer 2 recruitment intelligence...")
    base_dir = Path(__file__).resolve().parent.parent
    
    # Raw tables
    p11 = pd.read_csv(base_dir / "data/raw/playing_eleven.csv")
    mapping = pd.read_csv(base_dir / "data/raw/competition_team_player_mapping.csv")
    teams = pd.read_csv(base_dir / "data/raw/teams.csv")
    comps = pd.read_csv(base_dir / "data/raw/competitions.csv")
    matches = pd.read_csv(base_dir / "data/raw/matches.csv")
    
    # Processed ball-by-ball
    df = pd.read_parquet(PROCESSED_DATA_DIR / "ball_by_ball_pressure_classified.parquet")
    
    # Eligible overall ranked players (Layer 1)
    all_bat = pd.read_csv(OUTPUTS_DIR / "all_eligible_batters.csv")
    all_bowl = pd.read_csv(OUTPUTS_DIR / "all_eligible_bowlers.csv")
    
    # 1. Identify IPL competitions and teams
    ipl_comps = set(comps[comps['comp_name'].str.contains('IPL', case=False, na=False)]['comp_id'])
    ipl_teams = set(teams[teams['comp_id'].isin(ipl_comps)]['team_id'])
    
    # Team dictionary
    team_dict = teams[['team_id', 'team_name']].drop_duplicates().set_index('team_id')['team_name'].to_dict()
    
    # 2. Player appearances and teams from playing_eleven
    p11_played = p11[p11['is_played'].astype(str).str.lower().isin(['true', '1'])].copy()
    
    # Total matches played per player in playing_eleven
    player_matches = p11_played.groupby('player_id')['match_id'].nunique().to_dict()
    
    # IPL matches played per player
    ipl_p11 = p11_played[p11_played['team_id'].isin(ipl_teams)]
    player_ipl_matches = ipl_p11.groupby('player_id')['match_id'].nunique().to_dict()
    
    # All teams played for in playing_eleven or mapping
    p_teams_map = mapping.groupby('player_id')['team_name'].unique().to_dict()
    p_teams_p11 = p11_played.groupby('player_id')['team_id'].unique().to_dict()
    
    def get_all_teams(p_id):
        t_set = set(p_teams_map.get(p_id, []))
        for tid in p_teams_p11.get(p_id, []):
            if tid in team_dict:
                t_set.add(team_dict[tid])
        return sorted(list(t_set))
        
    def get_ipl_teams_list(p_id):
        all_t = get_all_teams(p_id)
        # IPL teams: Chennai Super Kings, Delhi Capitals, Gujarat Titans, Kolkata Knight Riders, 
        # Lucknow Super Giants, Mumbai Indians, Punjab Kings, Rajasthan Royals, Royal Challengers Bengaluru, Sunrisers Hyderabad
        ipl_franchise_names = {
            'Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans', 'Kolkata Knight Riders',
            'Lucknow Super Giants', 'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals',
            'Royal Challengers Bengaluru', 'Sunrisers Hyderabad'
        }
        return [t for t in all_t if t in ipl_franchise_names]

    # Batting order / position from playing_eleven
    bat_order = p11_played[p11_played['batting_order'].notna()].copy()
    bat_order['batting_order'] = pd.to_numeric(bat_order['batting_order'], errors='coerce')
    player_median_pos = bat_order.groupby('player_id')['batting_order'].median().to_dict()
    
    def get_position_role(pos):
        if pd.isna(pos):
            return "Specialist Middle Order"
        if pos <= 2.5:
            return "Top Order (Opener / No. 1-2)"
        elif pos <= 4.0:
            return "Top-Middle Order (No. 3-4)"
        elif pos <= 7.0:
            return "Middle-Overs Finisher (No. 5-7)"
        else:
            return "Lower Order / Tail (No. 8-11)"

    # 3. Format performance breakdown under pressure
    # Batting format split under pressure
    p_bat_df = df[df['is_high_pressure']]
    bat_ipl_p = p_bat_df[p_bat_df['comp_type'] == 'IPL'].groupby('striker_id').agg(
        ipl_p_balls=('is_ball_faced', 'sum'),
        ipl_p_runs=('batter_runs', 'sum'),
        ipl_p_dismissals=('is_wicket', lambda s: (s & (df.loc[s.index, 'dismissed_player_id'] == df.loc[s.index, 'striker_id'])).sum())
    ).reset_index()
    bat_ipl_p['ipl_p_sr'] = np.where(bat_ipl_p['ipl_p_balls'] > 0, (bat_ipl_p['ipl_p_runs'] / bat_ipl_p['ipl_p_balls'] * 100).round(1), 0.0)
    bat_ipl_p['ipl_p_avg'] = np.where(bat_ipl_p['ipl_p_dismissals'] > 0, (bat_ipl_p['ipl_p_runs'] / bat_ipl_p['ipl_p_dismissals']).round(1), bat_ipl_p['ipl_p_runs'].astype(float))
    bat_ipl_p = bat_ipl_p.rename(columns={'striker_id': 'player_id'})

    bat_t20i_p = p_bat_df[p_bat_df['comp_type'] == 'T20I'].groupby('striker_id').agg(
        t20i_p_balls=('is_ball_faced', 'sum'),
        t20i_p_runs=('batter_runs', 'sum'),
        t20i_p_dismissals=('is_wicket', lambda s: (s & (df.loc[s.index, 'dismissed_player_id'] == df.loc[s.index, 'striker_id'])).sum())
    ).reset_index()
    bat_t20i_p['t20i_p_sr'] = np.where(bat_t20i_p['t20i_p_balls'] > 0, (bat_t20i_p['t20i_p_runs'] / bat_t20i_p['t20i_p_balls'] * 100).round(1), 0.0)
    bat_t20i_p['t20i_p_avg'] = np.where(bat_t20i_p['t20i_p_dismissals'] > 0, (bat_t20i_p['t20i_p_runs'] / bat_t20i_p['t20i_p_dismissals']).round(1), bat_t20i_p['t20i_p_runs'].astype(float))
    bat_t20i_p = bat_t20i_p.rename(columns={'striker_id': 'player_id'})

    # Bowling format split under pressure
    bowl_ipl_p = p_bat_df[p_bat_df['comp_type'] == 'IPL'].groupby('bowler_id').agg(
        ipl_p_balls=('is_legal_ball', 'sum'),
        ipl_p_runs=('bowler_runs_conceded', 'sum'),
        ipl_p_wickets=('is_bowler_wicket', 'sum')
    ).reset_index()
    bowl_ipl_p['ipl_p_econ'] = np.where(bowl_ipl_p['ipl_p_balls'] > 0, (bowl_ipl_p['ipl_p_runs'] / (bowl_ipl_p['ipl_p_balls'] / 6.0)).round(2), 0.0)
    bowl_ipl_p = bowl_ipl_p.rename(columns={'bowler_id': 'player_id'})

    bowl_t20i_p = p_bat_df[p_bat_df['comp_type'] == 'T20I'].groupby('bowler_id').agg(
        t20i_p_balls=('is_legal_ball', 'sum'),
        t20i_p_runs=('bowler_runs_conceded', 'sum'),
        t20i_p_wickets=('is_bowler_wicket', 'sum')
    ).reset_index()
    bowl_t20i_p['t20i_p_econ'] = np.where(bowl_t20i_p['t20i_p_balls'] > 0, (bowl_t20i_p['t20i_p_runs'] / (bowl_t20i_p['t20i_p_balls'] / 6.0)).round(2), 0.0)
    bowl_t20i_p = bowl_t20i_p.rename(columns={'bowler_id': 'player_id'})

    # 4. Categorization Logic
    rr_team_id = 3
    rr_player_ids = set(p11_played[p11_played['team_id'] == rr_team_id]['player_id']) | set(mapping[mapping['team_id'] == rr_team_id]['player_id'])
    all_ipl_player_ids = set(p11_played[p11_played['team_id'].isin(ipl_teams)]['player_id']) | set(mapping[mapping['team_id'].isin(ipl_teams)]['player_id'])

    def assign_category(p_id):
        if p_id in rr_player_ids:
            return "Historical Rajasthan Royals"
        elif p_id in all_ipl_player_ids:
            return "Other IPL Franchise"
        else:
            return "International-Only"

    # --- PROCESS BATTERS ---
    rec_bat = all_bat.copy()
    rec_bat = rec_bat.merge(bat_ipl_p[['player_id', 'ipl_p_balls', 'ipl_p_sr', 'ipl_p_avg']], on='player_id', how='left')
    rec_bat = rec_bat.merge(bat_t20i_p[['player_id', 't20i_p_balls', 't20i_p_sr', 't20i_p_avg']], on='player_id', how='left')
    rec_bat['ipl_p_balls'] = rec_bat['ipl_p_balls'].fillna(0).astype(int)
    rec_bat['t20i_p_balls'] = rec_bat['t20i_p_balls'].fillna(0).astype(int)
    rec_bat['ipl_p_sr'] = rec_bat['ipl_p_sr'].fillna(0.0)
    rec_bat['t20i_p_sr'] = rec_bat['t20i_p_sr'].fillna(0.0)
    
    rec_bat['category'] = rec_bat['player_id'].apply(assign_category)
    rec_bat['historical_teams'] = rec_bat['player_id'].apply(lambda pid: ", ".join(get_all_teams(pid)[:3]))
    rec_bat['ipl_franchises'] = rec_bat['player_id'].apply(lambda pid: ", ".join(get_ipl_teams_list(pid)))
    rec_bat['matches_played_p11'] = rec_bat['player_id'].apply(lambda pid: player_matches.get(pid, int(rec_bat.loc[rec_bat['player_id'] == pid, 'norm_matches'].values[0])))
    rec_bat['median_bat_pos'] = rec_bat['player_id'].apply(lambda pid: player_median_pos.get(pid, np.nan))
    rec_bat['batting_role'] = rec_bat['median_bat_pos'].apply(get_position_role)

    # --- PROCESS BOWLERS ---
    rec_bowl = all_bowl.copy()
    rec_bowl = rec_bowl.merge(bowl_ipl_p[['player_id', 'ipl_p_balls', 'ipl_p_econ', 'ipl_p_wickets']], on='player_id', how='left')
    rec_bowl = rec_bowl.merge(bowl_t20i_p[['player_id', 't20i_p_balls', 't20i_p_econ', 't20i_p_wickets']], on='player_id', how='left')
    rec_bowl['ipl_p_balls'] = rec_bowl['ipl_p_balls'].fillna(0).astype(int)
    rec_bowl['t20i_p_balls'] = rec_bowl['t20i_p_balls'].fillna(0).astype(int)
    rec_bowl['ipl_p_econ'] = rec_bowl['ipl_p_econ'].fillna(0.0)
    rec_bowl['t20i_p_econ'] = rec_bowl['t20i_p_econ'].fillna(0.0)
    
    rec_bowl['category'] = rec_bowl['player_id'].apply(assign_category)
    rec_bowl['historical_teams'] = rec_bowl['player_id'].apply(lambda pid: ", ".join(get_all_teams(pid)[:3]))
    rec_bowl['ipl_franchises'] = rec_bowl['player_id'].apply(lambda pid: ", ".join(get_ipl_teams_list(pid)))
    rec_bowl['matches_played_p11'] = rec_bowl['player_id'].apply(lambda pid: player_matches.get(pid, int(rec_bowl.loc[rec_bowl['player_id'] == pid, 'norm_matches'].values[0])))
    
    # Save enriched datasets
    rec_bat.to_parquet(OUTPUTS_DIR / "rr_recruitment_batters.parquet", index=False)
    rec_bowl.to_parquet(OUTPUTS_DIR / "rr_recruitment_bowlers.parquet", index=False)
    rec_bat.to_csv(OUTPUTS_DIR / "rr_recruitment_batters.csv", index=False)
    rec_bowl.to_csv(OUTPUTS_DIR / "rr_recruitment_bowlers.csv", index=False)
    
    print("Layer 2 RR Recruitment datasets successfully created!")
    print(f"Batters by Category:\n{rec_bat['category'].value_counts()}")
    print(f"Bowlers by Category:\n{rec_bowl['category'].value_counts()}")

if __name__ == "__main__":
    build_rr_recruitment_dataset()
