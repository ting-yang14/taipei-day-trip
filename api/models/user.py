import jwt
import os
from dotenv import load_dotenv
from ..database import database
from flask_bcrypt import Bcrypt
mysql_pool = database.MySQLPool(**database.dbconfig)

load_dotenv()
bcrypt = Bcrypt()
class User:
    def __init__(self):
        pass

    def check_email_repeat(self, request):
        check_email_query = """
            SELECT EXISTS (SELECT * 
                           FROM user 
                           WHERE email = %s)
        """
        val = (request["email"],)
        result =  mysql_pool.execute(check_email_query, val)[0]
        keys = list(result.keys())
        repeat_email_num = result[keys[0]]
        if repeat_email_num:
            return True
        else:
            return False
    
    def signup(self, request):
        signup_query = """
            INSERT INTO user 
            (name, email, password) 
            VALUES (%s, %s, %s);
        """
        hashed_password = bcrypt.generate_password_hash(request["password"]).decode('utf8')
        val = (request["name"], request["email"], hashed_password,)
        mysql_pool.execute(signup_query, val, True)
        return True
    
    def signin(self, request):
        signin_query = """
            SELECT id, password 
            FROM user 
            WHERE email = %s
        """
        val = (request["email"],)
        user_info = mysql_pool.execute(signin_query, val)[0]
        user_id = user_info["id"]
        user_password = user_info["password"]
        check_result = bcrypt.check_password_hash(user_password, request["password"])
        if check_result:
            return user_id
        else:
            return check_result

    def get_user_info(self, user_id):
        get_user_info_query = """
            SELECT id, name, email 
            FROM user 
            WHERE id = %s
        """ 
        val = (user_id,)
        user_info = mysql_pool.execute(get_user_info_query, val)[0]
        return user_info

    def set_auth(self, user_id):
        access_token = jwt.encode({"id": user_id}, os.getenv('JWT_SECRET_KEY'), "HS256")
        return access_token

    def check_auth(self, access_token):
        decode_token = jwt.decode(access_token, os.getenv('JWT_SECRET_KEY'), algorithms = "HS256")
        user_id = decode_token["id"]
        return user_id