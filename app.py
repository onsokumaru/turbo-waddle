from UI import *
from database import *
import sqlite3

# create database, connection, and cursor
conn = sqlite3.connect('appDB.db')
c = conn.cursor()

# populate database tables with data
populate_database(c, conn)

# program start
main_menu()

