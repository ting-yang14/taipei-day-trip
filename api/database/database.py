from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()
dbconfig = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "database": os.getenv('DB_DATABASE')
}
connection_pool = pooling.MySQLConnectionPool(
    pool_name = "test",
    pool_size = 5,
    pool_reset_session = True,
    autocommit = True,
    **dbconfig
)
a=10
def db_setting():
   print(a)
class MySQLPool():
    def __init__(self, host, user, password, database, pool_name="test", pool_size=5):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
