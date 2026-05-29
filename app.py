import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="iRetain | Workforce Analytics", layout="wide")

# --- 2. REFINED PROFESSIONAL UI CSS ---
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; color: #333333; }
    [data-testid="stSidebar"] { background-color: #f37021; }
    [data-testid="stSidebar"] .st-emotion-cache-10trblm { color: white; }
    
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

    /* Button Styling */
    div.stButton > button { background-color: #f37021 !important; color: white !important; border-radius: 4px; border: none; width: 100%; font-weight: 600; }
    .large-btn-container div.stButton > button { padding: 15px 10px !important; font-size: 18px !important; height: 60px !important; }
    .small-btn-container div.stButton > button { padding: 5px !important; font-size: 13px !important; height: auto !important; margin-bottom: 8px; }
    
    .chart-container { padding: 5px; }
    </style>
    """, unsafe_allow_html=True)


# --- 3. AUTOMATED PORTFOLIO TRIGGER ENGINE ---
def run_portfolio_trigger_check(df, manager_id):
    """
    Evaluates whether the ER Manager's portfolio average risk has risen significantly.
    Compiles the top 10 highest risk employees if criteria are satisfied.
    """
    manager_portfolio = df[df['ER manager ID'] == manager_id]
    if len(manager_portfolio) == 0:
        return
        
    avg_portfolio_risk = manager_portfolio['Attrition_Risk_Percentage'].mean()
    
    # Automated system warning threshold
    if avg_portfolio_risk > 40.0:
        top_10_high_risk = manager_portfolio.sort_values(by='Attrition_Risk_Percentage', ascending=False).head(10)
        
        table_rows = ""
        for _, row in top_10_high_risk.iterrows():
            table_rows += f"""
            <tr>
                <td style='border: 1px solid #dddddd; padding: 8px;'>{row['EMPID']}</td>
                <td style='border: 1px solid #dddddd; padding: 8px;'>{row['MAIN_GROUP']}</td>
                <td style='border: 1px solid #dddddd; padding: 8px;'>{row['GRADE']}</td>
                <td style='border: 1px solid #dddddd; padding: 8px; color: red; font-weight: bold;'>{row['Attrition_Risk_Percentage']:.1f}%</td>
            </tr>
            """
            
        st.warning(f"System Trigger Notification Issued: ER Manager portfolio average risk is {avg_portfolio_risk:.1f}%. ER Manager must intervene immediately.")
        
        # --- PRODUCTION MAILING CONFIGURATION BLOCK ---
        # msg = MIMEMultipart('alternative')
        # msg['Subject'] = f"IMMEDIATE INTERVENTION REQUIRED: High Risk Portfolio Alert (Manager ID: {manager_id})"
        # msg['From'] = "hr-alerts@company.com"
        # msg['To'] = f"manager_{manager_id}@company.com"


# --- 4. DATA LOADING & STATE SESSION INITIALIZATION ---
@st.cache_data
def load_base_data():
    file_path = 'Attrition11 (2).xlsx'
    if not os.path.exists(file_path):
        st.error(f"File Not Found: {file_path}")
        st.stop()
    df = pd.read_excel(file_path, sheet_name=0)
    df.columns = df.columns.str.strip()
    return df

# Initialize Session Dataframe if not yet declared to allow data updates
if 'master_data' not in st.session_state:
    st.session_state['master_data'] = load_base_data()

df = st.session_state['master_data']

# App Navigation Variables
if 'view_mode' not in st.session_state: st.session_state['view_mode'] = 'Percentage'
if 'risk_filter' not in st.session_state: st.session_state['risk_filter'] = 'High'
if 'current_page' not in st.session_state: st.session_state['current_page'] = "Zone wise turnover prediction"
if 'selected_empid' not in st.session_state: st.session_state['selected_empid'] = None
if 'remarks_empid' not in st.session_state: st.session_state['remarks_empid'] = None
if 'current_manager_id' not in st.session_state: st.session_state['current_manager_id'] = None


# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.title("iRETAIN")
st.sidebar.markdown("---")
page_options = ["Zone wise turnover prediction", "Employee risk indicator", "ER Manager Portal", "Remarks"]
selected_sidebar = st.sidebar.radio("NAVIGATION", page_options, 
                                    index=page_options.index(st.session_state['current_page']))

if selected_sidebar != st.session_state['current_page']:
    st.session_state['current_page'] = selected_sidebar
    if selected_sidebar != "Employee risk indicator" and selected_sidebar != "Remarks":
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


# --- PAGE 2: EMPLOYEE RISK INDICATOR ---
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
                st.write(f"**Work Location:** {row.get('Work_Location', row.get('Office_Location', 'N/A'))}")
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
                if level == 'High':
                    if 3 <= tenure <= 5:
                        st.write("• Profile falls within Critical Attrition Window (3-5 years).")
                    elif tenure > 10:
                        st.write(f"• Long-tenure fatigue ({int(tenure)} years); may require role rotation.")
                    else:
                        st.write("• High-risk markers detected in historical modeling.")
                    
                    if row.get('AGE', 0) < 30:
                        st.write("• Vulnerable age segment (<30 years) with high market mobility.")
                    if row.get('Distance From Home (KM)', row.get('Distance_From_Home_KM', 0)) > 1000:
                        st.write(f"• Extreme commute stress detected ({row.get('Distance From Home (KM)', row.get('Distance_From_Home_KM', 0))} KM).")
                elif level == 'Medium':
                    st.write("• Mid-tenure engagement dip detected.")
                else: 
                    st.write("• Stable organizational anchoring.")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"<div class='report-card' style='border-left-color: {h_color};'><h4>Mitigation Actionables</h4>", unsafe_allow_html=True)
                if level == 'High': 
                    st.write("• **ER Intervention:** Urgent 1:1 visit required.")
                    st.write("• **Retention Talk:** Discuss internal mobility and role rotation.")
                elif level == 'Medium':
                    st.write("• **Structured Connect:** ER Manager confidential 1:1.")
                else: 
                    st.write("• **Appreciation:** Nominate for performance award.")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- NATIVE DIALER IMPLEMENTATION ---
            st.divider()
            st.write("#### Action Center")
            mock_phone = f"+9198765{str(int(row['EMPID']))[-5:]}" if not pd.isna(row['EMPID']) else "+919999999999"
            
            col_call, _ = st.columns([1.5, 3])
            with col_call:
                st.markdown(
                    f"""
                    <a href="tel:{mock_phone}" style="text-decoration: none;">
                        <div style="background-color: #003366; color: white; text-align: center; 
                                    padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer;">
                            Call Employee ({mock_phone})
                        </div>
                    </a>
                    """, 
                    unsafe_allow_html=True
                )
        else: st.error("EMPID not found.")


# --- PAGE 3: ER MANAGER PORTAL ---
elif st.session_state['current_page'] == "ER Manager Portal":
    st.markdown("<h1 class='centered-title'>ER Manager Portal</h1>", unsafe_allow_html=True)
    er_id = st.number_input("Enter ER Manager ID", min_value=0, step=1, value=st.session_state['current_manager_id'] if st.session_state['current_manager_id'] else 0)
    
    if er_id:
        st.session_state['current_manager_id'] = er_id
        if 'ER manager ID' in df.columns and er_id in df['ER manager ID'].values:
            manager_df = df[df['ER manager ID'] == er_id]
            
            # Execute email alarm check logic automatically
            run_portfolio_trigger_check(df, er_id)

            mapped_total = len(manager_df)
            mapped_high_risk_df = manager_df[manager_df['Risk_Level'] == 'High'].sort_values(by='Attrition_Risk_Percentage', ascending=False)
            mapped_high_risk_count = len(mapped_high_risk_df)
            mapped_high_risk_pct = (mapped_high_risk_count / mapped_total * 100) if mapped_total > 0 else 0
            
            st.markdown("<div class='section-header'>Portfolio High Risk Profiling</div>", unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f"<div class='metric-container'><div class='metric-label'>Employees Mapped</div><div class='metric-value'>{mapped_total}</div></div>", unsafe_allow_html=True)
            with m2: st.markdown(f"<div class='metric-container'><div class='metric-label'>High Risk Count</div><div class='metric-value'>{mapped_high_risk_count}</div></div>", unsafe_allow_html=True)
            with m3: st.markdown(f"<div class='metric-container'><div class='metric-label'>High Risk (%)</div><div class='metric-value'>{mapped_high_risk_pct:.1f}%</div></div>", unsafe_allow_html=True)

            st.divider()
            
            # Implementation of requested view separations using conditional Tabs
            tab_all, tab_high_risk = st.tabs(["Active Portfolio Registry", "Show high risk employees tab"])
            
            with tab_all:
                st.write("#### Active Portfolio Registry")
                portfolio_selection = manager_df.sort_values(by='Attrition_Risk_Percentage', ascending=False)
                
                if not portfolio_selection.empty:
                    h_cols = st.columns([1, 2, 1, 1, 1.2])
                    h_cols[0].write("**EMPID**")
                    h_cols[1].write("**Group**")
                    h_cols[2].write("**Grade**")
                    h_cols[3].write("**Risk %**")
                    h_cols[4].write("**Actions**")
                    st.markdown("---")

                    for index, row in portfolio_selection.iterrows():
                        cols = st.columns([1, 2, 1, 1, 1.2])
                        r_color = "red" if row['Risk_Level'] == "High" else ("#FFCC00" if row['Risk_Level'] == "Medium" else "green")
                        
                        if cols[0].button(str(row['EMPID']), key=f"p_view_{row['EMPID']}"):
                            st.session_state['selected_empid'] = row['EMPID']
                            st.session_state['current_page'] = "Employee risk indicator"
                            st.rerun()
                            
                        cols[1].markdown(f"<span style='color:{r_color}; font-weight:500;'>{row['MAIN_GROUP']}</span>", unsafe_allow_html=True)
                        cols[2].markdown(f"<span style='color:{r_color}'>{row['GRADE']}</span>", unsafe_allow_html=True)
                        cols[3].markdown(f"<span style='color:{r_color}; font-weight:bold;'>{row['Attrition_Risk_Percentage']:.1f}%</span>", unsafe_allow_html=True)
                        
                        if cols[4].button("Remarks", key=f"rem_{row['EMPID']}"):
                            st.session_state['remarks_empid'] = row['EMPID']
                            st.session_state['current_page'] = "Remarks"
                            st.rerun()
                else:
                    st.success("No active employees mapped to your portfolio.")
                    
            with tab_high_risk:
                st.write("#### Critical Portfolio Hotspots")
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
                            st.session_state['current_page'] = "Remarks"
                            st.rerun()
                else:
                    st.success("No high-risk employees mapped to your portfolio.")
        else: st.error("Manager ID not found.")


# --- PAGE 4: REMARKS INTERVENTION FORM & DYNAMIC RECALIBRATION ---
elif st.session_state['current_page'] == "Remarks":
    st.markdown("<h1 class='centered-title'>Remarks</h1>", unsafe_allow_html=True)
    
    if not st.session_state['remarks_empid']:
        st.info("Please select an employee inside the ER Manager Portal to access active remarks entries.")
        if st.button("Go to ER Portal"):
            st.session_state['current_page'] = "ER Manager Portal"
            st.rerun()
    else:
        target_id = st.session_state['remarks_empid']
        emp_records = df[df['EMPID'] == target_id]
        
        if not emp_records.empty:
            emp_data = emp_records.iloc[0]
            base_pct = emp_data['Attrition_Risk_Percentage']
            base_tier = emp_data['Risk_Level']
            
            st.subheader(f"Pulse Questionnaire for EMPID: {target_id}")
            st.markdown(f"**Context Profile:** {emp_data['MAIN_GROUP']} | **Current Baseline:** <span style='color:red; font-weight:bold;'>{base_pct:.1f}% ({base_tier})</span>", unsafe_allow_html=True)
            
            if st.button("Cancel & Return to Dashboard"):
                st.session_state['current_page'] = "ER Manager Portal"
                st.rerun()
                
            st.divider()
            
            with st.form("remarks_capture_form"):
                status_dropdown = st.selectbox("Status", options=["Not started", "Ongoing", "Completed"])
                
                st.markdown("##### Parameter Metrics")
                likert_scales = {1: "Dissatisfied", 2: "Somewhat Dissatisfied", 3: "Neutral", 4: "Somewhat Satisfied", 5: "Satisfied"}
                
                # Labels cleaned up: Weights and explicit references to the word "Feedback" removed
                s_manager = st.radio("Manager", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                s_role = st.radio("Role", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                s_team = st.radio("Team & Workplace Relationships", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                s_learning = st.radio("Learning & Training", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                s_growth = st.radio("Career Growth Opportunities", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_scales[x], horizontal=True, index=2)
                
                text_comments = st.text_area("Manager Notes", placeholder="Enter notes from conversation here...")
                
                submit_form = st.form_submit_button("Submit")
                
                if submit_form:
                    # Priority-Weighted Score Logic (Manager: 30%, Role: 25%, Team: 20%, others: 12.5% each)
                    weighted_score = (
                        (s_manager * 0.30) + 
                        (s_role * 0.25) + 
                        (s_team * 0.20) + 
                        (s_learning * 0.125) + 
                        (s_growth * 0.125)
                    )
                    
                    # Risk mitigation modifier application based on status parameters
                    if status_dropdown == "Completed":
                        if weighted_score >= 4.0:
                            adjusted_risk = base_pct * 0.35   # Major risk drop for excellent sentiment
                        elif weighted_score >= 2.8:
                            adjusted_risk = base_pct * 0.60   # Moderate risk drop
                        else:
                            adjusted_risk = base_pct * 0.85   # Minor drop for low fulfillment resolutions
                    elif status_dropdown == "Ongoing":
                        adjusted_risk = base_pct * 0.80       # Uniform 20% drop during open intervention
                    else:
                        adjusted_risk = base_pct              # Unaltered if not started
                        
                    # Enforce data limits
                    adjusted_risk = min(max(adjusted_risk, 0.0), 100.0)
                    
                    # Recalculate operational risk tier thresholds
                    if adjusted_risk < 30.0:
                        adjusted_tier = "Low"
                    elif adjusted_risk < 60.0:
                        adjusted_tier = "Medium"
                    else:
                        adjusted_tier = "High"
                        
                    # Update active session configuration states
                    st.session_state['master_data'].loc[st.session_state['master_data']['EMPID'] == target_id, 'Attrition_Risk_Percentage'] = adjusted_risk
                    st.session_state['master_data'].loc[st.session_state['master_data']['EMPID'] == target_id, 'Risk_Level'] = adjusted_tier
                    
                    st.success(f"Form submitted. Updated attrition risk score for EMPID {target_id} dropped from {base_pct:.1f}% to {adjusted_risk:.1f}% ({adjusted_tier}).")
        else:
            st.error("Error matching requested employee data references.")
