import pymysql
from pymysql.cursors import DictCursor

def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Aadi@123",
        database="ecommerce_db",
        port=3306,
        cursorclass=DictCursor,
        autocommit=True
    )
