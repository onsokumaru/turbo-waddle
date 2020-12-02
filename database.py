import sqlite3
import time
import random


# create database and cursor
# conn = sqlite3.connect('appDB.db')
# c = conn.cursor()

# function to create tables, and insert data
def populate_database(cursor, connection):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Service_Requests(
            TICKET_NUM INTEGER PRIMARY KEY AUTOINCREMENT,
            TECH_L_NAME     CHAR(30)     NOT NULL,
            TECH_F_NAME     CHAR(30)     NOT NULL,
            CUST_L_NAME     CHAR(30)     NOT NULL,
            CUST_F_NAME     CHAR(30)     NOT NULL,
            CUST_DEPART     TEXT         NOT NULL,
            REQUEST_DATE    TEXT         NOT NULL,
            REQUEST_DESC    TEXT         NOT NULL,
            IS_OPEN         INT          NOT NULL,
            COMPLETE_DATE   TEXT,
            NOTES           TEXT
        );

        CREATE TABLE IF NOT EXISTS Tech_Department(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            LAST_NAME          CHAR(30)  NOT NULL,
            FIRST_NAME         CHAR(30)  NOT NULL
        );                    

        INSERT INTO Tech_Department(LAST_NAME, FIRST_NAME)
        VALUES
            ('Hammond', 'Dickie'),
            ('Hannah', 'Chris'),
            ('Stubbs', 'Frankie'),
            ('Ott', 'Jeff');

        INSERT INTO Service_Requests (TECH_L_NAME,TECH_F_NAME,CUST_L_NAME,CUST_F_NAME,CUST_DEPART,REQUEST_DATE,REQUEST_DESC, IS_OPEN)
        VALUES
            ('Ott', 'Jeff', 'Doe', 'Jane', 'Accounting' , '2020-10-23', 'request for new printer', 1),
            ('Hannah', 'Chris', 'Smith', 'John', 'Marketing', '2020-10-23', 'request for new monitor', 1),
            ('Hammond', 'Dickie', 'Jones', 'Susan', 'IT', '2020-10-20', 'request for new NIC', 1),
            ('Stubbs', 'Frankie', 'Roberts', 'Mike', 'Sales', '2020-10-22', 'request for new laptop', 1),
            ('Ott', 'Jeff', 'Astor', 'Mary', 'IT', '2020-10-20', 'request for new router', 1);

        INSERT INTO Service_Requests (TECH_L_NAME,TECH_F_NAME,CUST_L_NAME,CUST_F_NAME,CUST_DEPART,REQUEST_DATE,REQUEST_DESC, IS_OPEN, COMPLETE_DATE)
        VALUES
            ('Hammond', 'Dickie', 'Steven', 'Mark', 'Accounting', '2020-10-24', 'fix jammed printer cartridge', 0, '2020-10-24'),
            ('Hannah', 'Chris', 'Miller', 'Sally', 'HR', '2020-09-15', 'lost internet access', 0, '2020-09-15'),
            ('Stubbs', 'Frankie', 'Jenkins', 'Leroy', 'Admin', '2020-09-30', 'request for new mousepad', 0, '2020-09-30'),
            ('Ott', 'Jeff', 'Hill', 'Dule', 'Sales', '2020-10-25', 'microsoft word not printing', 0, '2020-10-25'),
            ('Hammond', 'Dickie', 'Spencer', 'Shawn', 'Admin', '2020-10-05', 'email not sending', 0, '2020-10-05'),
            ('Hannah', 'Chris', 'Phillips', 'Ken', 'Marketing', '2020-09-10', 'computer will not power on', 0, '2020-09-12'),
            ('Stubbs', 'Frankie', 'Douglas', 'Tim', 'Marketing', '2020-10-22', 'laptop not connecting to wifi', 0, '2020-10-22'),
            ('Ott', 'Jeff', 'Roberts', 'Shannon', 'Sales', '2020-09-02', 'voip phones are down', 0, '2020-09-02'),
            ('Hannah', 'Chris', 'Williamson', 'Tim', 'Accounting', '2020-10-07', 'request for new laptop', 0, '2020-10-14'),
            ('Hammond', 'Dickie', 'Brown', 'Millie', 'HR', '2020-10-12', 'pc monitor is glitchy', 0, '2020-10-12');

    """)
    connection.commit()


# list of service techs
techs = ['Dickie Hammond', 'Chris Hannah', 'Jeff Ott', 'Frankie Stubbs']


# function to create service request
def create_request(cursor, connection, employee_last_name, employee_first_name, employee_department, request):
    tech_on_call = random.choice(techs)

    t_last_name = tech_on_call.split()[1]
    t_first_name = tech_on_call.split()[0]
    c_last_name = employee_last_name
    c_first_name = employee_first_name
    c_department = employee_department
    date = time.strftime('%Y-%m-%d')
    open_ticket = 1

    cursor.execute(
        "INSERT INTO Service_Requests(TECH_L_NAME, TECH_F_NAME, CUST_L_NAME, CUST_F_NAME, CUST_DEPART, REQUEST_DATE, REQUEST_DESC, IS_OPEN) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (t_last_name, t_first_name, c_last_name, c_first_name, c_department, date, request, open_ticket))

    connection.commit()


# function to query service request table and return results - open requests
def fetch_open_requests(cursor):
    closed = 1
    rows = cursor.execute("SELECT TECH_L_NAME,TECH_F_NAME,REQUEST_DATE,REQUEST_DESC,COMPLETE_DATE,NOTES FROM Service_Requests \
             where IS_OPEN = ? ORDER BY TECH_L_NAME", (closed,), ).fetchall()
    return rows


# function to query service request table and return results - closed requests
def fetch_closed_requests(cursor):
    is_open = 0
    rows = cursor.execute("SELECT TECH_L_NAME,TECH_F_NAME,REQUEST_DATE,REQUEST_DESC,COMPLETE_DATE,NOTES FROM Service_Requests \
             where IS_OPEN = ? ORDER BY TECH_L_NAME", (is_open,), ).fetchall()
    return rows

# function to format the results from sql query
def format_query_results(results):
    print("=" * 101)
    print("%-15s\t%-15s\t%-15s\t%-30s\t%-15s\t%-15s" % ("TECH L NAME", "TECH F NAME", "REQUEST DATE", "DESCRIPTION", "COMPLETE DATE", "NOTES"))
    print("=" * 101)
    for i in results:
        print("%-15s\t%-15s\t%-15s\t%-30s\t%-15s\t%-15s" % (i[0], i[1], i[2], i[3], i[4], i[5]))


def clear_database(cursor, connection):
    # function to drop both tables from database
    cursor.execute("DROP TABLE Service_Requests")
    cursor.execute("DROP TABLE Tech_Department")
    connection.commit()
