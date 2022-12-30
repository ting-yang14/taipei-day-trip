from ..database import database

mysql_pool = database.MySQLPool(**database.dbconfig)


class Booking:
    def __init__(self):
        pass

    def generate_booked_info(self, booked_info):
        booked_info = {
            "attraction": {
                "id": booked_info["id"],
                "name": booked_info["name"],
                "address": booked_info["address"],
                "image": booked_info["url"],
            },
            "date": booked_info["date"],
            "time": booked_info["time"],
            "price": booked_info["price"],
        }
        return booked_info

    def get_booked_info(self, user_id):
        get_booked_info_query = """
            SELECT attraction.id, attraction.name, attraction.address, 
                    img.url, 
                    booking.date, booking.time, booking.price
            FROM attraction 
            INNER JOIN img on img.attraction_id = attraction.id
            INNER JOIN booking on attraction.id = booking.attraction_id
            WHERE booking.user_id = %s 
            LIMIT 1;
        """
        val = (user_id,)
        result = mysql_pool.execute(get_booked_info_query, val)
        if result:
            return self.generate_booked_info(result[0])
        else:
            return {"data": None}

    def book_trip(self, user_id, request):
        book_trip_query = """
            REPLACE INTO booking 
            (user_id, 
            attraction_id, 
            date, 
            time, 
            price) 
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (
            user_id,
            request["attractionId"],
            request["date"],
            request["time"],
            request["price"],
        )
        mysql_pool.execute(book_trip_query, val, True)
        print("User " + str(user_id) + ": Booking Succeed!")

    def delete_trip_from_booking(self, user_id):
        delete_trip_from_booking_query = """
            DELETE FROM booking 
            WHERE user_id = %s
        """
        val = (user_id,)
        mysql_pool.execute(delete_trip_from_booking_query, val, True)
        print("User " + str(user_id) + ": Delete Succeed!")
