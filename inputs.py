from datetime import datetime

class Inputs:
    def __init__(self) -> None:
        pass
        
    # Variable Text is the message displayed to the user requesting the input
    # Variable error is the error message displayed to the user in case of a wrong input
    # Variable options is a list of the appropriate input options
    def input_method(text: str, error: str, options: list):
        while True:
            inp = input(text)
            if inp in options:
                return inp
            print(error)

    def validate(date_text: str):
        try:
            datetime.strptime(date_text, '%d-%m-%Y')
            return True
        except ValueError:
            print("Not a valid date")
            return False

    def input_date(text: str):
        while True:
            inp = input(text)
            if Inputs.validate(inp):
                date = datetime.strptime(inp, '%d-%m-%Y')
                return date.date()

    def input_int(text, error):
        while True:
            inp = input(text)
            if inp.isdigit():
                return inp
            print(error)
            
    def input_number(text, error):
        while True:
            inp = input(text)
            try:
                inp = float(inp)
                return inp
            except ValueError:
                if inp.isdigit():
                    return int(inp)
                print(error)

    