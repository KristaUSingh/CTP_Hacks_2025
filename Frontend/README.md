# CUNY PathFinder - Frontend
<div align="center"><img width="592" height="777" alt="Screenshot 2025-08-20 at 10 34 56 PM" src="https://github.com/user-attachments/assets/8c71eb7d-0956-40d1-8c27-2d7d39ab72f5"/></div>

This is the frontend for CUNY PathFinder. CUNY PathFinder's goal is to help CUNY students generate a personalized semester-by-semester course plan based on their major, graduation term, and completed courses.


# Features
- Interactive Streamlit UI
- Select campus, major, and graduation term
- Choose part-time or full-time credit loads
- Mark completed courses from your degree
- Generates a customized semester plan powered by the backend scheduler
- Displays results per term with credits, professor ratings, and workload
- Degree progress shown via a progress bar
- PDF Export directly from the UI — after you click Generate Plan, you can download a polished PDF of your schedule with one button


# Tech Stack 
- **Frontend:** Streamlit for rapid UI development
- **Backend:** FastAPI — provides the scheduling logic via REST API endpoints
- **Communication:** Frontend calls backend using requests → POST /plan
- **Data Handling:** Pandas to load course CSVs for UI elements
- **PDF Export:** Built into the Generate Plan workflow; the UI provides a Download PDF button after a plan is generated


# Project Structure 
```
Frontend/
│── .streamlit/             # Streamlit config (theme, settings)
│── CUNY PathFinder.png     # Logo (PNG)
│── CUNY PathFinder.svg     # Logo (SVG)
│── frontend.py             # Streamlit app entry point
│── README.md               # Documentation (this file)
```
