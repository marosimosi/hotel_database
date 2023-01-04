from admin_sqlite import DB_connection
from inputs import Inputs
from datetime import datetime
from datetime import date

class Admin:
    # Initialize the admin menu
    def __init__(self, db_path) -> None:
        self.db = DB_connection(db_path)
        while True:
            self.option = self.login()
            if self.option == "1":
                self.check_in()
            elif self.option == "2":
                self.check_out()
            elif self.option == "3":
                self.show_bookings()
            elif self.option == "4":
                self.show_reviews()
            elif self.option == "-1":
                return

    # Menu to get the option from the admin
    def login(self):
        login = Inputs.input_method(
            "\n1: Check in.\
            \n2: Check out.\
            \n3: Show all the bookings concerning a specific time period.\
            \n4: Show the worst 3 reviews and which rooms they concern.\
            \n-1: Exit\n", "\nNot a valid option.",
            ["1", "2", "3", "4", "-1"])
        return login

    # Function to check in a client
    def check_in(self):
        booking_id, _ = Inputs.input_number("\nEnter booking id: ", "\nNot a number!")
        if len(self.db.retrieval_query(f"SELECT * FROM Booking WHERE booking_id = {int(booking_id)}")) != 0:
            arrival_date = self.db.retrieval_query(f"SELECT arrival FROM Booking WHERE booking_id = {int(booking_id)}")[0][0]
            arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()
            if arrival_date <= date.today():
                room_id = int(self.db.get_a_room(booking_id))
                check_in_date = date.today()
                check_out_date = 'NULL'
                self.db.inster_fills(booking_id, room_id, check_in_date, check_out_date)
                print("Check in was successful!")
            else:
                print("You are too early! Your booking is for", arrival_date)
        else:
            print("There is no such booking!") 

    # Function to check out a client (respectfully)
    def check_out(self):
        booking_id, _ = Inputs.input_number("\nEnter booking id: ", "\nNot a number!")
        if len(self.db.retrieval_query(f"SELECT * FROM Fills WHERE booking_id = {int(booking_id)}")) != 0:
            info = self.db.retrieval_query(f"SELECT * FROM Fills WHERE booking_id = {int(booking_id)}")[0]
            room_id = info[1]
            check_in_date = datetime.strptime(info[2], '%Y-%m-%d').date()
            check_out_date = date.today()
            self.db.insert_fills(booking_id, room_id, check_in_date, check_out_date)
            print("Check out was successful!")
        else:
            print("There has been no check in for this booking.")

    # Function to show all the bookings concerning a specific time period
    def show_bookings(self):
        start_date = Inputs.input_date("Enter start date (DD-MM-YYYY): ")
        end_date = Inputs.input_date("Enter end date (DD-MM-YYYY): ")
        if start_date < end_date:
            self.db.return_bookings(start_date, end_date)
        else:
            print("Not valid time period.")

    # Function that shows the worst 3 reviews and which rooms they concern
    def show_reviews(self):
        self.db.return_reviews()


if __name__ == "__main__":
    menu = Admin("database.db")
