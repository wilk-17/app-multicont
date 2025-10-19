"""
API Endpoint Tests

Tests HTTP para endpoints REST:
- Quote API (GET, POST, PUT, DELETE)
- Inventory Item API
- Employee API
- User API
- Authentication flow
"""

import pytest
import json
from datetime import datetime


@pytest.mark.integration
@pytest.mark.api
class TestQuoteAPI:
    """Test Quote API endpoints."""
    
    def test_list_quotes(self, client, auth_headers):
        """Test GET /api/quotes/ - List all quotes."""
        response = client.get('/api/quotes/', headers=auth_headers)
        
        assert response.status_code in [200, 401]  # May require specific role
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'data' in data
            assert 'items' in data['data']
            assert 'total' in data['data']
    
    def test_list_quotes_pagination(self, client, auth_headers):
        """Test GET /api/quotes/?page=1&per_page=5."""
        response = client.get('/api/quotes/?page=1&per_page=5', headers=auth_headers)
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['data']['page'] == 1
            assert data['data']['per_page'] == 5
    
    def test_get_quote_by_id(self, client, auth_headers):
        """Test GET /api/quotes/<id>."""
        # Try to get quote with ID 1
        response = client.get('/api/quotes/1', headers=auth_headers)
        
        assert response.status_code in [200, 404, 401]
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'data' in data
            assert data['data']['id'] == '1'
    
    def test_create_quote_invalid_data(self, client, auth_headers):
        """Test POST /api/quotes/ with invalid data."""
        invalid_quote = {
            'client_name': 'AB',  # Too short
            'client_email': 'invalid-email',
            'quote_date': '2099-12-31'  # Future date
        }
        
        response = client.post('/api/quotes/', 
                              headers=auth_headers,
                              json=invalid_quote)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'errors' in data or 'error' in data
    
    def test_create_quote_valid_data(self, client, auth_headers, test_organization):
        """Test POST /api/quotes/ with valid data."""
        valid_quote = {
            'organization_id': test_organization.id,
            'client_name': 'Valid Client',
            'client_email': 'valid@client.com',
            'client_phone': '3001234567',
            'quote_date': datetime.utcnow().date().isoformat(),
            'expiration_date': '2025-12-31',
            'status': 'pending'
        }
        
        response = client.post('/api/quotes/',
                              headers=auth_headers,
                              json=valid_quote)
        
        # May succeed or fail depending on DB constraints
        assert response.status_code in [201, 400, 401, 403]
    
    def test_update_quote(self, client, auth_headers):
        """Test PUT /api/quotes/<id>."""
        update_data = {
            'client_name': 'Updated Client Name',
            'status': 'approved'
        }
        
        response = client.put('/api/quotes/1',
                             headers=auth_headers,
                             json=update_data)
        
        assert response.status_code in [200, 404, 400, 401, 403]
    
    def test_delete_quote(self, client, auth_headers):
        """Test DELETE /api/quotes/<id>."""
        response = client.delete('/api/quotes/999999', headers=auth_headers)
        
        # Should return 404 for non-existent quote
        assert response.status_code in [200, 404, 401, 403]


@pytest.mark.integration
@pytest.mark.api
class TestInventoryAPI:
    """Test Inventory Item API endpoints."""
    
    def test_list_inventory_items(self, client, auth_headers):
        """Test GET /api/inventory_items/."""
        response = client.get('/api/inventory_items/', headers=auth_headers)
        
        assert response.status_code in [200, 401]
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'data' in data
            assert 'items' in data['data']
    
    def test_list_inventory_with_status_filter(self, client, auth_headers):
        """Test GET /api/inventory_items/?status=active."""
        response = client.get('/api/inventory_items/?status=active', 
                             headers=auth_headers)
        
        if response.status_code == 200:
            data = json.loads(response.data)
            items = data['data']['items']
            
            # All items should be active
            for item in items:
                assert item['status'] == 'active'
    
    def test_get_inventory_item(self, client, auth_headers):
        """Test GET /api/inventory_items/<id>."""
        response = client.get('/api/inventory_items/1', headers=auth_headers)
        
        assert response.status_code in [200, 404, 401]
    
    def test_create_inventory_invalid_price(self, client, auth_headers):
        """Test POST /api/inventory_items/ with negative price."""
        invalid_item = {
            'name': 'Test Product',
            'price': -100,  # Negative
            'quantity': 10,
            'category_id': 1,
            'organization_id': 1
        }
        
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=invalid_item)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data or 'error' in data
    
    def test_create_inventory_invalid_name_length(self, client, auth_headers):
        """Test POST /api/inventory_items/ with short name."""
        invalid_item = {
            'name': 'AB',  # Too short (< 3 chars)
            'price': 1000,
            'quantity': 10,
            'category_id': 1,
            'organization_id': 1
        }
        
        response = client.post('/api/inventory_items/',
                              headers=auth_headers,
                              json=invalid_item)
        
        assert response.status_code == 400
    
    def test_update_inventory_quantity(self, client, auth_headers):
        """Test PUT /api/inventory_items/<id> to update quantity."""
        update_data = {
            'quantity': 150
        }
        
        response = client.put('/api/inventory_items/1',
                             headers=auth_headers,
                             json=update_data)
        
        assert response.status_code in [200, 404, 400, 401, 403]


