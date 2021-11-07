from sqlite3.dbapi2 import Cursor
# import pyodbc 
import sqlite3
import pandas as pd

# df = pd.read_csv('creds.csv')
def connect():
    # conn = pyodbc.connect('Driver={SQL Server};'
    #                   f'Server={df["Server"][0]};'
    #                   f'Database={df["Database Name"][0]};'
    #                   'Trusted_Connection=yes;')
    conn = sqlite3.connect('Users.sqlite')

    return conn

"""
    USER END POINTS 
"""
def get_users():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Users")
        result = list(cursor)
        users = {}
        for i in range(len(result)):
            users.update({
                f'User_{i}' : {
                    'Username' : result[i][0],
                    'FirstName' : result[i][1],
                    'LastName' : result[i][2],
                    'City' : result[i][3],
                    'Email' : result[i][4],
                    'Date Joined' : result[i][6]        
                }
            })
        conn.close()
        return users
    except Exception as e:
        # cursor.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()
   

def get_user(uname):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Users where Username = '{uname}'")
        result = list(cursor)
        conn.close()
        return {
            'Username' : result[0][0],
            'FirstName' : result[0][1],
            'LastName' : result[0][2],
            'City' : result[0][3],
            'Email' : result[0][4],
            'Password' : result[0][5],
            'Date Joined' : result[0][6]        
            }   
    except Exception as e:
        # cursor.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()

def post_user(
    uname,
    fname,
    lname,
    city,
    email,
    password,
    date
):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"insert into Users ([Username], [FirstName], [LastName], [City], [Email], [Password], [Date]) values ('{uname}', '{fname}', '{lname}', '{city}', '{email}', '{password}', '{date}')"
        )
        conn.commit()
        conn.close()
        return 'User has been successfully created'
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()

def update_user(
    uname,
    fname,
    lname,
    city,
    email,
    password,
):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"update Users set FirstName='{fname}', LastName='{lname}', City='{city}', Email='{email}', Password='{password}' where  Username='{uname}'"
        )
        conn.commit()
        conn.close()
        return 'User has been successfully updated'
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()

if __name__=="__main__":
    conn = connect()
    cursor = conn.cursor()
    sql_query = """
        CREATE TABLE Users(
        [Username] [nvarchar](255) NULL,
        [FirstName] [varchar](255) NULL,
        [LastName] [varchar](255) NULL,
        [City] [varchar](255) NULL,
        [Email] [nvarchar](255) NULL,
        [Password] [nvarchar](320) NULL,
        [Date] [date] NULL)
    """
    cursor.execute(sql_query)
    # print(get_users())
    # print(post_user(
    #     uname = "someone",
    #     fname = "Van",
    #     lname = "Helsing",
    #     city = "Hell",
    #     email = "vanhelsing@gmail.com",
    #     date = "11-03-2021",
    #     password = "van123"
    # ))