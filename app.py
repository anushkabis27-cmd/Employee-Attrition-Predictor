import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- iRetain CONFIG ---
# This hides the sidebar by default and sets the corporate title
st.set_page_config(page_title="iRetain | ICICI Bank", layout="wide", initial_sidebar_state="collapsed")

# Official ICICI Colors
ICICI_ORANGE = "#f37021"
ICICI_MAROON = "#8b191d"

# --- DATA LOADER ---
@st.cache_data
def load_data():
    # Points to your specific V8 analysis file
    file_path = 'Attrition_Final_Production_v8_Final_Analysis.xlsx'
    if not os.path.exists(file_path):
        st.error(f"Critical Error: Data file '{file_path}' not found on GitHub.")
        st.stop()
    df = pd.read_excel(file_path, sheet_name=0)
    df.columns = df.columns.str.strip()
    
    # Ensure Risk_Score exists for Page 1 and Page 2 logic
    if 'Risk_Score' not in df.columns:
        df['Risk_Score'] = df.get('Attrition_Risk_Percentage', df.get('Attrition Risk (%)', 0))
    
    return df[df['Status'].str.upper() == 'ACTIVE'].copy()

df = load_data()

# --- INITIALIZE NAVIGATION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "Cover"

# --- CSS FOR UI STYLING & SIDEBAR SUPPRESSION ---
if st.session_state.page == "Cover":
    # Complete hide of sidebar and orange background for cover
    st.markdown(f"""
        <style>
            [data-testid="stSidebar"] {{display: none;}}
            [data-testid="collapsedControl"] {{display: none;}}
            .stApp {{ background-color: {ICICI_ORANGE} !important; }}
            .main {{ color: white; font-family: 'Segoe UI', sans-serif; }}
            
            /* Cover Typography */
            .cover-title {{ text-align: center; color: white; font-size: 130px; font-weight: 900; margin-top: 20px; letter-spacing: -3px; line-height: 1; font-family: 'Trebuchet MS', sans-serif; }}
            .cover-subtitle {{ text-align: center; color: white; font-size: 38px; margin-bottom: 70px; font-weight: 800; line-height: 1.2; padding: 0 10%; }}
            
            /* Interactive Maroon Cards */
            div.stButton > button {{
                background-color: {ICICI_MAROON} !important;
                color: white !important;
                border: 2px solid rgba(255,255,255,0.2) !important;
                padding: 40px 20px !important;
                border-radius: 15px !important;
                height: 300px !important;
                width: 100% !important;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3) !important;
                transition: all 0.3s ease !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                font-family: 'Verdana', sans-serif !important;
                font-weight: bold !important;
                font-size: 20px !important;
            }}
            div.stButton > button:hover {{
                transform: translateY(-12px) !important;
                box-shadow: 0 20px 40px rgba(0,0,0,0.5) !important;
                border: 2px solid white !important;
            }}
        </style>
    """, unsafe_allow_html=True)
else:
    # White background for module pages for better data readability
    st.markdown("""<style>.stApp { background-color: white !important; color: black; }</style>""", unsafe_allow_html=True)

# --- PAGE ROUTING ---

