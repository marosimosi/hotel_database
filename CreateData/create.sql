BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Client" (
	"ssn"	integer NOT NULL,
	"email"	string NOT NULL,
	"telephone"	integer NOT NULL,
	"address"	string NOT NULL,
	PRIMARY KEY("ssn")
);
CREATE TABLE IF NOT EXISTS "Agency" (
	"name"	string NOT NULL,
	"web_page"	string NOT NULL,
	"commision"	float NOT NULL,
	"agency_ssn"	integer NOT NULL,
	PRIMARY KEY("agency_ssn"),
	FOREIGN KEY ("agency_ssn") REFERENCES "Client"("ssn")
);
CREATE TABLE IF NOT EXISTS "Booking" (
	"booking_id"	integer NOT NULL,
	"price"	float NOT NULL,
	"arrival"	date NOT NULL,
	"departure"	date NOT NULL,
	"downpayment"	float NOT NULL,
	"paid_amount"	float NOT NULL DEFAULT 0,
	"dp_due_date"	date NOT NULL,
	"pay_method"	string NOT NULL,
	"children"	integer NOT NULL DEFAULT 0,
	"adults"	integer NOT NULL,
	"ssn"	integer NOT NULL,
	PRIMARY KEY("booking_id" AUTOINCREMENT),
	FOREIGN KEY ("ssn") REFERENCES "Client"("ssn")
);
CREATE TABLE IF NOT EXISTS "Books" (
	"booking_id"	integer NOT NULL,
	"room_id"	integer NOT NULL,
	"booking_date"	date NOT NULL,
	PRIMARY KEY("booking_id","room_id"),
	FOREIGN KEY ("booking_id") REFERENCES "Booking"("booking_id"),
	FOREIGN KEY ("room_id") REFERENCES "Room"("room_id")
);
CREATE TABLE IF NOT EXISTS "Fills" (
	"booking_id"	integer NOT NULL,
	"room_id"	integer NOT NULL,
	"check_in"	date NOT NULL,
	"check_out"	date,
	PRIMARY KEY("booking_id","room_id"),
	FOREIGN KEY ("booking_id") REFERENCES "Booking"("booking_id"),
	FOREIGN KEY ("room_id") REFERENCES "Room"("room_id")
);
CREATE TABLE IF NOT EXISTS "Individual" (
	"Fname"	string NOT NULL,
	"Lname"	string NOT NULL,
	"Bdate"	date NOT NULL,
	"individual_ssn"	integer NOT NULL,
	PRIMARY KEY("individual_ssn"),
	FOREIGN KEY ("individual_ssn") REFERENCES "Client"("ssn")
);
CREATE TABLE IF NOT EXISTS "Review" (
	"review_id"	integer NOT NULL,
	"text"	text,
	"date"	date NOT NULL,
	"score"	integer NOT NULL,
	"ssn"	integer NOT NULL,
	"type_name"	string NOT NULL,
	PRIMARY KEY("review_id" AUTOINCREMENT),
	FOREIGN KEY ("ssn") REFERENCES "Client"("ssn"),
	FOREIGN KEY ("type_name") REFERENCES "Type"("type_name")
);
CREATE TABLE IF NOT EXISTS "Room" (
	"room_id"	integer NOT NULL,
	"floor"	integer NOT NULL,
	"type_name"	string NOT NULL,
	PRIMARY KEY("room_id" AUTOINCREMENT),
	FOREIGN KEY ("type_name") REFERENCES "Type"("type_name")
);
CREATE TABLE IF NOT EXISTS "Type" (
	"type_name"	string NOT NULL,
	"low_season"	float NOT NULL,
	"mid_season"	float NOT NULL,
	"high_season"	float NOT NULL,
	PRIMARY KEY("type_name")
);
COMMIT;
