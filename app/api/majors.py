from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

# This file defines an API endpoint to list all available majors from a CSV file.

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

@router.get("/")
def list_majors():
    path = DATA_DIR / "degree_requirements.csv"
    if not path.exists():
        raise HTTPException(status_code=500, detail="degree_requirements.csv not found")
    df = pd.read_csv(path)
    majors = sorted(df["major"].dropna().unique().tolist())
    return {"majors": majors}
