import json
attraction_list=[]
img_list=[]
with open ('taipei-attractions.json', 'r') as file:
    data = json.load(file)
    attractions=data['result']['results']
    for attraction in attractions:
        attraction_list.append((attraction["_id"], attraction["name"], attraction["CAT"], attraction["description"], attraction["address"][:3]+attraction["address"][5:], attraction["direction"], attraction["MRT"], attraction["latitude"], attraction["longitude"]))
        imgs=attraction["file"].split("https")
        for img in imgs:
            if img[-3:]=='JPG' or img[-3:]=='jpg':
                img_list.append((attraction["_id"], f'https{img}'))
        
import mysql.connector
from mysql.connector import Error
create_db_query=f"CREATE DATABASE taipei_day_trip"
create_attraction_table_query="""
CREATE TABLE attraction(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name NVARCHAR(40),
    category NVARCHAR(20),
    description NVARCHAR(4000),
    address NVARCHAR(100),
    transport NVARCHAR(1000),
    mrt NVARCHAR(20),
    lat FLOAT(8,6),
    lng FLOAT(9,6)
)
"""
create_img_table_query="""
CREATE TABLE img(
    id INT AUTO_INCREMENT PRIMARY KEY,
    attraction_id INT,
    url VARCHAR(512)   
)
"""
add_foreign_key_query=f"ALTER TABLE img ADD FOREIGN KEY(attraction_id) REFERENCES attraction(id)"
insert_attraction_query = """
    INSERT INTO attraction
    (id, name, category, description, address, transport, mrt, lat, lng)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
insert_img_query = """
    INSERT INTO img
    (attraction_id, url)
    VALUES (%s, %s)
"""
try:
    connection = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "test1234",
                    database = "taipei_day_trip"
    )
    cursor=connection.cursor()
    # cursor.execute(create_db_query)
    cursor.execute(create_attraction_table_query)
    cursor.execute(create_img_table_query)
    cursor.execute(add_foreign_key_query)
    cursor.executemany(insert_attraction_query, attraction_list)
    cursor.executemany(insert_img_query, img_list)
    connection.commit()
except mysql.connector.Error as error:
    print(f"Failed to insert attraction to attraction table {error}")
finally: 
    if connection.is_connected():
        cursor.close()
        connection.close()