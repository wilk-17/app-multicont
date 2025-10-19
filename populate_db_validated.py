#!/usr/bin/env python3
"""
Script de Población de Base de Datos - VERSIÓN VALIDADA
Basado en verificación completa de modelos (verify_models.py)
Todos los parámetros coinciden EXACTAMENTE con los constructores de los modelos
"""

from datetime import datetime, timedelta, date
import random
from decimal import Decimal
from app import create_app, db

# Importar TODOS los modelos
from app.entities.state import State
from app.entities.city import City
from app.entities.organization import Organization
from app.entities.branch import Branch
from app.entities.person import Person
from app.entities.employee import Employee
from app.entities.role import Role
from app.entities.user import User
from app.entities.brand import Brand
from app.entities.item_category import ItemCategory
from app.entities.inventory_item import InventoryItem
from app.entities.quote import Quote
from app.entities.quotation_line import QuotationLine
from app.entities.sales_order import SalesOrder
from app.entities.sales_order_item import SalesOrderItem
from app.entities.invoice import Invoice
from app.entities.invoice_item import InvoiceItem
from app.entities.sales_goal import SalesGoal
from app.entities.assignment import Assignment
from app.utils.security import hash_password

# ================================================================================
# DATOS DE PRUEBA REALISTAS
# ================================================================================

STATES_CITIES = {
    'Antioquia': ['Medellín', 'Envigado', 'Bello', 'Itagüí', 'Rionegro'],
    'Cundinamarca': ['Bogotá', 'Soacha', 'Chía', 'Zipaquirá', 'Facatativá'],
    'Valle del Cauca': ['Cali', 'Palmira', 'Tuluá', 'Buenaventura', 'Cartago'],
    'Atlántico': ['Barranquilla', 'Soledad', 'Malambo', 'Sabanalarga', 'Puerto Colombia'],
    'Santander': ['Bucaramanga', 'Floridablanca', 'Girón', 'Piedecuesta', 'Barrancabermeja']
}

FIRST_NAMES = ['Carlos', 'María', 'José', 'Ana', 'Luis', 'Laura', 'Pedro', 'Sofía', 
               'Miguel', 'Isabella', 'Juan', 'Valentina', 'Diego', 'Camila', 'Andrés']

LAST_NAMES = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 
              'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez']

COMPANIES = ['TechSolutions SA', 'InnovaCorp Ltda', 'GlobalTrade Colombia', 
             'SmartBusiness Group', 'EcoSystems Tech', 'DataPro Solutions',
             'CloudFirst Colombia', 'NetWorks Enterprise', 'InfoTech Global']

BRANDS = ['Samsung', 'Apple', 'Huawei', 'Xiaomi', 'LG', 'Sony', 'HP', 'Lenovo', 'Dell', 'Asus']

CATEGORIES = ['Smartphones', 'Laptops', 'Tablets', 'Accesorios', 'Audio', 
              'Wearables', 'Gaming', 'Networking', 'Storage', 'Monitores']

PRODUCTS = {
    'Smartphones': ['Galaxy S23', 'iPhone 15 Pro', 'Pixel 8', 'Redmi Note 13'],
    'Laptops': ['MacBook Pro M3', 'ThinkPad X1', 'Pavilion 15', 'ZenBook'],
    'Tablets': ['iPad Air', 'Galaxy Tab S9', 'MatePad Pro'],
    'Accesorios': ['AirPods Pro', 'Galaxy Buds', 'Magic Mouse', 'Keyboard MX Keys'],
    'Audio': ['Soundbar 5.1', 'Auriculares Bluetooth', 'Parlante Portátil']
}


# ================================================================================
# FUNCIONES DE POBLACIÓN
# ================================================================================

def populate_states_and_cities():
    """Poblar Estados y Ciudades"""
    print("\n1️⃣  Estados y Ciudades")
    states_created = 0
    cities_created = 0
    
    all_states = []
    all_cities = []
    
    for state_name, city_names in STATES_CITIES.items():
        # Verificar si existe
        state = State.query.filter_by(code=state_name[:3].upper()).first()
        
        if not state:
            # Crear estado - Parámetros: description, code
            state = State(
                description=state_name,
                code=state_name[:3].upper()
            )
            db.session.add(state)
            db.session.flush()
            states_created += 1
        
        all_states.append(state)
        
        # Crear ciudades
        for city_name in city_names:
            existing = City.query.filter_by(description=city_name, state_id=state.id).first()
            
            if not existing:
                # Crear ciudad - Parámetros: description, state_id, [code]
                city = City(
                    description=city_name,
                    state_id=state.id,
                    code=f"{state.code}-{len(all_cities)+1}"
                )
                db.session.add(city)
                all_cities.append(city)
                cities_created += 1
            else:
                all_cities.append(existing)
    
    db.session.commit()
    print(f"   ✓ Estados: {states_created} nuevos | Total: {State.query.count()}")
    print(f"   ✓ Ciudades: {cities_created} nuevas | Total: {City.query.count()}")
    
    return all_states, all_cities


