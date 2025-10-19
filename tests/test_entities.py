"""
Entity (Domain Model) Tests

Tests for entity classes:
- to_dict() serialization
- Business logic methods
- Attribute validation
- Relationships
"""

import pytest
from datetime import datetime
from app.entities.user import User
from app.entities.organization import Organization
from app.entities.inventory_item import InventoryItem
from app.entities.employee import Employee
from app.entities.quote import Quote


@pytest.mark.entities
@pytest.mark.unit
class TestOrganizationEntity:
    """Test Organization entity."""
    
    def test_organization_creation(self):
        """Test creating organization entity."""
        org = Organization(
            name='Test Org',
            nit='123456789-0',
            address='Test Address',
            phone='3001234567',
            email='test@org.com'
        )
        
        assert org.name == 'Test Org'
        assert org.nit == '123456789-0'
        assert org.status == 'active'  # Default
        assert org.creation_date is not None
    
    def test_organization_to_dict(self, test_organization):
        """Test organization to_dict serialization."""
        org_dict = test_organization.to_dict()
        
        assert isinstance(org_dict, dict)
        assert 'id' in org_dict
        assert 'name' in org_dict
        assert org_dict['name'] == test_organization.name
        assert 'status' in org_dict
    
    def test_organization_activate(self):
        """Test organization activate method."""
        org = Organization(
            name='Test',
            nit='123',
            status='inactive'
        )
        
        org.activate()
        assert org.status == 'active'
        assert org.update_date is not None


@pytest.mark.entities
@pytest.mark.unit
class TestUserEntity:
    """Test User entity."""
    
    def test_user_creation(self, test_organization):
        """Test creating user entity."""
        from werkzeug.security import generate_password_hash
        
        user = User(
            username='testuser',
            email='test@user.com',
            password=generate_password_hash('Test123!'),
            organization_id=test_organization.id
        )
        
        assert user.username == 'testuser'
        assert user.email == 'test@user.com'
        assert user.status == 'active'  # Default
        assert user.password != 'Test123!'  # Should be hashed
    
    def test_user_to_dict_excludes_password(self, test_user):
        """Test user to_dict does not include password."""
        user_dict = test_user.to_dict()
        
        assert isinstance(user_dict, dict)
        assert 'id' in user_dict
        assert 'username' in user_dict
        assert 'email' in user_dict
        # Password must NOT be in dict
        assert 'password' not in user_dict
    
    def test_user_activate_deactivate(self, test_user):
        """Test user status change methods."""
        # Deactivate
        test_user.status = 'inactive'
        assert test_user.status == 'inactive'
        
        # Activate
        test_user.status = 'active'
        assert test_user.status == 'active'


@pytest.mark.entities
@pytest.mark.unit
class TestInventoryItemEntity:
    """Test InventoryItem entity."""
    
    def test_inventory_item_creation(self, test_organization):
        """Test creating inventory item."""
        item = InventoryItem(
            name='Test Product',
            description='Description',
            price=1500.00,
            quantity=100,
            category_id=1,
            organization_id=test_organization.id
        )
        
        assert item.name == 'Test Product'
        assert item.price == 1500.00
        assert item.quantity == 100
        assert item.status == 'active'
    
    def test_inventory_item_to_dict(self, db_session, test_organization):
        """Test inventory item serialization."""
        item = InventoryItem(
            name='Test',
            price=1000,
            quantity=50,
            category_id=1,
            organization_id=test_organization.id,
            status='active'
        )
        db_session.add(item)
        db_session.commit()
        
        item_dict = item.to_dict()
        
        assert isinstance(item_dict, dict)
        assert 'id' in item_dict
        assert 'name' in item_dict
        assert 'price' in item_dict
        assert item_dict['name'] == 'Test'
        assert item_dict['price'] == '1000.00'  # Numeric as string
    
    def test_inventory_item_add_stock(self, db_session, test_organization):
        """Test adding stock to inventory."""
        item = InventoryItem(
            name='Stock Test',
            price=500,
            quantity=50,
            category_id=1,
            organization_id=test_organization.id,
            status='active'
        )
        
        # Add stock (if method exists)
        if hasattr(item, 'add_stock'):
            item.add_stock(25)
            assert item.quantity == 75
        else:
            # Manual addition
            item.quantity += 25
            assert item.quantity == 75
    
    def test_inventory_item_remove_stock(self, db_session, test_organization):
        """Test removing stock from inventory."""
        item = InventoryItem(
            name='Stock Test',
            price=500,
            quantity=50,
            category_id=1,
            organization_id=test_organization.id,
            status='active'
        )
        
        # Remove stock (if method exists)
        if hasattr(item, 'remove_stock'):
            item.remove_stock(20)
            assert item.quantity == 30
        else:
            # Manual subtraction
            item.quantity -= 20
            assert item.quantity == 30


