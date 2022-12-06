from flask import Blueprint, request, make_response
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
    if request.method=="GET":
        access_token = request.cookies.get('access_token')
        if access_token:
            try:
                connection = connection_pool.get_connection()
                cursor = connection.cursor()
                decode_token=jwt.decode(access_token, "secret_key", algorithms="HS256")
                get_member_info_query=f'SELECT id, name, email FROM member WHERE id="{decode_token["id"]}"'
                cursor.execute(get_member_info_query)
                member_info=cursor.fetchone()
                response=make_response({"data":{"id":member_info[0], "name":member_info[1],"email":member_info[2]}}, 200)
            except Error as error:
                response=make_response({"error":error}, 500)
        else:
            response=make_response({"data":None}, 200)
        return response
    if request.method=="PUT":
        req = request.get_json()
        try:
            connection = connection_pool.get_connection()
            cursor = connection.cursor()
            check_auth_query=f'SELECT * FROM member WHERE email="{req["email"]}" and password="{req["password"]}"'
            cursor.execute(check_auth_query)
            member_info=cursor.fetchone()
            if member_info:
                token = jwt.encode({'id': member_info[0]
                },"secret_key","HS256")
                response=make_response({"ok":True}, 200)
                response.set_cookie('access_token', token, expires=datetime.now() + timedelta(days=7))
            else:
                response=make_response({"error":"email or password incorrect"}, 400)
        except Error as error:
            response=make_response({"error":error}, 500)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            return response
    if request.method=="DELETE":
        response=make_response({"ok":True}, 200)
        response.set_cookie('access_token', "", expires=0)
        return response