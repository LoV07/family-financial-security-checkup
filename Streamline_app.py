import streamlit as st

st.set_page_config(
    page_title="LifeStage Financial Wellness Assessment",
    layout="wide"
)

st.title("🏠 LifeStage Financial Wellness Assessment")
st.caption(
    "Prototype Personalized Financial Security Checkup for Gen Z, Millennials and Families"
)

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.header("Employee Profile")

    age = st.slider("Age", 18, 60, 28)

    life_stage = st.selectbox(
        "Life Stage",
        [
            "Single",
            "Married",
            "Married with Children"
        ]
    )

    annual_income = st.number_input(
        "Annual Income (₹)",
        min_value=0,
        value=1200000,
        step=50000
    )

    dependents = st.number_input(
        "Number of Dependents",
        min_value=0,
        value=0 if life_stage == "Single" else 2
    )

# =========================
# GOALS
# =========================

st.header("🎯 Step 1: Financial Goals")

col1, col2 = st.columns(2)

with col1:

    if life_stage == "Married with Children":
        child_education = st.number_input(
            "Child Education Goal (₹)",
            min_value=0,
            value=3000000,
            step=100000
        )

        child_marriage = st.number_input(
            "Child Marriage Goal (₹)",
            min_value=0,
            value=2500000,
            step=100000
        )

    else:
        child_education = 0
        child_marriage = 0

    future_marriage_goal = st.number_input(
        "Future Marriage Fund (₹)",
        min_value=0,
        value=1000000 if life_stage == "Single" else 0,
        step=100000
    )

with col2:

    retirement_goal = st.number_input(
        "Retirement Corpus Goal (₹)",
        min_value=0,
        value=20000000,
        step=500000
    )

    home_purchase_goal = st.number_input(
        "Future Home Purchase Goal (₹)",
        min_value=0,
        value=5000000,
        step=100000
    )

    travel_goal = st.number_input(
        "Dream Travel / Lifestyle Goals (₹)",
        min_value=0,
        value=500000,
        step=50000
    )

    other_goals = st.number_input(
        "Other Goals (₹)",
        min_value=0,
        value=0,
        step=100000
    )

# =========================
# OBLIGATIONS
# =========================

st.header("💳 Step 2: Financial Obligations")

col3, col4 = st.columns(2)

with col3:
    annual_expense = st.number_input(
        "Annual Household Expense (₹)",
        min_value=0,
        value=600000,
        step=50000
    )

    years_support = st.slider(
        "Years Family Needs Support",
        1,
        30,
        15
    )

with col4:
    outstanding_loans = st.number_input(
        "Outstanding Loans (₹)",
        min_value=0,
        value=4000000,
        step=100000
    )

    education_loan = st.number_input(
        "Education Loan Outstanding (₹)",
        min_value=0,
        value=0,
        step=50000
    )

# =========================
# PROTECTION
# =========================

st.header("🛡️ Step 3: Existing Protection")

col5, col6 = st.columns(2)

with col5:

    existing_insurance = st.number_input(
        "Existing Life Insurance (₹)",
        min_value=0,
        value=2500000,
        step=100000
    )

    employer_cover = st.number_input(
        "Employer Life Cover (₹)",
        min_value=0,
        value=2000000,
        step=100000
    )

with col6:

    savings = st.number_input(
        "Savings & Investments (₹)",
        min_value=0,
        value=1500000,
        step=100000
    )

    emergency_fund = st.number_input(
        "Emergency Fund (₹)",
        min_value=0,
        value=100000,
        step=50000
    )

    rely_on_employer = st.radio(
        "Do you mainly rely on Employer Insurance?",
        ["Yes", "No"]
    )

# =========================
# CALCULATIONS
# =========================

income_replacement = annual_expense * years_support

total_goals = (
    child_education
    + child_marriage
    + future_marriage_goal
    + retirement_goal
    + home_purchase_goal
    + travel_goal
    + other_goals
)

existing_protection = (
    existing_insurance
    + employer_cover
    + savings
)

required_cover = max(
    0,
    total_goals
    + outstanding_loans
    + education_loan
    + income_replacement
    - existing_protection
)

# Protection Score

protection_score = min(
    100,
    round(
        (
            existing_protection
            / max(
                1,
                total_goals
                + outstanding_loans
                + education_loan
                + income_replacement
            )
        )
        * 100
    )
)

# =========================
# GEN Z / WELLNESS SCORE
# =========================

genz_score = 100

# Emergency fund should cover 6 months expenses

if emergency_fund < (annual_expense / 2):
    genz_score -= 20

if existing_insurance == 0:
    genz_score -= 20

