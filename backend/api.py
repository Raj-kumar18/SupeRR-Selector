import json
import os
import csv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

app = FastAPI(title="SupeRR Selector – Analytics API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _path(*parts):
    return os.path.join(BASE, *parts)

def _csv(rel_path: str) -> List[Dict]:
    p = _path(rel_path)
    if not os.path.exists(p):
        raise FileNotFoundError(f"File not found: {p}")
    with open(p, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def _parquet(rel_path: str) -> List[Dict]:
    import pandas as pd
    p = _path(rel_path)
    if not os.path.exists(p):
        raise FileNotFoundError(f"File not found: {p}")
    df = pd.read_parquet(p)
    # Convert NaN → None for JSON serialisability
    return json.loads(df.to_json(orient='records'))

# ---------------------------------------------------------------------------
# 1. Health check
# ---------------------------------------------------------------------------
@app.get('/health')
def health():
    return {'status': 'ok', 'message': 'SupeRR Selector API is running'}

# ---------------------------------------------------------------------------
# 2. KPIs
# ---------------------------------------------------------------------------
@app.get('/api/kpis')
def kpis():
    summary_path = _path('data', 'outputs', 'deliveries_summary.json')
    if os.path.exists(summary_path):
        with open(summary_path) as f:
            return json.load(f)

    # Build KPIs from actual processed data if summary file is missing
    try:
        import pandas as pd
        bbb_raw = pd.read_csv(_path('data', 'raw', 'ball_by_ball.csv'))
        pressure_df = pd.read_parquet(_path('data', 'processed', 'ball_by_ball_pressure_classified.parquet'))
        batters_rows = _csv('data/outputs/all_eligible_batters.csv')
        bowlers_rows = _csv('data/outputs/all_eligible_bowlers.csv')

        total = len(bbb_raw)
        legal = int((~bbb_raw['extras_type'].isin(['wide', 'Overstep', 'other'])).sum())
        matches = int(pressure_df['match_id'].nunique())
        pressure = int(pressure_df['is_high_pressure'].sum())
        qual_bat = len(batters_rows)
        qual_bow = len(bowlers_rows)

        result = {
            'total_deliveries': total,
            'legal_deliveries': legal,
            'matches_analyzed': matches,
            'pressure_deliveries': pressure,
            'qualified_batters': qual_bat,
            'qualified_bowlers': qual_bow,
        }
        os.makedirs(os.path.dirname(summary_path), exist_ok=True)
        with open(summary_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result
    except Exception as e:
        return {
            'total_deliveries': 0,
            'legal_deliveries': 0,
            'matches_analyzed': 0,
            'pressure_deliveries': 0,
            'qualified_batters': 0,
            'qualified_bowlers': 0,
            'error': str(e)
        }

# ---------------------------------------------------------------------------
# 3. Overall Layer 1 rankings
# ---------------------------------------------------------------------------
@app.get('/api/overall/batters')
def overall_batters():
    try:
        rows = _csv('data/outputs/top_10_batters_under_pressure.csv')
        return rows
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get('/api/overall/bowlers')
def overall_bowlers():
    try:
        rows = _csv('data/outputs/top_10_bowlers_under_pressure.csv')
        return rows
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------------------------------------------------------------------------
# 4. All eligible players (for comparison dropdowns etc.)
# ---------------------------------------------------------------------------
@app.get('/api/eligible/batters')
def eligible_batters():
    try:
        return _csv('data/outputs/all_eligible_batters.csv')
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get('/api/eligible/bowlers')
def eligible_bowlers():
    try:
        return _csv('data/outputs/all_eligible_bowlers.csv')
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------------------------------------------------------------------------
# 5. Layer 2 – RR Recruitment
# ---------------------------------------------------------------------------
@app.get('/api/recruitment')
def recruitment():
    result: Dict[str, Any] = {}

    # Try parquet first, fall back to CSV
    for key, par, csv_rel in [
        ('batters', 'data/outputs/rr_recruitment_batters.parquet', 'data/outputs/rr_recruitment_batters.csv'),
        ('bowlers', 'data/outputs/rr_recruitment_bowlers.parquet', 'data/outputs/rr_recruitment_bowlers.csv'),
    ]:
        try:
            result[key] = _parquet(par)
        except Exception:
            try:
                result[key] = _csv(csv_rel)
            except Exception as e:
                result[key] = []
                result[f'{key}_error'] = str(e)

    return result

# ---------------------------------------------------------------------------
# 6. Format splits
# ---------------------------------------------------------------------------
@app.get('/api/format/batters')
def format_batters():
    try:
        return _parquet('data/outputs/top_batters_format_split.parquet')
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get('/api/format/bowlers')
def format_bowlers():
    try:
        return _parquet('data/outputs/top_bowlers_format_split.parquet')
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
