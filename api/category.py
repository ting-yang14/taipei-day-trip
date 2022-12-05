from flask import Blueprint, jsonify
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

category = Blueprint("category", __name__)

        
@category.route("/categories", methods = ["GET"])
def api_categories():
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
        if "data" in result:
            return jsonify(result), 200
        return jsonify(result), 500