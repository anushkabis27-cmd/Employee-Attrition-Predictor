import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- iRetain CONFIG ---
st.set_page_config(page_title="iRetain | ICICI Bank", layout="wide", initial_sidebar_state="collapsed")

# Professional Color Palette
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
        st.error(f"Critical Error: Data file '{file_path}' not found.")
        st.stop()
    df = pd.read_excel(file_path, sheet_name=0)
    df.columns = df.columns.str.strip()
    if 'Risk_Score' not in df.columns:
        df['Risk_Score'] = df.get('Attrition_Risk_Percentage', df.get('Attrition Risk (%)', 0))
    return df[df['Status'].str.upper() == 'ACTIVE'].copy()

df = load_data()

if 'page' not in st.session_state:
    st.session_state.page = "Cover"

# --- CSS FOR GLOSSY COVER & ACCENTED TABS ---
if st.session_state.page == "Cover":
    st.markdown(f"""
        <style>
            [data-testid="stSidebar"] {{display: none;}}
            [data-testid="collapsedControl"] {{display: none;}}
            
            /* Glossy Diagonal Background */
            .stApp {{
                background: linear-gradient(135deg, {ICICI_ORANGE} 0%, #ff8c42 50%, {ICICI_ORANGE} 100%) !important;
                background-size: cover;
            }}
            
            /* iRetain Title - Bold White */
            .cover-title {{ text-align: center; color: white; font-size: 130px; font-weight: 900; margin-top: 10px; letter-spacing: -3px; line-height: 1.1; font-family: 'Trebuchet MS', sans-serif; }}
            
            /* Subtitle - Bold White */
            .cover-subtitle {{ text-align: center; color: white; font-size: 52px; margin-bottom: 60px; font-weight: 800; line-height: 1.1; padding: 0 5%; font-family: 'Arial', sans-serif; }}
            
            /* Maroon Buttons with Thick Left Bar & Internal Descriptions */
            div.stButton > button {{
                background-color: {ICICI_MAROON} !important;
                color: white !important;
                border: none !important;
                border-left: 15px solid #5a0d0f !important;
                padding: 40px 20px !important;
                border-radius: 4px 15px 15px 4px !important;
                height: 350px !important;
                width: 100% !important;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2) !important;
                transition: all 0.3s ease !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                font-family: 'Georgia', serif;
            }}
            div.stButton > button:hover {{
                transform: translateY(-10px) !important;
                box-shadow: 0 15px 30px rgba(0,0,0,0.3) !important;
                filter: brightness(1.1);
            }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""<style>.stApp { background-color: white !important; color: black; }</style>""", unsafe_allow_html=True)

# --- PAGE ROUTING ---

# 1. COVER PAGE
if st.session_state.page == "Cover":
    col_logo, col_slogan = st.columns([1, 1])
    with col_logo:
        st.image(LOGO_PATH, width=300)
    with col_slogan:
        st.markdown(f"<div style='text-align: right; color: white; font-size: 26px; font-weight: 900; margin-top: 25px;'><b>Predict. Prevent. Retain</b></div>", unsafe_allow_html=True)

    st.markdown("<h1 class='cover-title'>iRetain</h1>", unsafe_allow_html=True)
    st.markdown("<p class='cover-subtitle'><b>The Intelligent Workforce Turnover Risk Analyzer</b></p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("ZONE-WISE RISK SUMMARY\n\nAn overview of Turnover Risk across 4 zones"):
            st.session_state.page = "Summary"
            st.rerun()
    with c2:
        if st.button("EMPLOYEE RISK PREDICTOR\n\nIdentify Risk. Improve Retention"):
            st.session_state.page = "Predictor"
            st.rerun()
    with c3:
        if st.button("ER LOGIN\n\nMonitor turnover risk in your portfolio"):
            st.session_state.page = "Login"
            st.rerun()

# 2. INTERNAL MODULE PAGES
else:
    st.sidebar.image(LOGO_PATH, width=200)
    st.sidebar.title("Navigation")
    # ... Rest of your internal logic for charts and predictors follows here ...
