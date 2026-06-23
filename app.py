
import streamlit as st

st.set_page_config(page_title="Family Financial Security Checkup", layout="wide")

st.title("🏠 Family Financial Security Checkup")
st.caption("Demo Prototype: Goal Planning + Protection Gap Assessment")

with st.sidebar:
    st.header("Employee Profile")
    age = st.slider("Age", 18, 60, 28)
    annual_income = st.number_input("Annual Income (₹)", min_value=0, value=1200000, step=50000)
    dependents = st.number_input("Number of Dependents", min_value=0, value=2)

st.header("Step 1: Financial Goals")

col1, col2 = st.columns(2)

with col1:
    child_education = st.number_input("Child Education Goal (₹)", min_value=0, value=3000000, step=100000)
    child_marriage = st.number_input("Child Marriage Goal (₹)", min_value=0, value=2500000, step=100000)

with col2:
    retirement_goal = st.number_input("Retirement Corpus Goal (₹)", min_value=0, value=20000000, step=500000)
    other_goals = st.number_input("Other Family Goals (₹)", min_value=0, value=0, step=100000)

st.header("Step 2: Financial Obligations")

annual_expense = st.number_input("Annual Household Expense (₹)", min_value=0, value=600000, step=50000)
years_support = st.slider("Years Family Needs Support", 1, 30, 15)
outstanding_loans = st.number_input("Outstanding Loans (₹)", min_value=0, value=4000000, step=100000)

st.header("Step 3: Existing Protection")

col3, col4 = st.columns(2)

with col3:
    existing_insurance = st.number_input("Existing Life Insurance (₹)", min_value=0, value=2500000, step=100000)

with col4:
    employer_cover = st.number_input("Employer Life Cover (₹)", min_value=0, value=2000000, step=100000)
    savings = st.number_input("Savings & Investments (₹)", min_value=0, value=1500000, step=100000)

# Calculations
income_replacement = annual_expense * years_support
total_goals = child_education + child_marriage + retirement_goal + other_goals
existing_protection = existing_insurance + employer_cover + savings

required_cover = max(
    0,
    total_goals + outstanding_loans + income_replacement - existing_protection
)

protection_score = min(
    100,
    round((existing_protection / max(1, (total_goals + outstanding_loans + income_replacement))) * 100)
)

def estimate_monthly_premium(cover):
    cover_cr = cover / 10000000
    return round(cover_cr * 700, 0)

premium = estimate_monthly_premium(required_cover)

st.header("📊 Results")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Goals", f"₹{total_goals:,.0f}")
c2.metric("Income Replacement", f"₹{income_replacement:,.0f}")
c3.metric("Existing Protection", f"₹{existing_protection:,.0f}")
c4.metric("Required Cover", f"₹{required_cover:,.0f}")

st.subheader("Protection Score")
st.progress(protection_score / 100)
st.write(f"**{protection_score}/100**")

if protection_score < 30:
    st.error("High Protection Gap")
elif protection_score < 60:
    st.warning("Moderate Protection Gap")
else:
    st.success("Good Protection Level")

st.subheader("Goal Protection Status")

coverage_ratio = existing_protection / max(1, required_cover + existing_protection)

goals = {
    "Child Education": child_education,
    "Child Marriage": child_marriage,
    "Retirement": retirement_goal,
    "Outstanding Loans": outstanding_loans,
}

for goal, value in goals.items():
    if value <= 0:
        continue
    if coverage_ratio > 0.7:
        status = "✅ Protected"
    elif coverage_ratio > 0.4:
        status = "⚠️ Partially Protected"
    else:
        status = "❌ At Risk"

    st.write(f"{goal}: {status}")

st.subheader("Recommended Action")

st.info(
    f"Suggested Additional Term Cover: ₹{required_cover:,.0f}\n\n"
    f"Estimated Premium: ₹{premium:,.0f}/month"
)

st.download_button(
    "Download Summary",
    data=f"""
Protection Score: {protection_score}/100
Required Cover: ₹{required_cover:,.0f}
Estimated Premium: ₹{premium:,.0f}/month
""",
    file_name="protection_summary.txt"
)
