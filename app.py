import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. CONFIGURATION ---
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

    /* Section Header - Black */
    .section-header {
        color: #000000;
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 15px;
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
        padding: 10px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }

    /* Global Button Styling */
    div.stButton > button {
        background-color: #f37021 !important;
        color: white !important;
        border-radius: 4px;
        border: none;
        width: 100%;
        font-weight: 600;
    }
    
    /* Large buttons for Risk Filters */
    .large-btn-container div.stButton > button {
        padding: 15px 10px !important;
        font-size: 18px !important;
        height: 60px !important;
    }

    /* Small buttons for Numbers/Percentage */
    .small-btn-container div.stButton > button {
        padding: 5px !important;
        font-size: 13px !important;
        height: auto !important;
        margin-bottom: 8px;
    }
    
    .chart-container { padding: 5px; }
    hr { margin-top: 10px !important; margin-bottom: 10px !important; }
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

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.title("💠 iRETAIN")
st.sidebar.markdown("---")
page_options = ["Zone wise turnover prediction", "Employee risk indicator", "ER Login"]
selected_sidebar = st.sidebar.radio("NAVIGATION", page_options, 
                                    index=page_options.index(st.session_state['current_page']))

if selected_sidebar != st.session_state['current_page']:
    st.session_state['current_page'] = selected_sidebar
    st.session_state['selected_empid'] = None

# --- PAGE 1: ZONE WISE RISK SUMMARY ---
if st.session_state['current_page'] == "Zone wise turnover prediction":
    st.markdown("<h1 class='centered-title'>Zone-Wise Risk Summary</h1>", unsafe_allow_html=True)
    
    col_content, col_legend = st.columns([4, 1.2])

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
        st.write(f"#### Group wise - Risk: {st.session_state['risk_filter']} Level")
        
        color_map = {'High': '#D7191C', 'Medium': '#FFCC00', 'Low': '#28A745'}
        current_color = color_map[st.session_state['risk_filter']]

        zones = ['North', 'South', 'East', 'West']
        row1 = st.columns(2)
        row2 = st.columns(2)
        all_cols = row1 + row2

        for i, zone in enumerate(zones):
            with all_cols[i]:
                st.markdown(f"<div class='quadrant-box'><div class='zone-header'>{zone}</div><div class='chart-container'>", unsafe_allow_html=True)
                
                zone_data = df[(df['ZONE'].str.capitalize() == zone) & (df['Risk_Level'] == st.session_state['risk_filter'])]
                if not zone_data.empty:
                    counts = zone_data['MAIN_GROUP'].value_counts()
                    total_in_dept = df[df['ZONE'].str.capitalize() == zone]['MAIN_GROUP'].value_counts()
                    percentages = (counts / total_in_dept * 100).fillna(0)

                    fig, ax = plt.subplots(figsize=(5, 3))
                    bars = ax.bar(counts.index, counts.values, color=current_color)
                    max_v = max(counts.values) if not counts.empty else 10
                    ax.set_ylim(0, max_v * 1.35) 

                    for bar, label_val in zip(bars, percentages.values if st.session_state['view_mode'] == 'Percentage' else counts.values):
                        height = bar.get_height()
                        label = f"{label_val:.1f}%" if st.session_state['view_mode'] == 'Percentage' else f"{int(label_val)}"
                        ax.text(bar.get_x() + bar.get_width()/2., height + (max_v * 0.02), label, ha='center', va='bottom', fontsize=9, fontweight='bold')

                    ax.set_facecolor('#FFFFFF')
                    ax.tick_params(axis='x', rotation=45, labelsize=8)
                    ax.set_ylabel("Count", fontsize=9)
                    ax.set_xlabel("")
                    st.pyplot(fig)
                else:
                    st.write("No data found for this selection.")
                st.markdown("</div></div>", unsafe_allow_html=True)

    with col_legend:
        # Risk Filters First
        st.write("**Risk View Filter**")
        st.markdown('<div class="large-btn-container">', unsafe_allow_html=True)
        if st.button("High Risk"): st.session_state['risk_filter'] = 'High'
        st.write("")
        if st.button("Medium Risk"): st.session_state['risk_filter'] = 'Medium'
        st.write("")
        if st.button("Low Risk"): st.session_state['risk_filter'] = 'Low'
        st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        # Numbers/Percentage Buttons Second
        st.markdown('<div class="small-btn-container">', unsafe_allow_html=True)
        if st.button("In Numbers"): st.session_state['view_mode'] = 'Numbers'
        if st.button("In Percentage"): st.session_state['view_mode'] = 'Percentage'
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2 & 3: Standard Placeholder Logic ---
elif st.session_state['current_page'] == "Employee risk indicator":
    st.title("Employee risk indicator")
    emp_input = st.number_input("Enter EMPID", min_value=0)
    if emp_input:
        res = df[df['EMPID'] == emp_input]
        if not res.empty:
            st.write(res.iloc[0])

elif st.session_state['current_page'] == "ER Login":
    st.title("ER Manager Portal")
    er_id = st.number_input("Enter ER Manager ID", min_value=0)
    if 'ER manager ID' in df.columns and er_id in df['ER manager ID'].values:
        st.success(f"Access granted for Manager {er_id}")
