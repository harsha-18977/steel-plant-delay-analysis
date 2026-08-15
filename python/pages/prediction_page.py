import streamlit as st
import mysql.connector
import pandas as pd

from prediction import train_model

# ==========================================
# LOGIN CHECK
# ==========================================

if "logged_in" not in st.session_state:
    st.switch_page("pages/login.py")

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Delay Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Delay Prediction System")

if st.button("⬅ Back To Dashboard"):
    st.switch_page("pages/dashboard.py")

st.markdown("---")

# ==========================================
# DATABASE
# ==========================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vardhansql@004",
    database="steel_delay_analysis"
)

# ==========================================
# DROPDOWNS
# ==========================================

shops = pd.read_sql(
    "SELECT * FROM shops",
    connection
)

equipment = pd.read_sql(
    "SELECT * FROM equipment",
    connection
)

conveyors = pd.read_sql(
    "SELECT * FROM conveyors",
    connection
)

agencies = pd.read_sql(
    "SELECT * FROM agencies",
    connection
)

delay_types = pd.read_sql(
    "SELECT * FROM delay_types",
    connection
)

seasons = pd.read_sql(
    "SELECT * FROM seasons",
    connection
)

st.subheader("Prediction Inputs")

c1, c2 = st.columns(2)

with c1:

    shop = st.selectbox(
        "Shop",
        shops["shop_name"]
    )

    equipment_name = st.selectbox(
        "Equipment",
        equipment["equipment_name"]
    )

    conveyor = st.selectbox(
        "Conveyor",
        conveyors["conveyor_name"]
    )

with c2:

    agency = st.selectbox(
        "Agency",
        agencies["agency_name"]
    )

    delay_type = st.selectbox(
        "Delay Type",
        delay_types["delay_description"]
    )

    season = st.selectbox(
        "Season",
        seasons["season_name"]
    )

# ==========================================
# PREDICT
# ==========================================

if st.button("🚀 Predict Delay"):

    model = train_model()

    shop_id = int(
        shops[
            shops["shop_name"] == shop
        ]["shop_id"].iloc[0]
    )

    equipment_id = int(
        equipment[
            equipment["equipment_name"] == equipment_name
        ]["equipment_id"].iloc[0]
    )

    conveyor_id = int(
        conveyors[
            conveyors["conveyor_name"] == conveyor
        ]["conveyor_id"].iloc[0]
    )

    agency_id = int(
        agencies[
            agencies["agency_name"] == agency
        ]["agency_id"].iloc[0]
    )

    delay_type_id = int(
        delay_types[
            delay_types["delay_description"] == delay_type
        ]["delay_type_id"].iloc[0]
    )

    season_id = int(
        seasons[
            seasons["season_name"] == season
        ]["season_id"].iloc[0]
    )

    prediction = model.predict([
        [
            shop_id,
            equipment_id,
            conveyor_id,
            agency_id,
            delay_type_id,
            season_id
        ]
    ])

    delay_minutes = round(
        prediction[0],
        2
    )

    st.success(
        f"Predicted Delay: {delay_minutes} Minutes"
    )

    if delay_minutes < 60:

        st.success(
            "🟢 Risk Level : LOW"
        )

    elif delay_minutes < 120:

        st.warning(
            "🟡 Risk Level : MEDIUM"
        )

    else:

        st.error(
            "🔴 Risk Level : HIGH"
        )

connection.close()