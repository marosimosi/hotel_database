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
                self.show_worst_reviews()
            elif self.option == "5":
                self.show_best_reviews()
            elif self.option == "6":
                self.late_downpayment()
            elif self.option == "7":
                self.change_paid_amount()
            elif self.option == "-1":
                return

    # Menu to get the option from the admin
    def login(self):
        login = Inputs.input_method(
            "\n1: Check in.\
            \n2: Check out.\
            \n3: Show all the bookings concerning a specific time period.\
            \n4: Show the worst 3 reviews and which rooms they concern.\
            \n5: Show the best 3 reviews and which rooms they concern. \
            \n6: Check for late downpayments.\
            \n7: Change the paid amount of a booking.\
            \n-1: Exit\n", "\nNot a valid option.",
            ["1", "2", "3", "4", "5", "6", "7", "-1"])
        return login

    # Function to check in a client
    def check_in(self):
        booking_id = Inputs.input_int("\nEnter booking id: ", "\nNot a number!")
        if len(self.db.retrieval_query(f"SELECT * FROM Booking WHERE booking_id = {int(booking_id)}")) != 0:
            arrival_date = self.db.retrieval_query(f"SELECT arrival FROM Booking WHERE booking_id = {int(booking_id)}")[0][0]
            arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d').date()
            if arrival_date <= date.today():
                rooms = self.db.get_a_room(booking_id)
                for i in range(len(rooms)):
                    room_id = rooms[i][0]
                    check_in_date = date.today()
                    check_out_date = 'NULL'
                    self.db.insert_fills(booking_id, room_id, check_in_date, check_out_date)
                    print(f"Check in to room {room_id} was successful!")
            else:
                print("You are too early! Your booking is for", arrival_date)
        else:
            print("There is no such booking!") 

    # Function to check out a client (respectfully)
    def check_out(self):
        booking_id = Inputs.input_int("\nEnter booking id: ", "\nNot a number!")
        if len(self.db.retrieval_query(f"SELECT * FROM Fills WHERE booking_id = {int(booking_id)}")) != 0:
            info = self.db.retrieval_query(f"SELECT * FROM Fills WHERE booking_id = {int(booking_id)}")
            departure_date = self.db.departure(booking_id)
            departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
            if departure_date > date.today():
                print(f"Are you sure you want to check out early? You don't have to check out until {departure_date}.")
                answer = Inputs.input_method("Yes/No: ", "\nNot a valid option.", ["Yes", "No"])
                if answer == "Yes":
                    for i in range(len(info)):
                        room_id = info[i][1]
                        check_in_date = datetime.strptime(info[i][2], '%Y-%m-%d').date()
                        check_out_date = date.today()
                        self.db.insert_fills(booking_id, room_id, check_in_date, check_out_date)
                        print(f"Check out from room {room_id} was successful!")
            else:
                for i in range(len(info)):
                    room_id = info[i][1]
                    check_in_date = datetime.strptime(info[i][2], '%Y-%m-%d').date()
                    check_out_date = date.today()
                    self.db.insert_fills(booking_id, room_id, check_in_date, check_out_date)
                    print(f"Check out from room {room_id} was successful!")
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
    def show_worst_reviews(self):
        self.db.return_worst_reviews()

    # Function that shows the best 3 reviews and which rooms they concern
    def show_best_reviews(self):
        self.db.return_best_reviews()

    # Function to show late downpayments
    def late_downpayment(self):
        late_dps_individuals = self.db.late_downpayments_individuals()
        late_dps_agency = self.db.late_downpayments_agency()
        if len(late_dps_individuals) == 0 and len(late_dps_agency) == 0:
            print("\nThere are no late downpayments! :)")
        if len(late_dps_individuals) != 0:
            print("\nLate Downpayments from individuals: ")
            print("Booking ID\tFirst Name\tLast Name\tEmail\t\tTelephone\tDownpament Due Date\tOwed Amount")
            for i in range(len(late_dps_individuals)):
                print(f"{late_dps_individuals[i][0]}\t\t{late_dps_individuals[i][1]}\t\t{late_dps_individuals[i][2]}\t{late_dps_individuals[i][3]}\t{late_dps_individuals[i][4]}\t\t{late_dps_individuals[i][5]}\t{late_dps_individuals[i][6]}")
        if len(late_dps_agency) != 0:
            print("\nLate Downpayments from bookings by agencies: ")
            print("Booking ID\tName\t\tEmail\t\t\tWeb Page\t\tDownpament Due Date\tOwed Amount")
            for i in range(len(late_dps_agency)):
                print(f"{late_dps_agency[i][0]}\t\t{late_dps_agency[i][1]}\t{late_dps_agency[i][2]}\t{late_dps_agency[i][3]}\t\t{late_dps_agency[i][4]}\t\t{late_dps_agency[i][5]}")

    # Function to change the paid amount of a booking
    def change_paid_amount(self):
        booking_id = Inputs.input_int("\nEnter booking id: ", "\nNot a number!")
        info = self.db.get_bookings_info(booking_id)
        if len(info) != 0:
            price = info[1]
            arrival = info[2]
            departure = info[3]
            downpayment = info[4]
            paid_amount = info[5]
            dp_due_date = info[6]
            pay_method = info[7]
            children = info[8]
            adults = info[9]
            ssn = info[10]
            payment = Inputs.input_number("\nEnter new payment: ", "\nNot a number!")
            paid_amount += payment
            self.db.insert_booking(booking_id, price, arrival, departure, downpayment, paid_amount, dp_due_date, pay_method, children, adults, ssn)
            print("\nPayment was successful!")
            print(f"\nPrice: {price}\nDown-payment: {downpayment}\nPaid Amount: {paid_amount}")
            if paid_amount > price:
                print(f"The client has paid more than they should. They have paid {paid_amount-price} extra.")
            elif paid_amount == price:
                print("No more money owed for this booking.")
            elif paid_amount >= downpayment:
                print(f"The down-payment has been paid.\nMoney still owed for this booking: {price-paid_amount}\nDeadline: {departure}")
            elif paid_amount < downpayment:
                print(f"Money still owed for the down-payment: {downpayment-paid_amount}")



if __name__ == "__main__":
    menu = Admin("CreateData/database.db")