def populate_organizations_and_branches(cities):
    """Poblar Organizaciones y Sucursales"""
    print("\n2️⃣  Organizaciones y Sucursales")
    orgs_created = 0
    branches_created = 0
    
    all_orgs = []
    all_branches = []
    
    for company_name in COMPANIES:
        # Verificar si existe
        org = Organization.query.filter_by(current_name=company_name).first()
        
        if not org:
            # Crear organización - Parámetros: historical_name, current_name
            org = Organization(
                historical_name=company_name,
                current_name=company_name
            )
            db.session.add(org)
            db.session.flush()
            orgs_created += 1
        
        all_orgs.append(org)
        
        # Crear 2-3 sucursales
        existing_branches = Branch.query.filter_by(organization_id=org.id).count()
        
        if existing_branches < 2:
            for i in range(2):
                city = random.choice(cities)
                # Crear sucursal - Parámetros: organization_id, city_id
                branch = Branch(
                    organization_id=org.id,
                    city_id=city.id
                )
                db.session.add(branch)
                all_branches.append(branch)
                branches_created += 1
    
    db.session.commit()
    print(f"   ✓ Organizaciones: {orgs_created} nuevas | Total: {Organization.query.count()}")
    print(f"   ✓ Sucursales: {branches_created} nuevas | Total: {Branch.query.count()}")
    
    # Obtener todas las sucursales
    all_branches = Branch.query.all()
    return all_orgs, all_branches


def populate_persons_and_employees(branches, cities):
    """Poblar Personas y Empleados"""
    print("\n3️⃣  Personas y Empleados")
    persons_created = 0
    employees_created = 0
    
    all_persons = []
    all_employees = []
    
    for i in range(30):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        dni = str(random.randint(10000000, 99999999))
        
        # Verificar si ya existe DNI
        if Person.query.filter_by(dni=dni).first():
            continue
        
        city = random.choice(cities)
        
        # Crear persona - Parámetros: first_name, last_name, [dni, address, phone, city_id]
        person = Person(
            first_name=first_name,
            last_name=last_name,
            dni=dni,
            address=f"Calle {random.randint(1, 200)} # {random.randint(1, 100)}-{random.randint(1, 99)}",
            phone=f"+57 {random.randint(300, 350)}{random.randint(1000000, 9999999)}",
            city_id=city.id
        )
        db.session.add(person)
        db.session.flush()
        all_persons.append(person)
        persons_created += 1
        
        # 70% son empleados
        if random.random() < 0.7:
            branch = random.choice(branches)
            
            # Crear empleado - Parámetros: person_id, branch_id
            employee = Employee(
                person_id=person.id,
                branch_id=branch.id
            )
            db.session.add(employee)
            all_employees.append(employee)
            employees_created += 1
    
    db.session.commit()
    print(f"   ✓ Personas: {persons_created} nuevas | Total: {Person.query.count()}")
    print(f"   ✓ Empleados: {employees_created} nuevos | Total: {Employee.query.count()}")
    
    # Obtener todos los empleados
    all_employees = Employee.query.all()
    return all_persons, all_employees


