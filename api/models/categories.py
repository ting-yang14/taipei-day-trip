from ..database import database
from itertools import chain
mysql_pool = database.MySQLPool(**database.dbconfig)

class Categories:
    def __init__(self):
        pass
    
    def get_categories(self):
        get_categories_query = """
            SELECT DISTINCT category 
            FROM attraction
        """
        result = mysql_pool.execute(get_categories_query)
        category_list = list(chain.from_iterable(result))
        return category_list