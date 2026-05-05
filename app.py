import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & ICICI Theming
st.set_page_config(page_title="ICICI Turnover Predictor", layout="wide")

ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"
RED = "#FF0000"
YELLOW = "#FFD700"
GREEN = "#008000"

# High-end CSS for professional look
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Roboto', sans-serif; }}
    [data-testid="stSidebar"] {{ background-color: #f8f9fa; border-right: 1px solid #ddd; }}
    .orange-header-box {{
        background-color: {ICICI_ORANGE}; color: white; padding: 6px 18px;
        border-radius: 20px; font-weight: 700; display: inline-block; margin-bottom: 15px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
    }}
    .stat-box {{ 
        background-color: white; border: 1px solid #e0e0e0; padding: 20px; 
        text-align: center; border-radius: 8px; box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }}
    .dashboard-title {{ color: {ICICI_NAVY}; font-weight: 700; border-left: 5px solid {ICICI_ORANGE}; padding-left: 15px; margin: 20px 0; }}
    /* Sidebar Button styling */
    div.stButton > button {{ border-radius: 4px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
    /* Legend Specific Colors */
    button[key="btn_high"] {{ background-color: {RED} !important; color: white !important; border: none; }}
    button[key="btn_med"] {{ background-color: {YELLOW} !important; color: #333 !important; border: none; }}
    button[key="btn_low"] {{ background-color: {GREEN} !important; color: white !important; border: none; }}
    </style>
""", unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    data = pd.read_excel("Attrition_Final_Production_v6_Corrected.xlsx")
    data['EMPID'] = data['EMPID'].astype(str).str.zfill(6)
    return data

df = load_data()

# 3. Sidebar Navigation
with st.sidebar:
    st.markdown(f"<h2 style='color:{ICICI_NAVY};'>ICICI Predictor</h2>", unsafe_allow_html=True)
    if st.button("ZONE WISE RISK SUMMARY", key="nav_overview", use_container_width=True):
        st.session_state.page = 'Overview'
    st.write("")
    if st.button("EMPLOYEE SEARCH", key="nav_search", use_container_width=True):
        st.session_state.page = 'Search'

# Init State
if 'page' not in st.session_state: st.session_state.page = 'Overview'
if 'risk_filter' not in st.session_state: st.session_state.risk_filter = 'High'
if 'view_mode' not in st.session_state: st.session_state.view_mode = 'In Numbers'

# --- PAGE 1: OVERVIEW ---
if st.session_state.page == 'Overview':
    st.title("Zone Wise Risk Summary")
    st.markdown('<div class="dashboard-title">High Risk Segment Details</div>', unsafe_allow_html=True)
    
    active_df = df[df['Status'] == 'Active']
    high_risk_active = active_df[active_df['Risk_Level'] == 'High']
    
    # Global Dashboard Stats
    d1, d2, d3, d4, d5 = st.columns(5)
    with d1: st.markdown(f'<div class="stat-box"><b>Total High Risk</b><br><span style="color:{RED}; font-size:24px; font-weight:700;">{len(high_risk_active)}</span></div>', unsafe_allow_html=True)
    with d2: st.markdown(f'<div class="stat-box"><b>Risk Percentage</b><br><span style="font-size:24px; font-weight:700;">{(len(high_risk_active)/len(active_df)*100):.1f}%</span></div>', unsafe_allow_html=True)
    with d3: st.markdown(f'<div class="stat-box"><b>Avg Age</b><br><span style="font-size:24px; font-weight:700;">27.4</span></div>', unsafe_allow_html=True)
    with d4: st.markdown(f'<div class="stat-box"><b>Avg Tenure</b><br><span style="font-size:24px; font-weight:700;">4.1Y</span></div>', unsafe_allow_html=True)
    with d5: st.markdown(f'<div class="stat-box"><b>Risk Grade</b><br><span style="font-size:24px; font-weight:700;">DMII</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="dashboard-title">Detailed Risk Analysis</div>', unsafe_allow_html=True)

    main_col, legend_col = st.columns([5, 1.2])

    with legend_col:
        st.write("**Risk Category**")
        if st.button("High Risk", key="btn_high", use_container_width=True): st.session_state.risk_filter = 'High'
        if st.button("Medium Risk", key="btn_med", use_container_width=True): st.session_state.risk_filter = 'Medium'
        if st.button("Low Risk", key="btn_low", use_container_width=True): st.session_state.risk_filter = 'Low'
        
        st.write("---")
        st.write("**Display Units**")
        toggle = st.radio("Show bars:", ["In Numbers", "In Percentage"], horizontal=False, label_visibility="collapsed")
        st.session_state.view_mode = toggle

    with main_col:
        r1c1, r1c2 = st.columns(2)
        r2c1, r2c2 = st.columns(2)
        quads = [("North", r1c1), ("South", r1c2), ("East", r2c1), ("West", r2c2)]
        
        current_data = active_df[active_df['Risk_Level'] == st.session_state.risk_filter]
        
        for zone, col in quads:
            with col:
                z_total = len(active_df[active_df['ZONE'] == zone])
                z_count = len(current_data[current_data['ZONE'] == zone])
                z_share = (z_count / z_total * 100) if z_total > 0 else 0
                
                # Zonal Header Styling
                st.markdown(f"<h2 style='color:{ICICI_NAVY}; margin-bottom:5px;'>{zone}</h2>", unsafe_allow_html=True)
                st.markdown(f'<div class="orange-header-box">Count: {z_count} ({z_share:.1f}%)</div>', unsafe_allow_html=True)
                
                # Chart Calculation
                dept_data = current_data[current_data['ZONE'] == zone].groupby('MAIN_GROUP').size().reset_index(name='Count')
                dept_data['Percentage'] = (dept_data['Count'] / z_count * 100).round(1) if z_count > 0 else 0
                
                chart_color = RED if st.session_state.risk_filter == 'High' else (YELLOW if st.session_state.risk_filter == 'Medium' else GREEN)
                y_val = 'Count' if st.session_state.view_mode == "In Numbers" else 'Percentage'
                t_suffix = "" if st.session_state.view_mode == "In Numbers" else "%"
                
                fig = px.bar(dept_data, x='MAIN_GROUP', y=y_val, text_auto=True, color_discrete_sequence=[chart_color])
                fig.update_traces(width=0.4, texttemplate=f'%{{y}}{t_suffix}', textposition='outside')
                fig.update_layout(
                    height=320, margin=dict(l=10, r=10, t=10, b=50), 
                    xaxis_title="", yaxis_title=y_val,
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=11)
                )
                # Ensure group names are fully visible
                fig.update_xaxes(tickangle=30)
                st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: SEARCH ---
elif st.session_state.page == 'Search':
    st.markdown(f"<h1 style='color:{ICICI_NAVY};'>Employee Search</h1>", unsafe_allow_html=True)
    search_id = st.text_input("Enter 6-Digit Employee ID:")
    if search_id:
        res = df[df['EMPID'] == search_id.strip()]
        if not res.empty:
            emp = res.iloc[0]
            st.markdown(f"<div style='text-align:center; padding:40px; border:1px solid {ICICI_ORANGE}; border-radius:10px;'>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color:{ICICI_ORANGE}; font-size:110px; margin:0;'>{emp['Attrition_Risk_Percentage']}%</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='color:{ICICI_NAVY};'>Risk Category: {emp['Risk_Level']}</h2>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("The entered Employee ID was not found in the ICICI database.")
