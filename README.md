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

## Running via Docker
You can run the entire application (MySQL + Tkinter GUI) inside Docker containers. Note that running a Tkinter GUI inside Docker on Windows requires an X11 server like [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or Xming.

1. Ensure Docker Desktop is running.
2. Start an X11 server on your Windows host (e.g. VcXsrv) and allow access from public/private networks. Ensure "Disable access control" is checked.
3. Build and start the containers using Docker Compose:
   ```bash
   docker-compose up --build
   ```
This will spin up the `course_mysql_db` container and the `course_tkinter_app` container. The application will automatically connect to the containerized database and initialize it on startup.
