import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="iRetain - Intelligent Workforce Turnover Risk Analyzer",
    layout="wide"
)

# --- SESSION STATE FOR NAVIGATION ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- CUSTOM CSS ---
st.markdown("""
<style>

.main {
    background-color: #f37021;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f37021;
    border-right: 2px solid #7A0019;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* Hide default radio label */
div.row-widget.stRadio > div {
    flex-direction: column;
}

/* Main Titles */
.main-title {
    text-align: center;
    font-size: 110px;
    font-weight: bold;
    color: white;
    margin-top: 30px;
    text-shadow: 3px 3px 8px rgba(0,0,0,0.4);
    font-family: Georgia, serif;
}

.sub-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: white;
    margin-top: -30px;
    margin-bottom: 50px;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
}

/* Top right text */
.top-right {
    position: absolute;
    top: 20px;
    right: 40px;
    font-size: 24px;
    color: white;
    font-weight: bold;
}

/* Card Styling */
.home-card {
    background: linear-gradient(135deg, #7A0019, #5A0012);
    padding: 35px;
    border-radius: 20px;
    min-height: 260px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.35);
    transition: 0.3s ease;
    border-left: 10px solid #4A000F;
}

.home-card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 12px 25px rgba(0,0,0,0.45);
}

.card-title {
    font-size: 28px;
    font-weight: bold;
    color: white;
    margin-bottom: 25px;
}

.card-text {
    color: white;
    font-size: 20px;
}

/* Buttons */
.stButton>button {
    width: 100%;
    background-color: #7A0019;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.7rem;
    font-size: 18px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #5A0012;
    color: white;
}

/* Existing Styling */
.stMetric {
    background-color: #112240;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #233554;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}

h1, h2 {
    color: #64FFDA;
    font-family: Arial;
    text-shadow: 2px 2px 4px #000;
    font-weight: bold;
}

h3 {
    color: #f37021;
    font-weight: bold;
}

.risk-box {
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    border: 2px solid;
    background: rgba(0,0,0,0.3);
    margin-bottom: 25px;
}

.big-font {
    font-size: 85px !important;
    font-weight: bold;
}

.report-card {
    background: rgba(17, 34, 64, 0.9);
    padding: 25px;
    border-radius: 15px;
    border-left: 5px solid #f37021;
    margin-bottom: 20px;
    min-height: 250px;
}

.profile-text {
    font-size: 18px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# --- ROBUST DATA LOADER ---
@st.cache_data
def load_data():

    file_path = 'Attrition_Final_Production_v5_Corrected.xlsx'

    if not os.path.exists(file_path):
        st.error(f"⚠️ File Not Found: Please upload '{file_path}'")
        st.stop()

    try:
        df = pd.read_excel(file_path, sheet_name=0)

        # Standardize columns
        df.columns = df.columns.str.strip()

        # Active employees only
        if 'Status' in df.columns:
            active_df = df[df['Status'].str.upper() == 'ACTIVE'].copy()
        else:
            active_df = df.copy()

        return active_df

    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        st.stop()

df = load_data()

# =========================================================
# -------------------- HOME PAGE --------------------------
# =========================================================

if st.session_state.page == "Home":

    # ICICI LOGO
    col_logo1, col_logo2 = st.columns([1,5])

    with col_logo1:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/1/12/ICICI_Bank_Logo.svg",
            width=220
        )

    st.markdown(
        "<div class='top-right'>Predict. Prevent. Retain</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='main-title'>iRetain</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='sub-title'>The Intelligent Workforce Turnover Risk Analyzer</div>",
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    # --- CARDS ---
    col1, col2, col3 = st.columns(3)

    # CARD 1
    with col1:

        st.markdown("""
        <div class='home-card'>
            <div class='card-title'>
                Zone-wise Risk Summary
            </div>

            <div class='card-text'>
                An overview of Turnover Risk across 4 zones
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Zone-wise Risk Summary"):
            st.session_state.page = "Zone wise turnover prediction"
            st.rerun()

    # CARD 2
    with col2:

        st.markdown("""
        <div class='home-card'>
            <div class='card-title'>
                Employee Risk Predictor
            </div>

            <div class='card-text'>
                Identify Risk. Improve Retention
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Employee Risk Predictor"):
            st.session_state.page = "Employee risk indicator"
            st.rerun()

    # CARD 3
    with col3:

        st.markdown("""
        <div class='home-card'>
            <div class='card-title'>
                ER Login
            </div>

            <div class='card-text'>
                Monitor Turnover risk in your portfolio
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open ER Login"):
            st.session_state.page = "Employee risk indicator"
            st.rerun()

# =========================================================
# ----------- ZONE WISE TURNOVER PREDICTION ---------------
# =========================================================

elif st.session_state.page == "Zone wise turnover prediction":

    # BACK BUTTON
    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    st.title("🌐 Zone wise turnover prediction")
    st.markdown("#### Regional Vulnerability Matrix (Active Employees Only)")

    region_col = 'Home State' if 'Home State' in df.columns else (
        'ZONE' if 'ZONE' in df.columns else None
    )

    if region_col:

        regions = df[region_col].unique()[:4]

        cols = st.columns(2)

        for i, region in enumerate(regions):

            with cols[i % 2]:

                st.markdown(
                    f"<div class='stMetric'><h3>📍 {region}</h3>",
                    unsafe_allow_html=True
                )

                reg_df = df[df[region_col] == region]

                level_col = 'Risk_Level' if 'Risk_Level' in df.columns else 'Risk Level'

                counts = reg_df[level_col].value_counts(normalize=True) * 100

                fig, ax = plt.subplots(figsize=(6,3))

                cats = ['High', 'Medium', 'Low']

                vals = [
                    counts.get('High', 0),
                    counts.get('Medium', 0),
                    counts.get('Low', 0)
                ]

                colors = ['#FF3131', '#FFD700', '#2ECC71']

                bars = ax.bar(
                    cats,
                    vals,
                    color=colors,
                    edgecolor='white',
                    linewidth=1
                )

                ax.set_facecolor('#112240')
                fig.patch.set_facecolor('#0A192F')

                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                ax.set_ylim(0, 100)

                for bar in bars:

                    ax.text(
                        bar.get_x() + bar.get_width()/2.,
                        bar.get_height() + 2,
                        f'{bar.get_height():.1f}%',
                        ha='center',
                        color='#64FFDA',
                        fontweight='bold'
                    )

                st.pyplot(fig)

                st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("Regional columns not detected.")

# =========================================================
# ---------------- EMPLOYEE RISK INDICATOR ----------------
# =========================================================

elif st.session_state.page == "Employee risk indicator":

    # BACK BUTTON
    if st.button("⬅ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    st.title("🆔 Employee risk indicator")
    st.markdown("#### Predictive Insights & Retention Actionables")

    emp_id = st.number_input(
        "Enter EMPID to search",
        min_value=0,
        step=1
    )

    if emp_id:

        user_data = df[df['EMPID'] == emp_id]

        if not user_data.empty:

            row = user_data.iloc[0]

            score = row.get(
                'Attrition_Risk_Percentage',
                row.get('Attrition Risk (%)', 0)
            )

            level = row.get(
                'Risk_Level',
                row.get('Risk Level', 'Low')
            )

            h_color = (
                "#FF3131"
                if level == 'High'
                else ("#FFD700" if level == 'Medium' else "#2ECC71")
            )

            st.markdown(
                f"<div class='risk-box' style='border-color: {h_color};'>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<p class='big-font' style='color: {h_color};'>{score}%</p>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"<h1 style='color: {h_color};'>{level.upper()} RISK</h1>",
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.divider()

            # PROFILE
            st.subheader("📋 Employee Profile Details")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f"<p class='profile-text'><b>Grade:</b> {row.get('GRADE', 'N/A')}</p>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<p class='profile-text'><b>EMPID:</b> {row.get('EMPID', 'N/A')}</p>",
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    f"<p class='profile-text'><b>Age:</b> {row.get('AGE', 'N/A')}</p>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<p class='profile-text'><b>Tenure:</b> {row.get('TENURE_YRS', 'N/A')} Years</p>",
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    f"<p class='profile-text'><b>Home:</b> {row.get('Home State', 'N/A')}</p>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"<p class='profile-text'><b>Work:</b> {row.get('Work City', 'N/A')}</p>",
                    unsafe_allow_html=True
                )

            st.divider()

            # ANALYSIS
            col_a, col_b = st.columns(2)

            with col_a:

                st.markdown(
                    "<div class='report-card'><h4>🔍 Risk Factor Analysis</h4>",
                    unsafe_allow_html=True
                )

                if level == 'High':

                    st.write(
                        "• Profile falls within the Critical Attrition Window (3-5 years)."
                    )

                    st.write(
                        "• Grade-specific volatility detected for current role."
                    )

                    st.write(
                        "• Distance/Tenure ratio suggests immediate engagement risk."
                    )

                elif level == 'Medium':

                    st.write("• Mid-tenure engagement dip detected.")

                    st.write(
                        "• Potential career growth stagnation flagged by the model."
                    )

                else:

                    st.write("• High organizational anchoring.")

                    st.write("• Stable tenure-to-age ratio.")

                st.markdown("</div>", unsafe_allow_html=True)

            with col_b:

                st.markdown(
                    f"<div class='report-card' style='border-left-color: {h_color};'><h4>🚀 Mitigation Actionables</h4>",
                    unsafe_allow_html=True
                )

                if level == 'High':

                    st.write(
                        "• ER Physical Intervention: Urgent 1:1 visit required."
                    )

                    st.write(
                        "• Emergency Career Pathing: Explore immediate internal mobility."
                    )

                    st.write(
                        "• Relationship Reset: Senior-level mentorship pairing."
                    )

                elif level == 'Medium':

                    st.write(
                        "• Structured Connect: ER Manager confidential 1:1."
                    )

                    st.write(
                        "• OJP Allocation: Assign a new project to re-energize."
                    )

                else:

                    st.write(
                        "• Appreciation: Nominate for 'Star Performer' award."
                    )

                    st.write(
                        "• Growth Talk: Bi-annual career roadmap discussion."
                    )

                st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.error("EMPID not found in Active Database.")
