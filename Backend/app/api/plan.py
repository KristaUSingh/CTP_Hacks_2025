# app/api/plan.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
from app.scheduler import greedy_schedule

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

class PlanRequest(BaseModel):
    major: str
    upcoming_term: str   
    grad_term: str       
    completed_courses: List[str] = []
    max_credits_per_term: int = 15
    prefs: Optional[dict] = None

@router.post("/")
def generate_plan(req: PlanRequest):
    if not (DATA_DIR / "courses.csv").exists():
        raise HTTPException(status_code=500, detail="Data files missing in data/")

    try:
        result = greedy_schedule(
            major=req.major,
            upcoming_term=req.upcoming_term,
            grad_term=req.grad_term,
            completed_course_codes=req.completed_courses,
            max_credits_per_term=req.max_credits_per_term,
            data_dir=DATA_DIR
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))