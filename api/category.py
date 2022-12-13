import os
from dotenv import load_dotenv
from flask import Blueprint, make_response
from itertools import chain
from mysql.connector import pooling

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

headers={"Content-Type": "application/json"}
category = Blueprint("category", __name__)
        
@category.route("/categories", methods = ["GET"])
def get():
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        get_category_query = """
            SELECT DISTINCT category 
            FROM attraction
        """
        cursor.execute(get_category_query)
        category = cursor.fetchall()
        category_result = list(chain.from_iterable(category))
        response = make_response({"data": category_result}, 200, headers)
        return response
    except Exception as e:
        print(e)
        response = make_response({"error": True, "message": "伺服器內部錯誤"})
        return response
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        