import mysql.connector
from mysql.connector import Error
from app.utils.logger import get_logger
import os

logger = get_logger("db")

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=os.environ.get("DB_HOST", "localhost"),
                    user="root",
                    password="",
                    database="course_db"
                )
                logger.info("Successfully connected to MySQL database.")
            return self.connection
        except Error as e:
            logger.error(f"Error while connecting to MySQL: {e}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed.")

def get_db_connection():
    db = Database()
    return db.connect()
