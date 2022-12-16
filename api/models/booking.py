from ..database import database
mysql_pool = database.MySQLPool(**database.dbconfig)

class Booking:
    def __init__(self):
        pass

    def generate_booked_info(self, booking_info_list):
        return {
                "data": {
                        "attraction": {
                                        "id": booking_info_list[0],
                                        "name": booking_info_list[1],
                                        "address": booking_info_list[2],
                                        "image": booking_info_list[3]
                        },
                "date": booking_info_list[4],
                "time": booking_info_list[5],
                "price": booking_info_list[6]
                }
        }
    
    def get_booked_info(self, user_id):
        get_booked_info_query="""
            SELECT attraction.id, attraction.name, attraction.address, 
                    img.url, 
                    booking.date,booking.time, booking.price
            FROM attraction 
            INNER JOIN img on img.attraction_id = attraction.id
            INNER JOIN booking on attraction.id = booking.attraction_id
            WHERE booking.member_id = %s
            LIMIT 1;
        """
        result =  mysql_pool.execute(get_booked_info_query, (user_id,))
        if result:
            booked_info = self.generate_booked_info(result[0])
        else:
            booked_info = {"data": None}
        return booked_info
    
    def book_trip(self, user_id, request):
        book_trip_query="""
            REPLACE INTO booking 
            (member_id, attraction_id, date, time, price) 
            VALUES (%s, %s, %s, %s, %s)
        """
        mysql_pool.execute(book_trip_query, (user_id, request["attractionId"], request["date"], request["time"], request["price"],), True)
        print("User " + str(user_id) + ": Booking Succeed!")
        
    def delete_trip(self, user_id):
        delete_booked_info_query="""
            DELETE FROM booking 
            WHERE member_id = %s
        """
        mysql_pool.execute(delete_booked_info_query, (user_id,), True)
        print("User " + str(user_id) + ": Delete Succeed!")
        
