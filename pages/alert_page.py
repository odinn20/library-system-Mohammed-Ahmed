import streamlit as st
import pandas as pd
from ui import banner
banner("Dashboard", "A quick look at the state of the library.", image="dashboard.jpg", emoji="📊")
books = st.session_state["books"]

# ---------- Header ----------
st.caption("A quick look at the state of the library.")

# ---------- Empty library ----------
if books.empty:
    st.info("Your library is empty. Go to **Add Book** to add some books, or upload a CSV on the Home page.", icon="📭")
    st.stop()

books["return date"] = pd.to_datetime(books["return date"], errors="coerce")

today = pd.Timestamp.today().normalize()

available = int((books["Status"] == True).sum())
borrowed = int((books["Status"] == False).sum())

overdue_mask = (books["Status"] == False) & (books["return date"] < today)
overdue_books = books[overdue_mask].copy()
overdue_books["Days overdue"] = (today - overdue_books["return date"]).dt.days
overdue_books = overdue_books.sort_values("Days overdue", ascending=False)

# ---------- Statistics ----------
stats = [
    ("📚 Total Books", len(books)),
    ("✅ Available", available),
    ("📖 Borrowed", borrowed),
    ("⏰ Overdue", len(overdue_books)),
]

for col, (label, value) in zip(st.columns(4), stats):
    with col.container(border=True):
        st.metric(label, value)

# ---------- Overdue books ----------
st.subheader("⏰ Overdue Books")

with st.container(border=True):
    if overdue_books.empty:
        st.success("No overdue books. Everything is on time!", icon="🎉")
    else:
        st.caption(f"{len(overdue_books)} book(s) past their return date")
        st.dataframe(
            overdue_books,
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
                "Days overdue": st.column_config.NumberColumn("Days overdue", format="%d"),
            },
        )

# ---------- Genre chart ----------
st.subheader("🎭 Books by Genre")

with st.container(border=True):
    genre_counts = books["Genre"].value_counts()
    st.bar_chart(genre_counts, x_label="Genres", y_label="Total Books",color='Green')

# ---------- Save ----------
st.divider()
st.caption("Done for now? Download your updated file before you leave.")

st.download_button(
    label="⬇️ Download updated CSV",
    data=books.to_csv(index=False, date_format="%d/%m/%Y").encode("utf-8"),
    file_name="books.csv",
    mime="text/csv",
    key="download_csv",
)