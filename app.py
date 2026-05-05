import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ICICI Brand Color Palette
ICICI_CRIMSON = "#B02A30"
ICICI_ORANGE = "#F99D27"
ICICI_BLUE = "#005B75"
WHITE = "#FFFFFF"

# Risk Colors
RED = "#FF3131"
YELLOW = "#FFD700"
GREEN = "#2ECC71"

st.set_page_config(page_title="ICICI Attrition Sentinel", layout="wide")

# Custom CSS for ICICI Styling
st.markdown(f"""
    <style>
    .main {{ background-color: #F4F7F9; }}
    [data-testid="stSidebar"] {{
        background-color: {ICICI_ORANGE};
    }}
    [data-testid="stSidebar"] .st-emotion-cache-10trblm {{
        color: {WHITE};
    }}
    h1, h2 {{ color: {ICICI_BLUE}; font-family: 'Arial'; font-weight: bold; }}
    h3 {{ color: {ICICI_CRIMSON}; }}
    .big-font {{ font-size: 80px !important; font-weight: bold; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_and_model():
    # File name referenced verbatim
    df = pd.read_csv('final_attrition_dataset_500_v4_lateral.csv')
    le = LabelEncoder()
    df['GRADE_ID'] = le.fit_transform(df['GRADE'])
    df['GROUP_ID'] = le.fit_transform(df['MAIN_GROUP'])
    df['ZONE_ID'] = le.fit_transform(df['ZONE'])
    
    X = df[['AGE', 'TENURE_YRS', 'GRADE_ID', 'GROUP_ID', 'ZONE_ID']]
    y = df['ATTRITION']
    
    # Model uses min_samples_leaf to prevent 0% attrition scores
    rf = RandomForestClassifier(n_estimators=200, min_samples_leaf=8, random_state=42)
    rf.fit(X, y)
    
    raw_probs = rf.predict_proba(X)[:, 1] * 100
    # Ensuring risk is never 0
    df['Risk_Score'] = np.clip(raw_probs, 1.5, 98.5).round(2)
    
    # Define Risk Categories
    df['Risk_Category'] = df['Risk_Score'].apply(
        lambda x: 'High' if x >= 75 else ('Medium' if x >= 40 else 'Low')
    )
    return df

df = load_and_model()

# --- SIDEBAR ---
st.sidebar.title("ICICI Sentinel")
page = st.sidebar.radio("Go To:", ["Zone wise turnover prediction", "Employee risk indicator"])

# --- PAGE 1: ZONE WISE TURNOVER PREDICTION ---
if page == "Zone wise turnover prediction":
    st.title("🏙️ Zone wise turnover prediction")
    st.markdown("### Regional Risk Distribution Analysis")
    
    zones = ["North", "East", "West", "South"]
    rows = [st.columns(2), st.columns(2)]
    
    for idx, zone in enumerate(zones):
        with rows[idx // 2][idx % 2]:
            st.subheader(f"📍 {zone} Zone")
            
            zone_df = df[df['ZONE'] == zone]
            counts = zone_df['Risk_Category'].value_counts(normalize=True) * 100
            
            plot_data = pd.Series({'High': 0.0, 'Medium': 0.0, 'Low': 0.0})
            plot_data.update(counts)
            
            fig, ax = plt.subplots(figsize=(6, 4))
            categories = ['High', 'Medium', 'Low']
            values = [plot_data['High'], plot_data['Medium'], plot_data['Low']]
            colors = [RED, YELLOW, GREEN]
            
            bars = ax.bar(categories, values, color=colors, edgecolor=ICICI_BLUE, linewidth=1.5)
            
            ax.set_facecolor('#F4F7F9')
            fig.patch.set_facecolor('#F4F7F9')
            ax.set_ylabel('Percentage of Employees (%)', color=ICICI_BLUE, fontweight='bold')
            ax.set_ylim(0, 100)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                        f'{height:.1f}%', ha='center', va='bottom', 
                        fontweight='bold', color=ICICI_BLUE)

            plt.tight_layout()
            st.pyplot(fig)

# --- PAGE 2: EMPLOYEE RISK INDICATOR ---
elif page == "Employee risk indicator":
    st.title("👤 Employee risk indicator")
    
    emp_id = st.number_input("Enter Employee ID", min_value=0, step=1)
    
    if emp_id:
        user_data = df[df['EMPID'] == emp_id]
        if not user_data.empty:
            score = user_data['Risk_Score'].values[0]
            cat = user_data['Risk_Category'].values[0]
            
            # Colour logic for Individual Score
            if cat == 'High':
                hex_color = RED
            elif cat == 'Medium':
                hex_color = YELLOW
            else:
                hex_color = GREEN
            
            st.markdown(f"<p class='big-font' style='color: {hex_color};'>{score}%</p>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: {hex_color};'>{cat.upper()} RISK</h2>", unsafe_allow_html=True)
            
            st.divider()
            
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("💡 Analysis Factors")
                st.write(f"**Tenure:** {user_data['TENURE_YRS'].values[0]} Years")
                st.write(f"**Grade:** {user_data['GRADE'].values[0]}")
                st.write(f"**Age:** {user_data['AGE'].values[0]}")
                st.write(f"**Group:** {user_data['MAIN_GROUP'].values[0]}")
            
            with c2:
                st.subheader("🚀 Actionables")
                if cat == 'High':
                    st.write("* **ER manager should contact and understand career aspirations.**")
                    st.write("* **Evaluate for immediate retention or role enrichment.**")
                elif cat == 'Medium':
                    st.write("* **Schedule skip-level meeting to discuss growth.**")
                else:
                    st.write("* **Nominate for internal reward programs.**")
        else:
            st.error("Employee ID not found.")
