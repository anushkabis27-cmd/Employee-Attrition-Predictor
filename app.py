import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Brand Styles
st.set_page_config(page_title="ICICI Turnover Predictor", layout="wide")

ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"
HIGH_RED = "#FF4B4B"
MED_YELLOW = "#FFD700"
LOW_GREEN = "#28A745"

# Custom CSS for Rounded Rectangles & Color Themes
st.markdown(f"""
    <style>
    .orange-header {{ 
        background-color: {ICICI_ORANGE}; color: white; padding: 15px; 
        border-radius: 10px; text-align: center; font-weight: bold; font-size: 24px; 
    }}
    .quadrant-box {{ 
        background-color: #F0F2F6; padding: 20px; border-radius: 20px; 
        border: 1px solid #D1D5DB; margin-bottom: 20px; 
    }}
    .metric-box {{ 
        background-color: white; border-radius: 10px; padding: 15px; 
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05); text-align: center;
    }}
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

# 3. Page Navigation (Toggle Header)
if 'page' not in st.session_state: st.session_state.page = 'Overview'

nav_col1, nav_col2 = st.columns(2)
with nav_col1:
    if st.button("ZONE WISE RISK SUMMARY", use_container_width=True): st.session_state.page = 'Overview'
with nav_col2:
    if st.button("EMPLOYEE SEARCH", use_container_width=True): st.session_state.page = 'Search'

# --- PAGE 1: OVERVIEW ---
if st.session_state.page == 'Overview':
    st.markdown('<div class="orange-header">Zone Wise Risk Summary</div>', unsafe_allow_html=True)
    st.write("")

    # A. KEY DASHBOARD BOXES
    active_df = df[df['Status'] == 'Active']
    high_risk_active = active_df[active_df['Risk_Level'] == 'High']
    
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.markdown(f'<div class="metric-box"><b>Total High Risk</b><br><span style="color:{HIGH_RED}; font-size:24px;">{len(high_risk_active)}</span></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-box"><b>Risk %</b><br><span style="font-size:24px;">{(len(high_risk_active)/len(active_df)*100):.1f}%</span></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-box"><b>Avg Age</b><br><span style="font-size:24px;">{high_risk_active["AGE"].mean():.0f}</span></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-box"><b>Avg Tenure</b><br><span style="font-size:24px;">{high_risk_active["TENURE_YRS"].mean():.1f}Y</span></div>', unsafe_allow_html=True)
    with m5: st.markdown(f'<div class="metric-box"><b>Avg Grade Code</b><br><span style="font-size:24px;">{high_risk_active["Grade_Numeric"].mean():.1f}</span></div>', unsafe_allow_html=True)
    
    st.divider()

    # B. QUADRANTS (NORTH, SOUTH, EAST, WEST)
    row1_c1, row1_c2 = st.columns(2)
    row2_c1, row2_c2 = st.columns(2)
    
    quads = [{"name": "North", "col": row1_c1}, {"name": "South", "col": row1_c2},
             {"name": "East", "col": row2_c1}, {"name": "West", "col": row2_c2}]
    
    for q in quads:
        with q["col"]:
            st.markdown(f'<div class="quadrant-box">', unsafe_allow_html=True)
            st.subheader(f"{q['name']} Zone")
            
            # Interactive Legend Buttons for the Zone
            l1, l2, l3 = st.columns(3)
            with l1: 
                if st.button(f"High Risk ({q['name']})", key=f"h_{q['name']}", type="secondary", help="Click to see high risk count"):
                    hr = len(active_df[(active_df['ZONE'] == q['name']) & (active_df['Risk_Level'] == 'High')])
                    st.toast(f"{q['name']} High Risk: {hr}", icon="🔴")
            with l2:
                if st.button(f"Medium Risk ({q['name']})", key=f"m_{q['name']}", type="secondary"):
                    mr = len(active_df[(active_df['ZONE'] == q['name']) & (active_df['Risk_Level'] == 'Medium')])
                    st.toast(f"{q['name']} Medium Risk: {mr}", icon="🟡")
            with l3:
                if st.button(f"Low Risk ({q['name']})", key=f"l_{q['name']}", type="secondary"):
                    lr = len(active_df[(active_df['ZONE'] == q['name']) & (active_df['Risk_Level'] == 'Low')])
                    st.toast(f"{q['name']} Low Risk: {lr}", icon="🟢")

            # Chart
            z_data = high_risk_active[high_risk_active['ZONE'] == q['name']]
            dept_chart = z_data.groupby('MAIN_GROUP').size().reset_index(name='Count')
            dept_chart['%'] = (dept_chart['Count'] / len(z_data) * 100).round(1)
            
            fig = px.bar(dept_chart, x='MAIN_GROUP', y='Count', text='%', 
                         color_discrete_sequence=[ICICI_ORANGE])
            fig.update_traces(width=0.3, texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10), xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2: SEARCH ---
elif st.session_state.page == 'Search':
    st.markdown('<div class="orange-header">Employee Search</div>', unsafe_allow_html=True)
    search_id = st.text_input("Enter EMPID (6-Digits):", placeholder="e.g. 924197")
    
    if search_id:
        res = df[df['EMPID'] == search_id.strip()]
        if not res.empty:
            emp = res.iloc[0]
            st.markdown(f"<h1 style='text-align:center; color:{ICICI_ORANGE}; font-size:80px;'>{emp['Attrition_Risk_Percentage']}%</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:center;'>Risk Level: {emp['Risk_Level']}</h2>", unsafe_allow_html=True)
            
            # Actionables
            st.divider()
            st.subheader("Actionable Insights")
            st.markdown(f"* **Grade Analysis:** At Grade {emp['GRADE']}, tenure of {emp['TENURE_YRS']}Y is critical.")
            if emp['Risk_Level'] == 'High': st.markdown("* **Recommendation:** Schedule immediate stay interview.")
        else:
            st.error("Employee not found.")