def populate_roles_and_users(employees):
    """Poblar Roles y Usuarios"""
    print("\n4️⃣  Roles y Usuarios")
    
    # Verificar roles existentes
    admin_role = Role.query.filter_by(name='ADMIN').first()
    manager_role = Role.query.filter_by(name='MANAGER').first()
    sales_role = Role.query.filter_by(name='SALES').first()
    
    roles_created = 0
    if not admin_role:
        admin_role = Role(name='ADMIN')
        db.session.add(admin_role)
        roles_created += 1
    
    if not manager_role:
        manager_role = Role(name='MANAGER')
        db.session.add(manager_role)
        roles_created += 1
    
    if not sales_role:
        sales_role = Role(name='SALES')
        db.session.add(sales_role)
        roles_created += 1
    
    db.session.flush()
    
    # Crear usuarios para empleados
    users_created = 0
    all_roles = [admin_role, manager_role, sales_role]
    
    for i, employee in enumerate(employees[:15]):  # Primeros 15 empleados
        person = Person.query.get(employee.person_id)
        username = f"{person.first_name.lower()}{i+1}"
        
        # Verificar si ya existe
        if User.query.filter_by(username=username).first():
            continue
        
        # Asignar rol
        if i == 0:
            role = admin_role
        elif i % 3 == 0:
            role = manager_role
        else:
            role = sales_role
        
        # Crear usuario - Parámetros: username, password, role_id
        user = User(
            username=username,
            password=hash_password('password123'),
            role_id=role.id
        )
        db.session.add(user)
        users_created += 1
    
    db.session.commit()
    print(f"   ✓ Roles: {roles_created} nuevos | Total: {Role.query.count()}")
    print(f"   ✓ Usuarios: {users_created} nuevos | Total: {User.query.count()}")
    print(f"   📝 Password para nuevos usuarios: password123")
    
    return all_roles


def populate_brands_and_categories():
    """Poblar Marcas y Categorías"""
    print("\n5️⃣  Marcas y Categorías")
    brands_created = 0
    categories_created = 0
    
    all_brands = []
    all_categories = []
    
    for brand_name in BRANDS:
        brand = Brand.query.filter_by(name=brand_name).first()
        
        if not brand:
            # Crear marca - Parámetros: name, [description]
            # NOTA: creation_date se establece automáticamente en la DB
            brand = Brand(
                name=brand_name,
                description=f"Productos de {brand_name}"
            )
            db.session.add(brand)
            brands_created += 1
        
        all_brands.append(brand)
    
    for cat_name in CATEGORIES:
        category = ItemCategory.query.filter_by(name=cat_name).first()
        
        if not category:
            # Crear categoría - Parámetros: name
            category = ItemCategory(
                name=cat_name
            )
            db.session.add(category)
            categories_created += 1
        
        all_categories.append(category)
    
    db.session.commit()
    print(f"   ✓ Marcas: {brands_created} nuevas | Total: {Brand.query.count()}")
    print(f"   ✓ Categorías: {categories_created} nuevas | Total: {ItemCategory.query.count()}")
    
    # Obtener todos
    all_brands = Brand.query.all()
    all_categories = ItemCategory.query.all()
    return all_brands, all_categories


def populate_inventory(brands, categories):
    """Poblar Inventario"""
    print("\n6️⃣  Inventario")
    items_created = 0
    
    for category in categories[:5]:  # Primeras 5 categorías
        products = PRODUCTS.get(category.name, ['Producto Genérico'])
        
        for product_name in products:
            brand = random.choice(brands)
            item_name = f"{brand.name} {product_name}"
            
            # Verificar si ya existe
            if InventoryItem.query.filter_by(name=item_name).first():
                continue
            
            # Crear item - Parámetros: name, price, [quantity, description, category_id, brand_id]
            item = InventoryItem(
                name=item_name,
                price=Decimal(str(random.randint(100000, 5000000))),
                quantity=random.randint(10, 200),
                description=f"{product_name} de {brand.name} - Alta calidad",
                category_id=category.id,
                brand_id=brand.id
            )
            db.session.add(item)
            items_created += 1
    
    db.session.commit()
    print(f"   ✓ Items: {items_created} nuevos | Total: {InventoryItem.query.count()}")
    
    return InventoryItem.query.all()


def populate_sales_goals(branches, employees):
    """Poblar Metas de Ventas"""
    print("\n7️⃣  Metas de Ventas")
    goals_created = 0
    
    periods = ['MONTHLY', 'QUARTERLY', 'ANNUAL']
    
    # Metas para sucursales
    for branch in branches[:5]:
        for period in periods[:2]:  # Solo monthly y quarterly
            # Verificar si ya existe
            existing = SalesGoal.query.filter_by(
                branch_id=branch.id,
                period_type=period
            ).first()
            
            if existing:
                continue
            
            # Crear meta - Parámetros: period_type, start_date, end_date, target_amount, 
            #                           [employee_id, branch_id, created_by_user_id]
            # NOTA: creation_date se establece automáticamente
            goal = SalesGoal(
                period_type=period,
                start_date=date(2025, 10, 1),
                end_date=date(2025, 10, 31),
                target_amount=Decimal(str(random.randint(50000000, 200000000))),
                branch_id=branch.id
            )
            db.session.add(goal)
            goals_created += 1
    
    # Metas para empleados
    for employee in employees[:10]:
        existing = SalesGoal.query.filter_by(
            employee_id=employee.id,
            period_type='MONTHLY'
        ).first()
        
        if existing:
            continue
        
        goal = SalesGoal(
            period_type='MONTHLY',
            start_date=date(2025, 10, 1),
            end_date=date(2025, 10, 31),
            target_amount=Decimal(str(random.randint(10000000, 50000000))),
            employee_id=employee.id,
            branch_id=employee.branch_id
        )
        db.session.add(goal)
        goals_created += 1
    
    db.session.commit()
    print(f"   ✓ Metas: {goals_created} nuevas | Total: {SalesGoal.query.count()}")


