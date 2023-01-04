import sqlite3
import pandas as pd

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
        return

    def book(self, price, from_date, to_date, pay_method, adults, children, ssn):
        return