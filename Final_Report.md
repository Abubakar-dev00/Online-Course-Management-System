# Final Project Report: Online Course Management System

## 1. Process Model Implementation
**Which process model did you implement for project development and justify the usage of model?**

For the development of this Online Course Management System, we implemented the **Agile Iterative Model**. 

**Justification:**
- **Incremental Feature Delivery:** The application required various independent modules such as Authentication, Course Management, Enrollments, and Grading. The iterative model allowed us to develop the Database structure first, followed by Authentication, and then gradually add Tkinter views for subsequent modules.
- **Flexibility for UI Tweaks:** Developing desktop UI applications using Tkinter often requires continuous adjustments based on visual feedback. Agile permitted us to refine the layout (`views/`) while ensuring the business logic (`services/`) remained intact.

## 2. Software Process Improvement (SPI)
**Is any SPI done during the semester project?**

Yes, significant Software Process Improvement was implemented during the lifecycle of this project:
- **Separation of Concerns (Architecture):** Initially, database queries might have been mixed with UI code. We improved our process by strictly separating the codebase into `models`, `views`, and `services`.
- **Introduction of Automated Testing:** We integrated the `pytest` framework. Writing tests for critical services (like `course_service` and `enrollment_service`) improved our process by catching regressions early and ensuring robustness before runtime execution.
- **Centralized Logging:** We implemented a centralized logger (`utils/logger.py`) to systematically track application states and database errors, moving away from unstructured `print()` statements.

## 3. Version Control Implementation
**Implement the version control for semester project.**

Version control was rigorously managed using **Git**.
- The project repository was initialized with Git.
- A `.gitignore` file was utilized to exclude virtual environments (`.venv/`) and Python cache (`__pycache__/`) from being tracked.
- Meaningful commit messages were used to document the evolution of the software, tracking the addition of the database schema, the integration of Tkinter views, code refactoring, and unit test integrations.

## 4. Justification of Lehman’s Law
**How did your semester project justify Lehman’s LAW?**

Our project demonstrates two key laws of Lehman's Laws of Software Evolution:
- **Law of Continuing Change:** As the system expanded from simple user authentication to handling dynamic enrollments, assignments, and grading, the software had to continuously adapt. New roles (Admin vs. Student vs. Teacher) required the underlying database and service architecture to change constantly.
- **Law of Increasing Complexity:** As we added more features, the Tkinter `main.py` file started becoming complex due to initializing all frames at startup. To combat this increasing complexity, we had to *refactor* the application to use lazy-loading for views, preserving structure and performance.

## 5. Software Deployment Management
**Manage Software Deployment and explain it in the report (if applicable).**

For this desktop application, software deployment is managed locally using **PyInstaller** (or similar packaging tools).
- **Process:** The application, dependencies (`mysql-connector-python`, `pytest`), and assets are bundled into a single standalone executable. 
- **Deployment Strategy:** The executable along with a script to configure the MySQL database locally (`db_setup.py`) can be distributed to users (Admins, Teachers, Students) so they can run the application without needing to install the Python environment manually.

## 6. Refactoring Legacy Code
**Refactor the source code and remove legacy in source code.**

During development, we identified "code smells" and refactored the application to remove legacy structures:
- **Lazy Loading Implementation:** The original `main.py` pre-loaded every single Tkinter screen (`LoginView`, `DashboardView`, `CourseView`, etc.) into memory simultaneously at startup. This was inefficient. We refactored the `App` class to implement **Lazy Loading**, meaning views are now only instantiated when a user actually navigates to them, drastically reducing startup time and unnecessary database connections.

## 7. Unit Testing Integration
**Add unit test to project.**

We incorporated unit testing into our project using the `pytest` library and the built-in `unittest.mock` library.
- Tests are located in the `tests/test_services/` directory.
- We added tests for `auth_service.py`, `course_service.py`, and `enrollment_service.py`.
- Mocking was used extensively to simulate database interactions (`mock_get_db`), ensuring that unit tests are isolated from the actual MySQL database state.

## 8. Automated Testing
**Use automated testing to test the application (if applicable).**

Automated testing was executed via the CLI. By running `pytest tests/` in the terminal, the system automatically discovers and executes all written test cases. This automated suite ensures that any future modifications do not break the core CRUD functionalities of courses and enrollments.

## 9. Exception Handling Concepts
**Apply exception handling concepts.**

Exception handling is a core component of this project to prevent unexpected crashes and provide meaningful feedback:
- **Database Layer (`utils/db.py`):** `try...except Error as e` blocks are used to catch and log MySQL connection failures.
- **Service Layer (e.g., `services/course_service.py`):** Every database operation (INSERT, SELECT, UPDATE, DELETE) is wrapped in a `try...except...finally` block. 
- **Rollbacks:** If an `Exception` occurs during a database transaction, `conn.rollback()` is executed to maintain database integrity, and the connection cursor is safely closed in the `finally` block to prevent memory leaks.

## 10. Peer Reviews
**Implement the Peer reviews (inspections, walkthroughs, etc.).**

Throughout the project, **Walkthroughs** were utilized as our primary peer review method.
- **Code Walkthroughs:** Team members periodically gathered to review the logic behind complex features like the grading system and database referential integrity (cascading deletes).
- **UI/UX Inspections:** The Tkinter interface was reviewed to ensure consistency in styling (`utils/styles.py`), button placement, and user feedback mechanisms.

## 11. Team Roles and Learning Outcomes
**Team Roles and their Contribution to the Project + Learning outcome of this Project.**

**Hypothetical Team Structure:**
- **Lead Developer:** Responsible for system architecture, implementing the `services` layer, database connectivity, and writing unit tests.
- **UI/UX Developer:** Responsible for designing the Tkinter front-end (`views`), ensuring intuitive navigation, and managing the presentation logic.
- **Database Administrator (DBA) / QA:** Designed the MySQL schema (`db_setup.py`), optimized queries, and conducted manual and automated testing.

**Learning Outcomes:**
- Mastered building thick-client desktop applications using Python and Tkinter.
- Gained practical experience in integrating a relational database (MySQL) with a Python backend using raw SQL queries and parameterized inputs.
- Learned the importance of Software Architecture (separating Models, Views, and Services) for maintainability.
- Understood practical applications of Unit Testing, Mocking, and Exception Handling to build robust software.
