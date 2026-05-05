import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & ICICI Branding
st.set_page_config(page_title="ICICI Turnover Predictor", layout="wide")

ICICI_ORANGE = "#E77817"
ICICI_NAVY = "#05325C"

# 2. Data Loading (Handles the FileNotFoundError)
@st.cache_data
def load_data():
    try:
        # Matches the filename you confirmed is on GitHub/Colab
        data = pd.read_excel("Attrition_Final_Production.xlsx")
        # Ensure EMPID is treated as a string for searching
        data['EMPID'] = data['EMPID'].astype(str).str.zfill(6)
        return data
    except FileNotFoundError:
        st.error("Dataset 'Attrition_Final_Production.xlsx' not found. Please ensure it is in the root of your GitHub repo.")
        st.stop()

df = load_data()

# 3. Navigation State
if 'page' not in st.session_state:
    st.session_state.page = 'Overview'

# Custom Toggle Header
col_n1, col_n2 = st.columns(2)
with col_n1:
    if st.button("Zone-wise Risk Summary", use_container_width=True):
        st.session_state.page = 'Overview'
with col_n2:
    if st.button("Employee Search", use_container_width=True):
        st.session_state.page = 'Search'

st.divider()

# --- PAGE 1: ZONE-WISE RISK SUMMARY (QUADRANTS) ---
if st.session_state.page == 'Overview':
    st.title("Zone-wise Risk Summary")
    
    active_df = df[df['Status'] == 'Active']
    high_risk_active = active_df[active_df['Risk_Level'] == 'High']
    
    # Quadrant Layout (2x2)
    q_row1 = st.columns(2)
    q_row2 = st.columns(2)
    
    zones = [
        {"name": "North", "col": q_row1[0]},
        {"name": "South", "col": q_row1[1]},
        {"name": "East", "col": q_row2[0]},
        {"name": "West", "col": q_row2[1]}
    ]
    
    for q in zones:
        zone_name = q["name"]
        with q["col"]:
            # Metrics
            z_total = len(active_df[active_df['ZONE'] == zone_name])
            z_high = len(high_risk_active[high_risk_active['ZONE'] == zone_name])
            z_rate = (z_high / z_total * 100) if z_total > 0 else 0
            
            st.subheader(zone_name)
            st.metric(label="High Risk Count", value=f"{z_high} Employees", delta=f"{z_rate:.1f}% Risk Rate", delta_color="inverse")
            
            # Thin Bar Chart
            dept_data = high_risk_active[high_risk_active['ZONE'] == zone_name].groupby('MAIN_GROUP').size().reset_index(name='Count')
            dept_data['Percentage'] = (dept_data['Count'] / z_high * 100).round(1) if z_high > 0 else 0
            
            fig = px.bar(dept_summary := dept_data, x='MAIN_GROUP', y='Count', 
                         text='Percentage', hover_data={'Percentage': ':.1f%'},
                         color_discrete_sequence=[ICICI_ORANGE])
            
            fig.update_traces(width=0.3, texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
            st.divider()

# --- PAGE 2: EMPLOYEE SEARCH ---
elif st.session_state.page == 'Search':
    st.title("Employee Search")
    search_id = st.text_input("Enter 6-Digit EMPID:")
    
    if search_id:
        result = df[df['EMPID'] == search_id.strip()]
        if not result.empty:
            emp = result.iloc[0]
            if emp['Status'] == 'Inactive':
                st.warning("Employee has already left.")
            else:
                st.markdown(f"<h1 style='text-align:center; color:{ICICI_ORANGE}; font-size:80px;'>{emp['Attrition_Risk_Percentage']}%</h1>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align:center;'>{emp['Risk_Level']} RISK</h2>", unsafe_allow_html=True)
                
                # Details & Actionables
                st.write(f"**Grade:** {emp['GRADE']} | **Tenure:** {emp['TENURE_YRS']}Y | **Zone:** {emp['ZONE']}")
                st.subheader("Actionable Steps")
                st.write("- Conduct retention interview before June cycle.")
                if emp['Dist_Bin'] == 3: st.write("- Address Outstation relocation stress.")
        else:
            st.error("EMPID not found.")
