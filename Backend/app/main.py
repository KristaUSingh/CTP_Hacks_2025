from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import majors, plan  # <- import directly

app = FastAPI(title="Course Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(majors.router, prefix="/majors", tags=["majors"])
app.include_router(plan.router, prefix="/plan", tags=["plan"])

@app.get("/health")
def health():
    return {"status": "ok"}