from flask import Blueprint, request, make_response
from .models.booking import Booking
from .models.user import User
from .models.order import Order
from .models.validate_input import Validate

order = Blueprint("order", __name__)
model_booking = Booking()
model_user = User()
model_order = Order()
model_validate_input = Validate()
headers = {"Content-Type": "application/json"}


@order.route("/orders", methods=["POST"])
def post():
    order_request = request.get_json()
    access_token = request.cookies.get("access_token")
    request_validate = model_validate_input.validate_order_request(order_request)
    if not request_validate:
        response = make_response({"error": True, "message": "請輸入正確聯絡資訊"}, 400, headers)
        return response
    if access_token:
        try:
            user_id = model_user.check_auth(access_token)
            order_response = model_order.order_trip(user_id, order_request)
            response = make_response(order_response, 200, headers)
            model_booking.delete_trip_from_booking(user_id)
            return response
        except Exception as e:
            print(e)
            response = make_response(
                {"error": True, "message": "伺服器內部錯誤"}, 500, headers
            )
            return response
    else:
        response = make_response({"error": True, "message": "未登入系統，拒絕存取"}, 403, headers)
        return response


@order.route("/order/<string:orderNumber>", methods=["GET"])
def get(orderNumber):
    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            user_id = model_user.check_auth(access_token)
            order_info = model_order.get_order_info(user_id, orderNumber)
            response = make_response(order_info, 200, headers)
            return response
        except Exception as e:
            print(e)
            response = make_response(
                {"error": True, "message": "伺服器內部錯誤"}, 500, headers
            )
            return response
    else:
        response = make_response({"error": True, "message": "未登入系統，拒絕存取"}, 403, headers)
        return response
