import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from fpdf import FPDF
import base64

# --- 1. Creative UI & Professional Fonts ---
st.set_page_config(page_title="Aadhaar Intelligence Hub", layout="wide", page_icon="🆔")

# Injecting Custom CSS for "Inter" font and Glassmorphism UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    
    .main { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); }
    
    /* Glassmorphism Card Effect */
    .stMetric {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #FFFFFF;
        border-radius: 10px;
        color: #64748B;
        border: 1px solid #E2E8F0;
        padding: 10px 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: white !important;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PDF Generator Logic ---
def create_pdf(state_name, total_upd, total_enr, risk_count):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Aadhaar Intelligence Hub - Executive Summary", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Focus Region: {state_name}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Key Metrics:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"- Total Update Activities: {total_upd:,.0f}", ln=True)
    pdf.cell(200, 10, txt=f"- Total New Enrolments: {total_enr:,.0f}", ln=True)
    pdf.cell(200, 10, txt=f"- High-Risk Districts Identified: {risk_count}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, txt="Disclaimer: This report is generated based on historical data trends and predictive modeling for resource allocation optimization.")
    return pdf.output(dest='S').encode('latin-1')

# --- 3. Data Engine ---
@st.cache_resource
def get_connection():
    return sqlite3.connect('aadhaar_analysis.db', check_same_thread=False)

conn = get_connection()

# --- 4. Sidebar: Regional Control & PDF Download ---
with st.sidebar:
    st.image("https://uidai.gov.in/images/logo/aadhaar_english_logo.svg", width=160)
    st.markdown("### **Regional Control**")
    try:
        states = pd.read_sql("SELECT DISTINCT state FROM aadhaar_stats ORDER BY state", conn)['state'].tolist()
        selected_state = st.selectbox("Select State", states, index=states.index("Maharashtra") if "Maharashtra" in states else 0)
    except:
        st.error("⚠️ Database missing. Run builder script first.")
        st.stop()
    
    st.divider()
    st.markdown("### **Administrative Tools**")
    
    # Pre-calculating Data for PDF
    query_raw = f"SELECT * FROM aadhaar_stats WHERE state = '{selected_state}'"
    df_pdf = pd.read_sql(query_raw, conn)
    pdf_upd = df_pdf[['bio_age_5_17', 'bio_age_17_', 'demo_age_5_17', 'demo_age_17_']].sum().sum()
    pdf_enr = df_pdf['age_0_5'].sum()
    pdf_risk = len(df_pdf[df_pdf[['bio_age_5_17', 'bio_age_17_']].sum(axis=1) > 2000]['district'].unique())

    # Download Button Logic
    pdf_bytes = create_pdf(selected_state, pdf_upd, pdf_enr, pdf_risk)
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name=f"Aadhaar_Briefing_{selected_state}.pdf",
        mime="application/pdf"
    )

    st.divider()
    st.markdown("🔒 **System Integrity: High**")
    st.caption("AI-Powered Resource Allocation")

# --- 5. Main Analytics Engine ---
query = f"SELECT * FROM aadhaar_stats WHERE state = '{selected_state}'"
df = pd.read_sql(query, conn)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
df['total_activity'] = df[['bio_age_5_17', 'bio_age_17_', 'demo_age_5_17', 'demo_age_17_']].sum(axis=1)

# --- 6. Visual Command Center ---
st.title("🛡️ Aadhaar Intelligence Hub")
st.markdown(f"**Operational Intelligence for {selected_state}**")

# Interactive Metric Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("ASK Workload", f"{df['total_activity'].sum():,.0f}", "Live")
m2.metric("MBU Requirement", f"{df['bio_age_5_17'].sum():,.0f}", "-12% Gap")
m3.metric("Avg Enrolment", f"{int(df['age_0_5'].mean()):,.0f}", "Daily")
m4.metric("Risk Zones", pdf_risk, "⚠️ High Load")

st.markdown("---")

# --- 7. The Functional Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Performance Insights", "🚚 Fleet Deployment", "📅 Surge Forecasting"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### **Regional Demand Heatmap**")
        map_data = df.groupby('district')['total_activity'].sum().reset_index()
        fig_map = px.sunburst(map_data, path=['district'], values='total_activity',
                             color='total_activity', color_continuous_scale='Blues')
        fig_map.update_layout(margin=dict(t=0, l=0, r=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        st.markdown("#### **Digital Divide (MBU Gap)**")
        gap_data = df.groupby('district')[['age_0_5', 'bio_age_5_17']].sum().reset_index()
        fig_gap = px.bar(gap_data.nlargest(8, 'age_0_5'), x='district', y=['age_0_5', 'bio_age_5_17'],
                        barmode='group', color_discrete_sequence=['#3B82F6', '#EF4444'])
        st.plotly_chart(fig_gap, use_container_width=True)

with tab2:
    st.markdown("#### **🚚 Strategic Mobile Van Planner**")
    van_df = df.groupby('district').agg({'age_0_5':'sum', 'bio_age_5_17':'sum', 'total_activity':'mean'}).reset_index()
    van_df['Priority'] = (van_df['age_0_5'] - van_df['bio_age_5_17']).clip(lower=0) * (van_df['total_activity'] / 100)
    top_vans = van_df.nlargest(4, 'Priority')
    
    cols = st.columns(4)
    for i, (idx, row) in enumerate(top_vans.iterrows()):
        with cols[i]:
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 10px; border-left: 5px solid #F59E0B; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <p style="margin:0; color: #6B7280; font-size: 0.8rem;">Priority Route {i+1}</p>
                <h4 style="margin:0;">{row['district']}</h4>
                <p style="margin:0; color: #EF4444; font-weight: bold;">Priority Score: {row['Priority']:.0f}</p>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("#### **🚀 Predictive Traffic Gauge**")
    day_avg = df.groupby(df['date'].dt.day_name())['total_activity'].mean().reset_index()
    current_day = datetime.now().strftime('%A')
    day_load = day_avg[day_avg['date'] == current_day]['total_activity'].values[0] if current_day in day_avg['date'].values else 1000
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta", value = day_load,
        title = {'text': f"System Load: {current_day}"},
        gauge = {'axis': {'range': [None, 5000]},
                 'bar': {'color': "#2563EB"},
                 'steps' : [{'range': [0, 2500], 'color': "#D1FAE5"},
                            {'range': [2500, 4000], 'color': "#FEF3C7"},
                            {'range': [4000, 5000], 'color': "#FEE2E2"}]}))
    st.plotly_chart(fig_gauge, use_container_width=True)