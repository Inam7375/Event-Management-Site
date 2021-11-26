from sqlite3.dbapi2 import Cursor
# import pyodbc 
import sqlite3
from numpy.core.fromnumeric import sort
import pandas as pd
import os


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

def get_rwp_designs(username):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM Designs where City = "Rawalpindi"')
        result = list(cursor)
        cursor.execute(f'SELECT Image FROM UserDesigns where Username = "{username}"')
        liked_images = [i[0] for i in list(cursor)]
        print(liked_images)
        designs = []
        for i in range(len(result)):
            designs.append({
                    'Image' : result[i][0],
                    'City' : result[i][1],
                    'Style' : result[i][2],
                    'Category' : result[i][3],
                    'Liked' : 'Yes' if  result[i][0] in liked_images else 'No'   
            })
        conn.close()
        return designs
    except Exception as e:
        # cursor.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()
   
def get_isb_designs(username):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM Designs where City = "Islamabad"')
        result = list(cursor)
        cursor.execute(f'SELECT Image FROM UserDesigns where Username = "{username}"')
        liked_images = [i[0] for i in list(cursor)]
        designs = []
        for i in range(len(result)):
            designs.append({
                    'Image' : result[i][0],
                    'City' : result[i][1],
                    'Style' : result[i][2],
                    'Category' : result[i][3],
                    'Liked' : 'Yes' if  result[i][0] in liked_images else 'No'   

            })
        conn.close()
        return designs
    except Exception as e:
        # cursor.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()
   
def get_all_designs():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM Designs')
        result = list(cursor)
        designs = []
        for i in range(len(result)):
            designs.append({
                    'Image' : result[i][0],
                    'City' : result[i][1],
                    'Style' : result[i][2],
                    'Category' : result[i][3]
            })
        conn.close()
        return designs
    except Exception as e:
        # cursor.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()
   
def user_likes_design(image, username):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f"insert into UserDesigns ([Username], [Image]) values ('{username}', '{image}')"
        )
        conn.commit()
        conn.close()
        return 'User design has been successfully added'
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()

def user_dislikes_design(image, username):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            f'delete from UserDesigns where Username = "{username}" and Image = "{image}"'
        )
        conn.commit()
        conn.close()
        return 'User design has been successfully removed'
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()

def get_user_designs(username):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT Image FROM UserDesigns where Username = "{username}"')
        results = [i[0] for i in list(cursor)]
        results = tuple(results)
        cursor.execute(f'Select * from Designs where Images in {results[:-1] if len(results) < 1 else results}')
        results = list(cursor)
        designs = []
        for i in range(len(results)):
            designs.append({
                    'Image' : results[i][0],
                    'City' : results[i][1],
                    'Style' : results[i][2],
                    'Category' : results[i][3]
            })
        conn.close()
        return designs
    except Exception as e:
        # cursor.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()



def data_insertion():
    df = pd.DataFrame()
    dir_list = []
    dirs = os.listdir('scrapePosts\Islamabad')
    dir_list.append(['scrapePosts\Islamabad\\'+i for i in dirs])
    dirs = os.listdir('scrapePosts\Rawalpindi')
    dir_list.append(['scrapePosts\Rawalpindi\\'+i for i in dirs])
    
    for i in range(len(dir_list)):
        print(i)
        counter = 0
        for j in dir_list[i]:
            temp_df = pd.read_csv(j)
            if i == 0 and counter == 0:
                df = temp_df
            else:
                df = df.append(temp_df, sort=False) 
            counter = counter + 1
    df.reset_index(inplace=True)
    try:
        conn = connect()
        cursor = conn.cursor()
        for k in range(df.shape[0]):
            try:
                cursor.execute(
                    f"insert into Designs ([Images], [City], [Styles], [Categories]) values ('{df.Images[k]}', '{df.City[k]}', '{df.Styles[k]}', '{df.Categories[k]}')"
                )
                conn.commit()
            except Exception:
                pass
        conn.close()
        return 'Designs has been successfully inserted'
    except Exception as e:
        print(e)
        conn.rollback()
        return False
    else:
        if conn.connected == 1:
            conn.closed()

if __name__=="__main__":
    # print(get_user_designs('someone'))
    print(user_likes_design('https://kitandkaboodle.com/wp-content/uploads/2021/10/6R3A0151-1-1024x1024.jpg', 'someone'))
    # data_insertio n()
    # conn = connect()
    # cursor = conn.cursor()
    # sql_query = """
    #     select * from UserDesigns
    # """
    # sql_query = """
    #     CREATE TABLE Designs(
    #     [Images] [varchar](520) primary key,
    #     [City] [varchar](255) NULL,
    #     [Styles] [varchar](255) NULL,
    #     [Categories] [nvarchar](255) NULL)
    # """
    # print(list(cursor.execute(sql_query)))
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
    pass