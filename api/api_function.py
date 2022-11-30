from itertools import chain
from mysql.connector import Error, pooling

dbconfig = {
    "host": "localhost",
    "user":"root",
    "password": "TaipeiNO1",
    "database": "taipei_day_trip"
}
connection_pool = pooling.MySQLConnectionPool(
    pool_name = "test",
    pool_size = 5,
    pool_reset_session = True,
    autocommit = True,
    **dbconfig
)
def generate_attraction_data(attraction_data_list):
    return {
        "id": attraction_data_list[0], 
        "name": attraction_data_list[1], 
        "category": attraction_data_list[2], 
        "description": attraction_data_list[3],
        "address": attraction_data_list[4],
        "transport": attraction_data_list[5],
        "mrt": attraction_data_list[6],
        "lat": attraction_data_list[7],
        "lng": attraction_data_list[8],
        "images": attraction_data_list[9].split(",")
    }
def get_attractions(page, keyword = None):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        page = int(page)
        keyword_list = get_categories()["data"]
        if keyword == None:
            get_attractions_query = """
                SELECT attraction.id, attraction.name, attraction.category, attraction.description, attraction.address,
                attraction.transport, attraction.mrt, attraction.lat, attraction.lng,
                GROUP_CONCAT(img.url SEPARATOR ',')
                FROM attraction INNER JOIN img on img.attraction_id=attraction.id
                GROUP BY attraction.id
                LIMIT %s, 13
            """
            val = (page * 12,)
            cursor.execute(get_attractions_query, val)
        elif keyword in keyword_list:
            get_attraction_by_category_query = """
                SELECT attraction.id, attraction.name, attraction.category, attraction.description, attraction.address,
                attraction.transport, attraction.mrt, attraction.lat, attraction.lng,
                GROUP_CONCAT(img.url SEPARATOR ',')
                FROM attraction INNER JOIN img on img.attraction_id=attraction.id
                WHERE category = %s
                GROUP BY attraction.id
                LIMIT %s, 13
            """
            val = (keyword, page * 12,)
            cursor.execute(get_attraction_by_category_query, val)
        else:
            get_attraction_by_name_query = """
                SELECT attraction.id, attraction.name, attraction.category, attraction.description, attraction.address,
                attraction.transport, attraction.mrt, attraction.lat, attraction.lng,
                GROUP_CONCAT(img.url SEPARATOR ',')
                FROM attraction INNER JOIN img on img.attraction_id=attraction.id
                WHERE name LIKE %s
                GROUP BY attraction.id
                LIMIT %s, 13
            """
            val = ('%' + keyword + '%', page * 12,)
            cursor.execute(get_attraction_by_name_query, val)
        result_list = cursor.fetchall()
        data_list = []
        if len(result_list) == 13:
            nextPage = page + 1
            for i in range(0, 13):
                attraction = generate_attraction_data(result_list[i])
                data_list.append(attraction)
            result = {"nextPage": nextPage, "data": data_list}
        else:
            nextPage = None
            for i in range(0, len(result_list)):
                attraction = generate_attraction_data(result_list[i])
                data_list.append(attraction)
            result = {"nextPage": nextPage, "data": data_list}
    except Error as error:
        result = {"error": True, "message": error}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return result

def get_attraction(attractionId):
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        get_attraction_query = """
            SELECT attraction.id, attraction.name, attraction.category, attraction.description, attraction.address,
            attraction.transport, attraction.mrt, attraction.lat, attraction.lng,
            GROUP_CONCAT(img.url SEPARATOR ',')
            FROM attraction INNER JOIN img on img.attraction_id=attraction.id
            WHERE attraction.id = %s
            GROUP BY attraction.id
        """
        val = (attractionId,)
        cursor.execute(get_attraction_query, val)
        result_list = cursor.fetchone()
        if not result_list:
            result = {"error": True, "message": "attractionID not found"}
        data = generate_attraction_data(result_list)
        result = {"data": data}
    except Error as error:
        result = {"error": True, "message": error}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return result

def get_categories():
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        get_category_query = "SELECT DISTINCT category FROM attraction"
        cursor.execute(get_category_query)
        category = cursor.fetchall()
        category_result = list(chain.from_iterable(category))
        result = {"data": category_result}
    except Error as error:
        result = {"error": True, "message": error}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return result