# 1. COVER PAGE
if st.session_state.page == "Cover":
    # Branding Header
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 40px;">
            <img src="icicibanklogo.png" width="240">
            <div style="color: white; font-size: 24px; font-weight: 600; font-family: 'Georgia', serif;">Predict. Prevent. Retain</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h1 class='cover-title'>iRetain</h1>", unsafe_allow_html=True)
    st.markdown("<p class='cover-subtitle'>The Intelligent Workforce Turnover Risk Analyzer</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("ZONE-WISE RISK SUMMARY\n\nAn overview of Turnover Risk across 4 zones"):
            st.session_state.page = "Zone wise turnover prediction"
            st.rerun()

    with col2:
        if st.button("EMPLOYEE RISK PREDICTOR\n\nIdentify Risk. Improve Retention"):
            st.session_state.page = "Employee risk indicator"
            st.rerun()

    with col3:
        if st.button("ER LOGIN\n\nMonitor turnover risk in your portfolio"):
            st.session_state.page = "ER Login"
            st.rerun()

# 2. INTERNAL MODULE PAGES
else:
    # Sidebar Navigation (reappears here)
    st.sidebar.image("icicibanklogo.png", width=200)
    st.sidebar.title("Navigation")
    
    options = ["Back to Home", "Zone wise turnover prediction", "Employee risk indicator", "ER Login"]
    current_index = options.index(st.session_state.page) if st.session_state.page in options else 1
    selection = st.sidebar.radio("Go To:", options, index=current_index)

    if selection == "Back to Home":
        st.session_state.page = "Cover"
        st.rerun()
    elif selection != st.session_state.page:
        st.session_state.page = selection
        st.rerun()

    # --- PAGE 1: ZONE WISE TURNOVER PREDICTION ---
    if st.session_state.page == "Zone wise turnover prediction":
        st.title("🏙️ Zone-wise Turnover Prediction")
        st.markdown("<h3 style='color: #f37021;'>Regional Vulnerability Dashboard</h3>", unsafe_allow_html=True)
        
        # High risk defined as 75%+
        df['Is_High_Risk'] = df['Risk_Score'] >= 75
        
        # Mapping columns based on v8 file structure
        zone_col = 'ZONE' if 'ZONE' in df.columns else 'Zone'
        group_col = 'MAIN_GROUP' if 'MAIN_GROUP' in df.columns else ('Grade' if 'Grade' in df.columns else 'GRADE')
        
        report = df.groupby([zone_col, group_col])['Is_High_Risk'].mean() * 100
        report = report.unstack().fillna(0).round(2)
        
        zones = ["North", "East", "West", "South"]
        cols = st.columns(2)
        
        for i, zone in enumerate(zones):
            with cols[i % 2]:
                st.subheader(f"📍 {zone} Zone")
                if zone in report.index:
                    st.dataframe(report.loc[zone].rename("High Risk %").to_frame().style.background_gradient(cmap='Oranges'))
                else:
                    st.info(f"No data currently available for {zone} Zone.")

    # --- PAGE 2: EMPLOYEE RISK INDICATOR ---
    elif st.session_state.page == "Employee risk indicator":
        st.title("👤 Employee Risk Indicator")
        st.markdown("<h3 style='color: #f37021;'>Predictive Attrition Individual Search</h3>", unsafe_allow_html=True)
        
        emp_id = st.number_input("Enter Employee ID", min_value=0, step=1, help="Type the EMPID to generate report")
        
        if emp_id:
            user_data = df[df['EMPID'] == emp_id]
            
            if not user_data.empty:
                score = user_data['Risk_Score'].values[0]
                
                if score >= 75:
                    status, hex_color = "HIGH RISK", "#8b191d" # Maroon
                elif score >= 40:
                    status, hex_color = "MEDIUM RISK", "#f37021" # Orange
                else:
                    status, hex_color = "LOW RISK", "#008000" # Green
                
                # Custom Styling for search results
                st.markdown(f"""
                    <div style='text-align: center;'>
                        <p style='font-size: 80px; font-weight: bold; color: {hex_color}; margin-bottom: 0;'>{score}%</p>
                        <h2 style='color: {hex_color}; font-weight: bold; margin-top: 0;'>{status}</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("💡 Analysis Factors")
                    st.write(f"**Current Tenure:** {user_data['TENURE_YRS'].values[0]} Years")
                    st.write(f"**Current Grade:** {user_data['GRADE'].values[0]}")
                    st.info("Model identifies specific volatility in this tenure-grade cohort based on historical lateral movement patterns.")

                with col2:
                    st.subheader("🚀 Actionables")
                    if score >= 75:
                        st.warning("**ER Intervention Required:** Immediate 'Stay Interview' and compensation review recommended.")
                    elif score >= 40:
                        st.info("**Engagement Focus:** Discussion on career growth and skill mapping recommended.")
                    else:
                        st.success("**Recognition:** Nominate for peer-to-peer appreciation and future leadership roles.")
            else:
                st.error("Employee ID not found in the active database.")

    # --- PAGE 3: ER LOGIN ---
    elif st.session_state.page == "ER Login":
        st.title("🔐 ER Login")
        st.markdown("<h3 style='color: #8b191d;'>Portfolio Risk Monitoring</h3>", unsafe_allow_html=True)
        
        st.info("Model Statistics for authorized ER Managers and Portfolio Monitoring.")
        try:
            stats_df = pd.read_excel('Attrition_Final_Production_v8_Final_Analysis.xlsx', sheet_name='Regression_Stats')
            st.subheader("Statistical Performance")
            st.table(stats_df)
            st.write("Target R-Squared: **42.12%**")
            st.write("Statistical Significance (P-Value): **0.0000234**")
        except:
            st.warning("Regression stats sheet not found in the data file.")
