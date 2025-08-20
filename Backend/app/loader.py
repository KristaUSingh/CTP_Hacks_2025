from pathlib import Path
import pandas as pd
from typing import Dict

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
REQUIRED_TABLES = ["courses", "prereqs", "offerings", "professors", "degree_requirements"]

def load_csvs(data_dir: Path = DATA_DIR) -> Dict[str, pd.DataFrame]:
    """Load CSVs into pandas DataFrames. Raises if a required file is missing."""
    dfs = {}
    for name in REQUIRED_TABLES:
        path = data_dir / f"{name}.csv"
        if not path.exists():
            raise FileNotFoundError(f"Missing CSV: {path}")
        dfs[name] = pd.read_csv(path)
    return dfs

def validate_prereqs(dfs: Dict[str, pd.DataFrame]):
    """Basic sanity checks: prereq ids reference existing course ids."""
    courses = set(dfs["courses"]["id"].astype(int))
    bad = set(dfs["prereqs"]["course_id"].astype(int)).difference(courses) | \
          set(dfs["prereqs"]["requires_course_id"].astype(int)).difference(courses)
    if bad:
        raise ValueError(f"Prereqs reference unknown course ids: {sorted(bad)}")

def write_sqlite(dfs: Dict[str, pd.DataFrame], engine):
    """Write DataFrames to SQLite (if you choose to use SQL)."""
    for name, df in dfs.items():
        df.to_sql(name, engine, if_exists="replace", index=False)