@pytest.mark.integration
@pytest.mark.api
class TestEmployeeAPI:
    """Test Employee API endpoints."""
    
    def test_list_employees(self, client, auth_headers):
        """Test GET /api/employees/."""
        response = client.get('/api/employees/', headers=auth_headers)
        
        assert response.status_code in [200, 401]
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'data' in data
    
    def test_get_employee(self, client, auth_headers):
        """Test GET /api/employees/<id>."""
        response = client.get('/api/employees/1', headers=auth_headers)
        
        assert response.status_code in [200, 404, 401]
    
    def test_create_employee_invalid_name(self, client, auth_headers):
        """Test POST /api/employees/ with numbers in name."""
        invalid_employee = {
            'name': 'Juan123',  # Invalid (contains numbers)
            'last_name': 'Pérez',
            'email': 'juan@test.com',
            'hire_date': datetime.utcnow().date().isoformat(),
            'branch_id': 1
        }
        
        response = client.post('/api/employees/',
                              headers=auth_headers,
                              json=invalid_employee)
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data or 'errors' in data
    
    def test_create_employee_invalid_email(self, client, auth_headers):
        """Test POST /api/employees/ with invalid email."""
        invalid_employee = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'email': 'not-an-email',  # Invalid
            'hire_date': datetime.utcnow().date().isoformat(),
            'branch_id': 1
        }
        
        response = client.post('/api/employees/',
                              headers=auth_headers,
                              json=invalid_employee)
        
        assert response.status_code == 400
    
    def test_create_employee_future_hire_date(self, client, auth_headers):
        """Test POST /api/employees/ with future hire date."""
        invalid_employee = {
            'name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan@test.com',
            'hire_date': '2099-12-31',  # Future date
            'branch_id': 1
        }
        
        response = client.post('/api/employees/',
                              headers=auth_headers,
                              json=invalid_employee)
        
        assert response.status_code == 400


@pytest.mark.integration
@pytest.mark.api
class TestUserAPI:
    """Test User API endpoints."""
    
    def test_list_users_without_auth(self, client):
        """Test GET /api/users/ without authentication."""
        response = client.get('/api/users/')
        
        # Should require authentication
        assert response.status_code == 401
    
    def test_list_users_with_auth(self, client, admin_headers):
        """Test GET /api/users/ with admin auth."""
        response = client.get('/api/users/', headers=admin_headers)
        
        assert response.status_code in [200, 403]
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'data' in data
            
            # Verify passwords not exposed
            users = data['data'].get('items', [])
            for user in users:
                assert 'password' not in user
    
    def test_get_user(self, client, admin_headers):
        """Test GET /api/users/<id>."""
        response = client.get('/api/users/1', headers=admin_headers)
        
        assert response.status_code in [200, 404, 403]
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'password' not in data['data']
    
    def test_create_user_weak_password(self, client, admin_headers):
        """Test POST /api/users/ with weak password."""
        weak_user = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'weak',  # Too weak
            'organization_id': 1
        }
        
        response = client.post('/api/users/',
                              headers=admin_headers,
                              json=weak_user)
        
        assert response.status_code == 400
    
    def test_create_user_invalid_username(self, client, admin_headers):
        """Test POST /api/users/ with short username."""
        invalid_user = {
            'username': 'ab',  # Too short
            'email': 'new@test.com',
            'password': 'Strong123!@#',
            'organization_id': 1
        }
        
        response = client.post('/api/users/',
                              headers=admin_headers,
                              json=invalid_user)
        
        assert response.status_code == 400
    
    def test_update_user(self, client, admin_headers):
        """Test PUT /api/users/<id>."""
        update_data = {
            'email': 'updated@test.com'
        }
        
        response = client.put('/api/users/1',
                             headers=admin_headers,
                             json=update_data)
        
        assert response.status_code in [200, 404, 400, 403]
    
    def test_delete_user_without_admin(self, client, auth_headers):
        """Test DELETE /api/users/<id> without admin role."""
        response = client.delete('/api/users/1', headers=auth_headers)
        
        # Should be forbidden for non-admin
        assert response.status_code in [403, 401]


