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
                print("Πάτησες το 2!")
            elif self.option == "3":
                print("Πάτησες το 3!")
            elif self.option == "-1":
                return

    def start(self):
        opt = Inputs.input_method(
            "1: Look for rooms\
            \n2: Check your bookings\
            \n3: Write a review\
            \n-1: Exit\n",
            "Not a valid option.", ["1","2","3","-1"])
        return opt

    def book(self):
        rooms = []
        from_date = Inputs.input_date("Arrival date (DD-MM-YYYY):  ")
        to_date = Inputs.input_date("Departure date (DD-MM-YYYY):  ")
        self.book_a_room(from_date, to_date, rooms)
        while True:
            price = 0
            for room in rooms:
                price += self.db.calc_price(room, from_date, to_date)
            print("Your total is", price, "€")
            more = Inputs.input_method(
                "1: Look for another room \n2: Finish\n",
                "Not a valid option.", ["1", "2"])
            if more == "1": 
                self.book_a_room(from_date, to_date, rooms)
            elif more == "2" and len(rooms) == 0:   #Doesnt book a room
                return
            elif more == "2" and len(rooms) != 0:   #Books room/rooms
                ssn = Inputs.input_number("Give your SSN: ", "Not valid SSN")
                if self.db.is_new(ssn):
                    print("Welcome back!")
                else:
                    self.new_client(ssn)
                adults = Inputs.input_number("Number of adults: ", "Not a valid number")
                children = Inputs.input_number("Number of children: ", "Not a valid number")
                pay_method = Inputs.input_method("Chose a pay method\
                    \n1:Credit card \n2:Debit card \n3:Cash\n",
                    "Not a valid option.", ["1","2","3"])
                self.db.book(price, from_date, to_date, pay_method, adults, children, ssn)
                return

    def book_a_room(self, from_date, to_date, rooms):
        available = False
        capacity = str(Inputs.input_method(
            "Chose capacity (1-4 people):  ",
            "Not a valid option.", ["1", "2", "3", "4"]))
        type = Inputs.input_method(
            "1: Deluxe \n2:Standard \n3:Budget\n",
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
            print("This room type is not available :(")
            return
        print("It is available!")
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
        bdate = input("Birth date: ")
        email = input("E-mail address: ")
        tel = input("Telephone number: ")
        address = input("Address: ")
        self.db.new_client(ssn, email, tel, address, fname, lname, bdate)
        return
        
        
        

if __name__ == "__main__":
    menu = Client("database.db")
