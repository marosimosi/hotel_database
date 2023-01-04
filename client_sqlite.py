import sqlite3
import pandas as pd

class DB_Connection:
    def __init__(self, path_name) -> None:
        self.connection = sqlite3.connect(path_name)
    
    def check_availability(self, type_name, from_date, to_date):
        return []

    def read_reviews(self, type_name):
        return

    def calc_price(self, room, from_date, to_date):
        return 0

    def is_new(self, ssn):
        return True

    def new_client(self, ssn, email, tel, address, fname, lname, bdate):
        return

    def book(self, price, from_date, to_date, pay_method, adults, children, ssn):
        return