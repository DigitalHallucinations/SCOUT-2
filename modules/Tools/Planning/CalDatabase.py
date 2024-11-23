# modules/Tools/Planning/CalDatabase.py

import sqlite3
from sqlite3 import Error
import os

DB_PATH = 'modules/Tools/Planning/calendar.db'

class Database:
    def __init__(self):
        self.conn = self.create_connection()
        self.create_table()

    def create_connection(self):
        """ create a database connection to the SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH)
        except Error as e:
            print(e)
        return conn

    def create_table(self):
        """ create a table for appointments """
        try:
            sql_create_appointments_table = """ CREATE TABLE IF NOT EXISTS appointments (
                                                id integer PRIMARY KEY,
                                                date text NOT NULL,
                                                details text NOT NULL
                                            ); """
            c = self.conn.cursor()
            c.execute(sql_create_appointments_table)
        except Error as e:
            print(e)

    async def add_appointment(self, date, details):
        """ add a new appointment """
        sql = ''' INSERT INTO appointments(date, details)
                  VALUES(?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, (date, details))
        self.conn.commit()

    async def update_appointment(self, date, old_details, new_details):
        """ update an existing appointment """
        sql = ''' UPDATE appointments
                  SET details = ?
                  WHERE date = ? AND details = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (new_details, date, old_details))
        self.conn.commit()

    async def delete_appointment(self, date, details):
        """ delete an appointment """
        sql = ''' DELETE FROM appointments
                  WHERE date = ? AND details = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, (date, details))
        self.conn.commit()

    def get_appointments(self, date):
        """ get appointments for a specific date """
        cur = self.conn.cursor()
        cur.execute("SELECT details FROM appointments WHERE date=?", (date,))
        rows = cur.fetchall()
        return [row[0] for row in rows]

    def get_appointments_by_week(self, start_date, end_date):
        """ get appointments for a specific week """
        cur = self.conn.cursor()
        cur.execute("SELECT date, details FROM appointments WHERE date BETWEEN ? AND ?", (start_date, end_date))
        rows = cur.fetchall()
        return rows

    def get_appointments_by_month(self, year, month):
        """ get appointments for a specific month """
        cur = self.conn.cursor()
        cur.execute("SELECT date, details FROM appointments WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?", (year, month))
        rows = cur.fetchall()
        return rows

    def get_appointments_by_year(self, year):
        """ get appointments for a specific year """
        cur = self.conn.cursor()
        cur.execute("SELECT date, details FROM appointments WHERE strftime('%Y', date) = ?", (year,))
        rows = cur.fetchall()
        return rows

# Initialize the database and create the table if it doesn't exist
if not os.path.exists(DB_PATH):
    db = Database()