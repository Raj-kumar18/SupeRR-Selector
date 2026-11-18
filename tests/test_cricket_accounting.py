"""
test_cricket_accounting.py - Automated tests validating core MCC cricket logic and state calculations.
"""
import unittest
import pandas as pd
from config import PROCESSED_DATA_DIR, OUTPUTS_DIR

class TestCricketAccounting(unittest.TestCase):
    def test_data_integrity(self):
        df = pd.read_parquet(PROCESSED_DATA_DIR / 'ball_by_ball_processed.parquet')
        self.assertEqual(len(df), 200999)
        self.assertEqual(df['is_legal_ball'].sum(), 192445)
        
    def test_wicket_accounting(self):
        df = pd.read_parquet(PROCESSED_DATA_DIR / 'ball_by_ball_processed.parquet')
        self.assertEqual(df['is_wicket'].sum(), 10881)
        self.assertEqual(df['is_bowler_wicket'].sum(), 10272)
        
    def test_no_duplicate_rankings(self):
        top_bat = pd.read_csv(OUTPUTS_DIR / 'top_10_batters_under_pressure.csv')
        top_bowl = pd.read_csv(OUTPUTS_DIR / 'top_10_bowlers_under_pressure.csv')
        self.assertEqual(len(top_bat), 10)
        self.assertEqual(len(top_bowl), 10)
        self.assertFalse(top_bat['player_id'].duplicated().any())
        self.assertFalse(top_bowl['player_id'].duplicated().any())

if __name__ == '__main__':
    unittest.main()
