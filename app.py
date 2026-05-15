import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('Attrition.csv')
    return df

df = load_data()

# Helper function to generate reasons and actionables (Placeholder logic)
def get_insights(row):
    reasons = []
    actions = []
    
    if row['Distance_From_Home_KM'] > 1000:
        reasons.append("High Distance from Home")
        actions.append("Discuss remote work options or relocation assistance.")
    if row['TENURE_YRS'] < 2:
        reasons.append("Early Career/Low Tenure")
        actions.append("Assign a mentor and conduct a 30-60-90 day feedback session.")
    if row['Attrition_Risk_Percentage'] > 70:
        reasons.append("High Statistical Probability (ML Model)")
        actions.append("Immediate 1-on-1 meeting to discuss career growth and pain points.")
    
    if not reasons:
        reasons = ["General Market Factors"]
        actions = ["Regular engagement and performance recognition."]
        
    return ", ".join(reasons), ", ".join(actions)

# Initialize Session State for Navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'ER_Login'
if 'selected_empid' not in st.session_state:
    st.session_state['selected_empid'] = None

# --- PAGE 2: EMPLOYEE RISK PREDICTOR (Detail View) ---
def show_employee_details(empid):
    st.button("⬅️ Back to ER Dashboard", on_click=lambda: st.session_state.update({"current_page": "ER_Login"}))
    
    emp_data = df[df['EMPID'] == empid].iloc[0]
    reason, actionables = get_insights(emp_data)
    
    st.title(f"Employee Risk Predictor: {empid}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Risk Percentage", f"{emp_data['Attrition_Risk_Percentage']}%")
    col2.metric("Risk Level", emp_data['Risk_Level'])
    col3.metric("Tenure", f"{emp_data['TENURE_YRS']} Yrs")

    st.subheader("Employee Profile")
    st.json({
        "Grade": emp_data['GRADE'],
        "Location": emp_data['Work_Location'],
        "Zone": emp_data['ZONE'],
        "Main Group": emp_data['MAIN_GROUP']
    })

    st.error(f"**Primary Reason for Risk:** {reason}")
    st.success(f"**Recommended Actionables:** {actionables}")

# --- PAGE 3: ER LOGIN ---
def show_er_login():
    st.title("ER Manager Login")
    
    manager_id = st.number_input("Enter your ER Manager ID", min_value=0, step=1, value=0)
    
    if st.button("Search"):
        if manager_id in df['ER manager ID'].values:
            st.session_state['manager_logged_in'] = manager_id
            st.success(f"Welcome, Manager {manager_id}")
        else:
            st.error("Manager ID not found.")

    if 'manager_logged_in' in st.session_state:
        mid = st.session_state['manager_logged_in']
        manager_df = df[df['ER manager ID'] == mid]
        high_risk_count = len(manager_df[manager_df['Risk_Level'] == 'High'])
        
        st.divider()
        st.subheader(f"Dashboard for Manager ID: {mid}")
        
        # Display Summary Metric
        st.metric("Total Employees in High Risk Category", high_risk_count)
        
        # Button to show the list
        if st.button("View High Risk Employees List"):
            st.session_state['show_list'] = True
            
        if st.session_state.get('show_list'):
            high_risk_list = manager_df[manager_df['Risk_Level'] == 'High']
            
            if not high_risk_list.empty():
                st.write("Click on an Employee ID to view detailed risk analysis:")
                
                # Create a list of buttons for each employee
                for index, row in high_risk_list.iterrows():
                    emp_id = row['EMPID']
                    risk_pct = row['Attrition_Risk_Percentage']
                    
                    # Using columns to make it look like a list
                    c1, c2, c3 = st.columns([2, 2, 1])
                    c1.write(f"**EMPID:** {emp_id}")
                    c2.write(f"**Risk:** {risk_pct}%")
                    if c3.button("View Details", key=f"btn_{emp_id}"):
                        st.session_state['selected_empid'] = emp_id
                        st.session_state['current_page'] = 'Risk_Predictor'
                        st.rerun()
            else:
                st.info("No high-risk employees mapped to your ID.")

# --- MAIN APP LOGIC ---
if st.session_state['current_page'] == 'ER_Login':
    show_er_login()
elif st.session_state['current_page'] == 'Risk_Predictor':
    show_employee_details(st.session_state['selected_empid'])