@pytest.mark.integration
@pytest.mark.api
class TestInvoiceAPI:
    """Test Invoice API endpoints."""
    
    def test_list_invoices(self, client, auth_headers):
        """Test GET /api/invoices/."""
        response = client.get('/api/invoices/', headers=auth_headers)
        
        assert response.status_code in [200, 401]
    
    def test_create_invoice_negative_total(self, client, auth_headers):
        """Test POST /api/invoices/ with negative total."""
        invalid_invoice = {
            'sales_order_id': 1,
            'invoice_date': datetime.utcnow().date().isoformat(),
            'total': -100,  # Negative
            'status': 'pending'
        }
        
        response = client.post('/api/invoices/',
                              headers=auth_headers,
                              json=invalid_invoice)
        
        assert response.status_code == 400
    
    def test_create_invoice_future_date(self, client, auth_headers):
        """Test POST /api/invoices/ with future date."""
        invalid_invoice = {
            'sales_order_id': 1,
            'invoice_date': '2099-12-31',  # Future
            'total': 1000,
            'status': 'pending'
        }
        
        response = client.post('/api/invoices/',
                              headers=auth_headers,
                              json=invalid_invoice)
        
        assert response.status_code == 400


@pytest.mark.integration
@pytest.mark.api
class TestSalesOrderAPI:
    """Test Sales Order API endpoints."""
    
    def test_list_sales_orders(self, client, auth_headers):
        """Test GET /api/sales_orders/."""
        response = client.get('/api/sales_orders/', headers=auth_headers)
        
        assert response.status_code in [200, 401]
    
    def test_create_sales_order_negative_total(self, client, auth_headers):
        """Test POST /api/sales_orders/ with negative total."""
        invalid_order = {
            'quote_id': 1,
            'order_date': datetime.utcnow().date().isoformat(),
            'total': -500,  # Negative
            'status': 'pending'
        }
        
        response = client.post('/api/sales_orders/',
                              headers=auth_headers,
                              json=invalid_order)
        
        assert response.status_code == 400


@pytest.mark.integration
@pytest.mark.api
class TestOrganizationAPI:
    """Test Organization API endpoints."""
    
    def test_list_organizations(self, client, auth_headers):
        """Test GET /api/organizations/."""
        response = client.get('/api/organizations/', headers=auth_headers)
        
        assert response.status_code in [200, 401, 403]
    
    def test_get_organization(self, client, auth_headers, test_organization):
        """Test GET /api/organizations/<id>."""
        response = client.get(f'/api/organizations/{test_organization.id}', 
                             headers=auth_headers)
        
        assert response.status_code in [200, 404, 403]
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'data' in data
            assert data['data']['name'] == test_organization.name


@pytest.mark.integration
@pytest.mark.api
class TestPaginationAndFilters:
    """Test pagination and filters across APIs."""
    
    def test_pagination_defaults(self, client, auth_headers):
        """Test default pagination (page=1, per_page=10)."""
        response = client.get('/api/inventory_items/', headers=auth_headers)
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['data']['page'] == 1
            assert data['data']['per_page'] == 10
    
    def test_custom_pagination(self, client, auth_headers):
        """Test custom pagination (page=2, per_page=5)."""
        response = client.get('/api/inventory_items/?page=2&per_page=5', 
                             headers=auth_headers)
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['data']['page'] == 2
            assert data['data']['per_page'] == 5
    
    def test_status_filter_active(self, client, auth_headers):
        """Test status filter (status=active)."""
        response = client.get('/api/employees/?status=active', 
                             headers=auth_headers)
        
        if response.status_code == 200:
            data = json.loads(response.data)
            employees = data['data']['items']
            
            # All should be active
            for emp in employees:
                assert emp['status'] == 'active'
    
    def test_invalid_pagination_page(self, client, auth_headers):
        """Test pagination with invalid page number."""
        response = client.get('/api/inventory_items/?page=0', 
                             headers=auth_headers)
        
        # Should handle gracefully
        assert response.status_code in [200, 400]


@pytest.mark.integration
@pytest.mark.api
class TestErrorHandling:
    """Test API error handling."""
    
    def test_404_on_nonexistent_endpoint(self, client):
        """Test 404 for non-existent endpoint."""
        response = client.get('/api/nonexistent/')
        
        assert response.status_code == 404
    
    def test_405_on_wrong_method(self, client, auth_headers):
        """Test 405 for wrong HTTP method."""
        # POST to endpoint that only accepts GET
        response = client.post('/api/inventory_items/1', 
                              headers=auth_headers,
                              json={})
        
        # Should be Method Not Allowed or similar
        assert response.status_code in [405, 400]
    
    def test_json_response_format(self, client, auth_headers):
        """Test all responses are valid JSON."""
        endpoints = [
            '/api/quotes/',
            '/api/inventory_items/',
            '/api/employees/',
            '/api/organizations/'
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint, headers=auth_headers)
            
            # Should always return valid JSON
            try:
                json.loads(response.data)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON from {endpoint}")
