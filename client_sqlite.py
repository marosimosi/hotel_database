import sqlite3
import pandas as pd

class DB_Connection:
    def __init__(self, path_name) -> None:
        self.connection = sqlite3.connect(path_name)
    
    def check_availability(self, type_name, from_date, to_date):
        return 0