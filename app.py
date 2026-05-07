import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE CONFIGURATION & ICICI BRANDING
st.set_page_config(page_title="ICICI Turnover Predictor", layout="wide")

ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"
RED = "#FF0000"
YELLOW = "#FFD700"
GREEN = "#008000"

# Custom CSS for Professional Layout
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Roboto', sans-serif; }}
    
    /* Sidebar Navigation */
    [data-testid="stSidebar"] {{ background-color: #f8f9fa; border-right: 1px solid #ddd; }}
    div.stButton > button {{ 
        background-color: {ICICI_ORANGE}; color: white; border-radius: 4px; 
        font-weight: 600; text-transform: uppercase; border: none; width: 100%;
    }}
    
    /* Zonal Headers: Orange Rounded Rectangles */
    .orange-metric-box {{
        background-color: {ICICI_ORANGE}; color: white; padding: 6px 18px;
        border-radius: 20px; font-weight: 700; display: inline-block; margin-bottom: 15px;
    }}
    
    /* Dashboard Titles */
    .dashboard-title {{ color: {ICICI_NAVY}; font-weight: 700; border-left: 5px solid {ICICI_ORANGE}; padding-left: 15px; margin: 20px 0; }}
    
    /* Stat Boxes */
    .stat-box {{ background-color: white; border: 1px solid #e0e0e0; padding: 20px; text-align: center; border-radius: 8px; }}
    
    /* Risk Legend Buttons */
    button[key="btn_high"] {{ background-color: {RED} !important; color: white !important; }}
    button[key="btn_med"] {{ background-color: {YELLOW} !important; color: #333 !important; }}
    button[key="btn_low"] {{ background-color: {GREEN} !important; color: white !important; }}
    </style>
""", unsafe_allow_html=True)

# 2. DATA LOADING
@st.cache_data
def load_data():
    try:
        # Loading from the new file name and specific data sheet
        file_name = "Attrition_Final_Production_v8_Final_Analysis.xlsx"
        data = pd.read_excel(file_name, sheet_name="Sheet1_Dataset")
        data['EMPID'] = data['EMPID'].astype(str).str.zfill(6)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}. Ensure the file is uploaded to GitHub.")
        st.stop()

df = load_data()

# 3. SIDEBAR NAVIGATION & HISTORY
if 'page' not in st.session_state: st.session_state.page = 'Overview'
if 'search_history' not in st.session_state: st.session_state.search_history = []
if 'risk_filter' not in st.session_state: st.session_state.risk_filter = 'High'
if 'view_mode' not in st.session_state: st.session_state.view_mode = 'In Numbers'

with st.sidebar:
    st.markdown(f"<h2 style='color:{ICICI_NAVY};'>ICICI Predictor</h2>", unsafe_allow_html=True)
    st.write("---")
    if st.button("ZONE WISE RISK SUMMARY", key="nav_overview"): st.session_state.page = 'Overview'
    st.write("")
    if st.button("EMPLOYEE SEARCH", key="nav_search"): st.session_state.page = 'Search'
    
    if st.session_state.search_history:
        st.write("---")
        st.write("#### Search History")
        for h_id in reversed(st.session_state.search_history[-5:]):
            if st.button(f"EMPID: {h_id}", key=f"hist_{h_id}"):
                st.session_state.page = 'Search'
                st.session_state.current_search = h_id

# --- PAGE 1: ZONE WISE RISK SUMMARY ---
if st.session_state.page == 'Overview':
    st.title("Zone Wise Risk Summary")
    st.markdown('<div class="dashboard-title">High Risk Segment Details</div>', unsafe_allow_html=True)
    
    active_df = df[df['Status'] == 'Active']
    high_risk_active = active_df[active_df['Risk_Level'] == 'High']
    
    # Header Dashboard
    d1, d2, d3, d4, d5 = st.columns(5)
    with d1: st.markdown(f'<div class="stat-box"><b>Total High Risk</b><br><span style="color:{RED}; font-size:24px; font-weight:700;">{len(high_risk_active)}</span></div>', unsafe_allow_html=True)
    with d2: st.markdown(f'<div class="stat-box"><b>Risk %</b><br><span style="font-size:24px; font-weight:700;">{(len(high_risk_active)/len(active_df)*100):.1f}%</span></div>', unsafe_allow_html=True)
    with d3: st.markdown(f'<div class="stat-box"><b>Avg Age</b><br><span style="font-size:24px; font-weight:700;">27.4</span></div>', unsafe_allow_html=True)
    with d4: st.markdown(f'<div class="stat-box"><b>Avg Tenure</b><br><span style="font-size:24px; font-weight:700;">4.1Y</span></div>', unsafe_allow_html=True)
    with d5: st.markdown(f'<div class="stat-box"><b>Risk Grade</b><br><span style="font-size:24px; font-weight:700;">DMII</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="dashboard-title">Detailed Risk Analysis</div>', unsafe_allow_html=True)
    main_col, legend_col = st.columns([5, 1.2])

    with legend_col:
        st.write("**Risk Category**")
        if st.button("High Risk", key="btn_high"): st.session_state.risk_filter = 'High'
        if st.button("Medium Risk", key="btn_med"): st.session_state.risk_filter = 'Medium'
        if st.button("Low Risk", key="btn_low"): st.session_state.risk_filter = 'Low'
        st.write("---")
        st.write("**Display Units**")
        st.session_state.view_mode = st.radio("Show bars:", ["In Numbers", "In Percentage"], label_visibility="collapsed")

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
                st.markdown(f"<h3 style='color:{ICICI_NAVY}; margin-bottom:5px; text-align:left;'>{zone}</h3>", unsafe_allow_html=True)
                st.markdown(f'<div class="orange-metric-box">Count: {z_count} ({z_share:.1f}%)</div>', unsafe_allow_html=True)
                
                dept_data = current_data[current_data['ZONE'] == zone].groupby('MAIN_GROUP').size().reset_index(name='Count')
                dept_data['Percentage'] = (dept_data['Count'] / z_count * 100).round(1) if z_count > 0 else 0
                chart_color = RED if st.session_state.risk_filter == 'High' else (YELLOW if st.session_state.risk_filter == 'Medium' else GREEN)
                y_val = 'Count' if st.session_state.view_mode == "In Numbers" else 'Percentage'
                fig = px.bar(dept_data, x='MAIN_GROUP', y=y_val, text_auto=True, color_discrete_sequence=[chart_color])
                fig.update_traces(width=0.4, textposition='outside')
                fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=50), xaxis_title="", yaxis_title=y_val, plot_bgcolor='rgba(0,0,0,0)')
                fig.update_xaxes(tickangle=30)
                st.plotly_chart(fig, use_container_width=True)

# --- PAGE 2: EMPLOYEE SEARCH ---
elif st.session_state.page == 'Search':
    st.markdown(f"<h1 style='color:{ICICI_NAVY};'>Employee Search</h1>", unsafe_allow_html=True)
    default_id = st.session_state.get('current_search', "")
    
    s_col1, s_col2 = st.columns([4, 1])
    with s_col1:
        search_id = st.text_input("Enter EMPID:", value=default_id, placeholder="Search...", label_visibility="collapsed")
    with s_col2:
        search_clicked = st.button("SEARCH DETAILS")

    if (search_clicked or default_id) and search_id:
        if search_id not in st.session_state.search_history: st.session_state.search_history.append(search_id)
        res = df[df['EMPID'] == search_id.strip()]
        if not res.empty:
            emp = res.iloc[0]
            risk_color = RED if emp['Risk_Level'] == 'High' else (YELLOW if emp['Risk_Level'] == 'Medium' else GREEN)
            
            st.markdown(f"<div style='text-align:center; padding:20px;'><h1 style='color:{risk_color}; font-size:100px; margin:0;'>{emp['Attrition_Risk_Percentage']}%</h1><h2 style='color:{risk_color}; margin-top:0;'>{emp['Risk_Level']} Risk</h2></div>", unsafe_allow_html=True)
            st.divider()
            detail_col, insight_col = st.columns([1, 1.5])

            with detail_col:
                st.markdown(f"<h4 style='color:{ICICI_NAVY};'>Employee Details</h4>", unsafe_allow_html=True)
                st.write(f"**Emp ID:** {emp['EMPID']}")
                st.write(f"**Age:** {emp['AGE']} Years")
                st.write(f"**Grade:** {emp['GRADE']}")
                st.write(f"**Tenure:** {emp['TENURE_YRS']} Years")
                # Using columns from v8 file
                st.write(f"**Work Location:** {emp.get('Office_State', 'N/A')}")
                st.write(f"**Home Location:** {emp.get('Home_State', 'N/A')}")

            with insight_col:
                st.markdown(f"<h4 style='color:{ICICI_NAVY};'>Reasons</h4>", unsafe_allow_html=True)
                with st.container(border=True):
                    if 25 <= emp['AGE'] <= 29: st.write("• Age falls within the high-risk bracket (25-29 years).")
                    if emp['TENURE_YRS'] >= 3: st.write(f"• Tenure of {emp['TENURE_YRS']}Y has reached risk threshold.")
                    if emp['Distance_From_Home_KM'] > 500: st.write("• High Distance: Work location is over 500km from home.")

                st.markdown(f"<h4 style='color:{ICICI_NAVY};'>Actionables</h4>", unsafe_allow_html=True)
                with st.container(border=True):
                    if emp['Risk_Level'] == 'High':
                        st.write("• **ER Manager Physical Intervention**: Urgent in-person visit to signal organizational care.")
                        st.write("• **Emergency Career Re-pathing**: Explore internal mobility across departments.")
                        st.write("• **Senior Leadership Recognition**: Personal acknowledgment from BU/HR head.")
                    elif emp['Risk_Level'] == 'Medium':
                        st.write("• **ER Manager Structured Connect**: 1:1 meeting to address team dynamics.")
                        st.write("• **OJP Re-energizer**: Offer rotation in a different business unit.")
                        st.write("• **Personalized Recognition**: Timely appreciation tied to actual contribution.")
                    else:
                        st.write("• **Future Goals Check-ins**: Bi-annual conversations for development roadmaps.")
                        st.write("• **OJP Internal Leads**: Assign as SMEs on cross-functional projects.")
                        st.write("• **Recognition Programs**: Nominate for 'Star Performer' awards.")
        else: st.error("EMPID not found.")
