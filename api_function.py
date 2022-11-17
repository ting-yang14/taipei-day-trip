from itertools import chain
import mysql.connector
from mysql.connector import Error, pooling

dbconfig = {
    "host": "localhost",
    "user":"root",
    "password": "test1234",
    "database": "taipei_day_trip"
}
connection_pool = pooling.MySQLConnectionPool(
    pool_name = "test",
    pool_size = 5,
    pool_reset_session = True,
    autocommit = True,
    **dbconfig
)

def get_attractions(page, keyword = None):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        page = int(page)
        keyword_list = get_categories()["data"]
        if keyword == None:
            get_attraction_id_query = "SELECT id FROM attraction"
            cursor.execute(get_attraction_id_query)
        elif keyword in keyword_list:
            get_attraction_by_category_query = "SELECT id FROM attraction WHERE category = %s"
            val = (keyword,)
            cursor.execute(get_attraction_by_category_query, val)
        else:
            get_attraction_by_name_query = "SELECT id FROM attraction WHERE name LIKE %s"
            val = ('%' + keyword + '%',)
            cursor.execute(get_attraction_by_name_query, val)
        result_id = cursor.fetchall()
        if not result_id:
            result = {"error":True, "message":"keyword not found"}
        else:
            id_list = list(chain.from_iterable(result_id))
            data_list = []
            if (page+1) * 12 < len(id_list):
                nextPage = page + 1
                for i in range(page * 12, (page + 1) * 12):
                    attraction = get_attraction(id_list[i])
                    data_list.append(attraction["data"])
                result = {"nextPage":nextPage, "data":data_list}
            if (page+1) * 12 - len(id_list) < 12:
                nextPage = None
                for i in range(page * 12, len(id_list)):
                    data_list.append(get_attraction(id_list[i])["data"])
                result = {"nextPage":nextPage, "data":data_list}
            else:
                result = {"error":True, "message":"page out of range"}
    except Error as error:
        result = {"error":True, "message":error}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return result

def get_attraction(attractionId):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        get_attraction_query = "SELECT * FROM attraction WHERE id = %s"
        val = (attractionId,)
        cursor.execute(get_attraction_query, val)
        attraction = cursor.fetchone()
        if not attraction:
            result = {"error":True, "message":"attractionID not found"}
        get_img_query = "SELECT url FROM img WHERE attraction_id = %s"
        cursor.execute(get_img_query, val)
        imgs = cursor.fetchall()
        img_result = list(chain.from_iterable(imgs))
        result = {"data":{
                        "id":attraction[0], 
                        "name":attraction[1], 
                        "category":attraction[2], 
                        "description":attraction[3],
                        "address":attraction[4],
                        "transport":attraction[5],
                        "mrt":attraction[6],
                        "lat":attraction[7],
                        "lng":attraction[8],
                        "images":img_result
                        }
                 }
    except Error as error:
        result = {"error":True, "message":error}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return result

def get_categories():
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        get_category_query = "SELECT category FROM attraction;"
        cursor.execute(get_category_query)
        category = cursor.fetchall()
        category_result = list(set(list(chain.from_iterable(category))))
        result = {"data": category_result}
    except Error as error:
        result = {"error": True, "message": error}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return result