from flask import Blueprint, request, make_response
from datetime import datetime, timedelta
from .models.user import User

user = Blueprint("user", __name__)
model_user = User()
headers = {"Content-Type": "application/json"}

@user.route("/user", methods = ["POST"])
def post():
    signup_request = request.get_json()
    try:
        check_result = model_user.check_email_repeat(signup_request)
        if check_result:
            response = make_response({"error": True, "message": "email已被註冊"}, 400, headers)
        else:
            signup_result = model_user.signup(signup_request)
            response = make_response({"ok": signup_result}, 200, headers)
        return response
    except Exception as e:
        print(e)
        response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
        return response
        
@user.route("/user/auth", methods = ["GET"])
def get():
    access_token = request.cookies.get('access_token')
    if access_token:
        try:
            user_id = model_user.check_auth(access_token)
            user_info = model_user.get_user_info(user_id)
            response = make_response({"data": user_info}, 200, headers)
        except Exception as e:
            print(e)
            response =make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
            return response
    else:
        response = make_response({"data": None}, 200, headers)
    return response

@user.route("/user/auth", methods = ["PUT"])
def put():
    signin_request = request.get_json()
    try:
        user_id = model_user.signin(signin_request)
        if user_id:
            access_token = model_user.set_auth(user_id)
            response = make_response({"ok": True}, 200)
            response.set_cookie("access_token", access_token, expires = datetime.now() + timedelta(days = 7))
        else:
            response = make_response({"error": True, "message": "email或密碼錯誤"}, 400)
        return response
    except Exception as e:
        print(e)
        response =make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
        return response

@user.route("/user/auth", methods = ["DELETE"])
def delete():
    response = make_response({"ok": True}, 200, headers)
    response.set_cookie("access_token", "", expires = 0)
    return response