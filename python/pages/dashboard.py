import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from io import BytesIO

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Steel Plant Delay Analysis",
    page_icon="🏭",
    layout="wide"
)

# ==========================================
# LOGIN CHECK
# ==========================================

if "logged_in" not in st.session_state:

    st.switch_page("pages/login.py")

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Hide Streamlit Elements */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

section[data-testid="stSidebar"] {
    display: none;
}

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #f5f7fa,
        #dfe9f3
    );
}

/* KPI Cards */
div[data-testid="metric-container"] {

    background: linear-gradient(
        135deg,
        #003366,
        #0059b3
    );

    padding: 20px;

    border-radius: 20px;

    box-shadow: 0px 8px 20px rgba(0,0,0,0.2);

    color: white;

    border-left: 6px solid #FFD700;
}

/* KPI Text */
div[data-testid="metric-container"] label {

    color: white !important;

    font-weight: bold;
}

/* Buttons */
.stButton > button {

    background: linear-gradient(
        135deg,
        #0059b3,
        #0099ff
    );

    color: white;

    border-radius: 12px;

    border: none;

    font-weight: bold;

    height: 50px;

    transition: 0.3s;
}

.stButton > button:hover {

    background: linear-gradient(
        135deg,
        #003366,
        #0059b3
    );

    transform: scale(1.03);
}

/* Select Boxes */
.stSelectbox {

    background: white;

    border-radius: 10px;
}

/* Dataframe */
[data-testid="stDataFrame"] {

    border-radius: 15px;

    overflow: hidden;

    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}

/* Headers */
h1 {

    color: #003366 !important;

    font-weight: bold;
}

h2, h3 {

    color: #0059b3 !important;
}

/* Recommendation Box */
.stAlert {

    border-radius: 15px;
}

