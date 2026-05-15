import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(page_title="iRetain | Workforce Analytics", layout="wide")

# --- 2. PROFESSIONAL CLEAN UI CSS ---
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; color: #333333; }
    [data-testid="stSidebar"] { background-color: #f37021; }
    
    .centered-title {
        text-align: center;
        color: #003366;
        font-family: 'Segoe UI', Arial;
        font-weight: bold;
        margin-bottom: 30px;
    }

    .section-header {
        color: #f37021;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }

    .metric-container {
        background-color: #FDFDFD;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        text-align: center;
    }
    .metric-value { font-size: 22px; font-weight: bold; color: #333333; }
    .metric-label { font-size: 13px; color: #666666; }

    /* Orange Rounded Border for Risk Filters */
    .filter-border {
        border: 2px solid #f37021;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        text-align: center;
    }

    .quadrant-box {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #EEEEEE;
        margin-bottom: 20px;
    }
    
    div.stButton > button {
        border-radius: 4px;
        font-weight: 500;
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

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.title("💠 iRETAIN")
page = st.sidebar.radio("NAVIGATION", ["Zone wise turnover prediction", "Employee risk indicator", "ER Login"])

# --- PAGE 1: ZONE WISE RISK SUMMARY ---
if page == "Zone wise turnover prediction":
    st.markdown("<h1 class='centered-title'>Zone-Wise Risk Summary</h1>", unsafe_allow_html=True)
    
    col_content, col_legend = st.columns([4, 1])

    with col_content:
        st.markdown("<div class='section-header'>High Risk Profiling</div>", unsafe_allow_html=True)
        
        total_emp = len(df)
        high_risk_count = len(df[df['Risk_Level'] == 'High'])
        high_risk_pct = (high_risk_count / total_emp) * 100

        m1, m2, m3 = st.columns(3)
        with m1: st.markdown(f"<div class='metric-container'><div class='metric-label'>Total Employees</div><div class='metric-value'>{total_emp}</div></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='metric-container'><div class='metric-label'>High Risk Employees</div><div class='metric-value'>{high_risk_count}</div></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='metric-container'><div class='metric-label'>High Risk Percentage</div><div class='metric-value'>{high_risk_pct:.1f}%</div></div>", unsafe_allow_html=True)

        st.divider()
        
        st.write(f"#### Departmental Risk: {st.session_state['risk_filter']} Level")
        
        color_map = {'High': '#D7191C', 'Medium': '#FDAE61', 'Low': '#1A9641'}
        current_color = color_map[st.session_state['risk_filter']]

        zones = ['North', 'South', 'East', 'West']
        rows = [st.columns(2), st.columns(2)]
        
        for i, zone in enumerate(zones):
            col_idx = i % 2
            row_idx = i // 2
            with rows[row_idx][col_idx]:
                st.markdown(f"<div class='quadrant-box'><b>📍 {zone} Zone</b>", unsafe_allow_html=True)
                
                # Filter for zone and selected risk level
                zone_data = df[(df['ZONE'].str.capitalize() == zone) & (df['Risk_Level'] == st.session_state['risk_filter'])]
                
                if not zone_data.empty:
                    # Logic: We always plot the numbers, but change the label based on view_mode
                    counts = zone_data['MAIN_GROUP'].value_counts()
                    total_in_dept = df[df['ZONE'].str.capitalize() == zone]['MAIN_GROUP'].value_counts()
                    percentages = (counts / total_in_dept * 100).fillna(0)

                    fig, ax = plt.subplots(figsize=(5, 3))
                    # The bar itself represents the count for stability
                    bars = ax.bar(counts.index, counts.values, color=current_color)
                    
                    # Add exact count or percentage over each bar
                    for bar, label_val in zip(bars, percentages.values if st.session_state['view_mode'] == 'Percentage' else counts.values):
                        height = bar.get_height()
                        label = f"{label_val:.1f}%" if st.session_state['view_mode'] == 'Percentage' else f"{int(label_val)}"
                        ax.text(bar.get_x() + bar.get_width()/2., height + (max(counts.values)*0.02),
                                label, ha='center', va='bottom', fontsize=8, fontweight='bold')

                    ax.set_ylabel("Count", fontsize=8)
                    ax.set_xlabel("") # Remove "Main group" title
                    ax.set_facecolor('#FFFFFF')
                    ax.tick_params(axis='x', rotation=45, labelsize=7)
                    st.pyplot(fig)
                else:
                    st.write("No entries found.")
                st.markdown("</div>", unsafe_allow_html=True)

    with col_legend:
        # Toggle Buttons (Top)
        if st.button("In Numbers"): st.session_state['view_mode'] = 'Numbers'
        if st.button("In Percentage"): st.session_state['view_mode'] = 'Percentage'
        
        st.write("") 

        # Risk Filter in Rounded Orange Border
        st.markdown('<div class="filter-border">', unsafe_allow_html=True)
        st.write("**Risk View Filter**")
        if st.button("High Risk"): st.session_state['risk_filter'] = 'High'
        if st.button("Medium Risk"): st.session_state['risk_filter'] = 'Medium'
        if st.button("Low Risk"): st.session_state['risk_filter'] = 'Low'
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGES 2 & 3: Standard Placeholder Logic ---
elif page == "Employee risk indicator":
    st.title("Employee risk indicator")
    emp_input = st.number_input("Enter EMPID", min_value=0)
    if emp_input:
        res = df[df['EMPID'] == emp_input]
        if not res.empty:
            st.write(res.iloc[0])

elif page == "ER Login":
    st.title("ER Manager Portal")
    er_id = st.number_input("Enter ER Manager ID", min_value=0)
    if er_id in df['ER manager ID'].values:
        st.success(f"Access granted for Manager {er_id}")
