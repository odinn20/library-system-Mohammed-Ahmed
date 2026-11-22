import streamlit as st
import pandas as pd
from ui import banner
banner("Inventory", "Every book in the library, available or borrowed.", image="inventory.jpg", emoji="🗂️")
books = st.session_state["books"]

# ---------- Header ----------
st.caption("Every book in the library, available or borrowed.")

# ---------- Empty library ----------
if books.empty:
    st.info("Your library is empty. Go to **Add Book** to add some books, or upload a CSV on the Home page.", icon="📭")
    st.stop()

m1, m2, m3 = st.columns(3)
m1.metric("Total Books", len(books))
m2.metric("Available", int((books["Status"] == True).sum()))
m3.metric("Borrowed", int((books["Status"] == False).sum()))

# ---------- Search + filters ----------
with st.container(border=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    search = c1.text_input("🔍 Search", placeholder="Type a book title...")
    genres = ["All genres"] + sorted(books["Genre"].dropna().unique())
    genre = c2.selectbox("Genre", genres)
    availability = c3.selectbox("Availability", ["All", "Available", "Borrowed"])

results = books

if search:
    results = results[results["title"].str.contains(search, case=False, na=False, regex=False)]

if genre != "All genres":
    results = results[results["Genre"] == genre]

if availability == "Available":
    results = results[results["Status"] == True]
elif availability == "Borrowed":
    results = results[results["Status"] == False]

# ---------- Results ----------
with st.container(border=True):
    if results.empty:
        st.error("No books match your search.", icon="⚠️")
    else:
        st.caption(f"Showing {len(results)} of {len(books)} book(s)")
        st.dataframe(
            results,
            hide_index=True,
            use_container_width=True,
            column_config={
                "ISNB": "ISNB",
                "title": "Title",
                "author": "Author",
                "Genre": "Genre",
                "Status": st.column_config.CheckboxColumn("Available"),
                "date taken": st.column_config.DateColumn("Date taken", format="DD/MM/YYYY"),
                "return date": st.column_config.DateColumn("Return date", format="DD/MM/YYYY"),
            },
        )

# ---------- Save ----------
st.divider()
st.caption("Want to keep your changes? Download your updated file before you leave.")

st.download_button(
    label="⬇️ Download updated CSV",
    data=st.session_state["books"].to_csv(index=False, date_format="%d/%m/%Y").encode("utf-8"),
    file_name="books.csv",
    mime="text/csv",
    key="download_csv",
)