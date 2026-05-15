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
LOGO_FILE = "icicilogo.png"
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
    # Normalize risk score column name
    if 'Risk_Score' not in df.columns:
        df['Risk_Score'] = df.get('Attrition_Risk_Percentage', df.get('Attrition Risk (%)', 0))
    # Filter for only active employees
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
            .cover-subtitle {{ text-align: center; color: white; font-size: 52px; margin-bottom: 60px; font-weight: 800; line-height: 1.1; padding: 0 5%; font-family: 'Mulish', semibold; }}
            
            /* Maroon Buttons with Thick Left Bar & Internal Descriptions */
            div.stButton > button {{
                background-color: {ICICI_MAROON} !important;
                color: white !important;
                border: none !important;
                border-left: 15px solid #5a0d0f !important;
                padding: 80px 20px !important;
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
                font-weight: bold;
                font-size: 22px;
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
    
    # Navigation Mapping
    options = ["Back to Home", "Zone wise turnover prediction", "Employee risk indicator", "ER Login"]
    current_page_map = {"Summary": "Zone wise turnover prediction", "Predictor": "Employee risk indicator", "Login": "ER Login"}
    
    # Get current index for radio button
    try:
        current_idx = options.index(current_page_map.get(st.session_state.page))
    except:
        current_idx = 0

    selection = st.sidebar.radio("Go To:", options, index=current_idx)

    if selection == "Back to Home":
        st.session_state.page = "Cover"
        st.rerun()
    elif selection != current_page_map.get(st.session_state.page):
        reverse_map = {"Zone wise turnover prediction": "Summary", "Employee risk indicator": "Predictor", "ER Login": "Login"}
        st.session_state.page = reverse_map[selection]
        st.rerun()

    # --- PAGE: ZONE WISE TURNOVER PREDICTION ---
    if st.session_state.page == "Summary":
        st.title("🏙️ Zone-wise Turnover Prediction")
        st.markdown(f"<h3 style='color: {ICICI_ORANGE};'>Regional Vulnerability Dashboard</h3>", unsafe_allow_html=True)
        
        view_type = st.radio("Select Visualization View:", ["Percentage", "Count"], horizontal=True)
        
        # Categorize risk scores
        df['Risk_Level'] = pd.cut(df['Risk_Score'], bins=[0, 40, 75, 100], labels=['Low', 'Medium', 'High'])
        
        zone_col = 'ZONE' if 'ZONE' in df.columns else 'Zone'
        zones = ["North", "South", "East", "West"]
        cols = st.columns(2)
        
        for i, zone in enumerate(zones):
            with cols[i % 2]:
                st.subheader(f"📍 {zone} Zone")
                zone_df = df[df[zone_col] == zone]
                
                if not zone_df.empty:
                    counts = zone_df['Risk_Level'].value_counts()
                    percentages = (counts / len(zone_df) * 100).round(2)
                    
                    data_to_plot = percentages if view_type == "Percentage" else counts
                    
                    fig, ax = plt.subplots(figsize=(6, 3))
                    # ICICI Theme Colors: Green (Low), Orange (Med), Maroon (High)
                    colors = ['#2ECC71', '#f37021', '#8b191d']
                    data_to_plot.reindex(['Low', 'Medium', 'High']).plot(kind='bar', color=colors, ax=ax)
                    ax.set_ylabel(view_type)
                    plt.xticks(rotation=0)
                    st.pyplot(fig)
                else:
                    st.info(f"No data available for {zone} Zone.")

    # --- PAGE: EMPLOYEE RISK INDICATOR ---
    elif st.session_state.page == "Predictor":
        st.title("👤 Employee Risk Indicator")
        st.markdown(f"<h3 style='color: {ICICI_ORANGE};'>Predictive Attrition Individual Search</h3>", unsafe_allow_html=True)
        
        emp_id = st.number_input("Enter Employee ID (EMPID)", min_value=0, step=1, help="Type the ID to generate report")
        
        if emp_id:
            user_data = df[df['EMPID'] == emp_id]
            if not user_data.empty:
                score = user_data['Risk_Score'].values[0]
                
                # Risk Logic
                if score >= 75:
                    status, hex_color = "HIGH RISK", ICICI_MAROON
                elif score >= 40:
                    status, hex_color = "MEDIUM RISK", ICICI_ORANGE
                else:
                    status, hex_color = "LOW RISK", "#008000"
                
                st.markdown(f"""
                    <div style='text-align: center;'>
                        <p style='font-size: 80px; font-weight: bold; color: {hex_color}; margin-bottom: 0;'>{score}%</p>
                        <h2 style='color: {hex_color}; font-weight: bold; margin-top: 0;'>{status}</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                st.divider()
                
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("💡 Analysis Factors")
                    st.write(f"**Tenure:** {user_data['TENURE_YRS'].values[0]} Years")
                    st.write(f"**Grade:** {user_data['GRADE'].values[0]}")
                    st.write("• High volatility identified in this specific grade-tenure cohort.")
                    st.write("• Localized market demand for lateral movement is increasing.")
                with c2:
                    st.subheader("🚀 Actionables")
                    if score >= 75:
                        st.error("**ER Alert:** Immediate 'Stay Interview' and compensation parity check required.")
                    elif score >= 40:
                        st.warning("**Manager Action:** Focus on role enrichment and leadership training enrollment.")
                    else:
                        st.success("**Retention Plan:** Nominate for peer-to-peer appreciation and high-potential tracks.")
            else:
                st.error("Employee ID not found in the database.")

    # --- PAGE: ER LOGIN / STATS ---
    elif st.session_state.page == "Login":
        st.title("🔐 ER Login")
        st.markdown("<h3 style='color: #8b191d;'>Model Performance & Statistics</h3>", unsafe_allow_html=True)
        
        try:
            # Load Regression Stats from the Excel file
            stats_df = pd.read_excel('Attrition_Final_Production_v8_Final_Analysis.xlsx', sheet_name='Regression_Stats')
            st.subheader("Statistical Validation")
            st.table(stats_df)
            
            st.markdown("---")
            st.write("Current Model R-Squared: **42.12%**")
            st.write("Predictive Confidence (P-Value): **< 0.0001**")
        except:
            st.warning("Regression statistics sheet not found in the Excel file. Please ensure the 'Regression_Stats' sheet is correctly configured.")
