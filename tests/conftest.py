"""
Pytest configuration and fixtures for app-multicont testing.

This module provides reusable fixtures for testing Flask application components:
- Database configuration (test database)
- Flask application (test config)
- Test client (HTTP requests)
- Authentication tokens (JWT)
- Database session management
"""

import pytest
from app import create_app, db
from app.entities.user import User
from app.entities.organization import Organization
from flask_jwt_extended import create_access_token
from datetime import datetime
import os


@pytest.fixture(scope='session')
def app():
    """
    Create and configure a Flask application for testing.
    
    Uses development database (Prueba1) for testing.
    Scope: session - created once per test session.
    """
    # Create app with test configuration
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
    })
    
    return app


@pytest.fixture(scope='session')
def _db(app):
    """
    Get database instance for testing.
    
    Uses existing development database (no create/drop).
    Scope: session.
    """
    with app.app_context():
        yield db


@pytest.fixture(scope='function')
def db_session(_db, app):
    """
    Create a database session for each test function.
    
    Uses existing database without rollback.
    Scope: function - new session per test.
    """
    with app.app_context():
        yield db.session


@pytest.fixture
def client(app, db_session):
    """
    Create a test client for making HTTP requests.
    
    Args:
        app: Flask application fixture
        db_session: Database session fixture
    
    Returns:
        FlaskClient: Test client for HTTP requests
    
    Example:
        def test_get_endpoint(client):
            response = client.get('/api/users/')
            assert response.status_code == 200
    """
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_organization(db_session):
    """
    Create a test organization for testing.
    
    Returns:
        Organization: Test organization entity
    """
    org = Organization(
        historical_name='Test Organization',
        current_name='Test Organization Current'
    )
    db_session.add(org)
    db_session.commit()
    return org


@pytest.fixture
def test_user(db_session, test_organization):
    """
    Create a test user with SALES role.
    
    Args:
        db_session: Database session fixture
        test_organization: Organization fixture
    
    Returns:
        User: Test user entity
    
    Credentials:
        username: testuser
        password: Test123!@#
        role: SALES
    """
    from werkzeug.security import generate_password_hash
    
    user = User(
        username='testuser',
        email='testuser@example.com',
        password=generate_password_hash('Test123!@#'),
        status='active',
        organization_id=test_organization.id
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_admin(db_session, test_organization):
    """
    Create a test admin user with ADMIN role.
    
    Args:
        db_session: Database session fixture
        test_organization: Organization fixture
    
    Returns:
        User: Test admin entity
    
    Credentials:
        username: testadmin
        password: Admin123!@#
        role: ADMIN
    """
    from werkzeug.security import generate_password_hash
    
    admin = User(
        username='testadmin',
        email='testadmin@example.com',
        password=generate_password_hash('Admin123!@#'),
        status='active',
        organization_id=test_organization.id
    )
    db_session.add(admin)
    db_session.commit()
    return admin


@pytest.fixture
def auth_token(app, test_user):
    """
    Generate a valid JWT token for test_user (SALES role).
    
    Args:
        app: Flask application fixture
        test_user: Test user fixture
    
    Returns:
        str: JWT access token
    
    Example:
        def test_protected_endpoint(client, auth_token):
            headers = {'Authorization': f'Bearer {auth_token}'}
            response = client.get('/api/protected/', headers=headers)
            assert response.status_code == 200
    """
    with app.app_context():
        token = create_access_token(
            identity=test_user.id,
            additional_claims={
                'username': test_user.username,
                'email': test_user.email,
                'organization_id': test_user.organization_id
            }
        )
        return token


@pytest.fixture
def admin_token(app, test_admin):
    """
    Generate a valid JWT token for test_admin (ADMIN role).
    
    Args:
        app: Flask application fixture
        test_admin: Test admin fixture
    
    Returns:
        str: JWT access token
    
    Example:
        def test_admin_only_endpoint(client, admin_token):
            headers = {'Authorization': f'Bearer {admin_token}'}
            response = client.delete('/api/users/1', headers=headers)
            assert response.status_code == 200
    """
    with app.app_context():
        token = create_access_token(
            identity=test_admin.id,
            additional_claims={
                'username': test_admin.username,
                'email': test_admin.email,
                'organization_id': test_admin.organization_id
            }
        )
        return token


@pytest.fixture
def auth_headers(auth_token):
    """
    Generate authorization headers with JWT token.
    
    Args:
        auth_token: JWT token fixture
    
    Returns:
        dict: Authorization headers for HTTP requests
    
    Example:
        def test_endpoint(client, auth_headers):
            response = client.get('/api/protected/', headers=auth_headers)
            assert response.status_code == 200
    """
    return {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def admin_headers(admin_token):
    """
    Generate authorization headers with admin JWT token.
    
    Args:
        admin_token: Admin JWT token fixture
    
    Returns:
        dict: Authorization headers for HTTP requests
    """
    return {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }


# Test data fixtures
@pytest.fixture
def sample_quote_data():
    """Sample data for creating quotes."""
    return {
        'organization_id': 1,
        'client_name': 'Test Client',
        'client_email': 'client@test.com',
        'client_phone': '3001234567',
        'items': [
            {
                'inventory_item_id': 1,
                'quantity': 5,
                'unit_price': 1000.00
            }
        ],
        'quote_date': datetime.utcnow().date().isoformat(),
        'expiration_date': '2025-12-31',
        'status': 'pending'
    }


@pytest.fixture
def sample_inventory_data():
    """Sample data for creating inventory items."""
    return {
        'name': 'Test Product',
        'description': 'Test product description',
        'price': 1500.00,
        'quantity': 100,
        'category_id': 1,
        'organization_id': 1,
        'status': 'active'
    }


@pytest.fixture
def sample_employee_data():
    """Sample data for creating employees."""
    return {
        'name': 'Juan',
        'last_name': 'Pérez',
        'email': 'juan.perez@test.com',
        'phone': '3001234567',
        'hire_date': datetime.utcnow().date().isoformat(),
        'status': 'active',
        'branch_id': 1
    }


@pytest.fixture
def sample_user_data():
    """Sample data for creating users."""
    return {
        'username': 'newuser',
        'email': 'newuser@test.com',
        'password': 'Secure123!@#',
        'status': 'active',
        'organization_id': 1
    }
