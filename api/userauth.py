from flask import Blueprint, jsonify, request, make_response
import json
import jwt
from datetime import datetime, timedelta
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

userauth = Blueprint("userauth", __name__)



@userauth.route("/user", methods = ["POST"])
def user():
    req = request.get_json()
    print(req)
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        check_email_query=f'SELECT EXISTS(SELECT * from member WHERE email="{req["email"]}")'
        cursor.execute(check_email_query)
        email_repeat=cursor.fetchone()
        print(email_repeat[0])
        if email_repeat[0]:
            response=make_response({"error":"email has been used"}, 400)
        else:
            add_user_query = f'INSERT INTO member (name, email, password) VALUES ("{req["name"]}","{req["email"]}","{req["password"]}")'
            cursor.execute(add_user_query)
            response=make_response({"ok":True}, 200)
    except Error as error:
        response=make_response({"error":error}, 500)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return response
        
    
    
@userauth.route("/user/auth", methods = ["GET", "PUT", "DELETE"])
def auth():
    # if request.method=="GET":
    #     result={
    #             "data": {
    #                     "id": 1,
    #                     "name": "彭彭彭",
    #                     "email": "ply@ply.com"
    #                     }
    #             }
    #     return jsonify(result), 200
    if request.method=="PUT":
        req = request.get_json()
        print(req)
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()
            check_auth_query=f'SELECT * FROM member WHERE email="{req["email"]}" and password="{req["password"]}"'
            cursor.execute(check_auth_query)
            member_info=cursor.fetchone()
            if member_info:
                token = jwt.encode({'id': member_info[0],'expiration': str(datetime.now() + timedelta(days=7))
                },"secret_key","HS256")
                print(token)
                detoken=jwt.decode(token, "secret_key", algorithms="HS256")
                print(detoken)
                
                response=make_response({"ok":True}, 200)
                response.set_cookie('access_token', token)
            else:
                response=make_response({"error":"email or password incorrect"}, 400)
        except Error as error:
            response=make_response({"error":error}, 500)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            return response
    # if request.method=="DELETE":
