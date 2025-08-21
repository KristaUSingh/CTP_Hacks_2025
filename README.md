# CUNY PathFinder - CTP_Hacks_2025
<div align="center"><img width="900" height="900" alt="CUNY PathFinder" src="https://github.com/user-attachments/assets/a38a9f21-63a8-41bb-a62f-313dd328ba02"/></div>

Explains the work done by our team, **Beaver Intelligence Unit**, for CUNY Tech Prep's Hackathon 2025. We created a tool that helps CUNY students map out their academic journey in a clear, personalized, and structured way. This project was completed using Streamlit for the frontend, FastAPI for the backend, and Pandas/NetworkX for scheduling logic.


# What is CUNY PathFinder?
CUNY PathFinder is a web-based platform that helps CUNY students generate a semester-by-semester course plan based on:
- Their **campus and major**
- Their **intended graduation term**
- Their **completed courses**
- Their **credit load preference** (part-time or full-time)
- Their **maximum credits** they want to take **per semester**

Unlike static degree checklists, PathFinder dynamically schedules courses while respecting prerequisites, balancing credit loads, and highlighting progress toward graduation. Students can export their plan as a polished PDF to share with advisors or keep for their own use. It helps students plan better by factoring in professor ratings, course difficulty, and availability across semesters. CUNY PathFinder reduces planning stress, prevents mistakes, and ensures students have a clear, structured roadmap to graduation. 


# Why is CUNY PathFinder Useful?
Academic planning is difficult and confusing for many students:
- Course catalogs are hard to read and disconnected from prerequisites
- Advising sessions are short and often rushed
- Missed prerequisites delay graduation
- Balancing workload with life responsibilities is stressful

CUNY PathFinder bridges this gap by providing students with a personalized, structured, and easy-to-read roadmap — turning confusing course catalogs into a clear graduation plan.


# Features
**1. Interactive Planner**
- Select campus, major, and graduation term
- Mark completed courses
- Choose part-time or full-time credit loads

**2. Smart Scheduling**
- Greedy algorithm ensures prerequisites are taken in order
- Caps credits per term for balance
- Prefers higher-rated professors where possible

**3. Progress Tracking**
- Progress bar toward 120 credits
- Displays completion of required vs elective categories

**4. PDF Export**
- After generating a plan, students can download a polished PDF directly from the UI


# Technical Overview
- **Frontend:** Streamlit (Python) for rapid UI development
- **Backend:** FastAPI (Python) providing REST API endpoints
- **Scheduling Logic:** Pandas + NetworkX for prerequisite DAG + greedy term-filling algorithm
- **Data:** Seed CSV files for courses and prerequisites (courses.csv, prereqs.csv)
- **PDF Export:** Streamlit export button + styled HTML-to-PDF generation


# Datasets 
- **CS_COURSE_CCNY Dataset:** CSV file that contains all the CS courses, terms they are usually offered, professors, their ratings, and the difficulty 
- **MATH_COURSE_CCNY Dataset:** CSV file that contains all the Math courses, terms they are usually offered, professors, their ratings, and the difficulty 


# Conclusion
CUNY PathFinder is our proof-of-concept solution to make academic planning simpler, clearer, and stress-free for CUNY students. By combining prerequisite checks, workload balancing, and personalized planning into a single tool, CUNY PathFinder provides students with a roadmap to graduation that they can actually understand and utilize. While the current version of CUNY PathFinder supports CCNY Computer Science and Math majors, the framework is designed to grow. Future work will expand coverage to all CUNY campuses and majors, with live integration into course catalogs and class schedules. With these improvements, CUNY PathFinder has the potential to become a CUNY-wide platform that allows every student to navigate their academic journey with clarity and confidence. 
