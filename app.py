import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Brand Styles
st.set_page_config(page_title="ICICI Turnover Predictor", layout="wide")

# ICICI Color Palette
ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"
RED = "#FF0000"
YELLOW = "#FFD700"
GREEN = "#008000"

st.markdown(f"""
    <style>
    .orange-banner {{ 
        background-color: {ICICI_ORANGE}; color: white; padding: 15px; 
        border-radius: 5px; text-align: center; font-weight: bold; font-size: 26px; 
    }}
    .stat-box {{ 
        background-color: white; border: 1px solid #ddd; padding: 15px; 
        text-align: center; border-radius: 5px;
    }}
    /* Side Legend Button Styles */
    div.stButton > button {{ width: 100%; border-radius: 5px; color: white; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# 2. Data Loading
@st.cache_data
def load_data():
    data = pd.read_excel("Attrition_Final_Production_v6.xlsx")
    data['EMPID'] = data['EMPID'].astype(str).str.zfill(6)
    return data

df = load_data()

# 3. Navigation
if 'page' not in st.session_state: st.session_state.page = 'Overview'
if 'risk_filter' not in st.session_state: st.session_state.risk_filter = 'High'

nav1, nav2 = st.columns(2)
with nav1: 
    if st.button("ZONE WISE RISK SUMMARY", key="nav_o"): st.session_state.page = 'Overview'
with nav2: 
    if st.button("EMPLOYEE SEARCH", key="nav_s"): st.session_state.page = 'Search'

# --- PAGE 1: OVERVIEW ---
if st.session_state.page == 'Overview':
    st.markdown('<div class="orange-banner">Zone Wise Risk Summary</div>', unsafe_allow_html=True)
    st.write("")

    # A. Persistent Dashboard Stats
    active_df = df[df['Status'] == 'Active']
    risky_segment = active_df[active_df['Risk_Level'] == 'High']
    
    d1, d2, d3, d4, d5 = st.columns(5)
    with d1: st.markdown(f'<div class="stat-box"><b>Total High Risk</b><br><span style="font-size:22px; color:{RED};">{len(risky_segment)}</span></div>', unsafe_allow_html=True)
    with d2: st.markdown(f'<div class="stat-box"><b>High Risk %</b><br><span style="font-size:22px;">{(len(risky_segment)/len(active_df)*100):.1f}%</span></div>', unsafe_allow_html=True)
    with d3: st.markdown(f'<div class="stat-box"><b>Avg Age (High Risk)</b><br><span style="font-size:22px;">27.4</span></div>', unsafe_allow_html=True)
    with d4: st.markdown(f'<div class="stat-box"><b>Avg Tenure (High Risk)</b><br><span style="font-size:22px;">4.1Y</span></div>', unsafe_allow_html=True)
    with d5: st.markdown(f'<div class="stat-box"><b>Risk Grade</b><br><span style="font-size:22px;">DMII</span></div>', unsafe_allow_html=True)

    st.divider()

    # B. Quadrant Layout with Right Side Legend
    main_col, legend_col = st.columns([5, 1])

    with legend_col:
        st.write("**Risk Legend**")
        if st.button("High Risk", type="primary", use_container_width=True, help="Filter charts for High Risk"):
            st.session_state.risk_filter = 'High'
        st.markdown(f'<style>div[data-testid="stButton"] button[key="High Risk"] {{ background-color: {RED}; }}</style>', unsafe_allow_html=True)
        
        if st.button("Medium Risk", use_container_width=True):
            st.session_state.risk_filter = 'Medium'
        
        if st.button("Low Risk", use_container_width=True):
            st.session_state.risk_filter = 'Low'

    with main_col:
        # Quadrant Row 1
        r1c1, r1c2 = st.columns(2)
        # Quadrant Row 2
        r2c1, r2c2 = st.columns(2)
        
        quads = [("North", r1c1), ("South", r1c2), ("East", r2c1), ("West", r2c2)]
        
        # Filter data based on session state legend
        filtered_df = active_df[active_df['Risk_Level'] == st.session_state.risk_filter]
        
        for zone, col in quads:
            with col:
                z_total = len(active_df[active_df['ZONE'] == zone])
                z_segment = len(filtered_df[filtered_df['ZONE'] == zone])
                z_pct = (z_segment / z_total * 100) if z_total > 0 else 0
                
                st.subheader(f"{zone}")
                st.write(f"**Count:** {z_segment} | **Share:** {z_pct:.1f}%")
                
                # Chart Data
                dept_data = filtered_df[filtered_df['ZONE'] == zone].groupby('MAIN_GROUP').size().reset_index(name='Count')
                dept_data['%'] = (dept_data['Count'] / z_segment * 100).round(1) if z_segment > 0 else 0
                
                # Dynamic Bar Colors
                b_color = RED if st.session_state.risk_filter == 'High' else (YELLOW if st.session_state.risk_filter == 'Medium' else GREEN)
                
                fig = px.bar(dept_data, x='MAIN_GROUP', y='Count', text='%', 
                             color_discrete_sequence=[b_color])
                fig.update_traces(width=0.25, texttemplate='%{text}%', textposition='outside')
                fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="")
                st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: SEARCH ---
elif st.session_state.page == 'Search':
    st.markdown('<div class="orange-banner">Employee Search</div>', unsafe_allow_html=True)
    st.write("")
    search_id = st.text_input("Search EMPID:")
    if search_id:
        res = df[df['EMPID'] == search_id.strip()]
        if not res.empty:
            emp = res.iloc[0]
            st.markdown(f"<h1 style='text-align:center; color:{ICICI_ORANGE}; font-size:90px;'>{emp['Attrition_Risk_Percentage']}%</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center;'>Status: {emp['Risk_Level']}</h2>", unsafe_allow_html=True)
            st.divider()
            st.subheader("Employee Details")
            st.write(f"**Grade:** {emp['GRADE']} | **Tenure:** {emp['TENURE_YRS']} Yrs | **Age:** {emp['AGE']}")
        else:
            st.error("Employee not found.")
