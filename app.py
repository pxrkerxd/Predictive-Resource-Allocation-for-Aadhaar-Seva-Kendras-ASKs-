import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- 1. Page & UI Styling ---
st.set_page_config(page_title="Aadhaar Intelligence Hub", layout="wide", page_icon="🆔")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .stTab { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Connection ---
@st.cache_resource
def get_connection():
    return sqlite3.connect('aadhaar_analysis.db', check_same_thread=False)

conn = get_connection()

# --- 3. Sidebar Navigation ---
with st.sidebar:
    st.image("https://uidai.gov.in/images/logo/aadhaar_english_logo.svg", width=180)
    st.title("Command Center")
    try:
        states = pd.read_sql("SELECT DISTINCT state FROM aadhaar_stats ORDER BY state", conn)['state'].tolist()
        selected_state = st.selectbox("Select State", states, index=states.index("Maharashtra") if "Maharashtra" in states else 0)
        st.divider()
        st.success("System Status: Online")
    except:
        st.error("Database not found. Run db_builder.py first.")
        st.stop()

# --- 4. Main Data Processing ---
query = f"SELECT * FROM aadhaar_stats WHERE state = '{selected_state}'"
df = pd.read_sql(query, conn)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
df['total_activity'] = df[['bio_age_5_17', 'bio_age_17_', 'demo_age_5_17', 'demo_age_17_']].sum(axis=1)

# --- 5. Dashboard Header ---
st.title("🛡️ Aadhaar Seva Kendra Intelligence Hub")
st.subheader(f"Regional Analytics & Deployment Strategy: {selected_state}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total ASK Load", f"{df['total_activity'].sum():,.0f}")
m2.metric("New Enrolments", f"{df['age_0_5'].sum():,.0f}")
m3.metric("MBU Requirement", f"{df['bio_age_5_17'].sum():,.0f}")
m4.metric("Active Districts", len(df['district'].unique()))

st.divider()

# --- 6. Functional Tabs ---
tab_map, tab_predict, tab_gap, tab_van, tab_raw = st.tabs([
    "🌍 Geospatial Map", "🚀 Predictive Allocation", "👶 MBU Gap Analysis", "🚚 Mobile Van Planner", "📋 Raw Data"
])

# -- Tab 1: Map --
with tab_map:
    map_data = pd.read_sql("SELECT state, SUM(total_activity) as demand FROM (SELECT state, (bio_age_5_17 + bio_age_17_ + demo_age_5_17 + demo_age_17_) as total_activity FROM aadhaar_stats) GROUP BY state", conn)
    fig_map = px.treemap(map_data, path=['state'], values='demand', color='demand', color_continuous_scale='OrRd')
    st.plotly_chart(fig_map, use_container_width=True)

# -- Tab 2: Predict --
with tab_predict:
    df['day_name'] = df['date'].dt.day_name()
    prediction = df.groupby(['district', 'day_name'])['total_activity'].mean().reset_index()
    selected_day = st.select_slider("Select Forecast Day", options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    pred_day = prediction[prediction['day_name'] == selected_day].nlargest(10, 'total_activity')
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.plotly_chart(px.bar(pred_day, x='total_activity', y='district', orientation='h', color='total_activity'), use_container_width=True)
    with col_b:
        st.subheader("System Stress Gauge")
        avg_load = pred_day['total_activity'].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = avg_load,
            gauge = {'axis': {'range': [None, 5000]}, 'bar': {'color': "black"},
                     'steps' : [{'range': [0, 2000], 'color': "green"}, {'range': [2000, 4000], 'color': "orange"}, {'range': [4000, 5000], 'color': "red"}]}))
        st.plotly_chart(fig_gauge, use_container_width=True)

# -- Tab 3: Gap --
with tab_gap:
    gap_df = df.groupby('district')[['age_0_5', 'bio_age_5_17']].sum().reset_index()
    gap_df['Gap_Score'] = (gap_df['age_0_5'] - gap_df['bio_age_5_17']).clip(lower=0)
    st.plotly_chart(px.scatter(gap_df, x='age_0_5', y='bio_age_5_17', size='Gap_Score', color='Gap_Score', text='district'), use_container_width=True)

# -- Tab 4: NEW - Mobile Van Route Logic --
with tab_van:
    st.header("🚚 Strategic Mobile Van Deployment")
    st.info("Logic: Districts with high Enrolment-to-Update Gap and high density are prioritized.")
    
    # Calculate Deployment Priority
    van_df = df.groupby('district').agg({
        'age_0_5': 'sum',
        'bio_age_5_17': 'sum',
        'total_activity': 'mean'
    }).reset_index()
    
    van_df['Gap_Percentage'] = ((van_df['age_0_5'] - van_df['bio_age_5_17']) / van_df['age_0_5'] * 100).clip(lower=0)
    # Score = (Gap %) * (Volume Density)
    van_df['Priority_Score'] = (van_df['Gap_Percentage'] * van_df['total_activity']) / 100
    
    top_van = van_df.nlargest(5, 'Priority_Score')
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Top Priority Routes")
        for i, row in top_van.iterrows():
            st.error(f"📍 **Route {i+1}: {row['district']}**\nPriority Score: {row['Priority_Score']:.1f}")
            st.caption(f"Reason: {row['Gap_Percentage']:.1f}% MBU Gap discovered.")
            
    with c2:
        fig_van = px.funnel(top_van, x='Priority_Score', y='district', title="Mobile Van Deployment Funnel")
        st.plotly_chart(fig_van, use_container_width=True)

# -- Tab 5: Raw --
with tab_raw:
    st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)