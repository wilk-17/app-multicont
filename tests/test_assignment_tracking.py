"""
Tests para el sistema de trazabilidad de asignaciones
Valida tracking de status: active → returned/lost
"""
import pytest
from datetime import date, datetime
from app import create_app, db
from app.entities.assignment import Assignment
from app.entities.employee import Employee
from app.entities.inventory_item import InventoryItem
from app.entities.person import Person
from app.entities.branch import Branch
from app.entities.organization import Organization
from app.entities.city import City
from app.entities.state import State
from app.use_cases.assignment_handler import AssignmentHandler


@pytest.fixture
def app():
    """Crear aplicación para testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de testing"""
    return app.test_client()


@pytest.fixture
def sample_data(app):
    """Crear datos de prueba"""
    with app.app_context():
        # Estado (State)
        state = State(description="Test State", code="TS")
        db.session.add(state)
        db.session.flush()
        
        # Ciudad (City)
        city = City(description="Test City", state_id=state.id, code="TC")
        db.session.add(city)
        db.session.flush()
        
        # Organización
        org = Organization(
            historical_name="Test Org Historical",
            current_name="Test Org Current"
        )
        db.session.add(org)
        db.session.flush()
        
        # Sucursal (Branch)
        branch = Branch(
            organization_id=org.id,
            city_id=city.id
        )
        db.session.add(branch)
        db.session.flush()
        
        # Persona
        person = Person(
            first_name="John",
            last_name="Doe",
            dni="123456789",
            phone="555-1234",
            city_id=city.id
        )
        db.session.add(person)
        db.session.flush()
        
        # Empleado
        employee = Employee(
            person_id=person.id,
            branch_id=branch.id
        )
        db.session.add(employee)
        db.session.flush()
        
        # Item de inventario
        item = InventoryItem(
            name="Laptop Dell",
            price=1500000,
            quantity=10,
            description="Laptop para asignación de prueba"
        )
        db.session.add(item)
        db.session.flush()
        
        db.session.commit()
        
        return {
            'employee_id': employee.id,
            'item_id': item.id
        }


