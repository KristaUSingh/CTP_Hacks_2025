from fastapi import APIRouter
from pathlib import Path
import pandas as pd

# This file defines an endpoint to list available majors
# try to read major(s) from courses.csv; if not present or file missing, return ["CS","MATH"]

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
FALLBACK = ["CS", "MATH"]

@router.get("/")
def list_majors():
    p = DATA_DIR / "courses.csv"
    if not p.exists():
        return {"majors": FALLBACK}
    df = pd.read_csv(p)
    cols = {c.strip().lower(): c for c in df.columns}
    col = cols.get("major") or cols.get("majors")
    return {"majors": sorted(df[col].dropna().astype(str).str.strip().unique().tolist())} if col else {"majors": FALLBACK}
