from ..database import database
mysql_pool = database.MySQLPool(**database.dbconfig)

class Attraction:
    def __init__(self):
        pass
    
    def images_string_to_list(self, attractions):
        for item in attractions:
            item["images"] = item.pop("GROUP_CONCAT(img.url SEPARATOR ',')").split(",")

    def get_attractions(self, keyword, page):
        page = int(page)
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
        attractions = mysql_pool.execute(get_attraction_by_keyword_query, val)
        self.images_string_to_list(attractions)
        if len(attractions) == 13:
            return {"nextPage": page + 1, "data": attractions[:12]}
        else:
            return {"nextPage": None, "data": attractions}

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
        val = (attractionId,)
        attraction = mysql_pool.execute(get_attraction_query, val)
        self.images_string_to_list(attraction)
        if attraction:
            return attraction[0]
        else:
            return None
