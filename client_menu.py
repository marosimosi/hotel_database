from client_sqlite import DB_Connection
from inputs import Inputs

class Client:
    def __init__(self, db_path) -> None:
        self.db = DB_Connection(db_path)
        while True:
            self.option = self.start()
            if self.option == "1":
                self.book()
            elif self.option == "2":
                self.check_bookings()
            elif self.option == "3":
                self.write_review()
            elif self.option == "-1":
                return

    def start(self):
        opt = Inputs.input_method(
            "\n\n1: Look for rooms\
            \n2: Check your bookings\
            \n3: Write a review\
            \n-1: Exit\n",
            "Not a valid option.", ["1","2","3","-1"])
        return opt

    def book(self):
        rooms = []
        while True:
            from_date = Inputs.input_date("\nArrival date (DD-MM-YYYY):  ")
            to_date = Inputs.input_date("Departure date (DD-MM-YYYY):  ")
            if (to_date - from_date).days > 0:
                break
            print("Departure date must be after arrival date")
        self.book_a_room(from_date, to_date, rooms)
        while True:
            price = 0
            for room in rooms:
                price += self.db.calc_price(room, from_date, to_date)
            print("\nYour total is", price, "€")
            more = Inputs.input_method(
                "1: Look for another room \n2: Finish\n",
                "Not a valid option.", ["1", "2"])
            if more == "1": 
                self.book_a_room(from_date, to_date, rooms)
            elif more == "2" and len(rooms) == 0:   #Doesnt book a room
                return
            elif more == "2" and len(rooms) != 0:   #Books room/rooms
                ssn = Inputs.input_number("\nGive your SSN: ", "Not valid SSN")
                if self.db.client_exists(ssn):
                    print("\nWelcome back!")
                else:
                    self.new_client(ssn)
                adults = Inputs.input_number("Number of adults: ", "Not a valid number")
                children = Inputs.input_number("Number of children: ", "Not a valid number")
                pay = Inputs.input_method("Chose a pay method\
                    \n1:Credit card \n2:Debit card \n3:Cash\n",
                    "Not a valid option.", ["1","2","3"])
                if pay == "1": pay_method = "credit_card"
                elif pay == "2": pay_method = "debit_card"
                elif pay == "3": pay_method = "cash"
                self.db.book(rooms, price, from_date, to_date, pay_method, adults, children, ssn)
                return

    def book_a_room(self, from_date, to_date, rooms):
        available = False
        capacity = str(Inputs.input_method(
            "\nChose capacity (1-4 people):  ",
            "Not a valid option.", ["1", "2", "3", "4"]))
        type = Inputs.input_method(
            "\n1: Deluxe \n2:Standard \n3:Budget\n",
            "Not a valid option.", ["1", "2", "3"])
        if type == "1":
            type_name = capacity+"deluxe"
        elif type == "2":
            type_name = capacity+"standard"
        elif type == "3":
            type_name = capacity+"budget"  
        av_rooms = self.db.check_availability(type_name, from_date, to_date) # list of available rooms for this type_name 
        
        for av_room in av_rooms:   # make sure this room is not already reserved for the same booking
            if av_room not in rooms:
                available = True
                break
        if not available:                    
            print("\nThis room type is not available :(")
            return
        print("\nIt is available!")
        while True:
            opt = Inputs.input_method("1: Book the room! \n2: See the reviews \n-1:Exit\n",
                "Not a valid option.", ["1", "2", "-1"])
            if opt == "1":
                rooms.append(av_room)
                return
            elif opt == "2":
                self.db.read_reviews(type_name)
            elif opt == "-1":
                return
        
    def new_client(self, ssn):
        fname = input("First name: ")
        lname = input("Last name: ")
        bdate = Inputs.input_date("Birth date: ")
        email = input("E-mail address: ")
        tel = Inputs.input_int("Telephone number: ")
        address = input("Address: ")
        self.db.new_client(ssn, email, tel, address, fname, lname, bdate)
        return       

    def check_bookings(self):
        ssn = Inputs.input_number("\nGive your SSN: ", "Not valid SSN")
        self.db.check_bookings(ssn)
        return 

    def write_review(self):
        ssn = Inputs.input_number("\nGive your SSN: ", "Not valid SSN")
        self.db.write_review(ssn)
        return

        
        
if __name__ == "__main__":
    menu = Client("CreateData/database.db")
