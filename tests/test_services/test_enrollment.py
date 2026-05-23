import pytest
from unittest.mock import patch, MagicMock
from app.services.enrollment_service import EnrollmentService

@pytest.fixture
def enrollment_service():
    return EnrollmentService()

@patch('app.services.enrollment_service.get_db_connection')
def test_enroll_student_success(mock_get_db, enrollment_service):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mocking fetchone for student exists (True), course exists (True), duplicate (False)
    mock_cursor.fetchone.side_effect = [
        {'id': 1}, # student exists
        {'id': 101}, # course exists
        None       # not a duplicate
    ]
    mock_cursor.lastrowid = 5
    
    enrollment_id = enrollment_service.enroll_student(1, 101, '2023-10-25')
    
    assert enrollment_id == 5
    mock_conn.commit.assert_called_once()
    assert mock_cursor.execute.call_count == 4 # 3 checks + 1 insert

@patch('app.services.enrollment_service.get_db_connection')
def test_enroll_student_duplicate(mock_get_db, enrollment_service):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mocking fetchone for student exists (True), course exists (True), duplicate (True)
    mock_cursor.fetchone.side_effect = [
        {'id': 1}, # student exists
        {'id': 101}, # course exists
        {'id': 5}  # duplicate exists
    ]
    
    with pytest.raises(ValueError, match="Student is already enrolled in this course."):
        enrollment_service.enroll_student(1, 101, '2023-10-25')
        
    mock_conn.commit.assert_not_called()

@patch('app.services.enrollment_service.get_db_connection')
def test_get_enrollments_for_course(mock_get_db, enrollment_service):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        {'enrollment_id': 1, 'student_id': 2, 'student_name': 'Alice', 'date': '2023-10-25'}
    ]
    
    results = enrollment_service.get_enrollments_for_course(101)
    
    assert len(results) == 1
    assert results[0]['student_name'] == 'Alice'

@patch('app.services.enrollment_service.get_db_connection')
def test_remove_enrollment(mock_get_db, enrollment_service):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.rowcount = 1
    
    success = enrollment_service.remove_enrollment(5)
    
    assert success is True
    mock_conn.commit.assert_called_once()
