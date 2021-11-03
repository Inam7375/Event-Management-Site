import pyodbc 
import pandas as pd

df = pd.read_csv('creds.csv')
def connect():
    conn = pyodbc.connect('Driver={SQL Server};'
                      f'Server={df["Server"][0]};'
                      f'Database={df["Database Name"][0]};'
                      'Trusted_Connection=yes;')

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
        return users
    except Exception as e:
        cursor.rollback()
        return False
    except:
        if cursor.connected == 1:
            cursor.closed()
   

def get_user(uname):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Users where Username = '{uname}'")
        result = list(cursor)
        return {
            'Username' : result[0][0],
            'FirstName' : result[0][1],
            'LastName' : result[0][2],
            'City' : result[0][3],
            'Email' : result[0][4],
            'Date Joined' : result[0][6]        
            }   
        conn.close
    except Exception as e:
        cursor.rollback()
        return False
    else:
        if cursor.connected == 1:
            cursor.closed()

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
        cursor.commit()
        conn.close()
        return 'User has been successfully created'
    except Exception as e:
        print(e)
        cursor.rollback()
        return False
    except:
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
        cursor.commit()
        conn.close()
        return 'User has been successfully updated'
    except Exception as e:
        print(e)
        cursor.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()

if __name__=="__main__":
    print(get_users())
    # print(post_user(
    #     uname = "someone",
    #     fname = "Van",
    #     lname = "Helsing",
    #     city = "Hell",
    #     email = "vanhelsing@gmail.com",
    #     date = "11-03-2021",
    #     password = "van123"
    # ))