def populate_quotes_and_orders(persons, employees, inventory_items):
    """Poblar Cotizaciones, Órdenes e Invoices"""
    print("\n8️⃣  Cotizaciones, Órdenes y Facturas")
    quotes_created = 0
    quote_lines_created = 0
    orders_created = 0
    invoices_created = 0
    
    # Crear 20 cotizaciones
    for i in range(20):
        person = random.choice(persons)
        employee = random.choice(employees)
        
        # Crear cotización - Parámetros: customer_name, date, [total, employee_id]
        quote = Quote(
            customer_name=f"{person.first_name} {person.last_name}",
            date=date.today() - timedelta(days=random.randint(1, 90)),
            employee_id=employee.id
        )
        db.session.add(quote)
        db.session.flush()
        quotes_created += 1
        
        # Agregar 2-4 líneas
        quote_total = Decimal('0')
        for j in range(random.randint(2, 4)):
            item = random.choice(inventory_items)
            quantity = random.randint(1, 5)
            price = item.price
            
            # Crear línea - Parámetros: quote_id, item_id, quantity, price, [description]
            line = QuotationLine(
                quote_id=quote.id,
                item_id=item.id,
                quantity=quantity,
                price=price,
                description=f"Venta de {item.name}"
            )
            db.session.add(line)
            quote_lines_created += 1
            quote_total += price * quantity
        
        # Actualizar total de cotización
        quote.total = quote_total
        
        # 60% de las cotizaciones se convierten en órdenes
        if random.random() < 0.6:
            # Crear orden - Parámetros: quote_id, date, [total, employee_id]
            order = SalesOrder(
                quote_id=quote.id,
                date=quote.date + timedelta(days=random.randint(1, 7)),
                total=quote_total,
                employee_id=employee.id
            )
            db.session.add(order)
            db.session.flush()
            orders_created += 1
            
            # Crear items de la orden
            lines = QuotationLine.query.filter_by(quote_id=quote.id).all()
            for line in lines:
                # Crear item de orden - Parámetros: sales_order_id, item_id, quantity
                order_item = SalesOrderItem(
                    sales_order_id=order.id,
                    item_id=line.item_id,
                    quantity=line.quantity
                )
                db.session.add(order_item)
            
            # 70% de las órdenes generan factura
            if random.random() < 0.7:
                # Crear factura - Parámetros: sales_order_id, date, [total, quotation_line_id, employee_id]
                invoice = Invoice(
                    sales_order_id=order.id,
                    date=order.date + timedelta(days=random.randint(1, 5)),
                    total=quote_total * Decimal('1.19'),  # Con IVA
                    employee_id=employee.id
                )
                db.session.add(invoice)
                db.session.flush()
                invoices_created += 1
                
                # Crear items de factura
                for line in lines:
                    # Crear item de factura - Parámetros: invoice_id, item_id, quantity, price
                    inv_item = InvoiceItem(
                        invoice_id=invoice.id,
                        item_id=line.item_id,
                        quantity=line.quantity,
                        price=line.price
                    )
                    db.session.add(inv_item)
    
    db.session.commit()
    print(f"   ✓ Cotizaciones: {quotes_created} nuevas | Total: {Quote.query.count()}")
    print(f"   ✓ Líneas de cotización: {quote_lines_created} nuevas | Total: {QuotationLine.query.count()}")
    print(f"   ✓ Órdenes: {orders_created} nuevas | Total: {SalesOrder.query.count()}")
    print(f"   ✓ Facturas: {invoices_created} nuevas | Total: {Invoice.query.count()}")


