import os
import psycopg2
from connections import get_connection
from dotenv import load_dotenv

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY,
    first_name varchar(25) not null, last_name varchar(25) not null, income int not null, debt_total int not null,
    rent int default 1600, prop_tax int default 1.05, phone_number varchar(14) default 3025551206, power int default 80,
    water int default 72, garbage int default 14, cable int default 104, prescriptions int default 90,
    doctor_visits int default 150, daycare int default 75, carpayment1 int default 280, carpayment2 int default 280,
    autoinsurance int default 140, gasoline int default 150, groceries int default 200, pchi int default 80);"""

INSERT_INFO = """INSERT INTO users(first_name, last_name, prop_tax, phone_number, rent, debt_total, income,
    power_bill, water_bill, insurance) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

SELECT_INFO = """SELECT * from users where id = (%s);"""

class Query:
    def __init__(self, first_name, last_name, prop_tax, phone_number, rent, debt_total, income, power_bill, water_bill, insurance):
        self.first_name = first_name
        self.last_name = last_name
        self.prop_tax = prop_tax
        self.phone_number = phone_number
        self.rent = rent
        self.debt_total = debt_total
        self.income = income
        self.power_bill = power_bill
        self.water_bill = water_bill
        self.insurance = insurance

    def __str__(self):
        return f"""First Name: {self.first_name}
            Last Name: {self.last_name}
            Property Tax: {self.prop_tax}
            Phone Number: {self.phone_number}
            Rent: {self.rent}
            Debt Total: {self.debt_total}
            Income: {self.income}
            Power Bill: {self.power_bill}
            Water Bill: {self.water_bill}
            Insurance: {self.insurance}"""

    def create_tables(self):
        """
        Creates the table (copy safe)
        """
        with get_connection() as connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(CREATE_TABLE)

    def insert_all(self):
        """
        Inserts data when ALL data is known
        """
        with get_connection() as connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(INSERT_INFO, (self.first_name, self.last_name, self.prop_tax,
                                                 self.phone_number, self.rent, self.debt_total,
                                                 self.income, self.power_bill, self.water_bill,
                                                 self.insurance));

    def select_all(self, person_id):
        """
        Selects all data based off the passed person id
        Returns: A list of one tuple containing the attributes of the person_id passed
        """
        rows = []
        with get_connection() as connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(SELECT_INFO, (person_id,))
                    rows = cursor.fetchall()
        return rows
