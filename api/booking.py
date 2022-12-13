import jwt
import os
from dotenv import load_dotenv
from flask import Blueprint, request, make_response
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

headers = {"Content-Type": "application/json"}
booking = Blueprint("booking", __name__)

def generate_booking_info(booking_info_list):
    return {
            "data": {
                    "attraction": {
                                    "id": booking_info_list[0],
                                    "name": booking_info_list[1],
                                    "address": booking_info_list[2],
                                    "image": booking_info_list[3]
                    },
            "date": booking_info_list[4],
            "time": booking_info_list[5],
            "price": booking_info_list[6]
            }
    }
            
@booking.route("/booking", methods = ["GET"])
def get():
    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()
            decode_token = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms = "HS256")   
            get_booking_info_query="""
                SELECT attraction.id, attraction.name, attraction.address, 
                       img.url, 
                       booking.date,booking.time, booking.price
                FROM attraction INNER JOIN img on img.attraction_id = attraction.id
                INNER JOIN booking on attraction.id = booking.attraction_id
                WHERE booking.member_id = %s
                LIMIT 1;
            """
            val = (decode_token["id"],)
            cursor.execute(get_booking_info_query, val)
            result_list = cursor.fetchone()
            if result_list:
                booking_info = generate_booking_info(result_list)
                response = make_response(booking_info, 200, headers)
            else:
                response = make_response({"data": None}, 200, headers)
            return response
        except Exception as e:
            print(e)
            response = make_response({"error": True,"message": "伺服器內部錯誤"}, 500, headers)
            return response
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        response = make_response({"error": True, "message": "未登入系統，拒絕存取"}, 403, headers)
        return response
    
@booking.route("/booking", methods = ["POST"])
def post():
    req = request.get_json()
    for item in req.values():
        if not item:
           response = make_response({"error": True,"message": "建立失敗，輸入不正確或其他原因"}, 400, headers)
           return response

    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            decode_token = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms = "HS256") 
            connection = connection_pool.get_connection()
            cursor = connection.cursor() 
            add_booking_query="""
                REPLACE INTO booking (member_id, attraction_id, date, time, price) 
                VALUES (%s, %s, %s, %s, %s);
            """
            val = (decode_token["id"], req["attractionId"], req["date"], req["time"], req["price"],)
            cursor.execute(add_booking_query, val)
            response = make_response({"ok": True}, 200, headers)
            return response
        except Exception as e:
            print(e)
            response = make_response({"error": True,"message": "伺服器內部錯誤"}, 500, headers)
            return response
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        response = make_response({"error": True, "message": "未登入系統，拒絕存取"}, 403, headers)
        return response

@booking.route("/booking", methods = ["DELETE"])
def delete():
    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()
            decode_token = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms = "HS256")   
            delete_booking_info_query="""
                DELETE FROM booking 
                WHERE member_id = %s;
            """
            val = (decode_token["id"],)
            cursor.execute(delete_booking_info_query, val)
            response = make_response({"ok": True}, 200, headers)
            return response
        except Exception as e:
            print(e)
            response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
            return response
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        response = make_response({"error": True, "message": "未登入系統，拒絕存取"}, 403, headers)
        return response