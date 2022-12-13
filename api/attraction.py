import os
from dotenv import load_dotenv
from flask import Blueprint, request, make_response
from mysql.connector import pooling
# from .database import database

load_dotenv()

dbconfig = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "database": os.getenv('DB_DATABASE')
}
connection_pool = pooling.MySQLConnectionPool(
    pool_name = "test",
    pool_size = 5,
    pool_reset_session = True,
    autocommit = True,
    **dbconfig
)

headers = {"Content-Type": "application/json"}
attraction = Blueprint("attraction", __name__)
# connection_pool=database.db_setting()

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

@attraction.route("/attractions", methods = ["GET"])
def api_attractions():
    page = request.args.get('page')
    keyword = request.args.get('keyword')
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        page = int(page)
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
        else:
            get_attraction_by_keyword_query = """
                SELECT attraction.id, attraction.name, attraction.category, attraction.description, attraction.address,
                attraction.transport, attraction.mrt, attraction.lat, attraction.lng,
                GROUP_CONCAT(img.url SEPARATOR ',')
                FROM attraction INNER JOIN img on img.attraction_id=attraction.id
                WHERE category = %s OR name LIKE %s
                GROUP BY attraction.id 
                LIMIT %s, 13
            """
            val = (keyword, '%' + keyword + '%', page * 12,)
            cursor.execute(get_attraction_by_keyword_query, val)
        result_list = cursor.fetchall()
        data_list = []
        if len(result_list) == 13:
            nextPage = page + 1
            for i in range(0, 13):
                attraction = generate_attraction_data(result_list[i])
                data_list.append(attraction)
        else:
            nextPage = None
            for i in range(0, len(result_list)):
                attraction = generate_attraction_data(result_list[i])
                data_list.append(attraction)
        response = make_response({"nextPage": nextPage, "data": data_list}, 200, headers)
        return response
    except Exception as e:
        print(e)
        response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
        return response
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
@attraction.route("/attraction/<int:attractionId>", methods = ["GET"])
def api_attraction(attractionId):
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
            response = make_response({"error": True, "message": "景點編號不正確"}, 400, headers)
            return response
        data = generate_attraction_data(result_list)
        response = make_response({"data": data}, 200, headers)
        return response
    except Exception as e:
        print(e)
        response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
        return response
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
