import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="iRetain | Workforce Analytics", layout="wide")

# --- 2. CLEAN & PROFESSIONAL CSS ---
st.markdown("""
    <style>
    /* Clean white/light grey theme for readability */
    .main { background-color: #F8F9FA; color: #333333; }
    [data-testid="stSidebar"] { background-color: #f37021; }
    [data-testid="stSidebar"] .st-emotion-cache-10trblm { color: white; }
    
    /* Metrics Boxes - Clean, No Shadows */
    .metric-container {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        text-align: center;
    }
    .metric-value { font-size: 24px; font-weight: bold; color: #f37021; }
    .metric-label { font-size: 14px; color: #666666; margin-bottom: 5px; }

    /* Quadrant Boxes */
    .quadrant-box {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #DEE2E6;
        margin-bottom: 20px;
    }

    /* Headings - Professional, No Shadows */
    h1, h2, h3 { font-family: 'Segoe UI', Arial; color: #003366; text-shadow: none !important; }
    
    /* Buttons/Tabs Style */
    div.stButton > button {
        background-color: #f37021;
        color: white;
        border-radius: 4px;
        border: none;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LOADING ---
@st.cache_data
def load_data():
    file_path = 'Attrition.csv'
    if not os.path.exists(file_path):
        st.error("⚠️ File Not Found: Attrition.csv")
        st.stop()
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# --- 4. STATE MANAGEMENT ---
if 'view_mode' not in st.session_state: st.session_state['view_mode'] = 'Percentage'
if 'risk_filter' not in st.session_state: st.session_state['risk_filter'] = 'High'
if 'current_page' not in st.session_state: st.session_state['current_page'] = "Zone wise turnover prediction"
if 'selected_empid' not in st.session_state: st.session_state['selected_empid'] = None

# --- 5. SIDEBAR ---
st.sidebar.title("💠 iRETAIN")
page = st.sidebar.radio("NAVIGATION", ["Zone wise turnover prediction", "Employee risk indicator", "ER Login"])
st.session_state['current_page'] = page

# --- PAGE 1: ZONE WISE TURNOVER PREDICTION ---
if st.session_state['current_page'] == "Zone wise turnover prediction":
    st.title("Zone wise turnover prediction")
    
    # --- TOP METRICS ROW ---
    total_emp = len(df)
    high_risk_count = len(df[df['Risk_Level'] == 'High'])
    high_risk_pct = (high_risk_count / total_emp) * 100

    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f"<div class='metric-container'><div class='metric-label'>Total Employees</div><div class='metric-value'>{total_emp}</div></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='metric-container'><div class='metric-label'>High Risk Employees</div><div class='metric-value'>{high_risk_count}</div></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='metric-container'><div class='metric-label'>High Risk Percentage</div><div class='metric-value'>{high_risk_pct:.1f}%</div></div>", unsafe_allow_html=True)

    st.divider()

    # --- INTERACTIVE LEGEND & BUTTONS (Upper Right) ---
    col_main, col_legend = st.columns([4, 1])
    
    with col_legend:
        st.write("**Risk View Filter**")
        if st.button("🔴 High Risk"): st.session_state['risk_filter'] = 'High'
        if st.button("🟡 Medium Risk"): st.session_state['risk_filter'] = 'Medium'
        if st.button("🟢 Low Risk"): st.session_state['risk_filter'] = 'Low'
        
        st.write("**Data Type**")
        b1, b2 = st.columns(2)
        if b1.button("Numbers"): st.session_state['view_mode'] = 'Numbers'
        if b2.button("Percentage"): st.session_state['view_mode'] = 'Percentage'

    with col_main:
        st.subheader(f"Zone Analysis: {st.session_state['risk_filter']} Risk ({st.session_state['view_mode']})")
        
        # Color Mapping
        color_map = {'High': '#FF4B4B', 'Medium': '#FFD700', 'Low': '#28A745'}
        current_color = color_map[st.session_state['risk_filter']]

        # Define 4 Zones
        zones = ['North', 'South', 'East', 'West']
        q1, q2 = st.columns(2)
        q3, q4 = st.columns(2)
        quads = [q1, q2, q3, q4]

        for i, zone in enumerate(zones):
            with quads[i]:
                st.markdown(f"<div class='quadrant-box'><b>📍 {zone} Zone</b>", unsafe_allow_html=True)
                
                # Filter data for the zone and specific risk level
                zone_df = df[(df['ZONE'].str.capitalize() == zone) & (df['Risk_Level'] == st.session_state['risk_filter'])]
                
                if not zone_df.empty:
                    # Group by Department (MAIN_GROUP)
                    dept_counts = zone_df['MAIN_GROUP'].value_counts()
                    
                    if st.session_state['view_mode'] == 'Percentage':
                        # Percentage relative to total employees in that zone's department
                        total_zone_dept = df[df['ZONE'].str.capitalize() == zone]['MAIN_GROUP'].value_counts()
                        dept_data = (dept_counts / total_zone_dept * 100).fillna(0)
                        ylabel = "% Risk"
                    else:
                        dept_data = dept_counts
                        ylabel = "Count"

                    # Plotting
                    fig, ax = plt.subplots(figsize=(5, 3))
                    dept_data.plot(kind='bar', ax=ax, color=current_color)
                    ax.set_ylabel(ylabel)
                    ax.tick_params(axis='x', rotation=45, labelsize=8)
                    st.pyplot(fig)
                else:
                    st.write("No data for this selection.")
                st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2 & 3 (Logic remains same as prior clean version) ---
elif st.session_state['current_page'] == "Employee risk indicator":
    st.title("Employee risk indicator")
    emp_id = st.number_input("Enter EMPID", min_value=0, step=1)
    if emp_id:
        user_data = df[df['EMPID'] == emp_id]
        if not user_data.empty:
            row = user_data.iloc[0]
            st.metric("Attrition Risk", f"{row['Attrition_Risk_Percentage']}%")
            st.write(f"**Level:** {row['Risk_Level']}")
        else:
            st.error("Employee not found.")

elif st.session_state['current_page'] == "ER Login":
    st.title("ER Manager Portal")
    er_id = st.number_input("ER Manager ID", min_value=0, step=1)
    if er_id in df['ER manager ID'].values:
        st.success(f"Dashboard loaded for Manager {er_id}")
