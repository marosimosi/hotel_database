import sqlite3
import pandas as pd

#generate Type, Rate, Room

typedata = pd.read_excel("type.xlsx")
ratedata = pd.read_excel("rate.xlsx")
roomdata = pd.read_excel("room.xlsx")
with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()

    for _, row in typedata.iterrows():
        type_name = row["type_name"]
        capacity = row["capacity"]
        rate_id = row["rate_id"]
        cursor.execute(
            f"""INSERT or REPLACE INTO TYPE
        VALUES (?,?,?);""", (type_name, rate_id, capacity)
        )
        
    for _, row in ratedata.iterrows():
        rate_id = int(row["rate_id"])
        low_season = float(row["low"])
        mid_season = float(row["mid"])
        high_season = float(row["high"])
        cursor.execute(
            f"""INSERT or REPLACE INTO RATE
        VALUES (?,?,?,?);""", (rate_id, mid_season, low_season, high_season)
        )

    for _, row in roomdata.iterrows():
        room_id = row["room_id"]
        floor = row["floor"]
        type_name = row["type_name"]
        cursor.execute(
            f"""INSERT or REPLACE INTO ROOM
        VALUES (?,?,?);""", (room_id, floor, type_name)
        )

    conn.commit()