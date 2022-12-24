import os
from dotenv import load_dotenv
from mysql.connector import pooling

load_dotenv()

dbconfig = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "database": os.getenv('DB_DATABASE')
}
class MySQLPool:
    def __init__(self, host, user, password, database, pool_name = "mysql_pool", pool_size = 5):
        res = {}
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        res["host"] = self.__host
        res["user"] = self.__user
        res["password"] = self.__password
        res["database"] = self.__database
        self.dbconfig = res
        self.pool = self.create_pool(pool_name = pool_name, pool_size = pool_size)

    def create_pool(self, pool_name = "mysql_pool", pool_size = 5):
        connection_pool = pooling.MySQLConnectionPool(
                    pool_name = pool_name,
                    pool_size = pool_size,
                    pool_reset_session = True,
                    **self.dbconfig
                )
        return connection_pool
    
    def close(self, conn, cursor):
        cursor.close()
        conn.close()

    def execute(self, query, val = None, commit = False):
        conn = self.pool.get_connection()
        cursor = conn.cursor(dictionary = True)
        if val:
            cursor.execute(query, val)
        else:
            cursor.execute(query)
        if commit:
            conn.commit()
            self.close(conn, cursor)
            return None
        else:
            res = cursor.fetchall()
            self.close(conn, cursor)
            return res