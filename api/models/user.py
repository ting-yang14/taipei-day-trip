import jwt
import os
from dotenv import load_dotenv
from ..database import database
mysql_pool = database.MySQLPool(**database.dbconfig)

load_dotenv()

class User:
    def __init__(self):
        pass

    def check_email_repeat(self, email):
        check_email_query = """
            SELECT EXISTS (SELECT * 
                           FROM member 
                           WHERE email = %s)
        """
        repeat_email_num =  mysql_pool.execute(check_email_query, (email,))[0][0]
        if repeat_email_num:
            return True
        else:
            return False
    
    def signup(self, request):
        signup_query = """
            INSERT INTO member 
            (name, email, password) 
            VALUES (%s, %s, %s);
        """
        mysql_pool.execute(signup_query, (request["name"], request["email"], request["password"],), True)
        result = True
        print("signup result:", result)
        return result
    
    def signin(self, request):
        signin_query = """
            SELECT * 
            FROM member 
            WHERE email = %s AND password = %s
        """
        user_id = mysql_pool.execute(signin_query, (request["email"], request["password"],))[0][0]
        return user_id

    def get_user_info(self, user_id):
        get_user_info_query = """
            SELECT id, name, email 
            FROM member 
            WHERE id = %s
        """ 
        result = mysql_pool.execute(get_user_info_query, (user_id,))[0]
        user_info = {"id": result[0], "name": result[1], "email": result[2]}
        return user_info

    def set_auth(self, user_id):
        access_token = jwt.encode({"id": user_id}, os.getenv('JWT_SECRET_KEY'), "HS256")
        return access_token

    def check_auth(self, access_token):
        decode_token = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms = "HS256")
        user_id = decode_token["id"]
        return user_id