import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(page_title="iRetain | Workforce Analytics", layout="wide")

# --- 2. REFINED PROFESSIONAL UI CSS ---
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; color: #333333; }
    [data-testid="stSidebar"] { background-color: #f37021; }
    [data-testid="stSidebar"] .st-emotion-cache-10trblm { color: white; }
    
    /* Centered Main Title */
    .centered-title {
        text-align: center;
        color: #003366;
        font-family: 'Segoe UI', Arial;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Section Headers */
    .section-header {
        color: #f37021;
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 10px;
    }

    /* Metric Boxes - Orange with White Text */
    .metric-container {
        background-color: #f37021;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        color: white;
    }
    .metric-value { font-size: 26px; font-weight: bold; color: white; }
    .metric-label { font-size: 14px; color: white; }

    /* Quadrant Box Styling */
    .quadrant-box {
        background-color: #FFFFFF;
        padding: 0px;
        border-radius: 8px;
        border: 1px solid #EEEEEE;
        margin-bottom: 10px;
        overflow: hidden;
    }

    /* Orange Zone Header */
    .zone-header {
        background-color: #f37021;
        color: white;
        padding: 8px;
        font-size: 22px;
        font-weight: bold;
        text-align: center;
    }

    /* Professional Risk Indicator Styles */
    .risk-box { padding: 30px; border-radius: 20px; text-align: center; border: 2px solid; background: #FAFAFA; margin-bottom: 25px; }
    .big-font { font-size: 70px !important; font-weight: bold; }
    .report-card { background: #FFFFFF; padding: 25px; border-radius: 15px; border-left: 5px solid #f37021; border-top: 1px solid #EEE; border-right: 1px solid #EEE; border-bottom: 1px solid #EEE; margin-bottom: 20px; min-height: 200px; }

    /* Global Button Styling */
    div.stButton > button {
        background-color: #f37021 !important;
        color: white !important;
        border-radius: 4px;
        border: none;
        width: 100%;
    }
    
    /* Small buttons for Numbers/Percentage */
    .small-btn div.stButton > button {
        padding: 2px 5px !important;
        font-size: 12px !important;
        height: 32px !important;
    }

    /* Large buttons for Risk Filters */
    .large-btn div.stButton > button {
        padding: 15px 10px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        height: 60px !important;
    }
    
    .chart-container { padding: 5px; }
    hr { margin-top: 10px !important; margin-bottom: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOADING & LOGIC ---
@st.cache_data
def load_data():
    file_path = 'Attrition.csv'
    if not os.path.exists(file_path):
        st.error("⚠️ File Not Found: Attrition.csv")
        st.stop()
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    return df

def get_insights(row):
    """Generate dynamic reasons and actionables for the detail page."""
    level = row.get('Risk_Level', 'Low')
    reasons, actions = [], []
    if level == 'High':
        reasons = ["Profile falls within Critical Attrition Window (3-5 years).", "Distance/Tenure ratio suggests immediate risk."]
        actions = ["**ER Intervention:** Urgent 1:1 visit required.", "**Relationship Reset:** Senior-level mentorship pairing."]
    elif level == 'Medium':
        reasons = ["Mid-tenure engagement dip detected.", "Potential career growth stagnation flagged."]
        actions = ["**Structured Connect:** ER Manager confidential 1:1.", "**OJP Allocation:** Re-energize with new project."]
    else:
        reasons = ["Stable organizational anchoring.", "High tenure-to-age ratio."]
        actions = ["**Appreciation:** Nominate for 'Star Performer'.", "**Growth Talk:** Bi-annual career roadmap."]
    return reasons, actions

df = load_data()

# --- 4.
