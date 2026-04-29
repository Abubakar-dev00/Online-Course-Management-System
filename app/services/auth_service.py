from app.utils.db import get_db_connection
from app.utils.logger import get_logger
from app.models.user_model import User

logger = get_logger("auth_service")

class AuthService:
    def __init__(self):
        pass

    def login(self, username, password):
        if not username or not password:
            raise ValueError("Username and password cannot be empty.")
            
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, username, role FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            
            if result:
                logger.info(f"User {username} logged in successfully as {result['role']}.")
                return User(result['id'], result['username'], result['role'])
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                return None
        except Exception as e:
            logger.error(f"Error during login: {e}")
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()
