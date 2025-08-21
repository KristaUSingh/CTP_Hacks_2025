from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import majors, plan


app = FastAPI(title="Course Planner API")

@app.get("/")
def root():
    return {"status": "Backend running on Vercel 🚀"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(majors.router, prefix="/majors", tags=["majors"])
app.include_router(plan.router, prefix="/generate-plan", tags=["plan"])

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
