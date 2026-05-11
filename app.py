import streamlit as st
import pd as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- iRetain CONFIG ---
st.set_page_config(page_title="iRetain | ICICI Bank", layout="wide", initial_sidebar_state="collapsed")

# Official Colors
ICICI_ORANGE = "#f37021"
ICICI_MAROON = "#8b191d"
ICICI_BLUE = "#003366"

# --- LOGO LOGIC ---
LOGO_FILE = "icicibanklogo.png"
LOGO_PATH = LOGO_FILE if os.path.exists(LOGO_FILE) else "https://www.icicibank.com/assets/images/logo.png"

# --- DATA LOADER ---
@st.cache_data
def load_data():
    file_path = 'Attrition_Final_Production_v8_Final_Analysis.xlsx'
    if not os.path.exists(file_path):
        st.error(f"Critical Error: Data file '{file_path}' not found on GitHub.")
        st.stop()
    df = pd.read_excel(file_path, sheet_name=0)
    df.columns = df.columns.str.strip()
    if 'Risk_Score' not in df.columns:
        df['Risk_Score'] = df.get('Attrition_Risk_Percentage', df.get('Attrition Risk (%)', 0))
    return df[df['Status'].str.upper() == 'ACTIVE'].copy()

df = load_data()

if 'page' not in st.session_state:
    st.session_state.page = "Cover"

# --- CSS FOR UI STYLING ---
if st.session_state.page == "Cover":
    st.markdown(f"""
        <style>
            [data-testid="stSidebar"] {{display: none;}}
            [data-testid="collapsedControl"] {{display: none;}}
            .stApp {{ background-color: white !important; }}
            
            /* iRetain Title - Size 120 */
            .cover-title {{ text-align: center; color: {ICICI_BLUE}; font-size: 120px; font-weight: 900; margin-top: 10px; letter-spacing: -3px; line-height: 1.1; font-family: 'Trebuchet MS', sans-serif; }}
            
            /* Subtitle - Size 72 */
            .cover-subtitle {{ text-align: center; color: {ICICI_ORANGE}; font-size: 72px; margin-bottom: 60px; font-weight: 800; line-height: 1.1; padding: 0 5%; font-family: 'Arial', sans-serif; }}
            
            /* Box Title Styling - Georgia Semi-Bold */
            .box-title {{ font-family: 'Georgia', serif; font-weight: 600; font-size: 26px; margin-bottom: 10px; }}
            
            div.stButton > button {{
                background-color: {ICICI_MAROON} !important;
                color: white !important;
                border: none !important;
                padding: 40px 20px !important;
                border-radius: 15px !important;
                height: 320px !important;
                width: 100% !important;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1) !important;
                transition: all 0.3s ease !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
            }}
            div.stButton > button:hover {{
                transform: translateY(-10px) !important;
                box-shadow: 0 15px 30px rgba(0,0,0,0.2) !important;
            }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""<style>.stApp { background-color: white !important; color: black; }</style>""", unsafe_allow_html=True)

# --- PAGE ROUTING ---

# 1. COVER PAGE
if st.session_state.page == "Cover":
    # Header with Logo and Bold Slogan
    col_logo, col_slogan = st.columns([1, 1])
    with col_logo:
        st.image(LOGO_PATH, width=300)
    with col_slogan:
        st.markdown(f"<div style='text-align: right; color: {ICICI_ORANGE}; font-size: 26px; font-weight: 900; margin-top: 25px;'><b>Predict. Prevent. Retain</b></div>", unsafe_allow_html=True)

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
    st.sidebar.image(LOGO_PATH, width=200)
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
        st.markdown(f"<h3 style='color: {ICICI_ORANGE};'>Regional Vulnerability Dashboard</h3>", unsafe_allow_html=True)
        
        df['Is_High_Risk'] = df['Risk_Score'] >= 75
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
                    st.info(f"No data available for {zone} Zone.")

    # --- PAGE 2: EMPLOYEE RISK INDICATOR ---
    elif st.session_state.page == "Employee risk indicator":
        st.title("👤 Employee Risk Indicator")
        st.markdown(f"<h3 style='color: {ICICI_ORANGE};'>Predictive Attrition Individual Search</h3>", unsafe_allow_html=True)
        
        emp_id = st.number_input("Enter Employee ID", min_value=0, step=1)
        
        if emp_id:
            user_data = df[df['EMPID'] == emp_id]
            if not user_data.empty:
                score = user_data['Risk_Score'].values[0]
                hex_color = ICICI_MAROON if score >= 75 else (ICICI_ORANGE if score >= 40 else "#008000")
                status = "HIGH RISK" if score >= 75 else ("MEDIUM RISK" if score >= 40 else "LOW RISK")
                
                st.markdown(f"<div style='text-align: center;'><p style='font-size: 80px; font-weight: bold; color: {hex_color}; margin-bottom: 0;'>{score}%</p><h2 style='color: {hex_color}; font-weight: bold; margin-top: 0;'>{status}</h2></div>", unsafe_allow_html=True)
                st.divider()
                
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("💡 Analysis Factors")
                    st.write(f"**Tenure:** {user_data['TENURE_YRS'].values[0]} Years | **Grade:** {user_data['GRADE'].values[0]}")
                with c2:
                    st.subheader("🚀 Actionables")
                    if score >= 75: st.warning("ER Intervention Required: Immediate 'Stay Interview' recommended.")
                    elif score >= 40: st.info("Engagement Focus: Career growth discussion recommended.")
                    else: st.success("Recognition: Nominate for peer-to-peer appreciation.")
            else:
                st.error("Employee ID not found.")

    # --- PAGE 3: ER LOGIN ---
    elif st.session_state.page == "ER Login":
        st.title("🔐 ER Login")
        try:
            stats_df = pd.read_excel('Attrition_Final_Production_v8_Final_Analysis.xlsx', sheet_name='Regression_Stats')
            st.table(stats_df)
            st.write(f"Target R-Squared: **42.12%** | P-Value: **0.0000234**")
        except:
            st.warning("Stats sheet not found.")
