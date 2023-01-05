import sqlite3
import pandas as pd
from datetime import timedelta, datetime

class DB_Connection:
    def __init__(self, path_name) -> None:
        self.conn = sqlite3.connect(path_name)
    
    def check_availability(self, type_name, from_date, to_date):
        cursor = self.conn.cursor()
        sql = f"""SELECT room_id 
        FROM Room
        WHERE type_name = '{type_name}' AND room_id NOT IN (
        SELECT room_id
        FROM Books NATURAL JOIN Booking
        WHERE date('{from_date}') < departure AND arrival < date('{to_date}') )"""
        results = cursor.execute(sql).fetchall()
        for i in range(len(results)):
            results[i] = results[i][0]
        return results

    def read_reviews(self, type_name):
        cursor = self.conn.cursor()
        sql = f"""SELECT score, text, date
        FROM Review
        WHERE type_name = '{type_name}' """
        results = cursor.execute(sql).fetchall()
        if results == [] : 
            print("There are no reviews yet.")
            return
        print("score\t\tdate\tcomments")
        for i in results:
            print(f"{i[2]}\t{i[0]}\t{i[1]}")
        return

    def calc_price(self, room, from_date, to_date):
        cursor = self.conn.cursor()
        sql = f"""SELECT low_season, mid_season, high_season
        FROM Room NATURAL JOIN Type
        WHERE room_id = {room}"""
        results = cursor.execute(sql).fetchall()
        delta = (to_date - from_date).days     # num of days
        if 2<from_date.month<6 : return results[0][1] * delta
        elif (5 < from_date.month < 9)\
            or (from_date.month == 12 and from_date.day > 23)\
            or (from_date.month == 1 and from_date.day < 9) : return results[0][2] * delta
        else : return results[0][0] * delta

    def is_new(self, ssn):
        cursor = self.conn.cursor()
        sql = f"""SELECT COUNT(*)
        FROM Client
        WHERE ssn = {ssn}"""
        result = cursor.execute(sql).fetchall()[0][0]
        if result == 0: return False
        elif result == 1: return True

    def new_client(self, ssn, email, tel, address, fname, lname, bdate):
        cursor = self.conn.cursor()
        sql = """INSERT INTO CLIENT(ssn, email, telephone, address) 
        VALUES(?,?,?,?)"""
        cursor.execute(sql, (ssn, email, tel, address))
        sql = """INSERT INTO INDIVIDUAL(Fname, Lname, Bdate, individual_ssn) 
        VALUES(?,?,?,?)"""
        cursor.execute(sql, (fname, lname, bdate, ssn))
        self.conn.commit()
        return

    def book(self, rooms, price, from_date, to_date, pay_method, adults, children, ssn):
        downpayment = 0.2 * price
        paid_amount = 0
        booking_date = datetime.today().date()
        dp_due_date = from_date - timedelta(weeks = 2)
        cursor = self.conn.cursor()

        #INSERT BOOKING
        sql = """INSERT INTO BOOKING(price, arrival, departure, downpayment, paid_amount, dp_due_date, pay_method, children, adults, ssn) 
        VALUES(?,?,?,?,?,?,?,?,?,?)"""
        cursor.execute(sql, (price, from_date, to_date, downpayment, paid_amount, dp_due_date, pay_method, children, adults, ssn))
        
        #FIND BOOKING_ID 
        sql = """SELECT MAX(booking_id)
        FROM Booking"""
        booking_id = cursor.execute(sql).fetchall()[0][0]
        

        #INSERT BOOK FOR EACH ROOM
        for room in rooms:
           sql = """INSERT INTO BOOKS(booking_id, room_id, booking_date)
           VALUES(?,?,?)""" 
           cursor.execute(sql, (booking_id, room, booking_date))
        
        self.conn.commit()
        return