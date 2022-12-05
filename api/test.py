from mysql.connector import Error, pooling

dbconfig = {
    "host": "localhost",
    "user":"root",
    "password": "TaipeiNO1",
    "database": "taipei_day_trip"
}
connection_pool = pooling.MySQLConnectionPool(
    pool_name = "test",
    pool_size = 5,
    pool_reset_session = True,
    autocommit = True,
    **dbconfig
)

req={'name': '彭彭', 'email': 'ply@ply.com', 'password': '12345678'}

try:
    connection = connection_pool.get_connection()
    cursor = connection.cursor()
    check_email_query=f'SELECT EXISTS(SELECT * from member WHERE email="{req["email"]}")'
    print(check_email_query)
    cursor.execute(check_email_query)
    email_repeat=cursor.fetchone()
    print(type(email_repeat))
    if email_repeat[0]==1:
        print("repeat")
    else:
        print("not repeat")
    # add_user_query = """
    #     INSERT INTO member (name, email, password) VALUES (%s, %s, %s);
    # """
    # val = (req["name"], req["email"], req["password"],)
    # cursor.execute(add_user_query, val)
    result={"ok":True}
    print(result)
except Error as error:
    result = {"error": True, "message": error}
    print(result)
    # return jsonify(result), 500
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
    
    # return jsonify(result), 200