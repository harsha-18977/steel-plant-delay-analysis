import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from io import BytesIO
# ==========================================
# LOGIN CHECK
# ==========================================

if "logged_in" not in st.session_state:
    st.switch_page("pages/login.py")

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Department Analysis",
    page_icon="🏭",
    layout="wide"
)

# ==========================================
# DATABASE CONNECTION
# ==========================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vardhansql@004",
    database="steel_delay_analysis"
)

# ==========================================
# HEADER
# ==========================================

st.title("🏭 Department Analysis")

if st.button("⬅ Back To Dashboard"):
    st.switch_page("pages/dashboard.py")

st.markdown("---")

# ==========================================
# SHOP DROPDOWN
# ==========================================

shops_df = pd.read_sql(
    "SELECT * FROM shops",
    connection
)

selected_shop = st.selectbox(
    "Select Department",
    shops_df["shop_name"]
)

# ==========================================
# ANALYSIS QUERY
# ==========================================

query = f"""
SELECT
dr.delay_id,
dr.delay_date,
s.shop_name,
e.equipment_name,
c.conveyor_name,
a.agency_name,
dt.delay_description,
se.season_name,
dr.delay_minutes
FROM delay_records dr
JOIN shops s
ON dr.shop_id=s.shop_id
JOIN equipment e
ON dr.equipment_id=e.equipment_id
JOIN conveyors c
ON dr.conveyor_id=c.conveyor_id
JOIN agencies a
ON dr.agency_id=a.agency_id
JOIN delay_types dt
ON dr.delay_type_id=dt.delay_type_id
JOIN seasons se
ON dr.season_id=se.season_id
WHERE s.shop_name='{selected_shop}'
"""

df = pd.read_sql(
    query,
    connection
)

# ==========================================
# KPI CARDS
# ==========================================

total_delays = len(df)

avg_delay = round(
    df["delay_minutes"].mean(),
    2
)

top_equipment = (
    df["equipment_name"]
    .value_counts()
    .idxmax()
)

k1,k2,k3 = st.columns(3)

k1.metric(
    "Total Delays",
    total_delays
)

k2.metric(
    "Average Delay",
    avg_delay
)

k3.metric(
    "Top Equipment",
    top_equipment
)

st.markdown("---")

# ==========================================
# EQUIPMENT ANALYSIS
# ==========================================

st.subheader("⚙ Equipment Analysis")

equipment_df = (
    df.groupby("equipment_name")
    .size()
    .reset_index(name="Total_Delays")
)

fig = px.bar(
    equipment_df,
    x="equipment_name",
    y="Total_Delays",
    color="equipment_name"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# DELAY TYPE ANALYSIS
# ==========================================

st.subheader("⚠ Delay Type Analysis")

delay_df = (
    df.groupby("delay_description")
    .size()
    .reset_index(name="Total_Delays")
)

fig = px.pie(
    delay_df,
    names="delay_description",
    values="Total_Delays",
    hole=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# DELAY TABLE
# ==========================================

st.subheader("📋 Delay Records")

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

st.markdown("---")

st.subheader("📤 Export Department Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Department CSV",
    data=csv,
    file_name=f"{selected_shop}_report.csv",
    mime="text/csv"
)

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        index=False
    )

st.download_button(
    label="⬇ Download Department Excel",
    data=excel_buffer.getvalue(),
    file_name=f"{selected_shop}_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

connection.close()