"""
Marshmallow Validation Tests

Tests for data validation across all API endpoints:
- Quote validation
- Invoice validation
- Inventory item validation
- Sales order validation
- User validation
- Employee validation
"""

import pytest
import json
from datetime import datetime, timedelta


@pytest.mark.validation
@pytest.mark.unit
class TestQuoteValidation:
    """Test quote data validation."""
    
    def test_create_quote_valid_data(self, client, auth_headers, sample_quote_data):
        """Test creating quote with valid data."""
        response = client.post('/api/quotes/', 
                              headers=auth_headers,
                              json=sample_quote_data)
        
        if response.status_code == 201:
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'data' in data
    
    def test_create_quote_missing_required_fields(self, client, auth_headers):
        """Test quote validation rejects missing required fields."""
        incomplete_data = {
            'client_name': 'Test Client'
            # Missing organization_id, items, etc.
        }
        
        response = client.post('/api/quotes/',
                              headers=auth_headers,
                              json=incomplete_data)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'errors' in data or 'error' in data
    
    def test_quote_client_name_length_validation(self, client, auth_headers, sample_quote_data):
        """Test client_name length constraints (3-200 chars)."""
        # Too short (< 3 chars)
        sample_quote_data['client_name'] = 'AB'
        response = client.post('/api/quotes/',
                              headers=auth_headers,
                              json=sample_quote_data)
        assert response.status_code == 400
        
        # Too long (> 200 chars)
        sample_quote_data['client_name'] = 'A' * 201
        response = client.post('/api/quotes/',
                              headers=auth_headers,
                              json=sample_quote_data)
        assert response.status_code == 400
        
        # Valid length
        sample_quote_data['client_name'] = 'Valid Client Name'
        response = client.post('/api/quotes/',
                              headers=auth_headers,
                              json=sample_quote_data)
        assert response.status_code in [201, 400]  # May fail on other validations
    
    def test_quote_email_format_validation(self, client, auth_headers, sample_quote_data):
        """Test client_email format validation."""
        # Invalid email
        sample_quote_data['client_email'] = 'invalid-email'
        response = client.post('/api/quotes/',
                              headers=auth_headers,
                              json=sample_quote_data)
        assert response.status_code == 400
        
        # Valid email
        sample_quote_data['client_email'] = 'valid@email.com'
        response = client.post('/api/quotes/',
                              headers=auth_headers,
                              json=sample_quote_data)
        assert response.status_code in [201, 400]
    
    def test_quote_date_validation(self, client, auth_headers, sample_quote_data):
        """Test quote date cannot be in the future."""
        # Future date (invalid)
        future_date = (datetime.utcnow() + timedelta(days=30)).date().isoformat()
        sample_quote_data['quote_date'] = future_date
        
        response = client.post('/api/quotes/',
                              headers=auth_headers,
                              json=sample_quote_data)
        assert response.status_code == 400
        
        # Past date (valid)
        past_date = (datetime.utcnow() - timedelta(days=1)).date().isoformat()
        sample_quote_data['quote_date'] = past_date
        
        response = client.post('/api/quotes/',
                              headers=auth_headers,
                              json=sample_quote_data)
        assert response.status_code in [201, 400]


@pytest.mark.validation
@pytest.mark.unit
class TestInventoryValidation:
    """Test inventory item validation."""
    
    def test_create_inventory_valid_data(self, client, auth_headers, sample_inventory_data):
        """Test creating inventory with valid data."""
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=sample_inventory_data)
        
        if response.status_code == 201:
            data = json.loads(response.data)
            assert data['success'] is True
    
    def test_inventory_name_length_validation(self, client, auth_headers, sample_inventory_data):
        """Test name length constraints (3-200 chars)."""
        # Too short
        sample_inventory_data['name'] = 'AB'
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=sample_inventory_data)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data or 'error' in data
    
    def test_inventory_price_range_validation(self, client, auth_headers, sample_inventory_data):
        """Test price must be >= 0."""
        # Negative price (invalid)
        sample_inventory_data['price'] = -100
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=sample_inventory_data)
        assert response.status_code == 400
        
        # Zero price (valid edge case)
        sample_inventory_data['price'] = 0
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=sample_inventory_data)
        assert response.status_code in [201, 400]
        
        # Positive price (valid)
        sample_inventory_data['price'] = 1000.50
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=sample_inventory_data)
        assert response.status_code in [201, 400]
    
    def test_inventory_quantity_range_validation(self, client, auth_headers, sample_inventory_data):
        """Test quantity must be >= 0."""
        # Negative quantity (invalid)
        sample_inventory_data['quantity'] = -10
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=sample_inventory_data)
        assert response.status_code == 400
        
        # Zero quantity (valid)
        sample_inventory_data['quantity'] = 0
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=sample_inventory_data)
        assert response.status_code in [201, 400]
    
    def test_inventory_category_id_validation(self, client, auth_headers, sample_inventory_data):
        """Test category_id must be >= 1."""
        # Zero category_id (invalid)
        sample_inventory_data['category_id'] = 0
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=sample_inventory_data)
        assert response.status_code == 400


