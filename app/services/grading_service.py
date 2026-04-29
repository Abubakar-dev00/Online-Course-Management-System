from app.utils.db import get_db_connection
from app.utils.logger import get_logger

logger = get_logger("grading_service")

class GradingService:
    def add_grade(self, student_id, assignment_id, grade):
        if not grade:
            raise ValueError("Grade cannot be empty.")
            
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            # Check if grade already exists
            cursor.execute("SELECT id FROM grades WHERE student_id = %s AND assignment_id = %s", (student_id, assignment_id))
            if cursor.fetchone():
                # Update instead
                query = "UPDATE grades SET grade = %s WHERE student_id = %s AND assignment_id = %s"
                cursor.execute(query, (grade, student_id, assignment_id))
            else:
                query = "INSERT INTO grades (student_id, assignment_id, grade) VALUES (%s, %s, %s)"
                cursor.execute(query, (student_id, assignment_id, grade))
            
            conn.commit()
            logger.info(f"Grade added/updated for student {student_id} on assignment {assignment_id}.")
            return True
        except Exception as e:
            logger.error(f"Error adding grade: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_grades_for_assignment(self, assignment_id):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT g.id, s.name as student_name, g.grade
                FROM grades g
                JOIN students s ON g.student_id = s.id
                WHERE g.assignment_id = %s
            """
            cursor.execute(query, (assignment_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching grades: {e}")
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def update_progress(self, student_id, course_id, status):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM progress WHERE student_id = %s AND course_id = %s", (student_id, course_id))
            if cursor.fetchone():
                query = "UPDATE progress SET status = %s WHERE student_id = %s AND course_id = %s"
            else:
                query = "INSERT INTO progress (student_id, course_id, status) VALUES (%s, %s, %s)"
            cursor.execute(query, (student_id, course_id, status))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating progress: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_progress(self, student_id):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT p.id, c.title as course_title, p.status
                FROM progress p
                JOIN courses c ON p.course_id = c.id
                WHERE p.student_id = %s
            """
            cursor.execute(query, (student_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching progress: {e}")
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()
