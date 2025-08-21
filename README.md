# CUNY PathFinder - Datasets
This folder contains the course dataset used by **CUNY PathFinder**. The dataset provides detailed information about the courses required to fulfill degree requirements and serves as the foundation for building personalized, semester-by-semester degree plans.

The dataset is structured in CSV format for easy integration with Pandas, SQL, or other data processing tools. It is comprised of two CSV files, each dedicated to a major: Computer Science and Mathematics for the campus **The City College of New York (CCNY)**.


# Project Structure
```
data/
│── CS_COURSES.csv          # CSV file for Computer Science major Courses
│── Mathcourses.csv         # CSV file for Math major courses 
│── README.md               # Documentation (this file)
```

# Dataset Overview
Each row in the dataset represents a course and includes metadata such as credits, prerequisites, ratings, difficulty, and scheduling terms. The backend scheduler uses this dataset to generate valid course pathways, and the frontend uses it to display course details to students.


# Columns
- **ID** → Unique identifier for each course
- **COURSES** → Course code (e.g., MATH 20100, CSc 21200)
- **NAME** → Full course title
- **CREDITS** → Number of credit hours
- **DEPT** → Department offering the course (e.g., MATH, CS, SCIENCE)
- **TERMS** → Terms when the course is offered (Fall, Spring, Summer)
- **CATEGORY** → Classification (CORE, ELECTIVE, or options)
- **PROFESSOR** → Instructor name (if available)
- **RATING** → Average professor/course rating (1–5 scale)
- **DIFFICULTY** → Reported course difficulty (1–5 scale, higher = difficulty)
- **PREREQ** → Prerequisite courses required before enrollment
