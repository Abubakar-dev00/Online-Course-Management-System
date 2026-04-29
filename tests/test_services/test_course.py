import pytest
from unittest.mock import patch, MagicMock
from app.services.course_service import CourseService

@pytest.fixture
def course_service():
    return CourseService()

def test_add_course_empty_title(course_service):
    with pytest.raises(ValueError, match="Course title cannot be empty."):
        course_service.add_course("", "desc", 1)

@patch('app.services.course_service.get_db_connection')
def test_add_course_success(mock_get_db, course_service):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.lastrowid = 1
    
    course_id = course_service.add_course("Python 101", "Learn Python", 2)
    
    assert course_id == 1
    mock_conn.commit.assert_called_once()

@patch('app.services.course_service.get_db_connection')
def test_get_all_courses(mock_get_db, course_service):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        {'id': 1, 'title': 'Python 101', 'description': 'Intro', 'teacher_id': 2}
    ]
    
    courses = course_service.get_all_courses()
    
    assert len(courses) == 1
    assert courses[0].title == 'Python 101'
    assert courses[0].teacher_id == 2
