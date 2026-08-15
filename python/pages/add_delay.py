import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

# ---------------------------------------------------
# LOGIN CHECK
# ---------------------------------------------------

if "logged_in" not in st.session_state:
    st.switch_page("pages/login.py")

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Add Delay",
    page_icon="➕",
    layout="wide"
)

st.title("➕ Add New Delay Record")

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vardhansql@004",
    database="steel_delay_analysis"
)

cursor = connection.cursor()

# ---------------------------------------------------
# LOAD MASTER DATA
# ---------------------------------------------------

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

# ---------------------------------------------------
# FORM
# ---------------------------------------------------

with st.form("delay_form"):

    delay_date = st.date_input(
        "Delay Date",
        value=date.today()
    )

    shop = st.selectbox(
        "Shop",
        shops["shop_name"]
    )

    equipment_name = st.selectbox(
        "Equipment",
        equipment["equipment_name"]
    )

    conveyor_name = st.selectbox(
        "Conveyor",
        conveyors["conveyor_name"]
    )

    agency_name = st.selectbox(
        "Agency",
        agencies["agency_name"]
    )

    delay_desc = st.selectbox(
        "Delay Type",
        delay_types["delay_description"]
    )

    season_name = st.selectbox(
        "Season",
        seasons["season_name"]
    )

    delay_minutes = st.number_input(
        "Delay Minutes",
        min_value=1,
        step=1
    )

    submit = st.form_submit_button(
        "💾 Save Delay"
    )

# ---------------------------------------------------
# SAVE DELAY
# ---------------------------------------------------

if submit:

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
            conveyors["conveyor_name"] == conveyor_name
        ]["conveyor_id"].iloc[0]
    )

    agency_id = int(
        agencies[
            agencies["agency_name"] == agency_name
        ]["agency_id"].iloc[0]
    )

    delay_type_id = int(
        delay_types[
            delay_types["delay_description"] == delay_desc
        ]["delay_type_id"].iloc[0]
    )
    season_id = int(
        seasons[
            seasons["season_name"] == season_name
        ]["season_id"].iloc[0]
    )
    
    insert_query = """
    INSERT INTO delay_records
    (
    delay_date,
    shop_id,
    equipment_id,
    conveyor_id,
    agency_id,
    delay_type_id,
    season_id,
    delay_minutes
    )
    VALUES
    (CURDATE(),%s,%s,%s,%s,%s,%s,%s)
    """
    values = (
        shop_id,
        equipment_id,
        conveyor_id,
        agency_id,
        delay_type_id,
        season_id,
        delay_minutes
    )
    cursor.execute(insert_query, values)
    connection.commit()
    st.success(
        "✅ Delay Record Added Successfully!"
    )
connection.close()