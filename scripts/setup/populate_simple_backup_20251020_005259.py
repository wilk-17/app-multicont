"""
Script simplificado para poblar BD con modelos actuales
Fecha: 20 de Octubre de 2025
"""

import sys
from pathlib import Path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from app import create_app, db
from app.entities.state import State
from app.entities.city import City
from app.entities.organization import Organization
from app.entities.branch import Branch
from app.entities.person import Person
from app.entities.employee import Employee
from app.entities.user import User
from app.entities.role import Role
from app.entities.permission import Permission
from app.entities.user_role import UserRole
from app.entities.inventory_item import InventoryItem
from app.entities.item_category import ItemCategory
from app.entities.quote import Quote
from app.entities.quote_item import QuoteItem
from app.entities.quotation_line import QuotationLine
from app.entities.sales_order import SalesOrder
from app.entities.sales_order_item import SalesOrderItem
from app.entities.invoice import Invoice
from app.entities.invoice_item import InvoiceItem
from app.entities.assignment import Assignment
from app.utils.security import hash_password
from datetime import date
from decimal import Decimal

def main():
    print("\n🚀 POBLANDO BASE DE DATOS...\n")
    
    app = create_app()
    with app.app_context():
        try:
            # 1. Estados y Ciudades
            print("📍 Estados y ciudades...")
            state1 = State(description='Cundinamarca', code='CUN')
            state2 = State(description='Antioquia', code='ANT')
            db.session.add_all([state1, state2])
            db.session.flush()
            
            city1 = City(description='Bogotá', code='BOG', state_id=state1.id)
            city2 = City(description='Medellín', code='MED', state_id=state2.id)
            db.session.add_all([city1, city2])
            db.session.flush()
            
            # 2. Organizaciones y Sucursales
            print("🏢 Organizaciones y sucursales...")
            org1 = Organization(historical_name='multiCont', current_name='multiCont')
            org2 = Organization(historical_name='Automatiza Andina SAS', current_name='Automatiza Andina SAS')
            db.session.add_all([org1, org2])
            db.session.flush()
            
            branch1 = Branch(organization_id=org1.id, city_id=city1.id)
            branch2 = Branch(organization_id=org1.id, city_id=city2.id)
            db.session.add_all([branch1, branch2])
            db.session.flush()
            
            # 3. Personas y Empleados
            print("👥 Personas y empleados...")
            person1 = Person(dni='CC3001', first_name='Ana', last_name='García', 
                            address='Cra 10 #1-23', phone='300200001', city_id=city1.id)
            person2 = Person(dni='CC3002', first_name='Bruno', last_name='Pineda',
                            address='Cll 12 #3-45', phone='300200002', city_id=city2.id)
            person3 = Person(dni='CC3003', first_name='Carlos', last_name='Mora',
                            address='Cll 8 #9-10', phone='300200003', city_id=city1.id)
            db.session.add_all([person1, person2, person3])
            db.session.flush()
            
            emp1 = Employee(person_id=person1.id, branch_id=branch1.id)
            emp2 = Employee(person_id=person2.id, branch_id=branch2.id)
            emp3 = Employee(person_id=person3.id, branch_id=branch1.id)
            db.session.add_all([emp1, emp2, emp3])
            db.session.flush()
            
            # 4. Roles, Usuarios y Permisos
            print("🔐 Roles, usuarios y permisos...")
            role_admin = Role(name='ADMIN')
            role_manager = Role(name='MANAGER')
            role_sales = Role(name='SALES')
            db.session.add_all([role_admin, role_manager, role_sales])
            db.session.flush()
            
            user1 = User(username='admin', password=hash_password('admin123'), role_id=role_admin.id)
            user2 = User(username='manager', password=hash_password('manager123'), role_id=role_manager.id)
            user3 = User(username='sales', password=hash_password('sales123'), role_id=role_sales.id)
            db.session.add_all([user1, user2, user3])
            db.session.flush()
            
            perm1 = Permission(name='ADMIN_ALL')
            perm2 = Permission(name='READ_REPORTS')
            perm3 = Permission(name='WRITE_QUOTES')
            db.session.add_all([perm1, perm2, perm3])
            db.session.flush()
            
            ur1 = UserRole(user_id=user1.id, role_id=role_admin.id)
            ur2 = UserRole(user_id=user2.id, role_id=role_manager.id)
            ur3 = UserRole(user_id=user3.id, role_id=role_sales.id)
            db.session.add_all([ur1, ur2, ur3])
            
            # 5. Categorías e Inventario
            print("📦 Inventario...")
            cat1 = ItemCategory(name='Automatización')
            cat2 = ItemCategory(name='Sensores')
            db.session.add_all([cat1, cat2])
            db.session.flush()
            
            item1 = InventoryItem(name='PLC Omron NX1P2', price=Decimal('4500000'), quantity=5,
                                 description='Controlador programable', category_id=cat1.id)
            item2 = InventoryItem(name='Sensor E3Z', price=Decimal('180000'), quantity=50,
                                 description='Sensor fotoeléctrico', category_id=cat2.id)
            item3 = InventoryItem(name='Variador A1000', price=Decimal('6000000'), quantity=3,
                                 description='Variador de frecuencia', category_id=cat1.id)
            db.session.add_all([item1, item2, item3])
            db.session.flush()
            
            # 6. Cotizaciones
            print("💰 Cotizaciones...")
            quote1 = Quote(customer_name='Automatiza Andina SAS', date=date(2025, 4, 8),
                          total=Decimal('12800000'), employee_id=emp1.id)
            quote2 = Quote(customer_name='ControlTech SAS', date=date(2025, 5, 15),
                          total=Decimal('18300000'), employee_id=emp2.id)
            db.session.add_all([quote1, quote2])
            db.session.flush()
            
            qi1 = QuoteItem(quote_id=quote1.id, item_id=item2.id, quantity=10)  # QuoteItem no tiene price
            qi2 = QuoteItem(quote_id=quote1.id, item_id=item3.id, quantity=1)
            qi3 = QuoteItem(quote_id=quote2.id, item_id=item1.id, quantity=2)
            db.session.add_all([qi1, qi2, qi3])
            db.session.flush()
            
            # 7. Órdenes de Venta
            print("📝 Órdenes de venta...")
            order1 = SalesOrder(quote_id=quote2.id, date=date(2025, 5, 20),
                               total=Decimal('18300000'), employee_id=emp2.id)
            db.session.add(order1)
            db.session.flush()
            
            oi1 = SalesOrderItem(sales_order_id=order1.id, item_id=item1.id,
                                quantity=2)  # SalesOrderItem no tiene price
            db.session.add(oi1)
            db.session.flush()
            
            # 8. Facturas
            print("🧾 Facturas...")
            invoice1 = Invoice(sales_order_id=order1.id, date=date(2025, 5, 21),
                              total=Decimal('18300000'), employee_id=emp2.id)
            db.session.add(invoice1)
            db.session.flush()
            
            ii1 = InvoiceItem(invoice_id=invoice1.id, item_id=item1.id,
                             quantity=2, price=Decimal('4500000'))
            db.session.add(ii1)
            
            # 9. Asignaciones
            print("📌 Asignaciones...")
            assign1 = Assignment(employee_id=emp1.id, item_id=item1.id,
                                assigned_date=date(2025, 4, 1), status='active')
            db.session.add(assign1)
            
            # COMMIT FINAL
            db.session.commit()
            
            print("\n✅ BASE DE DATOS POBLADA EXITOSAMENTE\n")
            
            # Resumen
            print("📊 RESUMEN:")
            print(f"  • Estados: {State.query.count()}")
            print(f"  • Ciudades: {City.query.count()}")
            print(f"  • Organizaciones: {Organization.query.count()}")
            print(f"  • Sucursales: {Branch.query.count()}")
            print(f"  • Personas: {Person.query.count()}")
            print(f"  • Empleados: {Employee.query.count()}")
            print(f"  • Usuarios: {User.query.count()}")
            print(f"  • Roles: {Role.query.count()}")
            print(f"  • Categorías: {ItemCategory.query.count()}")
            print(f"  • Items: {InventoryItem.query.count()}")
            print(f"  • Cotizaciones: {Quote.query.count()}")
            print(f"  • Órdenes: {SalesOrder.query.count()}")
            print(f"  • Facturas: {Invoice.query.count()}")
            print(f"  • Asignaciones: {Assignment.query.count()}")
            
            print("\n🔐 CREDENCIALES:")
            print("  • admin / admin123")
            print("  • manager / manager123")
            print("  • sales / sales123\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
