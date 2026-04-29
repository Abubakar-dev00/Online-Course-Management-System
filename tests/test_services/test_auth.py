import pytest
from unittest.mock import patch, MagicMock
from app.services.auth_service import AuthService
from app.models.user_model import User

@pytest.fixture
def auth_service():
    return AuthService()

def test_login_empty_credentials(auth_service):
    with pytest.raises(ValueError, match="Username and password cannot be empty."):
        auth_service.login("", "password")
        
    with pytest.raises(ValueError, match="Username and password cannot be empty."):
        auth_service.login("user", "")

@patch('app.services.auth_service.get_db_connection')
def test_login_success(mock_get_db, auth_service):
    # Setup mock
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mock row returned by fetchone
    mock_cursor.fetchone.return_value = {'id': 1, 'username': 'admin', 'role': 'Admin'}
    
    # Execute
    user = auth_service.login("admin", "admin123")
    
    # Verify
    assert user is not None
    assert isinstance(user, User)
    assert user.username == 'admin'
    assert user.role == 'Admin'
    mock_cursor.execute.assert_called_once()

@patch('app.services.auth_service.get_db_connection')
def test_login_failure(mock_get_db, auth_service):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = None
    
    user = auth_service.login("admin", "wrongpassword")
    
    assert user is None
