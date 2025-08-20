import pandas as pd
import networkx as nx
from pathlib import Path
import uuid

# This file defines the greedy scheduling algorithm for course planning.

def build_term_range(start_term: str, end_term: str):
    """Generate terms from start_term up to and including end_term."""
    def term_to_tuple(term):
        year, sem = int(term[:-1]), term[-1]
        return year, sem

    def next_term(year, sem):
        return (year + 1, "S") if sem == "F" else (year, "F")

    start_year, start_sem = term_to_tuple(start_term)
    end_year, end_sem = term_to_tuple(end_term)

    seq = []
    y, s = start_year, start_sem
    while True:
        seq.append(f"{y}{s}")
        if (y, s) == (end_year, end_sem):
            break
        y, s = next_term(y, s)
    return seq

def greedy_schedule(major: str,
                    upcoming_term: str,
                    grad_term: str,
                    completed_course_codes=None,
                    max_credits_per_term: int = 15,
                    data_dir="data"):
    
    """
    Simple scheduler:
    - Reads CSVs
    - Builds prereq graph
    - Topologically orders courses
    - Greedily fills terms until credit cap reached
    """

    if completed_course_codes is None:
        completed_course_codes = []

    # Load CSVs
    courses = pd.read_csv(f"{data_dir}/courses.csv")
    prereqs = pd.read_csv(f"{data_dir}/prereqs.csv")

    # Filter courses by department/major - IMPLEMENTED WRONG 
    # courses = courses[courses["dept"].str.upper() == major.upper()]

    # Build course lookup
    code_to_id = dict(zip(courses["code"], courses["id"]))
    id_to_course = courses.set_index("id").to_dict("index")

    # Track completed courses
    completed_ids = {code_to_id[c] for c in completed_course_codes if c in code_to_id}

    # Build DAG of prereqs (only for this major’s courses)
    G = nx.DiGraph()
    for cid in courses["id"]:
        G.add_node(cid)
    for _, row in prereqs.iterrows():
        if row["course_id"] in G and row["requires_course_id"] in G:
            G.add_edge(row["requires_course_id"], row["course_id"])

    # Topological order
    try:
        topo_order = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        raise Exception("Cycle detected in prereqs")
    
    term_sequence = build_term_range(upcoming_term, grad_term)
    # Simple term sequence fallback
    if not term_sequence:
        term_sequence = ["2025F", "2026S", "2026F", "2027S", "2027F", "2028S"]

    terms = []
    term_idx = 0
    planned = set()
    remaining = [cid for cid in topo_order if cid not in completed_ids]

    while remaining and term_idx < len(term_sequence):
        current_term = []
        current_credits = 0
        placed_this_term = []

        for cid in remaining:
            course = id_to_course[cid]
            credits = int(course["credits"])

            # prereqs must be satisfied
            prereq_ids = [p for p in G.predecessors(cid)]
            if not set(prereq_ids).issubset(completed_ids.union(planned)):
                continue

            if current_credits + credits <= max_credits_per_term:
                current_term.append({
                    "id": int(cid),
                    "code": str(course["code"]),
                    "title": str(course["title"]),
                    "credits": credits
                })
                current_credits += credits
                placed_this_term.append(cid)

        if current_term:
            terms.append({
                "term": term_sequence[term_idx],
                "courses": current_term,
                "total_credits": current_credits
            })
            planned.update(placed_this_term)
            completed_ids.update(placed_this_term)
            remaining = [c for c in remaining if c not in placed_this_term]
        else:
            # nothing could be placed — avoid infinite loop
            break

        term_idx += 1

    return {
        "plan_id": str(uuid.uuid4()),
        "terms": terms,
        "totals": {
            "credits_planned": sum(t["total_credits"] for t in terms),
            "courses_planned": len(planned)
        }
    }