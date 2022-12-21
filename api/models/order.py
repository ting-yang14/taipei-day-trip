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

    def generate_order_number(self, user_id, attraction_id):
        now = datetime.now()
        order_number = f'{now.strftime("%Y%m%d%H%M%S")}{user_id}-{attraction_id}'
        return order_number
    
    def create_order(self, user_id, order_number, contact):
        create_order_query = """
            INSERT INTO cart
            (member_id, order_number, payment_status, contact_name, contact_email, contact_phone) 
            VALUES
            (%s, %s, 1, %s, %s, %s);
        """
        val = (user_id, 
               order_number, 
               contact["name"], 
               contact["email"], 
               contact["phone"],
               )
        mysql_pool.execute(create_order_query, val, True)
        print("User " + str(user_id) + " have create order")

    def handle_tappay_payment(self, request):
        post_url = f'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        post_data = {
                    "prime": request["prime"],
                    "partner_key": os.getenv('TAPPAY_PARTNER_KEY'),
                    "merchant_id": os.getenv('TAPPAY_MERCHANT_ID'),
                    "details":"TapPay Test",
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
        return payment_response
        
    def save_payment_response(self, user_id, order_number, payment_response):
        save_payment_response_query = """
            INSERT INTO payment
            (member_id, order_number, payment_status, msg, transaction_time_millis) 
            VALUES
            (%s, %s, %s, %s, %s)
        """
        mysql_pool.execute(save_payment_response_query, 
                           (user_id, order_number, 
                            payment_response["status"], 
                            payment_response["msg"], 
                            payment_response["transaction_time_millis"],
                           ),
                            True
        )
        print("payment response have saved")

    def update_payment_status_for_cart(self, user_id, payment_response):
        if payment_response["status"]==0:
            update_cart_payment_status_query = """
                UPDATE cart 
                SET payment_status = %s 
                WHERE member_id = %s
            """
            mysql_pool.execute(update_cart_payment_status_query, (payment_response["status"], user_id,), True)
        else:
            print("payment failed:" + payment_response["msg"])

    def update_payment_status_for_booking(self, user_id):
        update_booking_payment_status_query = """
            UPDATE booking 
            SET payment_status = 0 
            WHERE member_id = %s
        """
        mysql_pool.execute(update_booking_payment_status_query, (user_id,), True)
        print("booking payment status have updated")

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
        return order_response

    def order_trip(self, user_id, request):
        order_number = self.generate_order_number(user_id, request["order"]["trip"]["attraction"]["id"])
        self.create_order(user_id, order_number, request["order"]["contact"])
        payment_response = self.handle_tappay_payment(request)
        self.update_payment_status_for_booking(user_id)
        self.update_payment_status_for_cart(user_id, payment_response)
        self.save_payment_response(user_id, order_number, payment_response)
        order_response = self.create_order_response(order_number, payment_response)
        return order_response
    def get_order_by_order_number(self, order_number):
        pass
    
        
