import streamlit as st
import pandas as pd
from ui import banner
banner("Add a Book", "Add a new book to the library catalog.", image="add.jpg", emoji="➕")
GENRES = ("Fiction", "Science", "Adventure", "Horror", "Thriller", "Comedy")

if "new_status" not in st.session_state:
    st.session_state["new_status"] = True


def add_book():
    title = st.session_state["new_title"].strip()
    if not title:
        st.session_state["add_error"] = True
        return
    st.session_state["add_error"] = False

    books = st.session_state["books"]

    if st.session_state["new_status"]:
        date = pd.NaT
        return_date = pd.NaT
    else:
        date = pd.Timestamp(st.session_state["new_date"])
        return_date = date + pd.Timedelta(days=14)

    isnb = 1 if books["ISNB"].dropna().empty else int(books["ISNB"].max()) + 1

    new_row = pd.DataFrame({
        "ISNB": [isnb],
        "title": [title],
        "author": [st.session_state["new_author"].strip()],
        "Genre": [st.session_state["new_genre"]],
        "Status": [st.session_state["new_status"]],
        "date taken": [date],
        "return date": [return_date],
    })

    # Replace the table when it's empty, to avoid pandas dtype warnings from concatenating onto nothing
    if books.empty:
        st.session_state["books"] = new_row
    else:
        st.session_state["books"] = pd.concat([books, new_row], ignore_index=True)

    st.session_state["last_added"] = f"Added '{title}' (ISNB {isnb})"

    # Clear the form for the next book
    st.session_state["new_title"] = ""
    st.session_state["new_author"] = ""
    st.session_state["new_status"] = True


# ---------- Header ----------
st.caption("Add a new book to the library catalog.")

# ---------- Book details ----------
with st.container(border=True):
    st.subheader("📖 Book details")

    c1, c2 = st.columns(2)
    c1.text_input("Title", key="new_title", placeholder="e.g. The Hobbit")
    c2.text_input("Author", key="new_author", placeholder="e.g. J.R.R. Tolkien")

    c3, c4 = st.columns(2)
    c3.selectbox("Genre", GENRES, key="new_genre")
    with c4:
        st.write("")  # nudges the toggle down to line up with the selectbox
        st.toggle("Available", key="new_status")

# ---------- Borrowing details (only if not available) ----------
if not st.session_state["new_status"]:
    with st.container(border=True):
        st.subheader("📅 Borrowing details")

        d1, d2 = st.columns(2)
        picked = d1.date_input(
            "When was it borrowed?",
            value="today",
            max_value="today",
            key="new_date",
            format="DD/MM/YYYY",
        )
        due = pd.Timestamp(picked) + pd.Timedelta(days=14)
        d2.metric("Return date", due.strftime("%d/%m/%Y"))

# ---------- Add button + feedback ----------
st.button("➕ Add Book", type="primary", use_container_width=True, on_click=add_book)

if st.session_state.get("add_error"):
    st.error("Please enter a title.", icon="⚠️")

if "last_added" in st.session_state:
    st.toast(st.session_state.pop("last_added"), icon="✅")

# ---------- Save ----------
st.divider()
st.caption("Done adding books? Download your updated file before you leave.")

st.download_button(
    label="⬇️ Download updated CSV",
    data=st.session_state["books"].to_csv(index=False, date_format="%d/%m/%Y").encode("utf-8"),
    file_name="books.csv",
    mime="text/csv",
    key="download_csv",
)