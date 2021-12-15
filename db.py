from sqlite3.dbapi2 import Cursor
# import pyodbc 
import sqlite3
from numpy.core.fromnumeric import sort
import pandas as pd
import os
import numpy as np
import itertools 
import random
import pickle


def unique(list1):
    x = np.array(list1)
    return list(np.unique(x))


"""
IN CASE OF ML MODEL
"""

def load_model(filename):
    pkl_filename = filename + ".pkl"

    # Load from file
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model


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


def get_most_liked_designs_cat_wise(cat):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT count(Image), Image FROM UserDesigns group by Image')
        result = list(cursor)
        count = [i[0] for i in result]
        image = [i[1] for i in result]
        results = tuple(image)
        cursor.execute(f'Select * from Designs where Images in {results[:-1] if len(results) < 1 else results} and Categories = "{cat}"')
        # print(results)
        results = list(cursor)
        designs = []
        for i in range(len(results)):
            designs.append({
                    'Image' : results[i][0],
                    'City' : results[i][1],
                    'Style' : results[i][2],
                    'Category' : results[i][3],
                    'Likes' : count[i]
            })
        designs  = sorted(designs, key=lambda x: x['Likes'], reverse=True)
        conn.close()
        return designs
    except Exception as e:
        # cursor.rollback()
        return False
    # else:
    #     if conn.connected == 1:
    #         conn.closed()

def get_most_liked_designs_cat_city_wise(cat, city):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT count(Image), Image FROM UserDesigns group by Image')
        result = list(cursor)
        count = [i[0] for i in result]
        image = [i[1] for i in result]
        results = tuple(image)
        cursor.execute(f'Select * from Designs where Images in {results[:-1] if len(results) < 1 else results} and Categories = "{cat}" and City = "{city}"')
        # print(results)
        results = list(cursor)
        designs = []
        for i in range(len(results)):
            designs.append({
                    'Image' : results[i][0],
                    'City' : results[i][1],
                    'Style' : results[i][2],
                    'Category' : results[i][3],
                    'Likes' : count[i]
            })
        designs  = sorted(designs, key=lambda x: x['Likes'], reverse=True)
        conn.close()
        return designs
    except Exception as e:
        cursor.rollback()
        return False
    # else:
    #     if conn.connected == 1:
    #         conn.closed()

def get_search_items():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            select * from Designs where City in ("Rawalpindi", "Islamabad")
        """)
        result = list(cursor)
        conn.close()
        search_list_01 = unique([i[-1] for i in result])
        search_list_02 = unique([i[-2] for i in result])
        search_list_03 = unique([i[-3] for i in result])
        search_list = list(itertools.chain(search_list_01,search_list_02,search_list_03))
        return search_list 
    except Exception:
        conn.close()
        return False


def get_category_items():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            select * from Designs where City in ("Rawalpindi", "Islamabad")
        """)
        result = list(cursor)
        conn.close()
        search_list = unique([i[-1] for i in result])        
        return search_list 
    except Exception:
        conn.close()
        return False


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

def ratings_table_insertion(user, image, rating):
    try:
        conn = connect()
        cursor = conn.cursor()
        sql_query = f"""
            insert into Ratings 
            values (
                "{image}",
                "{user}",
                "{rating}"
            )
        """
        cursor.execute(sql_query)
        conn.commit()
        conn.close()
        return "Thankyou for your feedback"
    except Exception as e:
        print(e)
        conn.rollback()
        return False

def predictions(uname):
    """
        Fetch all images
    """
    conn = connect()
    cursor = conn.cursor()
    sql_query = 'select * from Ratings'
    cursor.execute(sql_query)
    ratings = list(cursor)
    ratings = [list(i) for i in ratings]
    if len(ratings) > 0:
        userRatings = [i for i in ratings if i[1] == uname]
        if len(userRatings) > 1:
            ratedImages = tuple([i[1] for i in userRatings])
            sql_query = f"SELECT * FROM Designs where City in ('Rawalpindi', 'Islamabad') and Images not in {ratedImages}"
            cursor.execute(sql_query)
            results = list(cursor)
            conn.close()
            data = [list(i) for i in results]
            df = pd.DataFrame(data = data, columns = [
                'image',
                'city',
                'category',
                'style'
            ])

            svd = load_model("SVD")

            df['Estimate_Score'] = df['image'].apply(lambda x: svd.predict(x, 'johny').est)
            df = df.sort_values(by=['Estimate_Score'], ascending=False)
            records = df.head().to_dict('records')
            records = [{k: v for k, v in d.items() if k != 'Estimate_Score'} for d in records]

            return records
        else:
            return "You have not rated enough designs. Please use this app a little more"

    else:
        return "You have not rated enough designs. Please use this app a little more"


if __name__=="__main__":
    # print(get_rwp_designs("van123"))
    print(predictions("johny"))
    # data_insertion()
    # conn = connect()
    # cursor = conn.cursor()
    # sql_query = """
    #     select * from Ratings
    # """
    # sql_query = """
    #     CREATE TABLE Ratings(
    #     [Images] [varchar](520) NOT NULL,
    #     [Users] [varchar](255) NOT NULL,
    #     [Ratings] [real] NOT NULL
    #     )
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