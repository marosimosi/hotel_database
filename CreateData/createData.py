import sqlite3
import pandas as pd


client_data = pd.read_excel("CreateData/ExcelFiles/client.xlsx")
agency_data = pd.read_excel("CreateData/ExcelFiles/agency.xlsx")
individual_data = pd.read_excel("CreateData/ExcelFiles/individual.xlsx")
reviews_data = pd.read_excel("CreateData/ExcelFiles/reviews.xlsx")
booking_data = pd.read_excel("CreateData/ExcelFiles/booking.xlsx")
books_data = pd.read_excel("CreateData/ExcelFiles/books.xlsx")
fills_data = pd.read_excel("CreateData/ExcelFiles/fills.xlsx")
typedata = pd.read_excel("CreateData/ExcelFiles/type.xlsx")
roomdata = pd.read_excel("CreateData/ExcelFiles/room.xlsx")

with sqlite3.connect("CreateData/database.db") as conn:
    cursor = conn.cursor()

    for _, row in client_data.iterrows():
        ssn = row["ssn"]
        email = row["email"]
        telephone = row["telephone"]
        address = row["address"]
        cursor.execute(
            f"""INSERT or REPLACE INTO CLIENT
        VALUES (?,?,?,?);""", (ssn, email, telephone, address)
        )

    for _, row in agency_data.iterrows():
        name = row["name"]
        web_page = row["web_page"]
        commision = float(row["comission"])
        agency_ssn = row["agency_ssn"]
        cursor.execute(
            f"""INSERT or REPLACE INTO AGENCY
        VALUES (?,?,?,?);""", (name, web_page, commision, agency_ssn)
        )

    for _, row in individual_data.iterrows():
        Fname = row["Fname"]
        Lname = row["Lname"]
        Bdate = row["Bdate"].date()
        individual_ssn = row["individual_ssn"]
        cursor.execute(
            f"""INSERT or REPLACE INTO INDIVIDUAL
            VALUES (?,?,?,?);""", (Fname, Lname, Bdate, individual_ssn)
        )

    for _, row in reviews_data.iterrows():
        review_id = row["review_id"]
        text = row["text"]
        date = row["date"].date()
        score = row["score"]
        ssn = row["ssn"]
        type_name = row["type_name"]
        cursor.execute(
            f"""INSERT or REPLACE INTO REVIEW
            VALUES (?,?,?,?,?,?);""", (review_id, text, date, score, ssn, type_name)
        )

    for _, row in booking_data.iterrows():
        booking_id = row["booking_id"]
        price = float(row["price"])
        arrival = row["arrival"].date()
        departure = row["departure"].date()
        downpayment = float(row["downpayment"])
        paid_amount = float(row["paid_amount"])
        dp_due_date = row["dp_due_date"].date()
        pay_method = row["pay_method"]
        children = row["children"]
        adults = row["adults"]
        ssn = row["ssn"]
        cursor.execute(
            f"""INSERT or REPLACE INTO BOOKING
        VALUES (?,?,?,?,?,?,?,?,?,?,?);""", (booking_id, price, arrival, departure, downpayment, paid_amount, dp_due_date, pay_method, children, adults, ssn)
        )

    for _, row in books_data.iterrows():
        booking_id = row["booking_id"]
        room_id = row["room_id"]
        booking_date = row["booking_date"].date()
        cursor.execute(
            f"""INSERT or REPLACE INTO BOOKS
            VALUES (?,?,?); """, (booking_id, room_id, booking_date) 
        )

    for _, row in fills_data.iterrows():
        booking_id = row["booking_id"]
        room_id = row["room_id"]
        check_in = row["check_in"].date()
        check_out = row["check_out"].date()
        cursor.execute(
            f"""INSERT or REPLACE INTO FILLS
            VALUES (?,?,?,?); """, (booking_id, room_id, check_in, check_out) 
        )

    for _, row in typedata.iterrows():
        type_name = row["type_name"]
        low_season = float(row["low"])
        mid_season = float(row["mid"])
        high_season = float(row["high"])
        cursor.execute(
            f"""INSERT or REPLACE INTO TYPE
        VALUES (?,?,?,?);""", (type_name, low_season, mid_season, high_season)
        )

    for _, row in roomdata.iterrows():
        room_id = row["room_id"]
        floor = row["floor"]
        type_name = row["type_name"]
        cursor.execute(
            f"""INSERT or REPLACE INTO ROOM
        VALUES (?,?,?);""", (room_id, floor, type_name)
        )

    conn.commit()
 