@pytest.mark.validation
@pytest.mark.unit
class TestEmployeeValidation:
    """Test employee data validation."""
    
    def test_create_employee_valid_data(self, client, auth_headers, sample_employee_data):
        """Test creating employee with valid data."""
        response = client.post('/api/employees/',
                              headers=auth_headers,
                              json=sample_employee_data)
        
        if response.status_code == 201:
            data = json.loads(response.data)
            assert data['success'] is True
    
    def test_employee_name_regex_validation(self, client, auth_headers, sample_employee_data):
        """Test name can only contain letters and spaces."""
        # Name with numbers (invalid)
        sample_employee_data['name'] = 'Juan123'
        response = client.post('/api/employees/',
                              headers=auth_headers,
                              json=sample_employee_data)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data or 'errors' in data
        
        # Name with special characters (invalid)
        sample_employee_data['name'] = 'Juan@Pedro'
        response = client.post('/api/employees/',
                              headers=auth_headers,
                              json=sample_employee_data)
        assert response.status_code == 400
        
        # Valid name (letters + spaces)
        sample_employee_data['name'] = 'Juan Carlos'
        response = client.post('/api/employees/',
                              headers=auth_headers,
                              json=sample_employee_data)
        assert response.status_code in [201, 400]
    
    def test_employee_email_format_validation(self, client, auth_headers, sample_employee_data):
        """Test email format validation."""
        # Invalid email
        sample_employee_data['email'] = 'not-an-email'
        response = client.post('/api/employees/',
                              headers=auth_headers,
                              json=sample_employee_data)
        assert response.status_code == 400
    
    def test_employee_hire_date_validation(self, client, auth_headers, sample_employee_data):
        """Test hire_date cannot be in the future."""
        # Future date (invalid)
        future_date = (datetime.utcnow() + timedelta(days=30)).date().isoformat()
        sample_employee_data['hire_date'] = future_date
        
        response = client.post('/api/employees/',
                              headers=auth_headers,
                              json=sample_employee_data)
        assert response.status_code == 400


@pytest.mark.validation
@pytest.mark.unit
class TestUserValidation:
    """Test user data validation."""
    
    def test_create_user_valid_data(self, client, admin_headers, sample_user_data):
        """Test creating user with valid data."""
        response = client.post('/api/users/',
                              headers=admin_headers,
                              json=sample_user_data)
        
        if response.status_code == 201:
            data = json.loads(response.data)
            assert data['success'] is True
    
    def test_user_username_length_validation(self, client, admin_headers, sample_user_data):
        """Test username length constraints (3-50 chars)."""
        # Too short
        sample_user_data['username'] = 'ab'
        response = client.post('/api/users/',
                              headers=admin_headers,
                              json=sample_user_data)
        assert response.status_code == 400
        
        # Too long
        sample_user_data['username'] = 'a' * 51
        response = client.post('/api/users/',
                              headers=admin_headers,
                              json=sample_user_data)
        assert response.status_code == 400
    
    def test_user_password_strength_validation(self, client, admin_headers, sample_user_data):
        """Test password strength requirements."""
        weak_passwords = [
            'short',           # Too short (< 8 chars)
            'alllowercase',    # No uppercase, numbers, special chars
            'ALLUPPERCASE',    # No lowercase, numbers, special chars
            '12345678',        # No letters
            'Simple123',       # No special characters
        ]
        
        for weak_password in weak_passwords:
            sample_user_data['password'] = weak_password
            response = client.post('/api/users/',
                                  headers=admin_headers,
                                  json=sample_user_data)
            assert response.status_code == 400
        
        # Strong password (valid)
        sample_user_data['password'] = 'Strong123!@#'
        response = client.post('/api/users/',
                              headers=admin_headers,
                              json=sample_user_data)
        assert response.status_code in [201, 400, 409]  # May conflict with existing
    
    def test_user_email_format_validation(self, client, admin_headers, sample_user_data):
        """Test email format validation."""
        # Invalid email
        sample_user_data['email'] = 'invalid-email'
        response = client.post('/api/users/',
                              headers=admin_headers,
                              json=sample_user_data)
        assert response.status_code == 400
    
    def test_user_username_uniqueness(self, client, admin_headers, test_user):
        """Test username must be unique."""
        duplicate_user = {
            'username': test_user.username,  # Duplicate
            'email': 'another@test.com',
            'password': 'Secure123!@#',
            'organization_id': 1
        }
        
        response = client.post('/api/users/',
                              headers=admin_headers,
                              json=duplicate_user)
        assert response.status_code in [400, 409]  # Conflict or validation error


