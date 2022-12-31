from admin_sqlite import DB_Connection
from inputs import Inputs

class Admin:
    # Initialize the admin menu
    def __init__(self, db_path) -> None:
        self.db = DB_Connection(db_path)
        while True:
            self.option = self.login()
            if self.option == 1:
                print("Πάτησες το 1!")
            elif self.option == 2:
                print("Πάτησες το 2!")
            elif self.option == -1:
                return

    # Menu to get the option from the admin
    def login(self):
        login = Inputs.input_option(
            "Press 1 to prtint the names of the clients\
            \nPress 2 ...\n", "Not a valid option.",
            [1, 2, -1])
        return login


if __name__ == "__main__":
    menu = Admin("database.db")
