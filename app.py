import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="iRetain | Workforce Analytics", layout="wide")

# --- SAFE RERUN UTILITY ---
def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# --- 2. REFINED PROFESSIONAL UI CSS WITH MINIMALIST SIDEBAR ---
st.markdown("""
    <link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Mulish:wght=600;700&display=swap'>

    <style>
    .main { background-color: #FFFFFF; color: #333333; }
    [data-testid="stSidebar"] { background-color: #f37021; }
    
    /* Document Header Styling */
    .centered-title { text-align: center; color: #003366; font-family: 'Segoe UI', Arial; font-weight: bold; margin-bottom: 20px; }
    .section-header { color: #000000; font-weight: bold; font-size: 20px; margin-bottom: 15px; }

    /* Metric Boxes - Orange with White Text */
    .metric-container { background-color: #f37021; padding: 15px; border-radius: 8px; text-align: center; color: white; }
    .metric-value { font-size: 26px; font-weight: bold; color: white; }
    .metric-label { font-size: 14px; color: white; }

    /* Quadrant Box Styling */
    .quadrant-box { background-color: #FFFFFF; padding: 0px; border-radius: 8px; border: 1px solid #EEEEEE; margin-bottom: 10px; overflow: hidden; }
    .zone-header { background-color: #f37021; color: white; padding: 10px; font-size: 24px; font-weight: bold; text-align: center; }

    /* Detail Page Styling */
    .risk-box { padding: 30px; border-radius: 20px; text-align: center; border: 2px solid; background: #FAFAFA; margin-bottom: 25px; }
    .big-font { font-size: 70px !important; font-weight: bold; }
    .report-card { background: #FFFFFF; padding: 25px; border-radius: 15px; border-left: 5px solid #f37021;
                   border-top: 1px solid #EEE; border-right: 1px solid #EEE; border-bottom: 1px solid #EEE; margin-bottom: 20px; }

    /* Standard Core App Button Layouts */
    div.stButton > button { background-color: #f37021 !important; color: white !important; border-radius: 4px; border: none; width: 100%; font-weight: 600; }
    .large-btn-container div.stButton > button { padding: 15px 10px !important; font-size: 18px !important; height: 60px !important; }
    .small-btn-container div.stButton > button { padding: 5px !important; font-size: 13px !important; height: auto !important; margin-bottom: 8px; }
    
    .chart-container { padding: 5px; }

    /* SIDEBAR OVERRIDES */
    [data-testid="stSidebar"] h1 {
        font-family: 'Mulish', sans-serif !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }

    [data-testid="stSidebar"] [data-testid="stWidgetFormWrapper"] {
        width: 100%;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        width: 100%;
        gap: 0px !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        display: block !important;
        width: 100% !important;
        padding: 6px 16px !important;
        margin: 0px !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        box-shadow: none !important;
        cursor: pointer !important;
        transition: background-color 0.15s ease-in-out;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        font-family: 'Mulish', sans-serif !important;
        font-weight: 600 !important;
        color: #000000 !important;
        font-size: 15px !important;
        margin: 0px !important;
        padding: 0px !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.12) !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: rgba(0, 0, 0, 0.08) !important;
        border-left: 4px solid #000000 !important;
        padding-left: 12px !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stBlock"] {
        display: none !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)


# --- 3. RISK BRACKET ENGINE ---
def classify_revised_risk_tier(score):
    if score <= 20.0:
        return 'Low'
    elif score <= 50.0:
        return 'Medium'
    else:
        return 'High'

def run_portfolio_trigger_check(df, manager_id):
    manager_portfolio = df[df['ER manager ID'] == manager_id]
    if len(manager_portfolio) == 0:
        return
        
    total_count = len(manager_portfolio)
    active_high_risk = len(manager_portfolio[
        (manager_portfolio['Risk_Level'] == 'High') & 
        (manager_portfolio['Intervention_Status'] != 'Completed')
    ])
    
    high_risk_share = (active_high_risk / total_count * 100) if total_count > 0 else 0
    
    if high_risk_share > 10.0: 
        st.warning(f"System Trigger Notification Issued: Your portfolio pending High Risk share is {high_risk_share:.1f}%. Please intervene immediately.")


# --- 4. HIGH-PERFORMANCE DATA ENGINE (CSV CACHE LAYER) ---
@st.cache_data
def load_base_data():
    excel_path = 'SIP Data final.xlsx'
    cache_path = 'SIP Data final_active_cache.csv'
    
    if os.path.exists(cache_path):
        df = pd.read_csv(cache_path)
        df.columns = df.columns.str.strip()
        return df
        
    if not os.path.exists(excel_path):
        st.error(f"Required Excel spreadsheet asset '{excel_path}' could not be found in the current directory.")
        st.stop()
        
    try:
        df = pd.read_excel(excel_path, sheet_name='Master Attrition Data')
    except Exception:
        df = pd.read_excel(excel_path, sheet_name=0)
        
    df.columns = df.columns.str.strip()
    df.to_csv(cache_path, index=False)
    return df

if 'master_data' not in st.session_state:
    st.session_state['master_data'] = load_base_data()

df = st.session_state['master_data']

# --- GEOGRAPHIC REGIONAL META MAPPING DICTIONARIES ---
city_to_state = {
    'Cuttack': 'Odisha', 'Pune': 'Maharashtra', 'Noida': 'Uttar Pradesh', 
    'Jodhpur': 'Rajasthan', 'Kolkata': 'West Bengal', 'Mumbai': 'Maharashtra', 
    'Hyderabad': 'Telangana', 'Ranchi': 'Jharkhand', 'Delhi': 'Delhi', 
    'Siliguri': 'West Bengal', 'Bangalore': 'Karnataka', 'Coimbatore': 'Tamil Nadu', 
    'Kanpur': 'Uttar Pradesh', 'Lucknow': 'Uttar Pradesh', 'Ahmedabad': 'Gujarat', 
    'Chennai': 'Tamil Nadu', 'Patna': 'Bihar'
}

city_coords = {
    'Cuttack': [20.4625, 85.8830], 'Pune': [18.5204, 73.8567], 'Noida': [28.5355, 77.3910], 
    'Jodhpur': [26.2389, 73.0243], 'Kolkata': [22.5726, 88.3639], 'Mumbai': [19.0760, 72.8777], 
    'Hyderabad': [17.3850, 78.4867], 'Ranchi': [23.3441, 85.3096], 'Delhi': [28.6139, 77.2090], 
    'Siliguri': [26.7271, 88.3953], 'Bangalore': [12.9716, 77.5946], 'Coimbatore': [11.0168, 76.9558], 
    'Kanpur': [26.4499, 80.3319], 'Lucknow': [26.8467, 80.9462], 'Ahmedabad': [23.0225, 72.5714], 
    'Chennai': [13.0827, 80.2707], 'Patna': [25.5941, 85.1376]
}

if 'State' not in df.columns:
    df['State'] = df['Work_Location'].map(city_to_state).fillna('Other')
if 'Latitude' not in df.columns:
    df['Latitude'] = df['Work_Location'].map(lambda x: city_coords[x][0] if x in city_coords else np.nan)
if 'Longitude' not in df.columns:
    df['Longitude'] = df['Work_Location'].map(lambda x: city_coords[x][1] if x in city_coords else np.nan)

if 'Age_Group' not in df.columns:
    df['Age_Group'] = pd.cut(df['AGE'], bins=[0, 24, 29, 39, 49, 100], labels=['Under 25', '25-29', '30-39', '40-49', '50 and Above'])
if 'Tenure_Group' not in df.columns:
    df['Tenure_Group'] = pd.cut(df['TENURE_YRS'], bins=[-1, 1, 3, 5, 10, 100], labels=['0-1 Yr', '1-3 Yrs', '3-5 Yrs', '5-10 Yrs', '10+ Yrs'])

# App Navigation Variables
if 'view_mode' not in st.session_state: st.session_state['view_mode'] = 'Percentage'
if 'risk_filter' not in st.session_state: st.session_state['risk_filter'] = 'High'
if 'current_page' not in st.session_state: st.session_state['current_page'] = "Zone wise turnover prediction"
if 'selected_empid' not in st.session_state: st.session_state['selected_empid'] = None
if 'remarks_empid' not in st.session_state: st.session_state['remarks_empid'] = None
if 'current_manager_id' not in st.session_state: st.session_state['current_manager_id'] = None
if 'er_authenticated' not in st.session_state: st.session_state['er_authenticated'] = False
if 'map_selected_state' not in st.session_state: st.session_state['map_selected_state'] = 'All India'


# --- 5. SIDEBAR NAVIGATION CONTROLLER ---
st.sidebar.title("iRETAIN")
st.sidebar.markdown("---")
page_options = [
    "Zone wise turnover prediction", 
    "Geographic Risk Heat Map", 
    "Employee risk indicator", 
    "ER Manager Portal", 
    "Feedback Form"
]

if st.session_state['current_page'] in page_options:
    default_index = page_options.index(st.session_state['current_page'])
else:
    default_index = 0
    st.session_state['current_page'] = page_options[0]

selected_sidebar = st.sidebar.radio("NAVIGATION", page_options, index=default_index)

if selected_sidebar != st.session_state['current_page']:
    st.session_state['current_page'] = selected_sidebar
    if selected_sidebar != "Employee risk indicator" and selected_sidebar != "Feedback Form":
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
        grid_rows = [st.columns(2), st.columns(2)]
        for i, zone in enumerate(zones):
            with grid_rows[i // 2][i % 2]:
                st.markdown(f"<div class='quadrant-box'><div class='zone-header'>{zone}</div><div class='chart-container'>", unsafe_allow_html=True)
                zone_data = df[(df['ZONE'].str.capitalize() == zone) & (df['Risk_Level'] == st.session_state['risk_filter'])]
                if not zone_data.empty:
                    counts = zone_data['MAIN_GROUP'].value_counts()
                    total_in_dept = df[df['ZONE'].str.capitalize() == zone]['MAIN_GROUP'].value_counts()
                    percentages = (counts / total_in_dept * 100).fillna(0)
                    fig, ax = plt.subplots(figsize=(5, 3))
                    bars = ax.bar(counts.index, counts.values, color=current_color)
                    max_v = max(counts.values) * 1.35 if not counts.empty else 10
                    ax.set_ylim(0, max_v)
                    for bar, label_val in zip(bars, percentages.values if st.session_state['view_mode'] == 'Percentage' else counts.values):
                        height = bar.get_height()
                        label = f"{label_val:.1f}%" if st.session_state['view_mode'] == 'Percentage' else f"{int(label_val)}"
                        ax.text(bar.get_x() + bar.get_width()/2., height + (max_v * 0.02), label, ha='center', va='bottom', fontsize=9, fontweight='bold')
                    ax.set_facecolor('#FFFFFF')
                    ax.tick_params(axis='x', rotation=45, labelsize=8)
                    ax.set_ylabel("Count", fontsize=9)
                    st.pyplot(fig)
                else: st.write("No data found for this selection.")
                st.markdown("</div></div>", unsafe_allow_html=True)

    with col_legend:
        st.write("**Risk View Filter**")
        st.markdown('<div class="large-btn-container">', unsafe_allow_html=True)
        if st.button("High Risk"): st.session_state['risk_filter'] = 'High'
        if st.button("Medium Risk"): st.session_state['risk_filter'] = 'Medium'
        if st.button("Low Risk"): st.session_state['risk_filter'] = 'Low'
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()
        st.markdown('<div class="small-btn-container">', unsafe_allow_html=True)
        if st.button("In Numbers"): st.session_state['view_mode'] = 'Numbers'
        if st.button("In Percentage"): st.session_state['view_mode'] = 'Percentage'
        st.markdown('</div>', unsafe_allow_html=True)


# --- PAGE 2: GEOGRAPHIC RISK HEAT MAP ---
elif st.session_state['current_page'] == "Geographic Risk Heat Map":
    st.markdown("<h1 class='centered-title'>Geographic Risk Heat Map</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>Filter Operations Control Panel</div>", unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        sel_dept = st.multiselect("Department", options=sorted(df['MAIN_GROUP'].dropna().unique().tolist()))
    with f2:
        sel_grade = st.multiselect("Grade / Band", options=sorted(df['GRADE'].dropna().unique().tolist()))
    with f3:
        sel_age = st.multiselect("Age Group", options=['Under 25', '25-29', '30-39', '40-49', '50 and Above'])
    with f4:
        sel_tenure = st.multiselect("Tenure Group", options=['0-1 Yr', '1-3 Yrs', '3-5 Yrs', '5-10 Yrs', '10+ Yrs'])

    map_df = df.copy()
    if sel_dept: map_df = map_df[map_df['MAIN_GROUP'].isin(sel_dept)]
    if sel_grade: map_df = map_df[map_df['GRADE'].isin(sel_grade)]
    if sel_age: map_df = map_df[map_df['Age_Group'].isin(sel_age)]
    if sel_tenure: map_df = map_df[map_df['Tenure_Group'].isin(sel_tenure)]

    st.divider()
    
    col_map_canvas, col_side_panel = st.columns([3, 1.2])
    
    with col_side_panel:
        st.markdown("<div class='section-header'>Regional Navigation Desk</div>", unsafe_allow_html=True)
        state_options = ['All India'] + sorted([s for s in map_df['State'].unique() if s != 'Other'])
        st.session_state['map_selected_state'] = st.selectbox("Select State Focus View", options=state_options, index=state_options.index(st.session_state['map_selected_state']) if st.session_state['map_selected_state'] in state_options else 0)
        
        if st.session_state['map_selected_state'] == 'All India':
            focused_df = map_df
            display_title = "All India Summary"
        else:
            focused_df = map_df[map_df['State'] == st.session_state['map_selected_state']]
            display_title = st.session_state['map_selected_state']

        s_total = len(focused_df)
        s_high = len(focused_df[focused_df['Risk_Level'] == 'High'])
        s_pct = (s_high / s_total * 100) if s_total > 0 else 0.0
        s_avg_score = focused_df['Attrition_Risk_Percentage'].mean() if s_total > 0 else 0.0

        st.markdown(f"""
        <div class='report-card'>
            <h4>{display_title} Dashboard</h4>
            <p><b>Total Headcount:</b> {s_total}</p>
            <p><b>High Risk Count:</b> {s_high}</p>
            <p><b>High Risk Concentration:</b> {s_pct:.1f}%</p>
            <p><b>Average Attrition Risk:</b> {s_avg_score:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state['map_selected_state'] != 'All India' and s_total > 0:
            st.markdown("##### Top Highest-Risk Cities")
            city_metrics = focused_df.groupby('Work_Location').apply(
                lambda x: pd.Series({
                    'High_Risk_Pct': (len(x[x['Risk_Level'] == 'High']) / len(x) * 100)
                }), include_groups=False
            ).reset_index().sort_values(by='High_Risk_Pct', ascending=False)
            
            for idx, c_row in city_metrics.head(5).iterrows():
                st.caption(f"• {c_row['Work_Location']}: {c_row['High_Risk_Pct']:.1f}% High Risk share")

    with col_map_canvas:
        geo_agg = map_df.groupby(['Work_Location', 'State', 'Latitude', 'Longitude']).apply(
            lambda x: pd.Series({
                'Total_Employees': len(x),
                'High_Risk_Employees': len(x[x['Risk_Level'] == 'High']),
                'High_Risk_Percentage': (len(x[x['Risk_Level'] == 'High']) / len(x) * 100),
                'Average_Risk_Score': x['Attrition_Risk_Percentage'].mean()
            }), include_groups=False
        ).reset_index()

        geo_agg['Risk_Category'] = geo_agg['High_Risk_Percentage'].apply(classify_revised_risk_tier)

        if st.session_state['map_selected_state'] == 'All India':
            center_lat, center_lon = 22.5, 78.5
            zoom_level = 3.6
            plot_df = geo_agg
        else:
            plot_df = geo_agg[geo_agg['State'] == st.session_state['map_selected_state']]
            if not plot_df.empty:
                center_lat, center_lon = plot_df['Latitude'].mean(), plot_df['Longitude'].mean()
                zoom_level = 5.5
            else:
                center_lat, center_lon = 22.5, 78.5
                zoom_level = 3.6

        if not plot_df.empty:
            fig_map = px.scatter_mapbox(
                plot_df,
                lat="Latitude",
                lon="Longitude",
                size="Total_Employees",
                color="High_Risk_Percentage",
                color_continuous_scale=["#28A745", "#FFCC00", "#D7191C"], 
                range_color=[0, 100],
                zoom=zoom_level,
                center={"lat": center_lat, "lon": center_lon},
                text="Work_Location",
                mapbox_style="carto-positron",
                height=580,
                hover_name="Work_Location",
                labels={"High_Risk_Percentage": "High Risk %"},
                custom_data=["Total_Employees", "High_Risk_Employees", "High_Risk_Percentage", "Risk_Category"]
            )

            fig_map.update_shapes(dict(xs=None))
            fig_map.update_traces(
                hovertemplate="<br>".join([
                    "<b>City: %{hovertext}</b>",
                    "Total Employees: %{customdata[0]}",
                    "High Risk Employees: %{customdata[1]}",
                    "High Risk %: %{customdata[2]:.1f}%",
                    "Risk Category: %{customdata[3]}"
                ])
            )

            fig_map.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                coloraxis_colorbar=dict(
                    title="High Risk %",
                    thicknessmode="pixels", thickness=15,
                    lenmode="pixels", len=300,
                    yanchor="top", y=1,
                    xanchor="left", x=0.02
                )
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("No matching geographic records available for the specified criteria configuration.")


# --- PAGE 3: EMPLOYEE RISK INDICATOR ---
elif st.session_state['current_page'] == "Employee risk indicator":
    st.markdown("<h1 class='centered-title'>Employee Risk Indicator</h1>", unsafe_allow_html=True)
    if st.session_state['selected_empid']:
        emp_id = st.session_state['selected_empid']
        if st.button("Back to ER Dashboard"):
            st.session_state['selected_empid'] = None
            st.session_state['current_page'] = "ER Manager Portal"
            st.rerun()
    else: 
        emp_id = st.number_input("Enter EMPID to search", min_value=0, step=1)

    if emp_id:
        user_data = df[df['EMPID'] == emp_id]
        if not user_data.empty:
            row = user_data.iloc[0]
            score = row.get('Attrition_Risk_Percentage', 0)
            level = row.get('Risk_Level', 'Low')
            tenure = row.get('TENURE_YRS', 0)
            h_color = "#D7191C" if level == 'High' else ("#FFCC00" if level == 'Medium' else "#28A745")
            
            st.markdown(f"<div class='risk-box' style='border-color: {h_color}; color: {h_color};'><p class='big-font'>{score:.1f}%</p><h1>{level.upper()} RISK</h1></div>", unsafe_allow_html=True)
            
            st.subheader("Employee Profile Details")
            c1, c2, c3 = st.columns(3)
            with c1: 
                st.write(f"**EMPID:** {row['EMPID']}")
                st.write(f"**Grade:** {row['GRADE']}")
                st.write(f"**Work Location:** {row.get('Work_Location', 'N/A')}")
                st.write(f"**Intervention Status:** `{row.get('Intervention_Status', 'Not started')}`")
            with c2: 
                st.write(f"**Age:** {row['AGE']}")
                st.write(f"**Tenure:** {tenure} Yrs")
                st.write(f"**Home Location:** {row.get('Home_Location', 'N/A')}")
            with c3: 
                st.write(f"**Zone:** {row['ZONE']}")
                st.write(f"**Group:** {row['MAIN_GROUP']}")

            st.divider()
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("<div class='report-card'><h4>Risk Factor Analysis</h4>", unsafe_allow_html=True)
                if row['GRADE'] in ['ALT', 'CM']:
                    st.write("• Highly stable organizational anchor profile.")
                if 3.0 <= tenure <= 5.0:
                    st.write("• Tenure falls in primary risk of 3-5 Year bracket.")
                if 25 <= row['AGE'] <= 29:
                    st.write("• Volatile Age Group of 25-29 years.")
                if row.get('Distance From Home (KM)', 0) > 800:
                    st.write("• High geographic distance from Home (>800 KM from home).")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"<div class='report-card' style='border-left-color: {h_color};'><h4>Mitigation Actionables</h4>", unsafe_allow_html=True)
                if row.get('Intervention_Status', 'Not started') == 'Completed':
                    st.write("• Intervention Concluded: Feedback form logged successfully.")
                elif level == 'High':
                    st.write("• Urgent Action Needed: Immediate 1:1 session with ER Manager.")
                    st.write("• Discuss career aspirations & growth expectations within organization.")
                    st.write("• Map short-term milestones, internal recognition hooks, and upskilling goals.")
                    st.write("• Explore structural paths like branch transfers or flexible arrangements to handle travel strain.")
                elif level == 'Medium':
                    st.write("• Engage in career path alignment discussions.")
                else: 
                    st.write("• Maintain standard contact & regular checkins.")
                st.markdown("</div>", unsafe_allow_html=True)

            st.divider()
            st.write("#### Action Center")
            mock_phone = f"+9198765{str(int(row['EMPID']))[-5:]}" if not pd.isna(row['EMPID']) else "+919999999999"
            
            col_call, _ = st.columns([1.5, 3])
            with col_call:
                st.markdown(f"""
                    <a href="tel:{mock_phone}" style="text-decoration: none;">
                        <div style="background-color: #003366; color: white; text-align: center; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer;">
                            Call Employee ({mock_phone})
                        </div>
                    </a>
                """, unsafe_allow_html=True)
        else: st.error("EMPID not found.")


# --- PAGE 4: ER MANAGER PORTAL ---
elif st.session_state['current_page'] == "ER Manager Portal":
    st.markdown("<h1 class='centered-title'>ER Manager Portal</h1>", unsafe_allow_html=True)
        
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        input_er_id = st.number_input("Enter ER Manager ID", min_value=0, step=1, value=st.session_state['current_manager_id'] if st.session_state['current_manager_id'] else 0)
    
    with col_btn:
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        login_clicked = st.button("Log in")

    if login_clicked:
        if 'ER manager ID' in df.columns and input_er_id in df['ER manager ID'].values:
            st.session_state['current_manager_id'] = input_er_id
            st.session_state['er_authenticated'] = True
        else:
            st.session_state['er_authenticated'] = False
            st.error("Manager ID not found.")

    if st.session_state['er_authenticated'] and st.session_state['current_manager_id']:
        active_id = st.session_state['current_manager_id']
        manager_df = df[df['ER manager ID'] == active_id]
        
        run_portfolio_trigger_check(df, active_id)

        total_employees_mapped = len(manager_df)
        
        mapped_high_risk_df = manager_df[
            (manager_df['Risk_Level'] == 'High') & 
            (manager_df['Intervention_Status'] != 'Completed')
        ].sort_values(by='Attrition_Risk_Percentage', ascending=False)
        
        high_risk_employees = len(mapped_high_risk_df)
        high_risk_pct = (high_risk_employees / total_employees_mapped * 100) if total_employees_mapped > 0 else 0
        
        st.markdown("<div class='section-header'>Portfolio Overview </div>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1: st.markdown(f"<div class='metric-container'><div class='metric-label'>Total Mapped Employees</div><div class='metric-value'>{total_employees_mapped}</div></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='metric-container'><div class='metric-label'>High Risk Employees</div><div class='metric-value'>{high_risk_employees}</div></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='metric-container'><div class='metric-label'>High Risk Share (%)</div><div class='metric-value'>{high_risk_pct:.1f}%</div></div>", unsafe_allow_html=True)

        st.divider()
        st.write("#### Active Pending Actionables")
        
        if not mapped_high_risk_df.empty:
            h_cols_hr = st.columns([1, 2, 1, 1, 1.2])
            h_cols_hr[0].write("**EMPID**")
            h_cols_hr[1].write("**Group**")
            h_cols_hr[2].write("**Grade**")
            h_cols_hr[3].write("**Risk %**")
            h_cols_hr[4].write("**Actions**")
            st.markdown("---")

            for index, row in mapped_high_risk_df.iterrows():
                cols = st.columns([1, 2, 1, 1, 1.2])
                
                if cols[0].button(str(row['EMPID']), key=f"hr_view_{row['EMPID']}"):
                    st.session_state['selected_empid'] = row['EMPID']
                    st.session_state['current_page'] = "Employee risk indicator"
                    st.rerun()
                    
                cols[1].markdown(f"<span style='color:red; font-weight:500;'>{row['MAIN_GROUP']}</span>", unsafe_allow_html=True)
                cols[2].markdown(f"<span style='color:red'>{row['GRADE']}</span>", unsafe_allow_html=True)
                cols[3].markdown(f"<span style='color:red; font-weight:bold;'>{row['Attrition_Risk_Percentage']:.1f}%</span>", unsafe_allow_html=True)
                
                if cols[4].button("Remarks", key=f"hr_rem_{row['EMPID']}"):
                    st.session_state['remarks_empid'] = row['EMPID']
                    st.session_state['current_page'] = "Feedback Form"
                    st.rerun()
        else:
            st.success("No high-risk pending employee interventions remain in your active work list.")


# --- PAGE 5: FEEDBACK FORM INTERVENTION ---
elif st.session_state['current_page'] == "Feedback Form":
    st.markdown("<h1 class='centered-title'>Feedback Form</h1>", unsafe_allow_html=True)
    
    if not st.session_state['remarks_empid']:
        st.info("Please select an employee ID inside the ER Manager Portal to open the evaluation matrix")
        
        col_nav, _ = st.columns([1.5, 3])
        with col_nav:
            if st.button("Go to ER Portal"):
                st.session_state['current_page'] = "ER Manager Portal"
                st.rerun()
    else:
        target_id = st.session_state['remarks_empid']
        
        if f"success_banner_{target_id}" in st.session_state and st.session_state[f"success_banner_{target_id}"]:
            st.success(st.session_state[f"success_banner_{target_id}"])
            
            col_back, _ = st.columns([2.0, 3.0])
            with col_back:
                if st.button("Return to ER Manager Portal Workspace"):
                    st.session_state[f"success_banner_{target_id}"] = None
                    st.session_state['remarks_empid'] = None
                    st.session_state['current_page'] = "ER Manager Portal"
                    st.rerun()
        else:
            emp_records = df[df['EMPID'] == target_id]
            
            if not emp_records.empty:
                emp_data = emp_records.iloc[0]
                base_pct = emp_data['Attrition_Risk_Percentage']
                base_tier = emp_data['Risk_Level']
                
                st.subheader(f"Questionnaire for EMPID: {target_id}")
                st.markdown(f"**Context Profile:** {emp_data['MAIN_GROUP']} | **Current Baseline:** <span style='color:red; font-weight:bold;'>{base_pct:.1f}% ({base_tier})</span>", unsafe_allow_html=True)
                
                if st.button("Cancel & Return to Dashboard"):
                    st.session_state['remarks_empid'] = None
                    st.session_state['current_page'] = "ER Manager Portal"
                    st.rerun()
                    
                st.divider()
                
                status_selection = st.selectbox("Status", options=["Not Started", "Ongoing", "Completed"], index=2)
                
                with st.form("remarks_capture_form"):
                    st.markdown("##### Score Parameters Matrix")
                    likert_scales = {1: "Dissatisfied", 2: "Somewhat Dissatisfied", 3: "Neutral", 4: "Somewhat Satisfied", 5: "Satisfied"}
                    
                    s_manager = st.radio("Guidance & Support from Manager", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                    s_role = st.radio("Experience in the Current Role", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                    s_team = st.radio("Team & Workplace Environment", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                    s_learning = st.radio("Learning & Training Ecosystem", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                    s_growth = st.radio("Career Growth Opportunities", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                    
                    text_comments = st.text_area("Comments", placeholder="Enter any other remarks ...")
                    
                    submit_form = st.form_submit_button("Submit")
                    
                    if submit_form:
                        weighted_score = (
                            (s_manager * 0.30) + 
                            (s_role * 0.25) + 
                            (s_team * 0.20) + 
                            (s_learning * 0.125) + 
                            (s_growth * 0.125)
                        )
                        
                        if weighted_score >= 4.0:
                            adjusted_risk = base_pct * 0.60
                        elif weighted_score >= 3.0:
                            adjusted_risk = base_pct * 0.85
                        elif weighted_score >= 2.0:
                            adjusted_risk = base_pct * 1.10
                        else:
                            adjusted_risk = base_pct * 1.25
                            
                        adjusted_risk = min(max(adjusted_risk, 0.0), 100.0)
                        adjusted_tier = classify_revised_risk_tier(adjusted_risk)
                        
                        if str(emp_data['GRADE']).strip().upper() in ['ALT', 'CM']:
                            adjusted_risk = min(adjusted_risk, 50.0)
                            adjusted_tier = classify_revised_risk_tier(adjusted_risk)
                        
                        risk_delta = adjusted_risk - base_pct
                        if risk_delta < 0:
                            change_msg = f"decreased by {abs(risk_delta):.2f}%"
                        elif risk_delta > 0:
                            change_msg = f"increased by {risk_delta:.2f}%"
                        else:
                            change_msg = "remained unchanged"
                        
                        st.session_state['master_data'].loc[st.session_state['master_data']['EMPID'] == target_id, 'Attrition_Risk_Percentage'] = adjusted_risk
                        st.session_state['master_data'].loc[st.session_state['master_data']['EMPID'] == target_id, 'Risk_Level'] = adjusted_tier
                        st.session_state['master_data'].loc[st.session_state['master_data']['EMPID'] == target_id, 'Intervention_Status'] = status_selection
                        
                        st.session_state['master_data'].to_csv('SIP Data final_active_cache.csv', index=False)
                        
                        st.session_state[f"success_banner_{target_id}"] = f"Feedback submitted and successfully removed from pending queue. The risk percentage of Emp ID {target_id} {change_msg}."
                        st.rerun()
            else:
                st.error("Error matching requested employee references.")
