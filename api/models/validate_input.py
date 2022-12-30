import re
import datetime


class Validate:
    def __init__(self):
        self.email_reg = (
            "^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$"
        )
        self.password_reg = "^[A-Za-z\d@$!%*#?&]{8,16}$"
        self.date_reg = "^((20[0-9]{2})-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))$"
        self.phone_reg = "^09\d{8}$"
        self.time_reg = "morning|afternoon"
        self.name_reg = "^[a-zA-Z0-9_\u4e00-\u9fa5]{1,10}$"

    def check_email(self, email):
        if re.fullmatch(self.email_reg, email):
            return True
        else:
            return False

    def check_password(self, password):
        if re.fullmatch(self.password_reg, password):
            return True
        else:
            return False

    def check_phone(self, phone):
        if re.fullmatch(self.phone_reg, phone):
            return True
        else:
            return False

    def check_name(self, name):
        if re.fullmatch(self.name_reg, name):
            return True
        else:
            return False

    def check_date(self, date):
        today = datetime.date.today()
        today_strf = today.strftime("%Y-%m-%d")
        today_strp = datetime.datetime.strptime(today_strf, "%Y-%m-%d")
        date_strp = datetime.datetime.strptime(date, "%Y-%m-%d")
        if (re.fullmatch(self.date_reg, date) != None) and today_strp <= date_strp:
            return True
        else:
            return False

    def check_time(self, time):
        if re.fullmatch(self.time_reg, time):
            return True
        else:
            return False

    def validate_signin_request(self, request):
        email = request["email"]
        password = request["password"]
        return self.check_email(email) and self.check_password(password)

    def validate_signup_request(self, request):
        name = request["name"]
        email = request["email"]
        password = request["password"]
        return (
            self.check_name(name)
            and self.check_email(email)
            and self.check_password(password)
        )

    def validate_booking_request(self, request):
        date = request["date"]
        time = request["time"]
        return self.check_date(date) and self.check_time(time)

    def validate_order_request(self, request):
        name = request["order"]["contact"]["name"]
        email = request["order"]["contact"]["email"]
        phone = request["order"]["contact"]["phone"]
        return (
            self.check_name(name)
            and self.check_email(email)
            and self.check_phone(phone)
        )