class TestAssignmentTracking:
    """Tests de trazabilidad de asignaciones"""
    
    def test_create_assignment(self, app, sample_data):
        """Test crear asignación nueva (status=active por defecto)"""
        with app.app_context():
            assignment = Assignment(
                employee_id=sample_data['employee_id'],
                item_id=sample_data['item_id']
            )
            db.session.add(assignment)
            db.session.commit()
            
            # Validar campos por defecto
            assert assignment.status == 'active'
            assert assignment.assigned_date == date.today()
            assert assignment.return_date is None
            assert assignment.condition is None
            assert assignment.notes is None
            assert assignment.creation_date is not None
            print(f"✅ Asignación creada: ID={assignment.id}, status={assignment.status}")
    
    def test_mark_returned_good_condition(self, app, sample_data):
        """Test marcar asignación como devuelta en buen estado"""
        with app.app_context():
            # Crear asignación
            assignment = Assignment(
                employee_id=sample_data['employee_id'],
                item_id=sample_data['item_id']
            )
            db.session.add(assignment)
            db.session.commit()
            assignment_id = assignment.id
            
            # Marcar como devuelta
            handler = AssignmentHandler()
            returned = handler.mark_returned(
                assignment_id,
                condition='good',
                notes='Item devuelto en perfecto estado'
            )
            
            # Validar cambios
            assert returned.status == 'returned'
            assert returned.return_date == date.today()
            assert returned.condition == 'good'
            assert returned.notes == 'Item devuelto en perfecto estado'
            print(f"✅ Asignación devuelta: ID={returned.id}, condition={returned.condition}")
    
    def test_mark_returned_damaged(self, app, sample_data):
        """Test marcar asignación como devuelta dañada"""
        with app.app_context():
            assignment = Assignment(
                employee_id=sample_data['employee_id'],
                item_id=sample_data['item_id']
            )
            db.session.add(assignment)
            db.session.commit()
            assignment_id = assignment.id
            
            handler = AssignmentHandler()
            returned = handler.mark_returned(
                assignment_id,
                condition='damaged',
                notes='Pantalla rota, requiere reparación'
            )
            
            assert returned.status == 'returned'
            assert returned.condition == 'damaged'
            assert 'rota' in returned.notes
            print(f"✅ Asignación devuelta dañada: {returned.notes}")
    
    def test_mark_lost(self, app, sample_data):
        """Test marcar asignación como perdida"""
        with app.app_context():
            assignment = Assignment(
                employee_id=sample_data['employee_id'],
                item_id=sample_data['item_id']
            )
            db.session.add(assignment)
            db.session.commit()
            assignment_id = assignment.id
            
            handler = AssignmentHandler()
            lost = handler.mark_lost(
                assignment_id,
                notes='Item extraviado en traslado'
            )
            
            assert lost.status == 'lost'
            assert lost.condition == 'missing'
            assert lost.notes == 'Item extraviado en traslado'
            print(f"✅ Asignación perdida: ID={lost.id}, status={lost.status}")
    
    def test_employee_history(self, app, sample_data):
        """Test obtener historial completo de empleado"""
        with app.app_context():
            # Crear múltiples asignaciones con diferentes estados
            assignments = [
                Assignment(employee_id=sample_data['employee_id'], item_id=sample_data['item_id']),
                Assignment(employee_id=sample_data['employee_id'], item_id=sample_data['item_id']),
                Assignment(employee_id=sample_data['employee_id'], item_id=sample_data['item_id'])
            ]
            for a in assignments:
                db.session.add(a)
            db.session.commit()
            
            # Cambiar estados
            handler = AssignmentHandler()
            handler.mark_returned(assignments[1].id, condition='good')
            handler.mark_lost(assignments[2].id)
            
            # Obtener historial
            history = handler.get_employee_history(sample_data['employee_id'])
            
            # Validar
            assert history['employee_id'] == sample_data['employee_id']
            assert history['summary']['total_assignments'] == 3
            assert history['summary']['active_count'] == 1
            assert history['summary']['returned_count'] == 1
            assert history['summary']['lost_count'] == 1
            
            print(f"✅ Historial de empleado: {history['summary']}")
    
    def test_filter_by_status(self, app, sample_data):
        """Test filtrar asignaciones por status"""
        with app.app_context():
            # Crear asignaciones
            for _ in range(3):
                assignment = Assignment(
                    employee_id=sample_data['employee_id'],
                    item_id=sample_data['item_id']
                )
                db.session.add(assignment)
            db.session.commit()
            
            # Marcar una como devuelta
            all_assignments = Assignment.query.filter_by(employee_id=sample_data['employee_id']).all()
            handler = AssignmentHandler()
            handler.mark_returned(all_assignments[0].id, condition='good')
            
            # Filtrar solo activas
            result = handler.get_by_employee(sample_data['employee_id'], status='active')
            assert result['total'] == 2
            print(f"✅ Asignaciones activas: {result['total']}")
            
            # Filtrar solo devueltas
            result = handler.get_by_employee(sample_data['employee_id'], status='returned')
            assert result['total'] == 1
            print(f"✅ Asignaciones devueltas: {result['total']}")
    
    def test_to_dict_includes_tracking_fields(self, app, sample_data):
        """Test que to_dict() incluye todos los campos de tracking"""
        with app.app_context():
            assignment = Assignment(
                employee_id=sample_data['employee_id'],
                item_id=sample_data['item_id']
            )
            db.session.add(assignment)
            db.session.commit()
            
            # Marcar como devuelta
            handler = AssignmentHandler()
            returned = handler.mark_returned(assignment.id, condition='good', notes='Test')
            
            # Validar serialización
            data = returned.to_dict()
            assert 'status' in data
            assert 'return_date' in data
            assert 'condition' in data
            assert 'notes' in data
            assert 'creation_date' in data
            assert 'update_date' in data
            
            assert data['status'] == 'returned'
            assert data['condition'] == 'good'
            print(f"✅ Serialización completa: {list(data.keys())}")


def run_tests():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("🧪 EJECUTANDO TESTS DE TRAZABILIDAD DE ASIGNACIONES")
    print("="*70)
    
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == '__main__':
    run_tests()
