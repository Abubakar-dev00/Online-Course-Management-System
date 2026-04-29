from app.utils.db import get_db_connection
from app.utils.logger import get_logger
from app.models.course_model import Course

logger = get_logger("course_service")

class CourseService:
    def add_course(self, title, description, teacher_id):
        if not title:
            raise ValueError("Course title cannot be empty.")
            
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            query = "INSERT INTO courses (title, description, teacher_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (title, description, teacher_id))
            conn.commit()
            logger.info(f"Course '{title}' added successfully.")
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error adding course: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_all_courses(self):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM courses"
            cursor.execute(query)
            results = cursor.fetchall()
            return [Course(r['id'], r['title'], r['description'], r['teacher_id']) for r in results]
        except Exception as e:
            logger.error(f"Error fetching courses: {e}")
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def update_course(self, course_id, title, description, teacher_id):
        if not title:
            raise ValueError("Course title cannot be empty.")
            
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            query = "UPDATE courses SET title = %s, description = %s, teacher_id = %s WHERE id = %s"
            cursor.execute(query, (title, description, teacher_id, course_id))
            conn.commit()
            logger.info(f"Course ID {course_id} updated successfully.")
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error updating course: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def delete_course(self, course_id):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            query = "DELETE FROM courses WHERE id = %s"
            cursor.execute(query, (course_id,))
            conn.commit()
            logger.info(f"Course ID {course_id} deleted successfully.")
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting course: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()
