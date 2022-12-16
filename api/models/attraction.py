from ..database import database
mysql_pool = database.MySQLPool(**database.dbconfig)

class Attraction:
    def __init__(self):
        pass
    
    def generate_attraction_data(self, attraction_data_list):
        return {
            "id": attraction_data_list[0], 
            "name": attraction_data_list[1], 
            "category": attraction_data_list[2], 
            "description": attraction_data_list[3],
            "address": attraction_data_list[4],
            "transport": attraction_data_list[5],
            "mrt": attraction_data_list[6],
            "lat": attraction_data_list[7],
            "lng": attraction_data_list[8],
            "images": attraction_data_list[9].split(",")
        }

    def get_attractions(self, keyword, page):
        page = int(page)
        attractions=[]
        get_attraction_by_keyword_query = """
                SELECT attraction.id, attraction.name, attraction.category, attraction.description, attraction.address,
                attraction.transport, attraction.mrt, attraction.lat, attraction.lng,
                GROUP_CONCAT(img.url SEPARATOR ',')
                FROM attraction 
                INNER JOIN img on img.attraction_id = attraction.id
                WHERE category = %s OR name LIKE %s
                GROUP BY attraction.id 
                LIMIT %s, 13
            """
        val = (keyword, '%' + keyword + '%', page*12,)
        result = mysql_pool.execute(get_attraction_by_keyword_query, val)
        if len(result) == 13:
            nextPage = page + 1
        else:
            nextPage = None
        for i in range(0, len(result)):
            if i == 12:
                break
            attraction = self.generate_attraction_data(result[i])
            attractions.append(attraction)
        response = {"nextPage": nextPage, "data": attractions}
        return response

    def get_attraction(self, attractionId):
        get_attraction_query = """
            SELECT 
                attraction.id, attraction.name, attraction.category, 
                attraction.description, attraction.address,
                attraction.transport, attraction.mrt, attraction.lat, attraction.lng,
            GROUP_CONCAT(img.url SEPARATOR ',')
            FROM attraction 
            INNER JOIN img on img.attraction_id = attraction.id
            WHERE attraction.id = %s
            GROUP BY attraction.id
        """
        result = mysql_pool.execute(get_attraction_query, (attractionId,))
        if result:
            attraction = self.generate_attraction_data(result[0])
        else:
            attraction = None
        return attraction
