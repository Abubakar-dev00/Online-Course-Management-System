from app.utils.db import get_db_connection
from app.utils.logger import get_logger

logger = get_logger("enrollment_service")

class EnrollmentService:
    def enroll_student(self, student_id, course_id, date):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            # Check for duplicate
            cursor.execute("SELECT id FROM enrollments WHERE student_id = %s AND course_id = %s", (student_id, course_id))
            if cursor.fetchone():
                raise ValueError("Student is already enrolled in this course.")
                
            query = "INSERT INTO enrollments (student_id, course_id, date) VALUES (%s, %s, %s)"
            cursor.execute(query, (student_id, course_id, date))
            conn.commit()
            logger.info(f"Student {student_id} enrolled in course {course_id}.")
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error enrolling student: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_enrollments_for_course(self, course_id):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT e.id as enrollment_id, s.id as student_id, s.name as student_name, e.date 
                FROM enrollments e
                JOIN students s ON e.student_id = s.id
                WHERE e.course_id = %s
            """
            cursor.execute(query, (course_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching enrollments: {e}")
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()
                
    def get_enrollments_for_student(self, student_user_id):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT e.id as enrollment_id, c.id as course_id, c.title as course_title, e.date 
                FROM enrollments e
                JOIN courses c ON e.course_id = c.id
                JOIN students s ON e.student_id = s.id
                WHERE s.user_id = %s
            """
            cursor.execute(query, (student_user_id,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching enrollments for student: {e}")
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()

    def remove_enrollment(self, enrollment_id):
        conn = get_db_connection()
        if not conn:
            raise Exception("Database connection failed.")
            
        try:
            cursor = conn.cursor()
            query = "DELETE FROM enrollments WHERE id = %s"
            cursor.execute(query, (enrollment_id,))
            conn.commit()
            logger.info(f"Enrollment {enrollment_id} removed.")
            return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error removing enrollment: {e}")
            conn.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()
