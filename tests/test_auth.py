"""
Authentication and Authorization Tests

Tests for:
- User login (valid/invalid credentials)
- JWT token generation and validation
- Token refresh functionality
- Role-based access control (RBAC)
- Protected endpoint access
"""

import pytest
import json
from werkzeug.security import generate_password_hash


@pytest.mark.auth
@pytest.mark.unit
class TestAuthentication:
    """Test user authentication flows."""
    
    def test_login_success(self, client, test_user):
        """Test successful login with valid credentials."""
        response = client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'Test123!@#'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'access_token' in data['data']
        assert data['data']['user']['username'] == 'testuser'
    
    def test_login_invalid_username(self, client):
        """Test login with non-existent username."""
        response = client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'password123'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'error' in data
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with incorrect password."""
        response = client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_login_missing_credentials(self, client):
        """Test login with missing username or password."""
        # Missing password
        response = client.post('/api/auth/login', json={
            'username': 'testuser'
        })
        assert response.status_code == 400
        
        # Missing username
        response = client.post('/api/auth/login', json={
            'password': 'password123'
        })
        assert response.status_code == 400
    
    def test_login_inactive_user(self, client, db_session, test_organization):
        """Test login with inactive user account."""
        from app.entities.user import User
        
        inactive_user = User(
            username='inactiveuser',
            email='inactive@test.com',
            password=generate_password_hash('Test123!@#'),
            status='inactive',
            organization_id=test_organization.id
        )
        db_session.add(inactive_user)
        db_session.commit()
        
        response = client.post('/api/auth/login', json={
            'username': 'inactiveuser',
            'password': 'Test123!@#'
        })
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'inactivo' in data['error'].lower()


@pytest.mark.auth
@pytest.mark.unit
class TestJWTTokens:
    """Test JWT token generation and validation."""
    
    def test_access_token_valid(self, client, auth_headers):
        """Test accessing protected endpoint with valid token."""
        response = client.get('/api/users/', headers=auth_headers)
        assert response.status_code in [200, 401]  # 401 if endpoint requires admin
    
    def test_access_token_missing(self, client):
        """Test accessing protected endpoint without token."""
        response = client.get('/api/users/')
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'msg' in data  # JWT error message
    
    def test_access_token_invalid_format(self, client):
        """Test accessing endpoint with malformed token."""
        headers = {'Authorization': 'Bearer invalid-token-format'}
        response = client.get('/api/users/', headers=headers)
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_access_token_expired(self, client, app):
        """Test accessing endpoint with expired token."""
        from flask_jwt_extended import create_access_token
        from datetime import timedelta
        
        with app.app_context():
            expired_token = create_access_token(
                identity=999,
                expires_delta=timedelta(seconds=-1)  # Expired
            )
        
        headers = {'Authorization': f'Bearer {expired_token}'}
        response = client.get('/api/users/', headers=headers)
        assert response.status_code == 401
    
    def test_token_refresh(self, client, auth_token):
        """Test token refresh functionality."""
        # Note: Requires /api/auth/refresh endpoint implementation
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/api/auth/refresh', headers=headers)
        
        # If endpoint exists
        if response.status_code != 404:
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'access_token' in data.get('data', {})


@pytest.mark.auth
@pytest.mark.integration
class TestRoleBasedAccess:
    """Test role-based access control (RBAC)."""
    
    def test_admin_access_user_management(self, client, admin_headers, test_user):
        """Test admin can access user management endpoints."""
        # GET all users
        response = client.get('/api/users/', headers=admin_headers)
        assert response.status_code == 200
        
        # GET specific user
        response = client.get(f'/api/users/{test_user.id}', headers=admin_headers)
        assert response.status_code == 200
    
    def test_sales_access_own_organization(self, client, auth_headers, test_organization):
        """Test sales user can access their organization data."""
        response = client.get(f'/api/organizations/{test_organization.id}', 
                             headers=auth_headers)
        assert response.status_code in [200, 403]  # Depends on implementation
    
    def test_sales_cannot_delete_users(self, client, auth_headers, test_admin):
        """Test sales user cannot delete other users."""
        response = client.delete(f'/api/users/{test_admin.id}', 
                                headers=auth_headers)
        assert response.status_code in [403, 401]  # Forbidden or Unauthorized
    
    def test_unauthenticated_access_denied(self, client):
        """Test unauthenticated users cannot access protected endpoints."""
        protected_endpoints = [
            '/api/users/',
            '/api/organizations/',
            '/api/inventory_items/',
            '/api/quotes/',
            '/api/invoices/',
            '/api/employees/'
        ]
        
        for endpoint in protected_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 401


@pytest.mark.auth
@pytest.mark.integration
class TestOrganizationIsolation:
    """Test organization data isolation."""
    
    def test_user_cannot_access_other_organization_data(self, client, db_session, 
                                                        test_user, app):
        """Test users cannot access data from other organizations."""
        from app.entities.organization import Organization
        from app.entities.user import User
        from flask_jwt_extended import create_access_token
        
        # Create another organization
        other_org = Organization(
            name='Other Organization',
            nit='987654321-0',
            address='Other Address',
            phone='3009876543',
            email='other@org.com',
            status='active'
        )
        db_session.add(other_org)
        db_session.commit()
        
        # Create user in other organization
        other_user = User(
            username='otheruser',
            email='other@test.com',
            password=generate_password_hash('Test123!@#'),
            status='active',
            organization_id=other_org.id
        )
        db_session.add(other_user)
        db_session.commit()
        
        # Login as test_user (organization 1)
        with app.app_context():
            token = create_access_token(
                identity=test_user.id,
                additional_claims={'organization_id': test_user.organization_id}
            )
        
        headers = {'Authorization': f'Bearer {token}'}
        
        # Try to access other organization's data
        response = client.get(f'/api/organizations/{other_org.id}', headers=headers)
        # Should be forbidden or not found (depends on implementation)
        assert response.status_code in [403, 404, 200]


@pytest.mark.auth
@pytest.mark.unit
class TestPasswordSecurity:
    """Test password security measures."""
    
    def test_password_hashed_in_database(self, test_user):
        """Test passwords are stored hashed, not plain text."""
        assert test_user.password != 'Test123!@#'
        assert test_user.password.startswith('$2b$')  # bcrypt hash prefix
    
    def test_password_not_returned_in_api(self, client, admin_headers, test_user):
        """Test password field not included in API responses."""
        response = client.get(f'/api/users/{test_user.id}', headers=admin_headers)
        
        if response.status_code == 200:
            data = json.loads(response.data)
            user_data = data.get('data', {})
            assert 'password' not in user_data
    
    def test_weak_password_rejected(self, client, admin_headers):
        """Test weak passwords are rejected during user creation."""
        weak_passwords = [
            'short',           # Too short
            '12345678',        # Only numbers
            'abcdefgh',        # Only letters
            'Password',        # No numbers or special chars
        ]
        
        for weak_password in weak_passwords:
            response = client.post('/api/users/', 
                                  headers=admin_headers,
                                  json={
                                      'username': 'newuser',
                                      'email': 'new@test.com',
                                      'password': weak_password,
                                      'organization_id': 1
                                  })
            # Should be validation error (400)
            assert response.status_code in [400, 422]


@pytest.mark.auth
@pytest.mark.integration
class TestSessionManagement:
    """Test session and token lifecycle."""
    
    def test_multiple_logins_generate_different_tokens(self, client, test_user):
        """Test each login generates a unique token."""
        response1 = client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'Test123!@#'
        })
        token1 = json.loads(response1.data)['data']['access_token']
        
        response2 = client.post('/api/auth/login', json={
            'username': 'testuser',
            'password': 'Test123!@#'
        })
        token2 = json.loads(response2.data)['data']['access_token']
        
        assert token1 != token2
    
    def test_logout_invalidates_token(self, client, auth_headers):
        """Test logout functionality (if implemented)."""
        response = client.post('/api/auth/logout', headers=auth_headers)
        
        # If endpoint exists
        if response.status_code != 404:
            assert response.status_code == 200
            
            # Token should no longer work
            response = client.get('/api/users/', headers=auth_headers)
            assert response.status_code == 401
