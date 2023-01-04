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
        WHERE arrival < date('{end_date}') AND departure > date('{start_date}')
        ORDER BY arrival;"""
        bookings = self.retrieval_query(sql)
        if len(bookings) == 0:
            print("There are no bookings for this time period.")
        else:
            print("\nbooking_id\tprice\tarrival\t\tdeparture\tdownpayment\tpaid_amount\tdp_due_date\tpay_method\tchildren\tadults\tssn")
            for i in bookings:
                if len(i[7]) < 5:
                    print(f"{i[0]}\t\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}\t\t{i[5]}\t\t{i[6]}\t{i[7]}\t\t{i[8]}\t\t{i[9]}\t{i[10]}")
                else:
                    print(f"{i[0]}\t\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}\t\t{i[5]}\t\t{i[6]}\t{i[7]}\t{i[8]}\t\t{i[9]}\t{i[10]}")
        return bookings

    # Function to return all arrival dates
    def arrival(self):
        sql = """SELECT arrival
        FROM Booking"""
        arrivals = self.retrieval_query(sql)
        for i in arrivals:
            print(f"{i[0]}\t\t")
        return arrivals

    # Function that returns the worst 3 reviews and the rooms they concern
    def return_reviews(self):
        sql = """SELECT Review.*, R.room_id
            FROM Review, Type, Room as R
            WHERE Review.type_name = Type.type_name AND R.type_name = Type.type_name
            AND R.room_id in (
	            SELECT Room.room_id
	            FROM ((Review NATURAL JOIN Client NATURAL JOIN Booking) NATURAL JOIN Books) NATURAL JOIN Room
            )
            Order by score
            LIMIT 3;"""
        reviews = self.retrieval_query(sql)
        print("\nreview_id\tscore\troom_type\troom_id\t\tcomments")
        for i in reviews:
            if len(i[5]) > 7:
                print(f"{i[0]}\t\t{i[3]}\t{i[5]}\t{i[6]}\t\t{i[1]}")
            else:
                print(f"{i[0]}\t\t{i[3]}\t{i[5]}\t\t{i[6]}\t\t{i[1]}")
        return reviews
