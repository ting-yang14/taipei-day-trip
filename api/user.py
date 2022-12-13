import jwt
import os
from datetime import datetime, timedelta
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
user = Blueprint("user", __name__)

@user.route("/user", methods = ["POST"])
def post():
    req = request.get_json()
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        check_email_query = """
            SELECT EXISTS (SELECT * 
                           FROM member 
                           WHERE email = "%s")
        """
        val = (req["email"],)
        cursor.execute(check_email_query)
        email_repeat = cursor.fetchone()
        if email_repeat[0]:
            response = make_response({"error": True, "message": "email已被註冊"}, 400, headers)
        else:
            add_user_query = """
                INSERT INTO member (name, email, password) VALUES (%s, %s, %s);
            """
            val = (req["name"], req["email"], req["password"],)
            cursor.execute(add_user_query, val)
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
        
@user.route("/user/auth", methods = ["GET"])
def get():
    access_token = request.cookies.get('access_token')
    if access_token:
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()
            decode_token = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms = "HS256")
            get_member_info_query = """
                SELECT id, name, email 
                FROM member 
                WHERE id = %s
            """
            val = (decode_token["id"],)
            cursor.execute(get_member_info_query, val)
            member_info = cursor.fetchone()
            response = make_response({"data":{"id": member_info[0], "name": member_info[1], "email": member_info[2]}}, 200, headers)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        response = make_response({"data": None}, 200, headers)
    return response
    
@user.route("/user/auth", methods = ["PUT"])
def put():
    req = request.get_json()
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        check_auth_query = """
            SELECT * 
            FROM member 
            WHERE email = %s AND password = %s
        """
        val = (req["email"], req["password"],)
        cursor.execute(check_auth_query, val)
        member_info = cursor.fetchone()
        if member_info:
            token = jwt.encode({"id": member_info[0]
            }, os.getenv('JWT_SECRET_KEY'), "HS256")
            response = make_response({"ok": True}, 200)
            response.set_cookie("access_token", token, expires = datetime.now() + timedelta(days = 7))
        else:
            response = make_response({"error": True, "message": "email或密碼錯誤"}, 400)
        return response
    except Exception as e:
        print(e)
        response =make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
        return response
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        
@user.route("/user/auth", methods = ["DELETE"])
def delete():
    response = make_response({"ok": True}, 200, headers)
    response.set_cookie("access_token", "", expires = 0)
    return response