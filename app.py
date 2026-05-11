import streamlit as st
import pandas as pd
import numpy as np
import os

# --- iRetain CONFIG ---
st.set_page_config(page_title="iRetain | ICICI Bank", layout="wide", initial_sidebar_state="collapsed")

# Official Colors
ICICI_ORANGE = "#F99D27"
ICICI_MAROON = "#8b191d"
Blue = "#004A7F"

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

# --- CSS FOR INVISIBLE SIDEBAR ON COVER ---
if 'page' not in st.session_state:
    st.session_state.page = "Cover"

if st.session_state.page == "Cover":
    hide_sidebar_style = """
        <style>
            [data-testid="stSidebar"] {display: none;}
            [data-testid="collapsedControl"] {display: none;}
            .stApp { background-color: #f37021 !important; }
        </style>
    """
   st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 40px;">
        <img src="icicibanklogo.png" width="240">  <div style="color: white; font-size: 24px; font-weight: 600; font-family: 'Georgia', serif;">Predict. Prevent. Retain</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Standard Sidebar styling for other pages
    st.sidebar.image("icicibanklogo.png", width=200) # Update this to your local filename
    st.sidebar.title("Navigation")

# --- NAVIGATION LOGIC ---

# 1. COVER PAGE
if st.session_state.page == "Cover":
    # Branding Header
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 40px;">
            <img src="https://www.icicibank.com/assets/images/logo.png" width="240">
            <div style="color: white; font-size: 24px; font-weight: 600; font-family: 'Georgia', serif;">Predict. Prevent. Retain</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color:#004A7F ; font-size: 80px; font-weight: 900; margin-top: 20px; font-family: Trebuchet MS;'>iRetain</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 38px; font-weight: 600; padding: 0 10%;'>The Intelligent Workforce Turnover Risk Analyzer</p>", unsafe_allow_html=True)
    
    # Custom CSS for Maroon Buttons/Cards
    st.markdown(f"""
        <style>
        div.stButton > button {{
            background-color: {ICICI_MAROON} !important;
            color: white !important;
            border: 2px solid rgba(255,255,255,0.2) !important;
            padding: 40px 20px !important;
            border-radius: 15px !important;
            height: 300px !important;
            width: 100% !important;
            font-family: 'Verdana', sans-serif !important;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3) !important;
        }}
        div.stButton > button:hover {{
            transform: translateY(-12px) !important;
            border: 2px solid white !important;
        }}
        </style>
    """, unsafe_allow_html=True)

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

# 2. INTERNAL PAGES WITH SIDEBAR
else:
    # Sidebar reappears automatically
    st.sidebar.image("https://www.icicibank.com/assets/images/logo.png", width=200)
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
        # [Insert your GroupBy logic here as provided in previous block]

    # --- PAGE 2: EMPLOYEE RISK INDICATOR ---
    elif st.session_state.page == "Employee risk indicator":
        st.title("👤 Employee Risk Indicator")
        # [Insert your Individual Search logic here as provided in previous block]
