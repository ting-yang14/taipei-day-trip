from flask import Blueprint, request, make_response
from .models.booking import Booking
from .models.user import User
from .models.order import Order
order = Blueprint("order", __name__)
model_booking = Booking()
model_user = User()
model_order = Order()
headers = {"Content-Type": "application/json"}


@order.route("/orders", methods = ["POST"])
def post():
    order_request = request.get_json()
    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            user_id = model_user.check_auth(access_token)
            order_response = model_order.order_trip(user_id, order_request)
            response = make_response(order_response, 200, headers)
            return response
        except Exception as e:
            print(e)
            response = make_response({"error": True,"message": "伺服器內部錯誤"}, 500, headers)
            return response
    else:
        response = make_response({"error": True, "message": "未登入系統，拒絕存取"}, 403, headers)
        return response

@order.route("/order/<string:orderNumber>", methods = ["GET"])
def get_order(orderNumber):
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