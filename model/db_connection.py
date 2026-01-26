import mysql.connector
from config.db_config import DB_CONFIG

class DBConnection:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
