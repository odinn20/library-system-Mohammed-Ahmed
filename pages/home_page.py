import streamlit as st
import pandas as pd
from ui import banner

REQUIRED_COLUMNS = ["ISNB", "title", "author", "Genre", "Status", "date taken", "return date"]
DATE_COLS = ["date taken", "return date"]

banner("DSB 4 Library", "Browse, borrow, and keep track of every book in one place.", image="home.jpg")
def empty_library():
    return pd.DataFrame({
        "ISNB": pd.Series(dtype="int64"),
        "title": pd.Series(dtype="object"),
        "author": pd.Series(dtype="object"),
        "Genre": pd.Series(dtype="object"),
        "Status": pd.Series(dtype="bool"),
        "date taken": pd.Series(dtype="datetime64[ns]"),
        "return date": pd.Series(dtype="datetime64[ns]"),
    })


def read_library(file):
    """Returns (dataframe, None) on success or (None, error_message) on failure."""
    try:
        df = pd.read_csv(file)
    except pd.errors.EmptyDataError:
        # Completely empty file: start a fresh, blank library
        return empty_library(), None
    except Exception:
        return None, "Couldn't read that file. Make sure it's a valid CSV."

    df.columns = df.columns.str.strip()

    # A file with no rows (even with different headers) also starts a fresh, blank library
    if df.empty:
        return empty_library(), None

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return None, f"The file is missing these columns: {', '.join(missing)}"

    for col in DATE_COLS:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")

    # Accept True/False written as text, and treat blanks as available
    df["Status"] = (
        df["Status"].astype(str).str.strip().str.lower()
        .map({"true": True, "false": False})
        .fillna(True)
        .astype(bool)
    )

    return df, None


# ---------- Header ----------
st.caption("Browse, borrow, and keep track of every book in one place.")

# ---------- Welcome card ----------
with st.container(border=True):
    st.subheader("Welcome!")
    st.write("Glad to have you here. A big thank you to the people who make this place great:")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#####  Lead Instructor 🎓")
        st.write("Hadia")
    with c2:
        st.markdown("#####  Instructional Associates 🛠️")
        st.write("Jamila & Abdulrahman")
    with c3:
        st.markdown("#####  Best Students 🌟")
        st.write("YOU GUYS!!")

# ---------- Upload ----------
st.subheader("📂 Load your library data")

with st.container(border=True):
    st.caption("Have a saved library? Upload it here. Otherwise, head to **Add Book** and start from scratch.")

    uploaded = st.file_uploader("Upload your books.csv", type="csv", key="uploader")

    if uploaded is not None:
        file_id = f"{uploaded.name}-{uploaded.size}"

        # Only load when it's a NEW file, so edits made on other pages aren't overwritten on reruns
        if st.session_state.get("file_id") != file_id:
            df, error = read_library(uploaded)

            if error:
                st.error(error, icon="⚠️")
            else:
                st.session_state["books"] = df
                st.session_state["file_id"] = file_id
                if df.empty:
                    st.toast("Started a new empty library. Add your first book!", icon="📭")
                else:
                    st.toast(f"Loaded {len(df)} books from {uploaded.name}", icon="✅")

# ---------- Status ----------
books = st.session_state["books"]

if books.empty:
    st.info("Your library is empty. Upload a CSV above, or go to **Add Book** to create your first entry.", icon="📭")
else:
    st.subheader("📊 Library at a glance")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Books", len(books))
    m2.metric("Available", int((books["Status"] == True).sum()))
    m3.metric("Borrowed", int((books["Status"] == False).sum()))

    with st.expander("Preview your data"):
        st.dataframe(
            books,
            use_container_width=True,
            hide_index=True,
            column_config={
                "date taken": st.column_config.DateColumn("Date taken", format="DD/MM/YYYY"),
                "return date": st.column_config.DateColumn("Return date", format="DD/MM/YYYY"),
            },
        )