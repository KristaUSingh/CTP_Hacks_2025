import streamlit as st
import pandas as pd 
import requests
from yattag import Doc 
import pdfkit
import tempfile

# Website layout: titles, headers etc.
st.image("../Frontend/CUNY PathFinder.svg", width=300)
st.title("CUNY PathFinder!")

st.header("Please select your information below to generate your semesterly plan:")

# User input to generate plan
campus = st.selectbox("Select your CUNY Campus:", ["The City College of New York", "Baruch College", "York College", "Queens College", \
                                             "College of Staten Island", "Lehman College", "Brooklyn College", "Hunter College", \
                                             "John Jay College of Criminal Justice", "New York City College of Technology", \
                                             "Medger Evans College", "Borough of Manhattan Community College", "Kingsborough Community College", \
                                             "Queensborough Community College", "Bronx Community College", "Laguardia Community College"])

part_full_time = st.radio("Select if you are part-time or full-time:", ["Part-time", "Full-time"])

major = st.selectbox("Select your major:", ["Computer Science", "Mathematics"])

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
        df = pd.read_csv("/Users/kristasingh/Desktop/CUNY Tech Prep/Hackathon2025/CTP_Hacks_2025/CScourse.csv")
        options = df["degree_requirements_course_name"].unique().tolist()
        completed_courses = st.multiselect("Select the courses you already completed:", options=options)
    if major == "Mathematics":
        df = pd.read_csv("/Users/kristasingh/Desktop/CUNY Tech Prep/Hackathon2025/CTP_Hacks_2025/Mathcourse.csv")
        options = df["NAME"].unique().tolist()
        completed_courses = st.multiselect("Select the courses you already completed:", options=options)

# function to call endpoint

def generate_plan_endpoint(major, graduation, completed_courses, max_credits):
    api_url = "http://172.20.140.150:8501/"
    payload = {
        "major": major,
        "graduation_term": graduation,
        "completed_courses": completed_courses,
        "max_credits_per_terms": max_credits,
    }
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {e}")
        return None
    

# things inside the pdf 
def build_plan_html(data):
    doc, tag, text = Doc().tagtext()
    with tag("html"):
        with tag("head"):
            doc.stag("meta", charset="UTF-8")
            with tag("style"):
                text("""
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { text-align: center; color: #006D77; }
                h2 { margin-top: 30px; color: #333; }
                table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
                th { background-color: #83C5BE; color: #fff; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .summary { margin-top: 20px; font-weight: bold; }
                """)
        with tag("body"):
            with tag("h1"):
                text(f"{data['major']} 4-Year Plan ({data['grad_term']})")
            
            # Totals
            with tag("p", klass="summary"):
                text(f"Total Credits: {data['totals']['credits']} | Major Progress: {int(data['totals']['major_reqs_done']*100)}%")
            
            # Terms
            for term in data["terms"]:
                with tag("h2"):
                    text(term["term"])
                with tag("table"):
                    with tag("tr"):
                        for col in ["Code","Title","Credits","Professor","Rating","Workload"]:
                            with tag("th"): text(col)
                    for c in term["courses"]:
                        with tag("tr"):
                            with tag("td"): text(c["code"])
                            with tag("td"): text(c["title"])
                            with tag("td"): text(str(c["credits"]))
                            with tag("td"): text(c["prof"])
                            with tag("td"): text(f"{c['rating']:.1f}")
                            with tag("td"): text(f"{c['workload']:.1f}")
    return doc.getvalue()

# converts from HTML to PDF
def make_pdf_from_html(html):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdfkit.from_string(html, tmp.name)
        return tmp.name


# generate plan when button is clicked 
if st.button("Generate Plan"):
    data = generate_plan_endpoint(major, graduation, completed_courses, max_credits)
    if data:
        st.success("Success with generating plan!")
    
    html = build_plan_html(data)
    pdf_path = make_pdf_from_html(html)

    with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="plan.pdf", mime="application/pdf")
