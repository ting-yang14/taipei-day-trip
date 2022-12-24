from ..database import database
mysql_pool = database.MySQLPool(**database.dbconfig)

class Categories:
    def __init__(self):
        pass
    
    def get_categories(self):
        categories = []
        get_categories_query = """
            SELECT DISTINCT category 
            FROM attraction
        """
        result = mysql_pool.execute(get_categories_query)
        for item in result:
            categories.append(item["category"])
        return categories