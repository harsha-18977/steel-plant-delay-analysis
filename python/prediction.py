import mysql.connector
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def train_model():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vardhansql@004",
        database="steel_delay_analysis"
    )

    query = """
    SELECT
        shop_id,
        equipment_id,
        conveyor_id,
        agency_id,
        delay_type_id,
        season_id,
        delay_minutes
    FROM delay_records
    """

    df = pd.read_sql(query, connection)

    X = df[
        [
            "shop_id",
            "equipment_id",
            "conveyor_id",
            "agency_id",
            "delay_type_id",
            "season_id"
        ]
    ]

    y = df["delay_minutes"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    connection.close()

    return model