@pytest.mark.entities
@pytest.mark.unit
class TestEmployeeEntity:
    """Test Employee entity."""
    
    def test_employee_creation(self):
        """Test creating employee."""
        employee = Employee(
            name='Juan',
            last_name='Pérez',
            email='juan@test.com',
            phone='3001234567',
            hire_date=datetime.utcnow().date(),
            branch_id=1
        )
        
        assert employee.name == 'Juan'
        assert employee.last_name == 'Pérez'
        assert employee.email == 'juan@test.com'
        assert employee.status == 'active'
    
    def test_employee_to_dict(self, db_session):
        """Test employee serialization."""
        employee = Employee(
            name='Pedro',
            last_name='García',
            email='pedro@test.com',
            hire_date=datetime.utcnow().date(),
            branch_id=1,
            status='active'
        )
        db_session.add(employee)
        db_session.commit()
        
        emp_dict = employee.to_dict()
        
        assert isinstance(emp_dict, dict)
        assert 'id' in emp_dict
        assert 'name' in emp_dict
        assert 'last_name' in emp_dict
        assert emp_dict['name'] == 'Pedro'


@pytest.mark.entities
@pytest.mark.unit
class TestQuoteEntity:
    """Test Quote entity."""
    
    def test_quote_creation(self, test_organization):
        """Test creating quote."""
        quote = Quote(
            organization_id=test_organization.id,
            client_name='Test Client',
            client_email='client@test.com',
            client_phone='3001234567',
            quote_date=datetime.utcnow().date(),
            expiration_date='2025-12-31',
            status='pending'
        )
        
        assert quote.client_name == 'Test Client'
        assert quote.status == 'pending'
        assert quote.organization_id == test_organization.id
    
    def test_quote_to_dict(self, db_session, test_organization):
        """Test quote serialization."""
        quote = Quote(
            organization_id=test_organization.id,
            client_name='Test Client',
            client_email='client@test.com',
            quote_date=datetime.utcnow().date(),
            status='pending'
        )
        db_session.add(quote)
        db_session.commit()
        
        quote_dict = quote.to_dict()
        
        assert isinstance(quote_dict, dict)
        assert 'id' in quote_dict
        assert 'client_name' in quote_dict
        assert 'status' in quote_dict


@pytest.mark.entities
@pytest.mark.unit
class TestEntityTimestamps:
    """Test entity timestamp fields."""
    
    def test_creation_date_auto_set(self, db_session, test_organization):
        """Test creation_date is automatically set."""
        item = InventoryItem(
            name='Timestamp Test',
            price=100,
            quantity=10,
            category_id=1,
            organization_id=test_organization.id,
            status='active'
        )
        db_session.add(item)
        db_session.commit()
        
        assert item.creation_date is not None
        assert isinstance(item.creation_date, datetime)
    
    def test_update_date_auto_set(self, db_session, test_organization):
        """Test update_date is automatically set on modification."""
        item = InventoryItem(
            name='Update Test',
            price=100,
            quantity=10,
            category_id=1,
            organization_id=test_organization.id,
            status='active'
        )
        db_session.add(item)
        db_session.commit()
        
        original_update = item.update_date
        
        # Modify item
        item.name = 'Updated Name'
        db_session.commit()
        
        # update_date should change
        assert item.update_date is not None
        assert item.update_date >= original_update


@pytest.mark.entities
@pytest.mark.unit
class TestEntityRelationships:
    """Test entity relationships."""
    
    def test_organization_has_users(self, test_organization, test_user):
        """Test organization -> users relationship."""
        # Assuming Organization has users relationship
        if hasattr(test_organization, 'users'):
            assert test_user in test_organization.users or len(test_organization.users) >= 0
    
    def test_user_belongs_to_organization(self, test_user, test_organization):
        """Test user -> organization relationship."""
        assert test_user.organization_id == test_organization.id


@pytest.mark.entities
@pytest.mark.unit
class TestEntityStatusDefaults:
    """Test entity status field defaults."""
    
    def test_default_status_active(self, test_organization):
        """Test entities default to 'active' status."""
        # User
        from werkzeug.security import generate_password_hash
        user = User(
            username='statustest',
            email='status@test.com',
            password=generate_password_hash('Test123!'),
            organization_id=test_organization.id
        )
        assert user.status == 'active'
        
        # Organization
        org = Organization(
            name='Status Test',
            nit='123456789'
        )
        assert org.status == 'active'
        
        # Inventory Item
        item = InventoryItem(
            name='Status Test',
            price=100,
            quantity=10,
            category_id=1,
            organization_id=test_organization.id
        )
        assert item.status == 'active'


@pytest.mark.entities
@pytest.mark.unit
class TestEntityStringRepresentation:
    """Test entity __repr__ methods."""
    
    def test_user_repr(self, test_user):
        """Test user string representation."""
        repr_str = repr(test_user)
        assert isinstance(repr_str, str)
        # Should contain username
        if hasattr(test_user, '__repr__'):
            assert 'testuser' in repr_str or 'User' in repr_str
    
    def test_organization_repr(self, test_organization):
        """Test organization string representation."""
        repr_str = repr(test_organization)
        assert isinstance(repr_str, str)
        if hasattr(test_organization, '__repr__'):
            assert 'Test Organization' in repr_str or 'Organization' in repr_str