if education_loan > savings:
    genz_score -= 20

if rely_on_employer == "Yes":
    genz_score -= 20

if age < 35 and retirement_goal < annual_income * 10:
    genz_score -= 20

genz_score = max(0, genz_score)

overall_score = round(
    (protection_score * 0.7)
    + (genz_score * 0.3)
)

# =========================
# PREMIUM ESTIMATION
# =========================

def estimate_monthly_premium(cover):
    cover_cr = cover / 10000000
    return round(cover_cr * 700, 0)

premium = estimate_monthly_premium(required_cover)

# =========================
# RESULTS
# =========================

st.header("📊 Assessment Results")

r1, r2, r3, r4 = st.columns(4)

r1.metric(
    "Total Goals",
    f"₹{total_goals:,.0f}"
)

r2.metric(
    "Income Replacement",
    f"₹{income_replacement:,.0f}"
)

r3.metric(
    "Current Protection",
    f"₹{existing_protection:,.0f}"
)

r4.metric(
    "Required Cover",
    f"₹{required_cover:,.0f}"
)

# =========================
# SCORES
# =========================

st.subheader("Financial Protection Score")

st.progress(protection_score / 100)
st.write(f"**{protection_score}/100**")

if protection_score < 30:
    st.error("🔴 High Protection Gap")
elif protection_score < 60:
    st.warning("🟠 Moderate Protection Gap")
else:
    st.success("🟢 Well Protected")

st.subheader("LifeStage Financial Readiness Score")

st.progress(overall_score / 100)
st.write(f"**{overall_score}/100**")

if overall_score >= 80:
    st.success("🚀 Financially Future Ready")
elif overall_score >= 60:
    st.info("👍 Good Start, Some Gaps Exist")
elif overall_score >= 40:
    st.warning("⚠️ Moderate Financial Risk")
else:
    st.error("❌ High Financial Vulnerability")

# =========================
# GOAL STATUS
# =========================

st.subheader("🎯 Goal Protection Status")

coverage_ratio = (
    existing_protection
    / max(
        1,
        existing_protection + required_cover
    )
)

goal_status = {
    "Child Education": child_education,
    "Child Marriage": child_marriage,
    "Retirement": retirement_goal,
    "Home Purchase": home_purchase_goal,
    "Outstanding Loans": outstanding_loans
}

for goal, value in goal_status.items():

    if value <= 0:
        continue

    if coverage_ratio > 0.7:
        status = "✅ Protected"
    elif coverage_ratio > 0.4:
        status = "⚠️ Partially Protected"
    else:
        status = "❌ At Risk"

    st.write(f"**{goal}** : {status}")

# =========================
# RECOMMENDATIONS
# =========================

st.subheader("📌 Personalized Recommendations")

recommendations = []

if emergency_fund < annual_expense / 2:
    recommendations.append(
        "Build an emergency fund covering at least 6 months of expenses."
    )

if existing_insurance == 0:
    recommendations.append(
        "Purchase a term insurance plan immediately."
    )

if rely_on_employer == "Yes":
    recommendations.append(
        "Do not depend solely on employer-provided life insurance."
    )

if education_loan > savings:
    recommendations.append(
        "Reduce outstanding debt before taking additional liabilities."
    )

if protection_score < 60:
    recommendations.append(
        f"Increase protection by approximately ₹{required_cover:,.0f}."
    )

if not recommendations:
    recommendations.append(
        "Your financial wellness profile looks healthy. Continue periodic reviews."
    )

for rec in recommendations:
    st.write(f"• {rec}")

# =========================
# COVER RECOMMENDATION
# =========================

st.subheader("🛡️ Recommended Protection")

st.info(
    f"""
Suggested Additional Term Cover: ₹{required_cover:,.0f}

Estimated Monthly Premium: ₹{premium:,.0f}

Overall Financial Readiness Score: {overall_score}/100
"""
)

# =========================
# DOWNLOAD SUMMARY
# =========================

summary = f"""
LIFESTAGE FINANCIAL WELLNESS REPORT

Age: {age}
Life Stage: {life_stage}

Protection Score: {protection_score}/100
Financial Readiness Score: {overall_score}/100

Total Goals: ₹{total_goals:,.0f}
Income Replacement Need: ₹{income_replacement:,.0f}
Current Protection: ₹{existing_protection:,.0f}
Required Cover: ₹{required_cover:,.0f}

Estimated Premium: ₹{premium:,.0f}/month
"""

st.download_button(
    "📥 Download Assessment Report",
    data=summary,
    file_name="financial_wellness_report.txt"
)
