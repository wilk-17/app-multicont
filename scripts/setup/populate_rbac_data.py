"""
Script para poblar la base de datos con los datos del sistema RBAC
Usuarios: ana (ADMIN), bruno/carla (MANAGER), diego/elena/etc (SALES)
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.entities.user import User
from app.entities.role import Role
from app.entities.organization import Organization
from app.entities.state import State
from app.entities.city import City
from app.entities.branch import Branch
from app.entities.person import Person
from app.entities.employee import Employee
from app.entities.inventory_item import InventoryItem
from app.entities.brand import Brand
from werkzeug.security import generate_password_hash

def populate_rbac_data():
    """Pobla la base de datos con datos del sistema RBAC"""
    app = create_app()
    
    with app.app_context():
        print("="*80)
        print("POBLANDO BASE DE DATOS - SISTEMA RBAC MULTICONT")
        print("="*80)
        
        try:
            # 1. CREAR/ACTUALIZAR ROLES
            print("\n1. ROLES:")
            print("-"*80)
            
            # Actualizar roles existentes primero
            old_admin = Role.query.filter_by(name='Admin').first()
            if old_admin:
                old_admin.name = 'ADMIN'
                print("   ✓ Rol 'Admin' actualizado a 'ADMIN'")
            
            old_user = Role.query.filter_by(name='User').first()
            if old_user:
                old_user.name = 'MANAGER'
                print("   ✓ Rol 'User' actualizado a 'MANAGER'")
            
            db.session.commit()
            
            # Verificar y crear roles faltantes
            admin_role = Role.query.filter_by(name='ADMIN').first()
            if not admin_role:
                admin_role = Role(name='ADMIN')
                db.session.add(admin_role)
                print("   ✓ Rol 'ADMIN' creado")
            else:
                print("   - Rol 'ADMIN' ya existe")
            
            manager_role = Role.query.filter_by(name='MANAGER').first()
            if not manager_role:
                manager_role = Role(name='MANAGER')
                db.session.add(manager_role)
                print("   ✓ Rol 'MANAGER' creado")
            else:
                print("   - Rol 'MANAGER' ya existe")
            
            sales_role = Role.query.filter_by(name='SALES').first()
            if not sales_role:
                sales_role = Role(name='SALES')
                db.session.add(sales_role)
                print("   ✓ Rol 'SALES' creado")
            else:
                print("   - Rol 'SALES' ya existe")
            
            viewer_role = Role.query.filter_by(name='VIEWER').first()
            if not viewer_role:
                viewer_role = Role(name='VIEWER')
                db.session.add(viewer_role)
                print("   ✓ Rol 'VIEWER' creado")
            else:
                print("   - Rol 'VIEWER' ya existe")
            
            db.session.commit()
            
            # 2. CREAR USUARIOS RBAC
            print("\n2. USUARIOS RBAC:")
            print("-"*80)
            
            users_data = [
                ('ana', 'ana123', 'ADMIN'),
                ('bruno', 'bruno123', 'MANAGER'),
                ('carla', 'carla123', 'MANAGER'),
                ('diego', 'diego123', 'SALES'),
                ('elena', 'elena123', 'SALES'),
                ('felipe', 'felipe123', 'SALES'),
                ('gloria', 'gloria123', 'SALES'),
                ('hugo', 'hugo123', 'SALES'),
            ]
            
            for username, password, role_name in users_data:
                existing_user = User.query.filter_by(username=username).first()
                if not existing_user:
                    role = Role.query.filter_by(name=role_name).first()
                    user = User(
                        username=username,
                        password=generate_password_hash(password),
                        role_id=role.id
                    )
                    db.session.add(user)
                    db.session.commit()  # Commit inmediatamente
                    print(f"   ✓ Usuario '{username}' creado ({role_name})")
                else:
                    print(f"   - Usuario '{username}' ya existe")
            
            # 3. CREAR DATOS GEOGRÁFICOS
            print("\n3. UBICACIONES GEOGRÁFICAS:")
            print("-"*80)
            
            state = State.query.first()
            if not state:
                state = State(description='Cundinamarca', code='CUN')
                db.session.add(state)
                db.session.flush()
                print("   ✓ Estado 'Cundinamarca' creado")
            else:
                print("   - Estado ya existe")
            
            city = City.query.first()
            if not city:
                city = City(description='Bogotá D.C.', state_id=state.id, code='BOG')
                db.session.add(city)
                db.session.flush()
                print("   ✓ Ciudad 'Bogotá' creada")
            else:
                print("   - Ciudad ya existe")
            
            # 4. CREAR ORGANIZACIÓN
            print("\n4. ORGANIZACIÓN:")
            print("-"*80)
            
            org = Organization.query.first()
            if not org:
                org = Organization(
                    historical_name='Multicont S.A.S. (Histórico)',
                    current_name='Multicont S.A.S.'
                )
                db.session.add(org)
                db.session.flush()
                print("   ✓ Organización 'Multicont S.A.S.' creada")
            else:
                print("   - Organización ya existe")
            
            # 5. CREAR SUCURSAL
            print("\n5. SUCURSAL:")
            print("-"*80)
            
            branch = Branch.query.first()
            if not branch:
                branch = Branch(
                    organization_id=org.id,
                    city_id=city.id
                )
                db.session.add(branch)
                db.session.flush()
                print("   ✓ Sucursal principal creada")
            else:
                print("   - Sucursal ya existe")
            
            # 6. CREAR PERSONAS Y EMPLEADOS
            print("\n6. PERSONAS Y EMPLEADOS:")
            print("-"*80)
            
            personas_data = [
                ('Ana', 'García', '1234567801', '555-0001'),
                ('Bruno', 'Martínez', '1234567802', '555-0002'),
                ('Carla', 'López', '1234567803', '555-0003'),
                ('Diego', 'Rodríguez', '1234567804', '555-0004'),
                ('Elena', 'Fernández', '1234567805', '555-0005'),
                ('Felipe', 'González', '1234567806', '555-0006'),
                ('Gloria', 'Sánchez', '1234567807', '555-0007'),
                ('Hugo', 'Ramírez', '1234567808', '555-0008'),
            ]
            
            for first_name, last_name, dni, phone in personas_data:
                existing_person = Person.query.filter_by(dni=dni).first()
                if not existing_person:
                    person = Person(
                        first_name=first_name,
                        last_name=last_name,
                        dni=dni,
                        phone=phone,
                        city_id=city.id
                    )
                    db.session.add(person)
                    db.session.flush()
                    
                    employee = Employee(
                        person_id=person.id,
                        branch_id=branch.id
                    )
                    db.session.add(employee)
                    print(f"   ✓ Persona '{first_name} {last_name}' y empleado creados")
                else:
                    print(f"   - Persona '{first_name} {last_name}' ya existe")
            
            db.session.flush()
            
            # 7. CREAR MARCAS
            print("\n7. MARCAS:")
            print("-"*80)
            
            marcas_data = [
                ('Dell', 'Equipos de cómputo Dell'),
                ('HP', 'Equipos de cómputo HP'),
                ('Lenovo', 'Equipos de cómputo Lenovo'),
                ('Samsung', 'Equipos electrónicos Samsung'),
                ('Apple', 'Equipos Apple'),
            ]
            
            for name, description in marcas_data:
                existing_brand = Brand.query.filter_by(name=name).first()
                if not existing_brand:
                    brand = Brand(name=name, description=description)
                    db.session.add(brand)
                    print(f"   ✓ Marca '{name}' creada")
                else:
                    print(f"   - Marca '{name}' ya existe")
            
            db.session.flush()
            
            # 8. CREAR ITEMS DE INVENTARIO
            print("\n8. ITEMS DE INVENTARIO:")
            print("-"*80)
            
            brand_dell = Brand.query.filter_by(name='Dell').first()
            brand_hp = Brand.query.filter_by(name='HP').first()
            brand_samsung = Brand.query.filter_by(name='Samsung').first()
            
            items_data = [
                ('Laptop Dell Latitude 5420', 3500000, 15, 'Laptop empresarial Dell', brand_dell.id if brand_dell else None),
                ('Monitor HP 24"', 800000, 30, 'Monitor Full HD 24 pulgadas', brand_hp.id if brand_hp else None),
                ('Teclado Mecánico Logitech', 250000, 50, 'Teclado mecánico gaming', None),
                ('Mouse Inalámbrico HP', 80000, 100, 'Mouse inalámbrico ergonómico', brand_hp.id if brand_hp else None),
                ('Impresora HP LaserJet Pro', 1500000, 10, 'Impresora láser monocromática', brand_hp.id if brand_hp else None),
                ('Disco Duro Externo 1TB', 200000, 40, 'Disco duro externo portátil', None),
                ('Webcam Logitech HD', 150000, 25, 'Webcam Full HD 1080p', None),
                ('Auriculares Samsung', 120000, 60, 'Auriculares bluetooth Samsung', brand_samsung.id if brand_samsung else None),
            ]
            
            for name, price, quantity, description, brand_id in items_data:
                existing_item = InventoryItem.query.filter_by(name=name).first()
                if not existing_item:
                    item = InventoryItem(
                        name=name,
                        price=price,
                        quantity=quantity,
                        description=description
                    )
                    if brand_id:
                        item.brand_id = brand_id
                    db.session.add(item)
                    print(f"   ✓ Item '{name}' creado")
                else:
                    print(f"   - Item '{name}' ya existe")
            
            db.session.flush()
            
            # COMMIT FINAL
            db.session.commit()
            
            print("\n" + "="*80)
            print("✅ BASE DE DATOS POBLADA EXITOSAMENTE")
            print("="*80)
            
            print("\n📋 RESUMEN:")
            print("-"*80)
            print(f"   Roles:         {Role.query.count()}")
            print(f"   Usuarios:      {User.query.count()}")
            print(f"   Organizaciones: {Organization.query.count()}")
            print(f"   Sucursales:    {Branch.query.count()}")
            print(f"   Empleados:     {Employee.query.count()}")
            print(f"   Marcas:        {Brand.query.count()}")
            print(f"   Items:         {InventoryItem.query.count()}")
            
            print("\n🔐 USUARIOS PARA TESTING:")
            print("-"*80)
            print("   ana / ana123        (ADMIN)")
            print("   bruno / bruno123    (MANAGER)")
            print("   carla / carla123    (MANAGER)")
            print("   diego / diego123    (SALES)")
            print("   elena / elena123    (SALES)")
            print("   felipe / felipe123  (SALES)")
            print("   gloria / gloria123  (SALES)")
            print("   hugo / hugo123      (SALES)")
            print("="*80 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == '__main__':
    populate_rbac_data()