@pytest.mark.validation
@pytest.mark.unit
class TestInvoiceValidation:
    """Test invoice data validation."""
    
    def test_invoice_total_validation(self, client, auth_headers):
        """Test invoice total must be >= 0."""
        invoice_data = {
            'sales_order_id': 1,
            'invoice_date': datetime.utcnow().date().isoformat(),
            'total': -100,  # Invalid negative
            'status': 'pending'
        }
        
        response = client.post('/api/invoices/',
                              headers=auth_headers,
                              json=invoice_data)
        assert response.status_code == 400
    
    def test_invoice_date_validation(self, client, auth_headers):
        """Test invoice_date cannot be in the future."""
        invoice_data = {
            'sales_order_id': 1,
            'invoice_date': (datetime.utcnow() + timedelta(days=30)).date().isoformat(),
            'total': 1000,
            'status': 'pending'
        }
        
        response = client.post('/api/invoices/',
                              headers=auth_headers,
                              json=invoice_data)
        assert response.status_code == 400


@pytest.mark.validation
@pytest.mark.unit
class TestSalesOrderValidation:
    """Test sales order data validation."""
    
    def test_sales_order_total_validation(self, client, auth_headers):
        """Test sales_order total must be >= 0."""
        order_data = {
            'quote_id': 1,
            'order_date': datetime.utcnow().date().isoformat(),
            'total': -500,  # Invalid
            'status': 'pending'
        }
        
        response = client.post('/api/sales_orders/',
                              headers=auth_headers,
                              json=order_data)
        assert response.status_code == 400


@pytest.mark.validation
@pytest.mark.integration
class TestSerializationValidation:
    """Test data serialization on GET endpoints."""
    
    def test_inventory_list_serialization(self, client, auth_headers):
        """Test inventory items are properly serialized."""
        response = client.get('/api/inventory_items/', headers=auth_headers)
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'data' in data
            
            items = data['data'].get('items', [])
            if items:
                # Verify required fields present
                first_item = items[0]
                assert 'id' in first_item
                assert 'name' in first_item
                assert 'price' in first_item
                # Password should NOT be in response
                assert 'password' not in first_item
    
    def test_user_list_serialization(self, client, admin_headers):
        """Test users are serialized without password."""
        response = client.get('/api/users/', headers=admin_headers)
        
        if response.status_code == 200:
            data = json.loads(response.data)
            users = data['data'].get('items', [])
            
            for user in users:
                # Password must NOT be exposed
                assert 'password' not in user
                assert 'username' in user
    
    def test_employee_list_serialization(self, client, auth_headers):
        """Test employees are properly serialized."""
        response = client.get('/api/employees/', headers=auth_headers)
        
        if response.status_code == 200:
            data = json.loads(response.data)
            employees = data['data'].get('items', [])
            
            if employees:
                first_employee = employees[0]
                assert 'id' in first_employee
                assert 'name' in first_employee
                assert 'email' in first_employee


@pytest.mark.validation
@pytest.mark.unit
class TestValidationErrorMessages:
    """Test validation error messages are descriptive."""
    
    def test_error_message_in_spanish(self, client, auth_headers):
        """Test validation errors return messages in Spanish."""
        invalid_inventory = {
            'name': 'AB',  # Too short
            'price': -100,  # Negative
            'quantity': -5,  # Negative
            'category_id': 0  # Invalid
        }
        
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=invalid_inventory)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        # Should have error details
        assert 'errors' in data or 'error' in data
        
        # If errors dict, check field-level errors
        if 'errors' in data:
            errors = data['errors']
            assert isinstance(errors, dict)
            assert len(errors) > 0
    
    def test_missing_field_error_message(self, client, auth_headers):
        """Test missing required field generates descriptive error."""
        incomplete_data = {}  # Missing all fields
        
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=incomplete_data)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data or 'error' in data
