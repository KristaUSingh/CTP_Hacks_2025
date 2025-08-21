# CUNY PathFinder - Backend
<div align="center"><img width="1920" height="1080" alt="CTP Hacks Presentation" src="https://github.com/user-attachments/assets/7c872add-b904-468f-9933-064d8f63f8ff"/></div>

The CUNY PathFinder backend, built by the Beavers Intelligence Unit for the CTP Hacks Hackathon 2025, is powered by FastAPI and designed to generate semester-by-semester course plans. It processes catalog data from CSV files, validates prerequisite requirements, and constructs term schedules using a greedy algorithm that balances workload and enforces credit limits.


# Features
- **Majors Discovery:** reads unique majors from courses.csv (safe fallback to ```["CS","MATH"]```).
- **Greedy Scheduler:** builds a prerequisite DAG, topologically sorts, and packs courses per term.
- **Prereq Validation:** sanity checks that prereq IDs exist in the catalog.
- **Workload Balancing:** uses a difficulty budget per term; lower cap in summer.
- **CSV-Driven Catalog:** swap data by editing files in data/ (no DB required).
- **OpenAPI Docs & CORS:** auto docs at /docs, dev-friendly CORS


# Project Structure
```
app/
 |-- api/
 │  ├─ majors.py           # GET /majors
│  └─ plan.py              # POST /plan
├─ loader.py               # CSV loading + prereq validation
├─ scheduler.py            # build_term_range + greedy_schedule
└─ main.py                 # FastAPI app, routers, CORS, /health
data/
 |-- cs/
  ├─ courses.csv
  ├─ prereqs.csv
  ├─ professors.csv
 |-- math/
  ├─ courses.csv
  ├─ prereqs.csv
  ├─ professors.csv
```


# Tech Stack
- **FastAPI:** API framework
- **Uvicorn:** ASGI server
- **Pandas:** CSV loading & joins
- **NetworkX:** prerequisite DAG & topological sort
- **Pydantic:** request validation
- **Python 3.10+:** version of Python used


# API Endpoints: 
### Core
- **GET /health**
 - **Purpose:** Liveness check for the service.
 - **Request:** No params.
 - **Response:** "ok" status indicator (HTTP 200).


- **GET /majors/**
 - **Purpose:** List available majors discovered from courses.csv.
 - **Request:** No params.
 - **Behavior:** Reads major or majors column; trims/uniques; falls back to ```["CS","MATH"]``` if missing.
 - **Responses:** 200: Array of majors, 500: Malformed/unreadable CSV (only if read fails).

- **POST /plan/**
  - **Purpose:** Generate a semester-by-semester plan between two terms (inclusive).

### Request Body Fields:
- Major: ```str — target major.```
- Upcoming_term: ```str — format Fall YYYY, Spring YYYY, or Summer YYYY``` 
- Grad_term: str — ```same format as above.```
- Completed_courses: ```List[str] = [] — course codes already taken.```
- Max_credits_per_term: ```int = 15 — cap for Fall/Spring; Summer is capped at 9 internally.```
- prefs: Optional[dict] = ```None  — reserved for future scheduling preferences.```

### Behavior:
- Loads CSVs; validates that prereq IDs exist.
- Builds a prerequisite DAG and topologically orders courses.
- Greedily packs courses into each term under credit and difficulty budgets.

### Responses:
 - **200:** Successful plan (may be full or partial with an “unscheduled courses” list).
 - **422:** Invalid input (e.g., bad term format) or prereq validation failure.
 - **409:** Prerequisite cycle detected (non-DAG).
 - **500:** Missing/invalid data files or unexpected error.
