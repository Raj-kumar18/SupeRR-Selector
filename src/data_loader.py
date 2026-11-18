"""
data_loader.py - Ingests and validates raw CSV files for SupeRR Selector Analytics.
"""
import pandas as pd
from pathlib import Path
from config import RAW_DATA_DIR

def load_raw_data(data_dir: Path = RAW_DATA_DIR) -> dict[str, pd.DataFrame]:
    """
    Loads all 6 raw CSV files into pandas DataFrames.
    Ensures safe reading without modifying original raw files.
    """
    files = {
        "competitions": "competitions.csv",
        "teams": "teams.csv",
        "matches": "matches.csv",
        "playing_eleven": "playing_eleven.csv",
        "mapping": "competition_team_player_mapping.csv",
        "ball_by_ball": "ball_by_ball.csv"
    }
    
    dfs = {}
    for name, fname in files.items():
        file_path = data_dir / fname
        if not file_path.exists():
            raise FileNotFoundError(f"Missing required raw file: {file_path}")
        dfs[name] = pd.read_csv(file_path, low_memory=False)
        
    return dfs

if __name__ == "__main__":
    dfs = load_raw_data()
    for k, v in dfs.items():
        print(f"Loaded {k:15s}: {len(v):>7,} rows")
