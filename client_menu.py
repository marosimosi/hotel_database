from client_sqlite import DB_Connection
from inputs import Inputs

class Client:
    # Initialize the admin menu
    def __init__(self, db_path) -> None:
        self.db = DB_Connection(db_path)
        while True:
            self.option = self.start()
            if self.option == "1":
                self.book()
            elif self.option == "2":
                print("Πάτησες το 2!")
            elif self.option == "3":
                print("Πάτησες το 2!")
            elif self.option == "-1":
                return

    # Menu to get the option from the admin
    def start(self):
        opt = Inputs.input_method(
            "1: Look for rooms\
            \n2: Check your bookings\
            \n3: Write a review\
            \n-1: Exit\n",
            "Not a valid option.", ["1","2","3","-1"])
        return opt

    def book(self):
        from_date = Inputs.input_date("Arrival date (DD-MM-YYYY):  ")
        to_date = Inputs.input_date("Departure date (DD-MM-YYYY):  ")
        self.book_a_room(from_date, to_date)
        while True:
            more = Inputs.input_method(
                "1: Look for another room \n2: Finish\n",
                "Not a valid option.", ["1", "2"]
            )

    def book_a_room(self, from_date, to_date):
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
        available = self.db.check_availability(type_name, from_date, to_date)  
        if available == 0:
            print("This room type is not available :(")
            return
        # while True:
        #     book = Inputs.input_method(
        #         "It is available!\
        #         \n\n1: Book the room! \n2: See the reviews\n",
        #         "Not a valid option.", [1, 2, 3, 4])

        
        
        



if __name__ == "__main__":
    menu = Client("database.db")
