import pandas as pd
import networkx as nx
from pathlib import Path
import uuid

# This file defines the greedy scheduling algorithm for course planning.

def greedy_schedule(major, completed_course_codes, max_credits_per_term=15, term_sequence=None, data_dir: Path=None):
    """
    Simple scheduler:
    - Reads CSVs
    - Builds prereq graph
    - Topologically orders courses
    - Greedily fills terms until credit cap reached
    """

    if data_dir is None:
        data_dir = Path(__file__).resolve().parents[1] / "data"

    # --- Load data ---
    courses = pd.read_csv(data_dir / "courses.csv")
    prereqs = pd.read_csv(data_dir / "prereqs.csv")
    degree_reqs = pd.read_csv(data_dir / "degree_requirements.csv")

    # --- Filter required courses for this major ---
    req_ids = degree_reqs[(degree_reqs["major"] == major) & (degree_reqs["required"] == True)]["course_id"].tolist()
    needed = courses[courses["id"].isin(req_ids)].copy()

    # Map course_id -> info
    course_map = {row["id"]: row for _, row in needed.iterrows()}
    code_to_id = {row["code"]: row["id"] for _, row in courses.iterrows()}

    # --- Build prereq graph ---
    G = nx.DiGraph()
    for cid in req_ids:
        G.add_node(cid)
    for _, row in prereqs.iterrows():
        if row["course_id"] in req_ids and row["requires_course_id"] in req_ids:
            G.add_edge(row["requires_course_id"], row["course_id"])

    # --- Topological sort ---
    try:
        topo_order = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        raise ValueError("Cycle detected in prereqs!")

    # --- Simulate scheduling ---
    completed_ids = {code_to_id[c] for c in completed_course_codes if c in code_to_id}
    plan_terms = []
    term_list = term_sequence or ["2025F", "2026S", "2026F", "2027S"]

    for term in term_list:
        term_courses = []
        total_credits = 0

        for cid in topo_order:
            if cid in completed_ids:
                continue
            # prereqs check
            prereq_ids = prereqs[prereqs["course_id"] == cid]["requires_course_id"].tolist()
            if not set(prereq_ids).issubset(completed_ids):
                continue
            # credit cap check
            credits = int(course_map[cid]["credits"])
            if total_credits + credits > max_credits_per_term:
                continue
            # assign this course
            course_info = course_map[cid]
            term_courses.append({
                "id": int(course_info["id"]),
                "code": course_info["code"],
                "title": course_info["title"],
                "credits": credits
            })
            total_credits += credits
            completed_ids.add(cid)

        if term_courses:
            plan_terms.append({
                "term": term,
                "courses": term_courses,
                "total_credits": total_credits
            })

        # stop if all required courses are done
        if set(req_ids).issubset(completed_ids):
            break

    return {
        "plan_id": str(uuid.uuid4()),
        "terms": plan_terms,
        "totals": {
            "credits_planned": sum(t["total_credits"] for t in plan_terms),
            "courses_planned": sum(len(t["courses"]) for t in plan_terms)
        }
    }