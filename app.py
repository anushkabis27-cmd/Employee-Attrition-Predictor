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
    /* Main Background */
    .stApp {{ background-color: {ICICI_ORANGE}; }}
    .main {{ color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    
    /* Header Branding */
    .header-container {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; }}
    .slogan {{ color: white; font-size: 40px; font-weight: 700; font-family: 'Mulish', semibold; }}
    
    /* Cover Page Typography */
    .cover-title {{ text-align: center; color: white; font-size: 130px; font-weight: 900; margin-top: 20px; letter-spacing: -3px; line-height: 1; font-family: 'Mulish', semibold; }}
    .cover-subtitle {{ text-align: center; color: white; font-size: 48px; margin-bottom: 70px; font-weight: 800; line-height: 1.2; padding: 0 10%; }}
    
    /* Interactive Maroon Cards */
    div.stButton > button {{
        background-color: {ICICI_MAROON} !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        padding: 40px 20px !important;
        border-radius: 15px !important;
        height: 200px !important;
        width: 100% !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-12px) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5) !important;
        background-color: #a31d22 !important;
        border: 2px solid white !important;
    }}

    /* Stylish Card Text */
    .card-title {{ font-size: 38px !important; font-weight: 800 !important; font-family: 'Mulish', semibold !important; display: block; margin-bottom: 15px; text-transform: uppercase; }}
    .card-desc {{ font-size: 24px !important; font-weight: 600 !important; opacity: 0.95; display: block; line-height: 1.4; font-style: italic; }}
    
    /* Module UI Styling */
    .module-card {{ background: white; padding: 25px; border-radius: 15px; color: #333; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
    
    /* Hide default sidebar on Cover */
    [data-testid="collapsedControl"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADER ---
@st.cache_data
def load_data():
    file_path = 'Attrition_Final_Production_v8_Final_Analysis.xlsx'
    if not os.path.exists(file_path):
        st.error(f"Critical Error: Data file '{file_path}' not found on GitHub.")
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
        <img src="https://www.icicibank.com/assets/images/logo.png" width="240">
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
        # Styled Text inside Button Label
        label1 = "ZONE-WISE RISK SUMMARY\n\nAn overview of Turnover Risk across 4 Zones"
        if st.button(label1, key="nav_summary"):
            st.session_state.page = "Summary"
            st.rerun()

    with col2:
        label2 = "EMPLOYEE RISK PREDICTOR\n\nIdentify Risk. Improve Retention"
        if st.button(label2, key="nav_predictor"):
            st.session_state.page = "Predictor"
            st.rerun()

    with col3:
        label3 = "ER LOGIN\n\nMonitor turnover risk in your portfolio"
        if st.button(label3, key="nav_login"):
            st.session_state.page = "Login"
            st.rerun()

# 2. ZONE-WISE SUMMARY
elif st.session_state.page == "Summary":
    if st.button("← Back to Home Dashboard"): st.session_state.page = "Cover"; st.rerun()
    st.markdown("<h2 style='color:white; text-align:center;'>Zone-wise Risk Summary</h2>", unsafe_allow_html=True)
    
    zones = ["North", "South", "East", "West"]
    cols = st.columns(2)
    
    for i, zone in enumerate(zones):
        with cols[i % 2]:
            st.markdown(f"<div class='module-card'><h3>📍 {zone} Zone</h3>", unsafe_allow_html=True)
            zone_col = 'ZONE' if 'ZONE' in df.columns else 'Zone'
            zone_df = df[df[zone_col] == zone] if zone_col in df.columns else df.iloc[i*100:(i+1)*100]
            
            level_col = 'Risk_Level' if 'Risk_Level' in df.columns else 'Risk Level'
            counts = zone_df[level_col].value_counts(normalize=True) * 100
            
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(['High', 'Medium', 'Low'], 
                   [counts.get('High', 0), counts.get('Medium', 0), counts.get('Low', 0)], 
                   color=[ICICI_MAROON, ICICI_ORANGE, '#2ECC71'])
            ax.set_ylabel('Percentage (%)')
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

# 3. EMPLOYEE RISK PREDICTOR
elif st.session_state.page == "Predictor":
    if st.button("← Back to Home Dashboard"): st.session_state.page = "Cover"; st.rerun()
    st.markdown("<h2 style='color:white; text-align:center;'>Individual Employee Risk Predictor</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='module-card'>", unsafe_allow_html=True)
        emp_id = st.number_input("Enter Employee ID (EMPID)", min_value=0, step=1)
        
        if emp_id:
            user_data = df[df['EMPID'] == emp_id]
            if not user_data.empty:
                row = user_data.iloc[0]
                score = row.get('Attrition_Risk_Percentage', 0)
                level = row.get('Risk_Level', 'Low')
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"<h1 style='color:{ICICI_MAROON if level=='High' else ICICI_ORANGE}; font-size:80px; text-align:center;'>{score}%</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='text-align:center;'>{level.upper()} RISK</h3>", unsafe_allow_html=True)
                with c2:
                    st.write(f"**Grade:** {row.get('GRADE', 'N/A')}")
                    st.write(f"**Tenure:** {row.get('TENURE_YRS', 0)} Years")
                    st.write(f"**Age:** {row.get('AGE', 0)}")
                    st.write(f"**Work City:** {row.get('Work City', 'N/A')}")
            else:
                st.error("Employee ID not found in the active database.")
        st.markdown("</div>", unsafe_allow_html=True)

# 4. ER LOGIN (Appendix)
elif st.session_state.page == "Login":
    if st.button("← Back to Home Dashboard"): st.session_state.page = "Cover"; st.rerun()
    st.markdown("<h2 style='color:white; text-align:center;'>ER Login | Model Statistics</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='module-card'>", unsafe_allow_html=True)
    try:
        stats_df = pd.read_excel('Attrition_Final_Production_v8_Final_Analysis.xlsx', sheet_name='Regression_Stats')
        st.table(stats_df)
        st.markdown("---")
        st.write("Target R-Squared: **42.12%** | P-Value: **0.0000234**")
    except:
        st.warning("Stats sheet not found.")
    st.markdown("</div>", unsafe_allow_html=True)
