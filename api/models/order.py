from ..database import database
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()
mysql_pool = database.MySQLPool(**database.dbconfig)


class Order:
    def __init__(self):
        pass

    def generate_order_number(self):
        now = datetime.now()
        self.order_number = f'{now.strftime("%Y%m%d%H%M%S")}{self.user_id}-{self.request["attraction_id"]}'

    def create_order(self):
        create_order_query = """
            INSERT INTO cart
            (user_id, 
            order_number, 
            attraction_id, 
            date, 
            time, 
            price,
            payment_status, 
            contact_name, 
            contact_email, 
            contact_phone) 
            VALUES
            (%s, %s, %s, %s, %s, %s, 1, %s, %s, %s);
        """
        val = (
            self.user_id,
            self.order_number,
            self.request["attraction_id"],
            self.request["date"],
            self.request["time"],
            self.request["price"],
            self.request["name"],
            self.request["email"],
            self.request["phone"],
        )
        mysql_pool.execute(create_order_query, val, True)
        print("User " + str(self.user_id) + " have create order")

    def handle_tappay_payment(self):
        post_url = f"https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
        post_data = {
            "prime": self.request["prime"],
            "partner_key": os.getenv("TAPPAY_PARTNER_KEY"),
            "merchant_id": os.getenv("TAPPAY_MERCHANT_ID"),
            "details": "TapPay Test",
            "amount": self.request["price"],
            "cardholder": {
                "phone_number": self.request["phone"],
                "name": self.request["name"],
                "email": self.request["email"],
            },
            "remember": True,
        }
        post_headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("TAPPAY_PARTNER_KEY"),
        }
        response = requests.post(post_url, json=post_data, headers=post_headers)
        self.payment_response = response.json()
        print("get payment response")

    def insert_payment_response(self):
        insert_payment_response_query = """
            INSERT INTO payment
            (user_id, order_number, payment_status, msg) 
            VALUES
            (%s, %s, %s, %s)
        """
        val = (
            self.user_id,
            self.order_number,
            self.payment_response["status"],
            self.payment_response["msg"],
        )
        mysql_pool.execute(insert_payment_response_query, val, True)
        print("payment response have saved")

    def update_cart_payment_status(self):

        update_cart_payment_status_query = """
            UPDATE cart 
            SET payment_status = 0 
            WHERE user_id = %s
            AND order_number = %s
        """
        val = (
            self.user_id,
            self.order_number,
        )
        mysql_pool.execute(update_cart_payment_status_query, val, True)
        print("cart payment status have updated")

    def create_order_response(self):
        order_response = {
            "data": {
                "number": self.order_number,
                "payment": {
                    "status": self.payment_response["status"],
                    "message": self.payment_response["msg"],
                },
            }
        }
        print("order response have created")
        return order_response

    def order_trip(self, user_id, request):
        self.user_id = user_id
        self.request = {
            "prime": request["prime"],
            "attraction_id": request["order"]["trip"]["attraction"]["id"],
            "date": request["order"]["trip"]["date"],
            "time": request["order"]["trip"]["time"],
            "price": request["order"]["price"],
            "name": request["order"]["contact"]["name"],
            "email": request["order"]["contact"]["email"],
            "phone": request["order"]["contact"]["phone"],
        }
        self.generate_order_number()
        self.create_order()
        self.handle_tappay_payment()
        self.insert_payment_response()
        if self.payment_response["status"] == 0:
            self.update_cart_payment_status()
        order_response = self.create_order_response()
        return order_response

    def get_order_info(self, user_id, order_number):
        get_order_info_query = """
            SELECT attraction.id, attraction.name, attraction.address, 
		           img.url, 
		           cart.date, cart.time, cart.price,
                   cart.order_number, cart.payment_status, cart.contact_name, 
                   cart.contact_email, cart.contact_phone
            FROM attraction
            INNER JOIN img on img.attraction_id = attraction.id
            INNER JOIN cart on cart.attraction_id = attraction.id
            WHERE cart.user_id = %s
            AND cart.order_number = %s
            LIMIT 1;
        """
        val = (
            user_id,
            order_number,
        )
        result = mysql_pool.execute(get_order_info_query, val)
        if result:
            return self.generate_order_info(result[0])
        else:
            return {"data": None}

    def generate_order_info(self, order_info):
        order_info = {
            "data": {
                "number": order_info["order_number"],
                "price": order_info["price"],
                "trip": {
                    "attraction": {
                        "id": order_info["id"],
                        "name": order_info["name"],
                        "address": order_info["address"],
                        "image": order_info["url"],
                    },
                    "date": order_info["date"],
                    "time": order_info["time"],
                },
                "contact": {
                    "name": order_info["contact_name"],
                    "email": order_info["contact_email"],
                    "phone": order_info["contact_phone"],
                },
                "status": order_info["payment_status"],
            }
        }
        return order_info
