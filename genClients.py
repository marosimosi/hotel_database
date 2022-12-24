import sqlite3
import pandas as pd


client_data = pd.read_excel("client.xlsx")
agency_data = pd.read_excel("agency.xlsx")
individual_data = pd.read_excel("individual.xlsx")

with sqlite3.connect("database.db") as conn:
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

    conn.commit()
