import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- iRetain THEME CONFIG ---
st.set_page_config(page_title="iRetain | ICICI Bank", layout="wide", initial_sidebar_state="collapsed")

# ICICI Colors
ICICI_ORANGE = "#f37021"
ICICI_MAROON = "#8b191d"

# Custom CSS for Professional Corporate Look
st.markdown(f"""
    <style>
    /* Background and Font */
    .stApp {{ background-color: {ICICI_ORANGE}; }}
    .main {{ color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    
    /* Header Branding */
    .header-container {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; }}
    .slogan {{ color: white; font-size: 18px; font-weight: 500; }}
    
    /* Cover Page Typography */
    .cover-title {{ text-align: center; color: white; font-size: 85px; font-weight: 800; margin-top: 50px; letter-spacing: -2px; }}
    .cover-subtitle {{ text-align: center; color: white; font-size: 24px; margin-bottom: 60px; font-weight: 400; opacity: 0.9; }}
    
    /* Maroon Tabs */
    .tab-card {{
        background-color: {ICICI_MAROON};
        padding: 35px 25px;
        border-radius: 12px;
        text-align: center;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        cursor: pointer;
    }}
    .tab-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 12px rgba(0,0,0,0.2); }}
    .tab-title {{ color: white; font-size: 22px; font-weight: 700; margin-bottom: 10px; }}
    .tab-desc {{ color: #FFDAD9; font-size: 15px; font-weight: 400; line-height: 1.4; }}
    
    /* Clean UI for Module Pages */
    .module-bg {{ background-color: #f4f4f4; color: #333; padding: 20px; border-radius: 10px; }}
    .stMetric {{ background-color: white; border: 1px solid #ddd; border-radius: 8px; box-shadow: none; }}
    
    /* Hide sidebar on Cover Page */
    [data-testid="collapsedControl"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADER ---
@st.cache_data
def load_data():
    file_path = 'Attrition_Final_Production_v8_Final_Analysis.xlsx'
    if not os.path.exists(file_path):
        st.error(f"File '{file_path}' not found.")
        st.stop()
    df = pd.read_excel(file_path, sheet_name=0)
    df.columns = df.columns.str.strip()
    return df[df['Status'].str.upper() == 'ACTIVE'].copy()

df = load_data()

# --- NAVIGATION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "Cover"

# --- HEADER SECTION ---
st.markdown(f"""
    <div class="header-container">
        <img src="https://www.icicibank.com/assets/images/logo.png" width="180">
        <div class="slogan">Predict. Prevent. Retain</div>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE ROUTING ---

# 1. COVER PAGE
if st.session_state.page == "Cover":
    st.markdown("<h1 class='cover-title'>iRetain</h1>", unsafe_allow_html=True)
    st.markdown("<p class='cover-subtitle'>The Intelligent Workforce Turnover Risk Analyzer</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""<div class='tab-card'><div class='tab-title'>Zone-wise Risk Summary</div>
                    <div class='tab-desc'>An overview of Turnover Risk across 4 zones</div></div>""", unsafe_allow_html=True)
        if st.button("Open Summary", key="btn1", use_container_width=True):
            st.session_state.page = "Summary"
            st.rerun()

    with col2:
        st.markdown(f"""<div class='tab-card'><div class='tab-title'>Employee Risk Predictor</div>
                    <div class='tab-desc'>Identify Risk. Improve Retention</div></div>""", unsafe_allow_html=True)
        if st.button("Open Predictor", key="btn2", use_container_width=True):
            st.session_state.page = "Predictor"
            st.rerun()

    with col3:
        st.markdown(f"""<div class='tab-card'><div class='tab-title'>ER Login</div>
                    <div class='tab-desc'>Monitor turnover risk in your portfolio.</div></div>""", unsafe_allow_html=True)
        if st.button("Login", key="btn3", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

# 2. ZONE-WISE SUMMARY
elif st.session_state.page == "Summary":
    if st.button("← Back to Home"): st.session_state.page = "Cover"; st.rerun()
    st.markdown("<h2 style='color:white;'>Zone-wise Risk Summary</h2>", unsafe_allow_html=True)
    
    # Simple clean bar charts
    zones = ["Uttar Pradesh", "Maharashtra", "West Bengal", "Gujarat"]
    cols = st.columns(2)
    for i, zone in enumerate(zones):
        with cols[i%2]:
            st.markdown(f"<div style='background:white; padding:15px; border-radius:10px; margin-bottom:10px; color:black;'><h3>📍 {zone}</h3>", unsafe_allow_html=True)
            zone_df = df[df['Home State'] == zone]
            counts = zone_df['Risk_Level'].value_counts(normalize=True) * 100
            
            fig, ax = plt.subplots(figsize=(6, 2.5))
            ax.bar(['High', 'Medium', 'Low'], [counts.get('High', 0), counts.get('Medium', 0), counts.get('Low', 0)], color=['#8b191d', '#f37021', '#2ECC71'])
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

# 3. EMPLOYEE RISK PREDICTOR
elif st.session_state.page == "Predictor":
    if st.button("← Back to Home"): st.session_state.page = "Cover"; st.rerun()
    st.markdown("<h2 style='color:white;'>Employee Risk Predictor</h2>", unsafe_allow_html=True)
    
    emp_id = st.number_input("Enter EMPID", min_value=0, step=1)
    if emp_id:
        user_data = df[df['EMPID'] == emp_id]
        if not user_data.empty:
            row = user_data.iloc[0]
            score = row['Attrition_Risk_Percentage']
            level = row['Risk_Level']
            
            st.markdown(f"""
                <div style='background:white; padding:30px; border-radius:15px; color:black; text-align:center;'>
                    <h1 style='color:{ICICI_MAROON if level=="High" else ICICI_ORANGE}; font-size:60px;'>{score}%</h1>
                    <h2>{level.upper()} RISK</h2>
                    <p>Grade: {row['GRADE']} | Tenure: {row['TENURE_YRS']} Yrs</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Employee not found.")

# 4. ER LOGIN (APPENDIX/STATS)
elif st.session_state.page == "Login":
    if st.button("← Back to Home"): st.session_state.page = "Cover"; st.rerun()
    st.markdown("<h2 style='color:white;'>ER Login | Model Statistics</h2>", unsafe_allow_html=True)
    
    st.markdown("<div style='background:white; padding:20px; border-radius:10px; color:black;'>", unsafe_allow_html=True)
    try:
        stats_df = pd.read_excel('Attrition_Final_Production_v5_Corrected.xlsx', sheet_name='Regression_Stats')
        st.table(stats_df)
        st.write("**Model Accuracy (R-Squared):** 42.12%")
        st.write("**Statistical P-Value:** 0.0000234")
    except:
        st.warning("Stats sheet not found.")
    st.markdown("</div>", unsafe_allow_html=True)
