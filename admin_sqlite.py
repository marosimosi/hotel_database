import sqlite3
import pandas as pd
from inputs import Inputs

class DB_connection:
    def __init__(self, db_path) -> None:
        self.conn = sqlite3.connect(db_path)

    # Inserts new entry in Fills table
    def insert_fills(self, booking_id, room_id, check_in, check_out):
        cursor = self.conn.cursor()
        sql = """INSERT OR REPLACE INTO FILLS(booking_id, room_id, check_in, check_out) 
        VALUES(?,?,?,?)"""
        cursor.execute(sql, (booking_id, room_id, check_in, check_out))
        self.conn.commit()

    # Gets an sql query and returns the contents
    def retrieval_query(self, sql: str) -> list:
        cursor = self.conn.cursor()
        results = cursor.execute(sql).fetchall()
        return results

    # Find room_id given the booking_id
    def get_a_room(self, booking_id):
        booking_id = int(booking_id)
        sql = f""" SELECT room_id
        FROM Books
        WHERE booking_id = {booking_id}"""
        room_id = self.retrieval_query(sql)[0][0]
        return room_id

    # Function to return all the bookings concerning a specific time period
    def return_bookings(self, start_date, end_date):
        sql = f""" SELECT *
        FROM Booking
        WHERE arrival < {end_date} AND departure > {start_date}"""
        bookings = self.retrieval_query(sql)
        for i in bookings:
            print(f"{i[0]}\t\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}")
        return bookings