# Online Course Management System

## Description
A comprehensive desktop application for managing online courses, built using Python's Tkinter framework and a MySQL database. It supports role-based access control for Admins, Teachers, and Students.

## Features
- **Role-based Login**: Admin, Teacher, and Student access.
- **Course Management**: Full CRUD capabilities for courses.
- **Student Enrollment**: Manage enrollments for specific courses.
- **Assignments & Grading**: Teachers can upload assignments and grade students.
- **Progress Tracking**: Track student progress across courses.
- **Message Board**: Post and view announcements.

## Technologies Used
- **Python (Tkinter)** for UI
- **MySQL** for Database
- **mysql-connector-python** for database connection
- **pytest** for unit testing

## How to Run Project
1. Install Python 3.
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app/main.py
   ```

## Database Setup Instructions
1. Make sure you have MySQL installed and running.
2. Ensure your MySQL credentials are set to `root` and `your_password` (or update `app/utils/db.py`).
3. Run the initial database setup script from the root directory:
   ```bash
   python db_setup.py
   ```
   This will create the `course_db` database, its tables, and insert sample data.
