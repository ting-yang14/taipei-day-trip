from flask import Blueprint, request, make_response
from .models.booking import Booking
from .models.user import User

booking = Blueprint("booking", __name__)
model_booking = Booking()
model_user = User()
headers = {"Content-Type": "application/json"}

@booking.route("/booking", methods = ["GET"])
def get():
    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            user_id = model_user.check_auth(access_token)
            booked_info = model_booking.get_booked_info(user_id)
            response = make_response(booked_info, 200, headers)
            return response
        except Exception as e:
            print(e)
            response = make_response({"error": True,"message": "伺服器內部錯誤"}, 500, headers)
            return response
    else:
        response = make_response({"error": True, "message": "未登入系統，拒絕存取"}, 403, headers)
        return response
    
@booking.route("/booking", methods = ["POST"])
def post():
    booking_request = request.get_json()
    access_token = request.cookies.get("access_token")
    for item in booking_request.values():
        if not item:
           response = make_response({"error": True,"message": "建立失敗，輸入不正確或其他原因"}, 400, headers)
           return response
    if access_token:
        try:
            user_id = model_user.check_auth(access_token)
            model_booking.book_trip(user_id, booking_request)
            response = make_response({"ok": True}, 200, headers)
            return response
        except Exception as e:
            print(e)
            response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
            return response
    else:
        response = make_response({"error": True, "message": "未登入系統，拒絕存取"}, 403, headers)
        return response

@booking.route("/booking", methods = ["DELETE"])
def delete():
    access_token = request.cookies.get("access_token")
    if access_token:
        try: 
            user_id = model_user.check_auth(access_token)  
            model_booking.delete_trip_from_booking(user_id)
            response = make_response({"ok": True}, 200, headers)
            return response
        except Exception as e:
            print(e)
            response = make_response({"error": True, "message": "伺服器內部錯誤"}, 500, headers)
            return response
    else:
        response = make_response({"error": True, "message": "未登入系統，拒絕存取"}, 403, headers)
        return response