/* Charts Container */
.element-container {

    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

logo_col,title_col,user_col = st.columns([1,5,1])

with logo_col:

    st.image(
        "assets/Rashtriya_Ispat_Nigam.svg",
        width=90
    )

with title_col:

    st.title(
        "Steel Plant Delay Analysis & Prediction System"
    )

    st.caption(
        "Rashtriya Ispat Nigam Limited (Vizag Steel)"
    )

with user_col:

    st.write("")

    st.write("")

    st.write(
        f"👤 {st.session_state.username}"
    )

# ==========================================
# NAVIGATION BAR
# ==========================================

nav1,nav2,nav3,nav4,nav5 = st.columns(5)

with nav1:

    st.button(
        "📊 Dashboard",
        use_container_width=True
    )

with nav2:

    if st.button(
        "➕ Add Delay",
        use_container_width=True
    ):
        st.switch_page(
            "pages/add_delay.py"
        )

with nav3:

    if st.button(
        "🏭 Department Analysis",
        use_container_width=True
    ):
        st.switch_page(
            "pages/department_analysis.py"
        )

with nav4:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.clear()

        st.switch_page(
            "pages/login.py"
        )
        
with nav5:

    if st.button(
        "🤖 Prediction",
        use_container_width=True
    ):
        st.switch_page(
            "pages/prediction_page.py"
        )

st.markdown("---")

# ==========================================
# DATABASE CONNECTION
# ==========================================

connection = mysql.connector.connect(

    host="localhost",

    user="root",

    password="vardhansql@004",

    database="steel_delay_analysis"

)

cursor = connection.cursor()
# ==========================================
# FILTERS
# ==========================================

st.subheader("🔍 Filters")

f1,f2,f3,f4,f5 = st.columns(5)

shops_df = pd.read_sql(
    "SELECT shop_name FROM shops",
    connection
)

equipment_df = pd.read_sql(
    "SELECT equipment_name FROM equipment",
    connection
)

agency_df = pd.read_sql(
    "SELECT agency_name FROM agencies",
    connection
)

conveyor_df = pd.read_sql(
    "SELECT conveyor_name FROM conveyors",
    connection
)

with f1:

    selected_shop = st.selectbox(
        "Shop",
        ["All"] +
        shops_df["shop_name"].tolist()
    )

with f2:

    selected_equipment = st.selectbox(
        "Equipment",
        ["All"] +
        equipment_df["equipment_name"].tolist()
    )

with f3:

    selected_agency = st.selectbox(
        "Agency",
        ["All"] +
        agency_df["agency_name"].tolist()
    )

with f4:

    selected_conveyor = st.selectbox(
        "Conveyor",
        ["All"] +
        conveyor_df["conveyor_name"].tolist()
    )

with f5:

    selected_year = st.selectbox(
        "Year",
        ["All"]
    )

st.markdown("---")

# ==========================================
# FILTER QUERY
# ==========================================

base_query = """
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
WHERE 1=1
"""

if selected_shop != "All":

    base_query += f"""
    AND s.shop_name='{selected_shop}'
    """

if selected_equipment != "All":

    base_query += f"""
    AND e.equipment_name='{selected_equipment}'
    """

if selected_agency != "All":

    base_query += f"""
    AND a.agency_name='{selected_agency}'
    """

if selected_conveyor != "All":

    base_query += f"""
    AND c.conveyor_name='{selected_conveyor}'
    """

filtered_df = pd.read_sql(
    base_query,
    connection
)

# ==========================================
# KPI CARDS
# ==========================================

total_delays = len(filtered_df)

avg_delay = round(
    filtered_df["delay_minutes"].mean(),
    2
) if len(filtered_df) > 0 else 0

total_shops = filtered_df[
    "shop_name"
].nunique()

total_equipment = filtered_df[
    "equipment_name"
].nunique()

k1,k2,k3,k4 = st.columns(4)

k1.metric(
    "📊 Total Delays",
    total_delays
)

k2.metric(
    "🏭 Shops",
    total_shops
)

k3.metric(
    "⚙ Equipment",
    total_equipment
)

k4.metric(
    "⏱ Avg Delay",
    avg_delay
)

st.markdown("---")
# ==========================================
# SHOP WISE DELAY ANALYSIS
# ==========================================

st.subheader("🏭 Shop Wise Delay Analysis")

shop_analysis = (
    filtered_df.groupby("shop_name")
    .size()
    .reset_index(name="Total_Delays")
)

fig = px.bar(
    shop_analysis,
    x="shop_name",
    y="Total_Delays",
    color="shop_name",
    text="Total_Delays"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ==========================================
# EQUIPMENT ANALYSIS
# ==========================================

st.subheader("⚙ Equipment Wise Delay Analysis")

equipment_analysis = (
    filtered_df.groupby("equipment_name")
    .size()
    .reset_index(name="Total_Delays")
)

fig = px.bar(
    equipment_analysis,
    x="equipment_name",
    y="Total_Delays",
    color="equipment_name",
    text="Total_Delays"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ==========================================
# SEASON ANALYSIS
# ==========================================

st.subheader("🌦 Season Wise Delay Analysis")

season_analysis = (
    filtered_df.groupby("season_name")
    .size()
    .reset_index(name="Total_Delays")
)

fig = px.pie(
    season_analysis,
    names="season_name",
    values="Total_Delays",
    hole=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ==========================================
# AGENCY ANALYSIS
# ==========================================

st.subheader("🏢 Agency Wise Delay Analysis")

agency_analysis = (
    filtered_df.groupby("agency_name")
    .size()
    .reset_index(name="Total_Delays")
)

fig = px.bar(
    agency_analysis,
    x="agency_name",
    y="Total_Delays",
    color="agency_name",
    text="Total_Delays"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ==========================================
# CONVEYOR ANALYSIS
# ==========================================

st.subheader("🚚 Conveyor Wise Delay Analysis")

conveyor_analysis = (
    filtered_df.groupby("conveyor_name")
    .size()
    .reset_index(name="Total_Delays")
)

fig = px.bar(
    conveyor_analysis,
    x="conveyor_name",
    y="Total_Delays",
    color="conveyor_name",
    text="Total_Delays"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ==========================================
# DELAY TYPE ANALYSIS
# ==========================================

st.subheader("⚠ Delay Type Analysis")

delay_analysis = (
    filtered_df.groupby("delay_description")
    .size()
    .reset_index(name="Total_Delays")
)

fig = px.pie(
    delay_analysis,
    names="delay_description",
    values="Total_Delays",
    hole=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")
# ==========================================
# MONTHLY TREND
# ==========================================

st.subheader("📈 Monthly Delay Trend")

filtered_df["delay_date"] = pd.to_datetime(
    filtered_df["delay_date"]
)

monthly_df = (
    filtered_df.groupby(
        filtered_df["delay_date"].dt.month_name()
    )
    .size()
    .reset_index(name="Total_Delays")
)

fig = px.line(
    monthly_df,
    x="delay_date",
    y="Total_Delays",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ==========================================
# EXPORT SECTION
# ==========================================

st.subheader("📤 Export Reports")

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="delay_report.csv",
    mime="text/csv"
)

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    filtered_df.to_excel(
        writer,
        index=False
    )

st.download_button(
    label="⬇ Download Excel",
    data=excel_buffer.getvalue(),
    file_name="delay_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("---")

# ==========================================
# RECOMMENDATION ENGINE
# ==========================================

st.subheader("💡 Recommendations")

if len(filtered_df) > 0:

    risky_equipment = (
        filtered_df["equipment_name"]
        .value_counts()
        .idxmax()
    )

    risky_count = (
        filtered_df["equipment_name"]
        .value_counts()
        .max()
    )

    st.warning(
        f"""
        High Risk Equipment : {risky_equipment}

        Delay Occurrences : {risky_count}

        Recommendation :
        Schedule preventive maintenance
        and inspection immediately.
        """
    )

st.markdown("---")

# ==========================================
# HIGH RISK EQUIPMENT
# ==========================================

st.markdown("---")

st.subheader("🚨 High Risk Equipment Ranking")

risk_df = (
    filtered_df.groupby("equipment_name")
    .size()
    .reset_index(name="Total_Delays")
    .sort_values(
        by="Total_Delays",
        ascending=False
    )
)

top5 = risk_df.head(5)

st.dataframe(
    top5,
    use_container_width=True
)

fig = px.bar(
    top5,
    x="equipment_name",
    y="Total_Delays",
    color="equipment_name",
    text="Total_Delays",
    title="Top 5 High Risk Equipment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
if len(top5) > 0:

    worst_equipment = top5.iloc[0]["equipment_name"]

    worst_count = top5.iloc[0]["Total_Delays"]

    st.error(
        f"""
        🚨 ALERT

        {worst_equipment}
        has recorded
        {worst_count}
        delays.

        Preventive maintenance
        is strongly recommended.
        """
    )
# ==========================================
# SEASONAL RISK ANALYSIS
# ==========================================

st.markdown("---")

st.subheader("🌦 Seasonal Risk Analysis")

season_risk_df = (
    filtered_df.groupby("season_name")
    .size()
    .reset_index(name="Total_Delays")
    .sort_values(
        by="Total_Delays",
        ascending=False
    )
)

st.dataframe(
    season_risk_df,
    use_container_width=True
)

fig = px.bar(
    season_risk_df,
    x="season_name",
    y="Total_Delays",
    color="season_name",
    text="Total_Delays",
    title="Season Wise Delay Risk"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
if len(season_risk_df) > 0:

    highest_risk_season = season_risk_df.iloc[0]["season_name"]

    highest_delay_count = season_risk_df.iloc[0]["Total_Delays"]

    st.warning(
        f"""
        ⚠ SEASONAL ALERT

        {highest_risk_season} season recorded
        {highest_delay_count} delays.

        Additional monitoring and preventive
        maintenance are recommended during this season.
        """
    )
# ==========================================
# DELAY RECORDS TABLE
# ==========================================

st.subheader("📋 Delay Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

st.markdown("---")

st.subheader("🕒 Recently Added Delays")

period = st.radio(
    "Select Time Range",
    ["Day", "Week", "Month"],
    horizontal=True
)

if period == "Day":

    recent_query = """
    SELECT
    dr.delay_date,
    s.shop_name,
    e.equipment_name,
    dt.delay_description,
    dr.delay_minutes
    FROM delay_records dr
    JOIN shops s ON dr.shop_id=s.shop_id
    JOIN equipment e ON dr.equipment_id=e.equipment_id
    JOIN delay_types dt ON dr.delay_type_id=dt.delay_type_id
    WHERE dr.delay_date >= CURDATE() - INTERVAL 1 DAY
    ORDER BY dr.delay_date DESC
    """

elif period == "Week":

    recent_query = """
    SELECT
    dr.delay_date,
    s.shop_name,
    e.equipment_name,
    dt.delay_description,
    dr.delay_minutes
    FROM delay_records dr
    JOIN shops s ON dr.shop_id=s.shop_id
    JOIN equipment e ON dr.equipment_id=e.equipment_id
    JOIN delay_types dt ON dr.delay_type_id=dt.delay_type_id
    WHERE dr.delay_date >= CURDATE() - INTERVAL 7 DAY
    ORDER BY dr.delay_date DESC
    """

else:

    recent_query = """
    SELECT
    dr.delay_date,
    s.shop_name,
    e.equipment_name,
    dt.delay_description,
    dr.delay_minutes
    FROM delay_records dr
    JOIN shops s ON dr.shop_id=s.shop_id
    JOIN equipment e ON dr.equipment_id=e.equipment_id
    JOIN delay_types dt ON dr.delay_type_id=dt.delay_type_id
    WHERE dr.delay_date >= CURDATE() - INTERVAL 30 DAY
    ORDER BY dr.delay_date DESC
    """

recent_df = pd.read_sql(
    recent_query,
    connection
)

st.dataframe(
    recent_df,
    use_container_width=True,
    height=300
)
connection.close()