import pandas as pd
import networkx as nx
from pathlib import Path
import uuid

# This file defines the greedy scheduling algorithm for course planning.

def build_term_range(start_term: str, end_term: str):
    """
    Generate terms from start_term up to and including end_term.
    Example:
    build_term_range("Fall 2025", "Spring 2026")
      -> ["Fall 2025", "Spring 2026"]
    """
    seasons = ["Spring", "Summer", "Fall"]

    def term_to_tuple(term):
        season, year = term.split()
        year = int(year)
        return year, season

    def next_term(year, season):
        idx = seasons.index(season)
        if idx == len(seasons) - 1:  # Fall → next Spring
            return year + 1, seasons[0]
        else:
            return year, seasons[idx + 1]

    start_year, start_season = term_to_tuple(start_term)
    end_year, end_season = term_to_tuple(end_term)

    seq = []
    y, s = start_year, start_season
    while True:
        seq.append(f"{s} {y}")
        if (y, s) == (end_year, end_season):
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
    Greedy course scheduler.

    - Loads course, professor, and prereq data from CSV files.
    - Merges professor information (name, rating, difficulty) into courses.
    - Builds a prerequisite graph of all courses for the major.
    - Performs a topological sort to get a valid course order.
    - Iterates through terms (Fall, Spring, Summer) between upcoming_term and grad_term.
    - For each term:
        * Caps total credits (default 15, Summer capped at 8).
        * Greedily selects courses in topo order if prerequisites are satisfied.
        * Balances workload by considering professor difficulty ratings
          (aims to keep total difficulty near average per term).
    - Returns a plan with terms, courses, total credits, and difficulty.
    - If not all courses fit, returns a partial plan plus a list of unscheduled courses.
    """

    # Check if student has already completed any courses (input validation)
    if completed_course_codes is None:
        completed_course_codes = []

    # Load CSVs
    data_dir = Path("data") / major.lower()
    courses = pd.read_csv(f"{data_dir}/courses.csv")
    professors = pd.read_csv(f"{data_dir}/professors.csv")
    courses = courses.merge(professors, left_on="professor_id", right_on="id", suffixes=("", "_prof")).drop(columns=["id_prof"])
    prereqs = pd.read_csv(f"{data_dir}/prereqs.csv")
    
    # Filter courses by department/major - STILL NEEDS TO BE IMPLEMENTED

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
    
    # Create the term sequence, return an error if term sequence is invalid
    term_sequence = build_term_range(upcoming_term, grad_term)
    if not term_sequence:
            raise ValueError(
        f"Invalid term range: upcoming_term={upcoming_term}, grad_term={grad_term}"
    )

    # Calculate average difficulty per term (total difficulty of all courses / # of terms)
    avg_difficulty_per_term = courses["difficulty"].sum() / len(term_sequence)

    terms = []  
    term_idx = 0 # Counter to track which term we are scheduling for
    planned = set() # Set of course IDs that have been planned to be taken
    remaining = [cid for cid in topo_order if cid not in completed_ids] # Remaining courses to schedule, excluding already completed ones

    while remaining and term_idx < len(term_sequence):
        current_term = []
        current_credits = 0
        placed_this_term = []
        current_workload = 0
        season, year = term_sequence[term_idx].split()
        is_summer = (season == "Summer")

        if is_summer:
            credit_cap = 9 # Summer terms typically have a lower credit cap
        else:
            credit_cap = max_credits_per_term


        for cid in remaining:
            course = id_to_course[cid]
            credits = int(course["credits"])
            difficulty = float(course["difficulty"])

            # prereqs must be satisfied
            prereq_ids = [p for p in G.predecessors(cid)]
            if not set(prereq_ids).issubset(completed_ids.union(planned)):
                continue

            # Check if adding this course exceeds credit cap or workload, add to current term if it does not
            if current_credits + credits <= credit_cap and current_workload + difficulty <= avg_difficulty_per_term * 1.25:
                current_term.append({
                    "id": int(cid),
                    "code": str(course["code"]),
                    "title": str(course["title"]),
                    "credits": credits,
                    "difficulty": difficulty
                })
                current_credits += credits
                current_workload += difficulty
                placed_this_term.append(cid)

        if current_term:
            terms.append({
                "term": term_sequence[term_idx],
                "courses": current_term,
                "total_credits": current_credits,
                "average_difficulty": current_workload/len(current_term)
            })
            planned.update(placed_this_term)
            completed_ids.update(placed_this_term)
            remaining = [c for c in remaining if c not in placed_this_term]
        else:
            # skip to next term if nothing else can be placed
            term_idx += 1
            continue

        term_idx += 1

    # Figure out which courses were left unscheduled
    all_course_ids = set(courses["id"])
    unscheduled = all_course_ids - planned - completed_ids

    # Case where some courses could not be scheduled
    if unscheduled:
        unscheduled_courses = [
            {
                "id": int(cid),
                "code": id_to_course[cid]["code"],
                "title": id_to_course[cid]["title"],
                "credits": int(id_to_course[cid]["credits"]),
                "difficulty": float(id_to_course[cid]["difficulty"])
            }
            for cid in unscheduled
        ]
        return {
            "error": "Unable to fit all courses into the schedule within the given timeframe.",
            "terms": terms,  # partial schedule
            "unscheduled_courses": unscheduled_courses,
            "totals": {
                "credits_planned": sum(t["total_credits"] for t in terms),
                "courses_planned": len(planned),
                "courses_unscheduled": len(unscheduled)
            }
        }

    # Normal case: everything fits
    return {
        "plan_id": str(uuid.uuid4()),
        "terms": terms,
        "totals": {
            "credits_planned": sum(t["total_credits"] for t in terms),
            "courses_planned": len(planned)
        }
    }