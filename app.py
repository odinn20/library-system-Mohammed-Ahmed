import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="DSB 4 Library", page_icon="📚", layout="wide")

DATE_COLS = ["date taken", "return date"]
SAMPLE_PATH = Path(r"C:\Users\moham\OneDrive\Desktop\Data Science\project 1\.venv\books.csv")


def load_starting_library():
    if SAMPLE_PATH.exists():
        df = pd.read_csv(SAMPLE_PATH)
        for col in DATE_COLS:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
        return df

    # Fallback: empty library if the file is missing
    return pd.DataFrame({
        "ISNB": pd.Series(dtype="int64"),
        "title": pd.Series(dtype="object"),
        "author": pd.Series(dtype="object"),
        "Genre": pd.Series(dtype="object"),
        "Status": pd.Series(dtype="bool"),
        "date taken": pd.Series(dtype="datetime64[ns]"),
        "return date": pd.Series(dtype="datetime64[ns]"),
    })


# Runs once per session, so it never overwrites books the user has added or uploaded
if "books" not in st.session_state:
    st.session_state["books"] = load_starting_library()

home_page = st.Page("pages/home_page.py", title="Home")
addbook_page = st.Page("pages/add_page.py", title="Add Book")
Change_status_page = st.Page("pages/Change_status.py", title="Change Book Status")
catalog_page = st.Page("pages/Catalog_page.py", title="Our Catalog")
inventory_page = st.Page("pages/inventory_page.py", title="Our inventory")
alert_page = st.Page("pages/alert_page.py", title="Dashboard")

pg = st.navigation(
    [home_page, addbook_page, Change_status_page, catalog_page, inventory_page, alert_page],
    position="top",
)
pg.run()