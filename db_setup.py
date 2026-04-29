import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS course_db")
            print("Database course_db created successfully.")
            
            # Switch to the new database
            cursor.execute("USE course_db")
            
            # Create tables
            tables = [
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('Admin', 'Teacher', 'Student') NOT NULL
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS courses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    teacher_id INT,
                    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE SET NULL
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    user_id INT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS enrollments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    course_id INT NOT NULL,
                    date DATE NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS assignments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    course_id INT NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    due_date DATE,
                    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS progress (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    course_id INT NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS grades (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    assignment_id INT NOT NULL,
                    grade VARCHAR(10),
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS announcements (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    course_id INT NOT NULL,
                    message TEXT NOT NULL,
                    date DATE NOT NULL,
                    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
                )
                """
            ]
            
            for table_query in tables:
                cursor.execute(table_query)
            print("Tables created successfully.")
            
            # Insert Sample Data
            # Note: passwords should be hashed in a real app, keeping plain text for simplicity as per requirements unless asked otherwise
            sample_users = [
                ("admin", "admin123", "Admin"),
                ("teacher1", "teach123", "Teacher"),
                ("student1", "stud123", "Student")
            ]
            
            cursor.executemany(
                "INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, %s)",
                sample_users
            )
            
            # If student1 exists, add to students table
            cursor.execute("SELECT id FROM users WHERE username='student1'")
            student_user = cursor.fetchone()
            if student_user:
                cursor.execute(
                    "INSERT IGNORE INTO students (name, email, user_id) VALUES (%s, %s, %s)",
                    ("John Doe", "john@example.com", student_user[0])
                )
            
            connection.commit()
            print("Sample data inserted successfully.")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    create_database()
