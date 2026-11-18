"""
SupeRR Selector Analytics - Configuration & Constants
Rajasthan Royals IPL 2027 Auction Analytics
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = DATA_DIR / "outputs"
REPORTS_DIR = BASE_DIR / "reports"
SRC_DIR = BASE_DIR / "src"

# Cricket Domain Constants
BOWLER_CREDITED_DISMISSALS = {
    "Bowled",
    "Caught",
    "LBW",
    "Stump",
    "Hit Wicket"
}

NON_BOWLER_DISMISSALS = {
    "RunOut",
    "Retire Out",
    "Obstracting the field",
    "Obstructing the field"
}

ILLEGAL_BALL_EXTRAS = {
    "wide",
    "Overstep",
    "other"
}

# Thresholds for Eligibility (Fair Comparison)
MIN_PRESSURE_BALLS_FACED_BATTER = 60
MIN_PRESSURE_BALLS_BOWLED_BOWLER = 60
MIN_MATCHES_PLAYED = 10
MIN_PRESSURE_INNINGS = 5

# Format Weighting
IPL_WEIGHT = 1.00
T20I_WEIGHT = 0.95
