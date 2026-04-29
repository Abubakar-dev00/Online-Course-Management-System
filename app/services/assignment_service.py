from app.utils.db import get_db_connection
from app.utils.logger import get_logger

logger = get_logger("assignment_service")

class AssignmentService:
    def add_assignment(self, course_id, title, due_date):
        if not title:
            raise ValueError("Assignment title cannot be empty.")
            
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            # Check if course exists
            cursor.execute("SELECT id FROM courses WHERE id = %s", (course_id,))
            if not cursor.fetchone():
                raise ValueError(f"Course with ID {course_id} does not exist.")
                
            query = "INSERT INTO assignments (course_id, title, due_date) VALUES (%s, %s, %s)"
            cursor.execute(query, (course_id, title, due_date))
            conn.commit()
            logger.info(f"Assignment '{title}' added to course {course_id}.")
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error adding assignment: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_assignments(self, course_id):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM assignments WHERE course_id = %s"
            cursor.execute(query, (course_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching assignments: {e}")
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def update_assignment(self, assignment_id, title, due_date):
        if not title:
            raise ValueError("Assignment title cannot be empty.")
            
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            query = "UPDATE assignments SET title = %s, due_date = %s WHERE id = %s"
            cursor.execute(query, (title, due_date, assignment_id))
            conn.commit()
            logger.info(f"Assignment ID {assignment_id} updated.")
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating assignment: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def delete_assignment(self, assignment_id):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            query = "DELETE FROM assignments WHERE id = %s"
            cursor.execute(query, (assignment_id,))
            conn.commit()
            logger.info(f"Assignment ID {assignment_id} deleted.")
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting assignment: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()
