import mysql.connector
from mysql.connector import errorcode

def GetConn():
    try:

        # drivers = [item for item in pyodbc.drivers()]
        # print(pyodbc.drivers())
        # driver = drivers[-1]
        # server = '192.168.1.74'
        # port = 3306 
        # database = 'mydb' 
        # username = 'root' 
        # password = '12345' 
        connection = mysql.connector.connect(
                user='root',
                password='12345',
                host='192.168.1.74',
                database='mydb',
                port=3306
        )
        cursor = connection.cursor()
        return cursor, connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None, None
