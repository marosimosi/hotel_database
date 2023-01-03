import sqlite3
import pandas as pd
from inputs import Inputs

class DB_connection:
    def __init__(self, db_path) -> None:
        self.conn = sqlite3.connect(db_path)

    # Inserts new entry in Fills table
    def inster_fills(self, booking_id, room_id, check_in, check_out):
        cursor = self.conn.cursor()
        sql = """INSERT INTO FILLS(booking_id, room_id, check_in, check_out) 
        VALUES(?,?,?,?)"""
        cursor.execute(sql, (booking_id, room_id, check_in, check_out))
        self.conn.commit()
