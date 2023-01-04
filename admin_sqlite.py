import sqlite3
import pandas as pd
from inputs import Inputs

class DB_connection:
    def __init__(self, db_path) -> None:
        self.conn = sqlite3.connect(db_path)

    # Insert or replace Fills entry
    def insert_fills(self, booking_id, room_id, check_in, check_out):
        cursor = self.conn.cursor()
        sql = """INSERT OR REPLACE INTO FILLS(booking_id, room_id, check_in, check_out) 
        VALUES(?,?,?,?)"""
        cursor.execute(sql, (booking_id, room_id, check_in, check_out))
        self.conn.commit()

    # Get an sql query and return the contents
    def retrieval_query(self, sql: str) -> list:
        cursor = self.conn.cursor()
        results = cursor.execute(sql).fetchall()
        return results

    # Find room_id given the booking_id
    def get_a_room(self, booking_id):
        booking_id = int(booking_id)
        sql = f""" SELECT room_id
        FROM Books NATURAL JOIN Booking
        WHERE booking_id = {booking_id}"""
        rooms = self.retrieval_query(sql)
        return rooms

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
    def return_worst_reviews(self):
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

    # Function that returns the best 3 reviews and the rooms they concern
    def return_best_reviews(self):
        sql = """SELECT Review.*, R.room_id
            FROM Review, Type, Room as R
            WHERE Review.type_name = Type.type_name AND R.type_name = Type.type_name
            AND R.room_id in (
	            SELECT Room.room_id
	            FROM ((Review NATURAL JOIN Client NATURAL JOIN Booking) NATURAL JOIN Books) NATURAL JOIN Room
            )
            Order by score DESC
            LIMIT 3;"""
        reviews = self.retrieval_query(sql)
        print("\nreview_id\tscore\troom_type\troom_id\t\tcomments")
        for i in reviews:
            if len(i[5]) > 7:
                print(f"{i[0]}\t\t{i[3]}\t{i[5]}\t{i[6]}\t\t{i[1]}")
            else:
                print(f"{i[0]}\t\t{i[3]}\t{i[5]}\t\t{i[6]}\t\t{i[1]}")
        return reviews

    # Function that returns the late downpayments by individuals
    def late_downpayments_individuals(self):
        sql = """SELECT booking_id, Fname, Lname, email, telephone, dp_due_date, downpayment - paid_amount
            FROM (Booking NATURAL JOIN Client), Individual
            WHERE dp_due_date < date('now') AND paid_amount < downpayment AND Client.ssn = individual_ssn;"""
        late_dps_individuals = self.retrieval_query(sql)
        return late_dps_individuals

    # Function that returns late downpayments by agencies
    def late_downpayments_agency(self):
        sql = """SELECT booking_id, name, email, web_page, dp_due_date, downpayment - paid_amount
            FROM (Booking NATURAL JOIN Client), Agency
            WHERE dp_due_date < date('now') AND paid_amount < downpayment AND Client.ssn = agency_ssn;"""
        late_dps_agency = self.retrieval_query(sql)
        return late_dps_agency

    # Insert or replace Booking entry
    def insert_booking(self, booking_id, price, arrival, departure, downpayment, paid_amount, dp_due_date, pay_method, children, adults, ssn):
        cursor = self.conn.cursor()
        sql = """INSERT OR REPLACE INTO BOOKING(booking_id, price, arrival, departure, downpayment, paid_amount, dp_due_date, pay_method, children, adults, ssn) 
        VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
        cursor.execute(sql, (booking_id, price, arrival, departure, downpayment, paid_amount, dp_due_date, pay_method, children, adults, ssn))
        self.conn.commit()

    # Get Booking info given the booking_id
    def get_bookings_info(self, booking_id):
        sql = f""" SELECT *
            FROM Booking
            WHERE booking_id = {booking_id}"""
        info = self.retrieval_query(sql)
        if len(info) != 0:
            info = info[0]
        else:
            print("There is no such booking!")
        return info
