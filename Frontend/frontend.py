import streamlit as st
import pandas as pd 
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
<<<<<<< Updated upstream
=======
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent / "data"
>>>>>>> Stashed changes

# Website layout: titles, headers etc.
st.image("../Frontend/CUNY PathFinder.svg", width=300)
st.title("Welcome to CUNY PathFinder!")

st.header("Please select your information below to generate your semesterly plan:")

# User input to generate plan
campus = st.selectbox("Select your CUNY Campus:", ["The City College of New York", "Baruch College", "York College", "Queens College", \
                                             "College of Staten Island", "Lehman College", "Brooklyn College", "Hunter College", \
                                             "John Jay College of Criminal Justice", "New York City College of Technology", \
                                             "Medger Evans College", "Borough of Manhattan Community College", "Kingsborough Community College", \
                                             "Queensborough Community College", "Bronx Community College", "Laguardia Community College"])

part_full_time = st.radio("Select if you are part-time or full-time:", ["Part-time", "Full-time"])

major = st.selectbox("Select your major:", ["Computer Science", "Mathematics"])

upcoming_term = st.selectbox("Select your upcoming term:", ["Fall 2025", "Spring 2026", "Fall 2026", "Spring 2027", \
                                                            "Fall 2027", "Spring 2028", "Fall 2028", "Spring 2029"])

graduation = st.selectbox("Select your graduation term:", ["Fall 2025", "Spring 2026", "Fall 2026", "Spring 2027", "Fall 2027", \
                                                           "Spring 2028", "Fall 2028", "Spring 2029"])

# Selection based on part-time vs. full-time for credits per term
if part_full_time == "Part-time": 
    max_credits = st.slider("Choose the max credits per term:", min_value=3, max_value=11)
else: 
    max_credits = st.slider("Choose the max credits per term:", min_value=12, max_value=21)

# Major classes selected per campus per major
if campus == "The City College of New York":
    if major == "Computer Science":
<<<<<<< Updated upstream
        df = pd.read_csv("/Users/kristasingh/Desktop/CUNY Tech Prep/Hackathon2025/CTP_Hacks_2025/Frontend/Frontend/courses.csv")
        options = df["code"].unique().tolist()
        completed_courses = st.multiselect("Select the courses you already completed:", options=options)
    if major == "Mathematics":
        df = pd.read_csv("/Users/kristasingh/Desktop/CUNY Tech Prep/Hackathon2025/CTP_Hacks_2025/Mathcourse.csv")
        options = df["NAME"].unique().tolist()
=======
        df = pd.read_csv(BASE_DIR / "computer science" / "courses.csv")
        options = df["code"].unique().tolist()
        completed_courses = st.multiselect("Select the courses you already completed:", options=options)
    if major == "Mathematics":
        df = pd.read_csv(BASE_DIR / "mathematics" / "courses.csv")
        options = df["code"].unique().tolist()
>>>>>>> Stashed changes
        completed_courses = st.multiselect("Select the courses you already completed:", options=options)

# function to call endpoint
def generate_plan_endpoint(major, upcoming_term, graduation, completed_courses, max_credits):
    api_url = "http://127.0.0.1:8000/generate-plan/"
    payload = {
        "major": major,
        "upcoming_term": upcoming_term,  
        "grad_term": graduation,
        "completed_courses": completed_courses,
        "max_credits_per_term": max_credits,
        "prefs": {}
    }
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {e}")
        return None


# things inside the pdf 
def make_pdf_from_data(data):
    # Build PDF filename dynamically
    pdf_name = f"{data['major'].replace(' ', '_')}_Semesterly_Plan.pdf"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        # Create doc with title metadata
        doc = SimpleDocTemplate(
            tmp.name,
            pagesize=letter,
            title=f"{data['major']} Semesterly Plan"
        )
        elements = []
        styles = getSampleStyleSheet()

        # Title
        elements.append(Paragraph(
            f"{data['major']} Semesterly Plan (Upcoming: {data['upcoming_term']} → Graduation: {data['grad_term']})",
            styles["Heading1"]
        ))

        elements.append(Spacer(1, 12))

        # Totals
        totals = data["totals"]
        totals_text = f"""
        <b>Total Credits Planned:</b> {totals.get('credits_planned', 0)}<br/>
        <b>Courses Planned:</b> {totals.get('courses_planned', 0)}
        """
        if "courses_unscheduled" in totals:
            totals_text += f"<br/><b>Courses Unscheduled:</b> {totals['courses_unscheduled']}"
        elements.append(Paragraph(totals_text, styles["Normal"]))
        elements.append(Spacer(1, 12))

        # Terms
        for term in data["terms"]:
            elements.append(Paragraph(term["term"], styles["Heading2"]))

            table_data = [["Code", "Title", "Credits", "Difficulty"]]
            for c in term["courses"]:
                table_data.append([c["code"], c["title"], str(c["credits"]), f"{c['difficulty']:.1f}"])

            table = Table(table_data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#83C5BE")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 12))

        # Unscheduled Courses
        if "unscheduled_courses" in data:
            elements.append(Paragraph("Unscheduled Courses", styles["Heading2"]))
            table_data = [["Code", "Title", "Credits", "Difficulty"]]
            for c in data["unscheduled_courses"]:
                table_data.append([c["code"], c["title"], str(c["credits"]), f"{c['difficulty']:.1f}"])

            table = Table(table_data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E29578")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]))
            elements.append(table)

        doc.build(elements)

        return tmp.name, pdf_name


# generate plan when button is clicked 
if st.button("Generate Plan"):
    data = generate_plan_endpoint(major, upcoming_term, graduation, completed_courses, max_credits)
    if data:
        st.success("Success with generating plan!")
        pdf_path, pdf_name = make_pdf_from_data(data)

        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name=pdf_name, mime="application/pdf")


