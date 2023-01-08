import sqlite3
import pandas as pd

#generate Type,Room

typedata = pd.read_excel("type.xlsx")
roomdata = pd.read_excel("room.xlsx")
with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()

    for _, row in typedata.iterrows():
        type_name = row["type_name"]
        low_season = float(row["low"])
        mid_season = float(row["mid"])
        high_season = float(row["high"])
        cursor.execute(
            f"""INSERT or REPLACE INTO TYPE
        VALUES (?,?,?,?);""", (type_name, low_season, mid_season, high_season)
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