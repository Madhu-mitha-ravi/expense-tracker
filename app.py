import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("Personal Expense Tracker")


if "expenses" not in st.session_state:
    st.session_state["expenses"] = []
if "budget" not in st.session_state:
    st.session_state["budget"] = 0


st.session_state["budget"] = st.number_input(
    "Set your monthly budget (₹)", min_value=0.0, value=float(st.session_state["budget"])
)

st.subheader("Add Expense")
with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0.0)

    submitted = st.form_submit_button("Add Expense")

if submitted:
    st.session_state["expenses"].append({
        "Date": date, "Category": category, "Amount": amount,
    })
    st.success("Expense added!")

st.write(st.session_state["expenses"])
# Convert to DataFrame
df = pd.DataFrame(st.session_state["expenses"])

st.subheader("Your Expenses")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("No expenses added yet.")

# Metrics
total_spent = df["Amount"].sum() if not df.empty else 0
remaining = st.session_state["budget"] - total_spent

col1, col2, col3 = st.columns(3)
col1.metric("Budget", f"₹{st.session_state['budget']:.2f}")
col2.metric("Total Spent", f"₹{total_spent:.2f}")
col3.metric("Remaining", f"₹{remaining:.2f}")

if remaining < 0:
    st.error("⚠️ You've exceeded your budget!")
    # Category-wise chart
if not df.empty:
    st.subheader("Spending by Category")
    category_totals = df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_totals)

    # CSV download
    st.subheader("Export")
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="expenses.csv",
        mime="text/csv"
    )