import streamlit as st
import pandas as pd
from ui import banner 
banner("Change Book Status", "Tick the box when a book is available, untick it when someone borrows it.", image="status.jpg", emoji="🔄")
books = st.session_state["books"]

# ---------- Header ----------
st.caption("Tick the box when a book is available, untick it when someone borrows it.")

# ---------- Empty library ----------
if books.empty:
    st.info("Your library is empty. Go to **Add Book** to add some books, or upload a CSV on the Home page.", icon="📭")
    st.stop()

# ---------- Summary ----------
m1, m2, m3 = st.columns(3)
m1.metric("Total Books", len(books))
m2.metric("Available", int((books["Status"] == True).sum()))
m3.metric("Borrowed", int((books["Status"] == False).sum()))

# ---------- Search ----------
with st.container(border=True):
    search = st.text_input("🔍 Search", placeholder="Type a book title...")

    if search:
        results = books[books["title"].str.contains(search, case=False, na=False, regex=False)]
        if results.empty:
            st.error("No book with that title", icon="⚠️")
        else:
            st.caption(f"{len(results)} book(s) found")
    else:
        results = books

# ---------- Table ----------
with st.container(border=True):
    edited = st.data_editor(
        results,
        hide_index=True,
        use_container_width=True,
        disabled=[col for col in results.columns if col != "Status"],
        column_config={
            "Status": st.column_config.CheckboxColumn(
                "Available", help="Untick to mark the book as borrowed"
            ),
            "date taken": st.column_config.DateColumn("Date taken", format="DD/MM/YYYY"),
            "return date": st.column_config.DateColumn("Return date", format="DD/MM/YYYY"),
        },
    )

# ---------- Apply changes ----------
changed = edited["Status"] != results["Status"]

if changed.any():
    # Rows that were just borrowed (Status changed to False)
    newly_borrowed = changed & (edited["Status"] == False)
    borrowed_index = newly_borrowed[newly_borrowed].index

    today = pd.Timestamp.today().normalize()

    books.loc[edited.index, "Status"] = edited["Status"]
    books.loc[borrowed_index, "date taken"] = today
    books.loc[borrowed_index, "return date"] = today + pd.Timedelta(days=14)

    st.session_state["status_msg"] = f"Updated {int(changed.sum())} book(s)"
    st.rerun()

if "status_msg" in st.session_state:
    st.toast(st.session_state.pop("status_msg"), icon="✅")

# ---------- Save ----------
st.divider()
st.caption("Done making changes? Download your updated file before you leave.")

st.download_button(
    label="⬇️ Download updated CSV",
    data=st.session_state["books"].to_csv(index=False, date_format="%d/%m/%Y").encode("utf-8"),
    file_name="books.csv",
    mime="text/csv",
    key="download_csv",
)