def populate_assignments(employees, inventory_items):
    """Poblar Asignaciones"""
    print("\n9️⃣  Asignaciones")
    assignments_created = 0
    
    # Asignar 1-2 items a cada empleado
    for employee in employees[:10]:
        num_assignments = random.randint(1, 2)
        
        for _ in range(num_assignments):
            item = random.choice(inventory_items)
            
            # Verificar si ya existe
            existing = Assignment.query.filter_by(
                employee_id=employee.id,
                item_id=item.id
            ).first()
            
            if existing:
                continue
            
            # Crear asignación - Parámetros: employee_id, item_id, assigned_date
            assignment = Assignment(
                employee_id=employee.id,
                item_id=item.id,
                assigned_date=date.today() - timedelta(days=random.randint(1, 90))
            )
            db.session.add(assignment)
            assignments_created += 1
    
    db.session.commit()
    print(f"   ✓ Asignaciones: {assignments_created} nuevas | Total: {Assignment.query.count()}")


def print_summary():
    """Imprime resumen final"""
    print("\n" + "="*80)
    print(" 📊 RESUMEN FINAL DE BASE DE DATOS")
    print("="*80)
    
    print(f"\n📍 Geografía:")
    print(f"   • Estados: {State.query.count()}")
    print(f"   • Ciudades: {City.query.count()}")
    
    print(f"\n🏢 Organizacional:")
    print(f"   • Organizaciones: {Organization.query.count()}")
    print(f"   • Sucursales: {Branch.query.count()}")
    print(f"   • Personas: {Person.query.count()}")
    print(f"   • Empleados: {Employee.query.count()}")
    
    print(f"\n👥 Usuarios:")
    print(f"   • Roles: {Role.query.count()}")
    print(f"   • Usuarios: {User.query.count()}")
    
    print(f"\n📦 Inventario:")
    print(f"   • Marcas: {Brand.query.count()}")
    print(f"   • Categorías: {ItemCategory.query.count()}")
    print(f"   • Items: {InventoryItem.query.count()}")
    print(f"   • Asignaciones: {Assignment.query.count()}")
    
    print(f"\n💰 Ventas:")
    print(f"   • Cotizaciones: {Quote.query.count()}")
    print(f"   • Líneas de Cotización: {QuotationLine.query.count()}")
    print(f"   • Órdenes: {SalesOrder.query.count()}")
    print(f"   • Items de Órdenes: {SalesOrderItem.query.count()}")
    print(f"   • Facturas: {Invoice.query.count()}")
    print(f"   • Items de Facturas: {InvoiceItem.query.count()}")
    
    print(f"\n🎯 Metas:")
    print(f"   • Metas de Ventas: {SalesGoal.query.count()}")
    
    print("\n" + "="*80)
    print(" ✅ POBLACIÓN COMPLETADA EXITOSAMENTE")
    print("="*80)
    print()


# ================================================================================
# FUNCIÓN PRINCIPAL
# ================================================================================

def main():
    """Ejecuta la población completa"""
    print("="*80)
    print(" 🚀 POBLACIÓN DE BASE DE DATOS - VERSIÓN VALIDADA")
    print("="*80)
    print("\n✅ Script basado en verificación de modelos (verify_models.py)")
    print("✅ Todos los parámetros coinciden con constructores reales")
    print("✅ Agrega datos SIN BORRAR existentes")
    print()
    
    app = create_app()
    with app.app_context():
        try:
            # Paso 1: Estados y Ciudades
            states, cities = populate_states_and_cities()
            
            # Paso 2: Organizaciones y Sucursales
            orgs, branches = populate_organizations_and_branches(cities)
            
            # Paso 3: Personas y Empleados
            persons, employees = populate_persons_and_employees(branches, cities)
            
            # Paso 4: Roles y Usuarios
            roles = populate_roles_and_users(employees)
            
            # Paso 5: Marcas y Categorías
            brands, categories = populate_brands_and_categories()
            
            # Paso 6: Inventario
            inventory_items = populate_inventory(brands, categories)
            
            # Paso 7: Metas
            populate_sales_goals(branches, employees)
            
            # Paso 8: Cotizaciones, Órdenes y Facturas
            populate_quotes_and_orders(persons, employees, inventory_items)
            
            # Paso 9: Asignaciones
            populate_assignments(employees, inventory_items)
            
            # Resumen
            print_summary()
            
            print("📝 Credenciales de usuarios:")
            print("   Username: [nombre][número] (ej: carlos1, maría2)")
            print("   Password: password123")
            print()
            print("🚀 Próximos pasos:")
            print("   1. Probar endpoints en Swagger UI: http://127.0.0.1:5000/api/docs/")
            print("   2. Usar login con nuevos usuarios")
            print("   3. Desarrollar frontend en Angular")
            print()
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()


if __name__ == "__main__":
    main()
