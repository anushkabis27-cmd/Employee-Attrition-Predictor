import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="ICICI Turnover Predictor", layout="wide")

# Brand Colors
ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"
RED = "#FF0000"
YELLOW = "#FFD700"
GREEN = "#008000"

# Custom CSS
st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{ background-color: white; border-right: 2px solid {ICICI_ORANGE}; }}
    .orange-header-box {{
        background-color: {ICICI_ORANGE}; color: white; padding: 5px 15px;
        border-radius: 15px; font-weight: bold; display: inline-block; margin-bottom: 15px;
    }}
    .stat-box {{ background-color: #F8F9FA; border: 1px solid #dee2e6; padding: 15px; text-align: center; border-radius: 10px; }}
    div.stButton > button {{ background-color: {ICICI_ORANGE}; color: white; border-radius: 5px; font-weight: bold; }}
    /* Color Specific Buttons for Legend */
    div.stButton > button[key="btn_high"] {{ background-color: {RED} !important; }}
    div.stButton > button[key="btn_med"] {{ background-color: {YELLOW} !important; color: black !important; }}
    div.stButton > button[key="btn_low"] {{ background-color: {GREEN} !important; }}
    </style>
""", unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    # Use the finalized production file
    data = pd.read_excel("Attrition_Final_Production_v5_Corrected.xlsx")
    data['EMPID'] = data['EMPID'].astype(str).str.zfill(6)
    return data

df = load_data()

# 3. Sidebar Navigation
with st.sidebar:
    st.write("### Navigation")
    if st.button("ZONE WISE RISK SUMMARY", key="nav_overview", use_container_width=True):
        st.session_state.page = 'Overview'
    if st.button("EMPLOYEE SEARCH", key="nav_search", use_container_width=True):
        st.session_state.page = 'Search'

# Init State
if 'page' not in st.session_state: st.session_state.page = 'Overview'
if 'risk_filter' not in st.session_state: st.session_state.risk_filter = 'High'

# --- PAGE 1: OVERVIEW ---
if st.session_state.page == 'Overview':
    st.title("Zone Wise Risk Summary")
    st.subheader("High Risk Segment Details")
    
    active_df = df[df['Status'] == 'Active']
    high_risk_active = active_df[active_df['Risk_Level'] == 'High']
    
    # Dashboard Row
    d1, d2, d3, d4, d5 = st.columns(5)
    with d1: st.markdown(f'<div class="stat-box"><b>Total High Risk</b><br><span style="color:{RED}; font-size:22px;">{len(high_risk_active)}</span></div>', unsafe_allow_html=True)
    with d2: st.markdown(f'<div class="stat-box"><b>Risk Percentage</b><br><span style="font-size:22px;">{(len(high_risk_active)/len(active_df)*100):.1f}%</span></div>', unsafe_allow_html=True)
    with d3: st.markdown(f'<div class="stat-box"><b>Avg Age</b><br><span style="font-size:22px;">27.4</span></div>', unsafe_allow_html=True)
    with d4: st.markdown(f'<div class="stat-box"><b>Avg Tenure</b><br><span style="font-size:22px;">4.1Y</span></div>', unsafe_allow_html=True)
    with d5: st.markdown(f'<div class="stat-box"><b>Risk Grade</b><br><span style="font-size:22px;">DMII</span></div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("Detailed Risk Analysis")

    main_col, legend_col = st.columns([5, 1.2])

    with legend_col:
        st.write("**Risk Category**")
        if st.button("High Risk", key="btn_high", use_container_width=True): st.session_state.risk_filter = 'High'
        if st.button("Medium Risk", key="btn_med", use_container_width=True): st.session_state.risk_filter = 'Medium'
        if st.button("Low Risk", key="btn_low", use_container_width=True): st.session_state.risk_filter = 'Low'

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
                
                # TITLES: Zone name outside, Count: {z_count} | Share: {z_share:.1f}%</div, unsafe_allow_html=True) inside box
                st.write(f"### {zone}") # Left aligned big title
                st.markdown(f'<div class="orange-header-box">{z_count} ({z_share:.1f}%)</div>', unsafe_allow_html=True)
                
                # Chart
                dept_data = current_data[current_data['ZONE'] == zone].groupby('MAIN_GROUP').size().reset_index(name='Count')
                chart_color = RED if st.session_state.risk_filter == 'High' else (YELLOW if st.session_state.risk_filter == 'Medium' else GREEN)
                
                fig = px.bar(dept_data, x='MAIN_GROUP', y='Count', text_auto=True, color_discrete_sequence=[chart_color])
                fig.update_traces(width=0.3)
                fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="")
                st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: SEARCH ---
elif st.session_state.page == 'Search':
    st.title("Employee Search")
    search_id = st.text_input("Enter 6-Digit EMPID:")
    if search_id:
        res = df[df['EMPID'] == search_id.strip()]
        if not res.empty:
            emp = res.iloc[0]
            st.markdown(f"<h1 style='text-align:center; color:{ICICI_ORANGE}; font-size:90px;'>{emp['Attrition_Risk_Percentage']}%</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center;'>Risk Category: {emp['Risk_Level']}</h2>", unsafe_allow_html=True)
        else:
            st.error("Employee not found.")
