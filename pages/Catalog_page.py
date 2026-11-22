import streamlit as st
import pandas as pd
from ui import banner 
banner("Catalog", "Every book that's available to borrow right now.", image="catalog.jpg")
books = st.session_state["books"]
available_books = books[books["Status"] == True]

if "show_all_catalog" not in st.session_state:
    st.session_state["show_all_catalog"] = False


def toggle_show_all():
    st.session_state["show_all_catalog"] = not st.session_state["show_all_catalog"]


# ---------- Header ----------
st.caption("Every book that's available to borrow right now.")

# ---------- Empty library ----------
if books.empty:
    st.info("Your library is empty. Go to **Add Book** to add some books, or upload a CSV on the Home page.", icon="📭")
    st.stop()

m1, m2 = st.columns(2)
m1.metric("Available Books", len(available_books))
m2.metric("Genres", available_books["Genre"].nunique())

# ---------- Search + filter ----------
with st.container(border=True):
    c1, c2 = st.columns([2, 1])
    search = c1.text_input("🔍 Search", placeholder="Type a book title...")
    genres = ["All genres"] + sorted(available_books["Genre"].dropna().unique())
    genre = c2.selectbox("Genre", genres)

    st.button(
        "🙈 Hide list" if st.session_state["show_all_catalog"] else "📖 Show all available books",
        on_click=toggle_show_all,
        use_container_width=True,
    )

# ---------- Results ----------
show_results = st.session_state["show_all_catalog"] or bool(search) or genre != "All genres"

if show_results:
    results = available_books

    if search:
        results = results[results["title"].str.contains(search, case=False, na=False, regex=False)]

    if genre != "All genres":
        results = results[results["Genre"] == genre]

    with st.container(border=True):
        if results.empty:
            st.error("There is no available book matching your search.", icon="⚠️")
        else:
            st.caption(f"Showing {len(results)} book(s)")
            st.dataframe(
                results[["ISNB", "title", "author", "Genre"]],
                hide_index=True,
                use_container_width=True,
                column_config={
                    "ISNB": "ISNB",
                    "title": "Title",
                    "author": "Author",
                    "Genre": "Genre",
                },
            )
else:
    st.info("Search for a title, pick a genre, or click **Show all available books**.", icon="👆")

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