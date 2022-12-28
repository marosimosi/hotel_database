import sqlite3
import pandas as pd


booking_data = pd.read_excel("booking.xlsx")
books_data = pd.read_excel("books.xlsx")
fills_data = pd.read_excel("fills.xlsx")
not_available_data = pd.read_excel("not_available.xlsx")

with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()

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
        type_name = row["type_name"]
        booking_date = row["booking_date"].date()
        cursor.execute(
            f"""INSERT or REPLACE INTO BOOKS
            VALUES (?,?,?); """, (booking_id, type_name, booking_date) 
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

    for _, row in not_available_data.iterrows():
        room_id = row["room_id"]
        date = row["date"].date()
        cursor.execute(
            f"""INSERT or REPLACE INTO NOT_AVAILABLE
            VALUES (?,?); """, (room_id, date)
        )

    conn.commit()
