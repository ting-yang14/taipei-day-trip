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

    def generate_order_number(self, user_id, request):
        attraction_id = request["order"]["trip"]["attraction"]["id"]
        now = datetime.now()
        order_number = f'{now.strftime("%Y%m%d%H%M%S")}{user_id}-{attraction_id}'
        return order_number
    
    def create_order(self, user_id, order_number, request):
        create_order_query = """
            INSERT INTO cart
            (member_id, 
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
            user_id, 
            order_number, 
            request["order"]["trip"]["attraction"]["id"],
            request["order"]["trip"]["date"],
            request["order"]["trip"]["time"],
            request["order"]["price"],
            request["order"]["contact"]["name"],
            request["order"]["contact"]["email"],
            request["order"]["contact"]["phone"],
        )
        mysql_pool.execute(create_order_query, val, True)
        print("User " + str(user_id) + " have create order")

    def handle_tappay_payment(self, request):
        post_url = f'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        post_data = {
            "prime": request["prime"],
            "partner_key": os.getenv('TAPPAY_PARTNER_KEY'),
            "merchant_id": os.getenv('TAPPAY_MERCHANT_ID'),
            "details": "TapPay Test",
            "amount": request["order"]["price"],
            "cardholder": {
                "phone_number": request["order"]["contact"]["phone"],
                "name": request["order"]["contact"]["name"],
                "email": request["order"]["contact"]["email"],
                "zip_code": "100",
                "address": "台北市天龍區芝麻街1號1樓",
                "national_id": "A123456789"
            },
            "remember": True
        }
        post_headers = {
            'Content-Type': 'application/json',
            'x-api-key': os.getenv('TAPPAY_PARTNER_KEY')
        }
        response = requests.post(post_url, json = post_data, headers = post_headers)
        payment_response = response.json()
        print(payment_response)
        return payment_response
        
    def insert_payment_response(self, user_id, order_number, payment_response):
        insert_payment_response_query = """
            INSERT INTO payment
            (member_id, order_number, payment_status, msg) 
            VALUES
            (%s, %s, %s, %s)
        """
        val = (
            user_id, order_number, 
            payment_response["status"], payment_response["msg"],
        )
        mysql_pool.execute(insert_payment_response_query, val, True)
        print("payment response have saved")

    def update_cart_payment_status(self, user_id, payment_response, order_number):
        if payment_response["status"] == 0:
            update_cart_payment_status_query = """
                UPDATE cart 
                SET payment_status = 0 
                WHERE member_id = %s
                AND order_number = %s
            """
            val = (user_id, order_number)
            mysql_pool.execute(update_cart_payment_status_query, val, True)
            print("cart payment status have updated")
        else:
            return

    
        

    def create_order_response(self, order_number, payment_response):
        order_response = {
            "data": {
                "number": order_number,
                "payment": {
                    "status": payment_response["status"],
                    "message": payment_response["msg"]
                }
            }
        }    
        print("order response have created")
        return order_response

    def order_trip(self, user_id, request):
        order_number = self.generate_order_number(user_id, request)
        self.create_order(user_id, order_number, request)
        payment_response = self.handle_tappay_payment(request)
        self.insert_payment_response(user_id, order_number, payment_response)
        self.update_cart_payment_status(user_id, payment_response, order_number)
        order_response = self.create_order_response(order_number, payment_response)

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
            WHERE cart.member_id = %s
            AND cart.order_number = %s
            LIMIT 1;
        """
        val = (user_id, order_number)
        result =  mysql_pool.execute(get_order_info_query, val)
        if result:
            order_info = self.generate_order_info(result[0])
        else:
            order_info = {"data": None}
        return order_info
    
    def generate_order_info(self, order_info_list):
        order_info = {
            "data": {
                "number": order_info_list[7],
                "price": order_info_list[6],
                "trip": {
                    "attraction": {
                        "id": order_info_list[0],
                        "name": order_info_list[1],
                        "address": order_info_list[2],
                        "image": order_info_list[3]
                    },
                    "date": order_info_list[4],
                    "time": order_info_list[5]
                },
                "contact": {
                    "name": order_info_list[9],
                    "email": order_info_list[10],
                    "phone": order_info_list[11]
                },
                "status": order_info_list[8]
            }
        }
        return order_info
    
        
