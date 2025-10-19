#!/usr/bin/env python3
"""
Script Completo de Población de Base de Datos
Genera datos de prueba realistas para todas las tablas del sistema
SIN VALORES NULOS - Todos los campos requeridos son llenados
"""

from datetime import datetime, timedelta
import random
from decimal import Decimal
from app import create_app, db
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


# Datos realistas para Colombia
STATES_CITIES = {
    'Antioquia': ['Medellín', 'Envigado', 'Bello', 'Itagüí', 'Rionegro'],
    'Cundinamarca': ['Bogotá', 'Soacha', 'Chía', 'Zipaquirá', 'Facatativá'],
    'Valle del Cauca': ['Cali', 'Palmira', 'Tuluá', 'Buenaventura', 'Cartago'],
    'Atlántico': ['Barranquilla', 'Soledad', 'Malambo', 'Sabanalarga', 'Puerto Colombia'],
    'Santander': ['Bucaramanga', 'Floridablanca', 'Girón', 'Piedecuesta', 'Barrancabermeja'],
    'Bolívar': ['Cartagena', 'Magangué', 'Turbaco', 'Arjona', 'El Carmen de Bolívar']
}

FIRST_NAMES = ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena', 'Felipe', 'Gloria', 'Hugo', 'Irene', 'Jorge',
               'Karla', 'Luis', 'María', 'Nelson', 'Olivia', 'Pedro', 'Quintero', 'Rosa', 'Sergio', 'Teresa']

LAST_NAMES = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 'Sánchez', 'Ramírez',
              'Torres', 'Flores', 'Rivera', 'Gómez', 'Díaz', 'Cruz', 'Morales', 'Reyes', 'Gutiérrez',
              'Ortiz', 'Jiménez', 'Hernández']

COMPANIES = ['TechSolutions', 'InnovaCorp', 'GlobalTrade', 'SmartBusiness', 'EcoSystems',
             'DataPro', 'CloudFirst', 'NetWorks', 'InfoTech', 'DigiTrends']

BRANDS = ['Samsung', 'Apple', 'Huawei', 'Xiaomi', 'LG', 'Sony', 'HP', 'Lenovo', 'Dell', 'Asus']

PRODUCT_CATEGORIES = ['Smartphones', 'Laptops', 'Tablets', 'Accesorios', 'Audio', 'Wearables', 
                      'Gaming', 'Networking', 'Storage', 'Monitores']

PRODUCTS = {
    'Smartphones': ['Galaxy S23', 'iPhone 15 Pro', 'Pixel 8', 'Redmi Note 13', 'Moto Edge 40'],
    'Laptops': ['MacBook Pro M3', 'ThinkPad X1', 'Pavilion 15', 'ZenBook', 'Legion 5'],
    'Tablets': ['iPad Air', 'Galaxy Tab S9', 'MatePad Pro', 'Mi Pad 6', 'Surface Pro 9'],
    'Accesorios': ['AirPods Pro', 'Galaxy Buds', 'Magic Mouse', 'Keyboard MX Keys', 'Webcam HD'],
    'Audio': ['Soundbar', 'Auriculares Bluetooth', 'Parlante Portátil', 'Micrófono USB', 'Audífonos Gaming']
}


def clear_database():
    """Limpia todas las tablas (solo para testing)"""
    print("\n⚠️  Limpiando base de datos...")
    
    # Orden inverso de dependencias
    InvoiceItem.query.delete()
    Invoice.query.delete()
    SalesOrderItem.query.delete()
    SalesOrder.query.delete()
    QuotationLine.query.delete()
    Quote.query.delete()
    Assignment.query.delete()
    SalesGoal.query.delete()
    InventoryItem.query.delete()
    ItemCategory.query.delete()
    Brand.query.delete()
    Employee.query.delete()
    User.query.delete()
    Person.query.delete()
    Branch.query.delete()
    Organization.query.delete()
    City.query.delete()
    State.query.delete()
    
    db.session.commit()
    print("✓ Base de datos limpiada")


def create_states_and_cities():
    """Crea estados y ciudades de Colombia"""
    print("\n1️⃣  Verificando Estados y Ciudades...")
    
    states = []
    cities = []
    
    for state_name, city_names in STATES_CITIES.items():
        # Verificar si ya existe el estado
        state = State.query.filter_by(code=state_name[:3].upper()).first()
        
        if not state:
            # Crear estado
            state = State(
                description=state_name,
                code=state_name[:3].upper()
            )
            db.session.add(state)
            db.session.flush()  # Para obtener el ID
            print(f"   ✓ Estado creado: {state_name}")
        else:
            print(f"   ⏭️  Estado ya existe: {state_name}")
        
        states.append(state)
        
        # Crear ciudades del estado
        for city_name in city_names:
            # Verificar si ya existe la ciudad
            existing_city = City.query.filter_by(description=city_name, state_id=state.id).first()
            
            if not existing_city:
                city = City(
                    description=city_name,
                    state_id=state.id,
                    code=f"{state.code}-{len(cities)+1}"
                )
                db.session.add(city)
                cities.append(city)
            else:
                cities.append(existing_city)
    
    db.session.commit()
    print(f"   📊 Total estados: {len(states)} | Ciudades: {City.query.count()}")
    
    return states, cities


def create_organizations_and_branches(cities):
    """Crea organizaciones y sucursales"""
    print("\n2️⃣  Creando Organizaciones y Sucursales...")
    
    organizations = []
    branches = []
    
    for i, company_name in enumerate(COMPANIES):
        # Crear organización
        org = Organization(
            historical_name=company_name,
            current_name=company_name
        )
        db.session.add(org)
        db.session.flush()
        organizations.append(org)
        
        # Crear 2-4 sucursales por organización
        num_branches = random.randint(2, 4)
        for j in range(num_branches):
            city = random.choice(cities)
            branch = Branch(
                description=f"{company_name} - Sede {city.description}",
                organization_id=org.id,
                city_id=city.id
            )
            db.session.add(branch)
            branches.append(branch)
    
    db.session.commit()
    print(f"   ✓ {len(organizations)} organizaciones creadas")
    print(f"   ✓ {len(branches)} sucursales creadas")
    
    return organizations, branches


def create_persons_and_employees(branches):
    """Crea personas y empleados"""
    print("\n3️⃣  Creando Personas y Empleados...")
    
    persons = []
    employees = []
    
    # Crear 50 personas
    for i in range(50):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        city = random.choice(branches).city_id if branches else None
        
        person = Person(
            first_name=first_name,
            last_name=last_name,
            dni=str(random.randint(10000000, 99999999)),
            phone=f"+57 {random.randint(300, 350)} {random.randint(1000000, 9999999)}",
            address=f"Calle {random.randint(1, 200)} # {random.randint(1, 100)}-{random.randint(1, 99)}",
            city_id=city
        )
        db.session.add(person)
        db.session.flush()
        persons.append(person)
        
        # 70% de las personas son empleados
        if random.random() < 0.7:
            branch = random.choice(branches)
            
            employee = Employee(
                person_id=person.id,
                branch_id=branch.id
            )
            db.session.add(employee)
            employees.append(employee)
    
    db.session.commit()
    print(f"   ✓ {len(persons)} personas creadas")
    print(f"   ✓ {len(employees)} empleados creados")
    
    return persons, employees


def create_roles_and_users(employees):
    """Crea roles y usuarios"""
    print("\n4️⃣  Creando Roles y Usuarios...")
    
    # Verificar si ya existen roles
    existing_roles = Role.query.all()
    if len(existing_roles) >= 3:
        roles = existing_roles[:3]
        print(f"   ⏭️  Roles ya existen, usando existentes")
    else:
        # Crear roles
        admin_role = Role(name='ADMIN', description='Administrador del sistema')
        manager_role = Role(name='MANAGER', description='Gerente')
        sales_role = Role(name='SALES', description='Vendedor')
        
        db.session.add_all([admin_role, manager_role, sales_role])
        db.session.flush()
        roles = [admin_role, manager_role, sales_role]
        print(f"   ✓ {len(roles)} roles creados")
    
    # Crear usuarios para algunos empleados
    users = []
    for i, employee in enumerate(employees[:20]):  # Primeros 20 empleados
        person = Person.query.get(employee.person_id)
        username = f"{person.first_name.lower()}{i+1}"
        
        # Asignar rol de manera alternada
        if i % 3 == 0:
            role = roles[1]  # MANAGER
        else:
            role = roles[2]  # SALES
        
        user = User(
            username=username,
            password=hash_password('password123'),  # Password genérica para testing
            role_id=role.id
        )
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    print(f"   ✓ {len(users)} usuarios creados")
    print(f"   📝 Password para todos los nuevos usuarios: password123")
    
    return roles, users


def create_brands_and_categories():
    """Crea marcas y categorías"""
    print("\n5️⃣  Creando Marcas y Categorías...")
    
    brands = []
    for brand_name in BRANDS:
        brand = Brand(
            name=brand_name,
            description=f"Productos de la marca {brand_name}"
        )
        db.session.add(brand)
        brands.append(brand)
    
    db.session.flush()
    
    categories = []
    for cat_name in PRODUCT_CATEGORIES:
        category = ItemCategory(
            name=cat_name
        )
        db.session.add(category)
        categories.append(category)
    
    db.session.commit()
    print(f"   ✓ {len(brands)} marcas creadas")
    print(f"   ✓ {len(categories)} categorías creadas")
    
    return brands, categories


def create_inventory(brands, categories, branches):
    """Crea inventario de productos"""
    print("\n6️⃣  Creando Inventario...")
    
    inventory_items = []
    
    for category in categories[:5]:  # Solo primeras 5 categorías para no saturar
        products = PRODUCTS.get(category.name, ['Producto Genérico'])
        
        for product_name in products:
            brand = random.choice(brands)
            
            item = InventoryItem(
                name=f"{brand.name} {product_name}",
                description=f"{product_name} de {brand.name} - Alta calidad",
                price=Decimal(str(random.randint(100000, 5000000))),
                quantity=random.randint(10, 200),
                category_id=category.id,
                brand_id=brand.id
            )
            db.session.add(item)
            inventory_items.append(item)
    
    db.session.commit()
    print(f"   ✓ {len(inventory_items)} items de inventario creados")
    
    return inventory_items


def create_sales_goals(branches, employees):
    """Crea metas de ventas"""
    print("\n7️⃣  Creando Metas de Ventas...")
    
    goals = []
    periods = ['MONTHLY', 'QUARTERLY', 'ANNUAL']
    months = list(range(1, 13))
    
    # Metas para sucursales
    for branch in branches[:5]:  # Primeras 5 sucursales
        for period in periods:
            goal = SalesGoal(
                goal_type='BRANCH',
                period=period,
                branch_id=branch.id,
                employee_id=None,
                target_amount=Decimal(str(random.randint(50000000, 200000000))),
                achieved_amount=Decimal(str(random.randint(20000000, 180000000))),
                start_date=datetime(2025, random.choice(months), 1).date(),
                end_date=datetime(2025, random.choice(months), 28).date()
            )
            db.session.add(goal)
            goals.append(goal)
    
    # Metas para empleados
    for employee in employees[:10]:  # Primeros 10 empleados
        goal = SalesGoal(
            goal_type='EMPLOYEE',
            period='MONTHLY',
            branch_id=employee.branch_id,
            employee_id=employee.id,
            target_amount=Decimal(str(random.randint(10000000, 50000000))),
            achieved_amount=Decimal(str(random.randint(5000000, 45000000))),
            start_date=datetime(2025, 10, 1).date(),
            end_date=datetime(2025, 10, 31).date()
        )
        db.session.add(goal)
        goals.append(goal)
    
    db.session.commit()
    print(f"   ✓ {len(goals)} metas de ventas creadas")
    
    return goals


def create_quotes_and_lines(persons, employees, inventory_items):
    """Crea cotizaciones con líneas"""
    print("\n8️⃣  Creando Cotizaciones...")
    
    quotes = []
    quotation_lines = []
    
    # Crear 30 cotizaciones
    for i in range(30):
        customer = random.choice(persons)
        employee = random.choice(employees)
        
        quote = Quote(
            customer_person_id=customer.id,
            employee_id=employee.id,
            quote_date=datetime.now() - timedelta(days=random.randint(1, 180)),
            valid_until=datetime.now() + timedelta(days=random.randint(1, 30)),
            status=random.choice(['PENDING', 'APPROVED', 'REJECTED', 'EXPIRED']),
            total_amount=Decimal('0')
        )
        db.session.add(quote)
        db.session.flush()
        
        # Agregar 2-5 líneas de productos
        num_items = random.randint(2, 5)
        quote_total = Decimal('0')
        
        for j in range(num_items):
            item = random.choice(inventory_items)
            quantity = random.randint(1, 5)
            unit_price = item.unit_price
            subtotal = unit_price * quantity
            
            line = QuotationLine(
                quote_id=quote.id,
                inventory_item_id=item.id,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            db.session.add(line)
            quotation_lines.append(line)
            quote_total += subtotal
        
        quote.total_amount = quote_total
        quotes.append(quote)
    
    db.session.commit()
    print(f"   ✓ {len(quotes)} cotizaciones creadas")
    print(f"   ✓ {len(quotation_lines)} líneas de cotización creadas")
    
    return quotes, quotation_lines


def create_sales_orders_and_invoices(quotes, quotation_lines, employees):
    """Crea órdenes de venta y facturas a partir de cotizaciones aprobadas"""
    print("\n9️⃣  Creando Órdenes de Venta y Facturas...")
    
    sales_orders = []
    sales_order_items = []
    invoices = []
    invoice_items = []
    
    # Tomar solo cotizaciones aprobadas
    approved_quotes = [q for q in quotes if q.status == 'APPROVED']
    
    for quote in approved_quotes[:15]:  # Primeras 15 aprobadas
        employee = random.choice(employees)
        
        # Crear orden de venta
        order = SalesOrder(
            quote_id=quote.id,
            employee_id=employee.id,
            order_date=quote.quote_date + timedelta(days=random.randint(1, 7)),
            expected_delivery=quote.quote_date + timedelta(days=random.randint(8, 30)),
            status=random.choice(['PENDING', 'CONFIRMED', 'DELIVERED', 'CANCELLED']),
            total_amount=quote.total_amount
        )
        db.session.add(order)
        db.session.flush()
        sales_orders.append(order)
        
        # Crear items de la orden
        quote_lines = QuotationLine.query.filter_by(quote_id=quote.id).all()
        for line in quote_lines:
            order_item = SalesOrderItem(
                sales_order_id=order.id,
                inventory_item_id=line.inventory_item_id,
                quantity=line.quantity,
                unit_price=line.unit_price,
                subtotal=line.subtotal
            )
            db.session.add(order_item)
            sales_order_items.append(order_item)
        
        # Si la orden está confirmada o entregada, crear factura
        if order.status in ['CONFIRMED', 'DELIVERED']:
            invoice = Invoice(
                sales_order_id=order.id,
                employee_id=employee.id,
                invoice_number=f"FAC-{random.randint(10000, 99999)}",
                invoice_date=order.order_date + timedelta(days=random.randint(1, 5)),
                due_date=order.order_date + timedelta(days=random.randint(30, 60)),
                status=random.choice(['PAID', 'PENDING', 'OVERDUE']),
                subtotal=order.total_amount,
                tax_amount=order.total_amount * Decimal('0.19'),  # IVA 19%
                total_amount=order.total_amount * Decimal('1.19')
            )
            db.session.add(invoice)
            db.session.flush()
            invoices.append(invoice)
            
            # Crear items de la factura
            for order_item in SalesOrderItem.query.filter_by(sales_order_id=order.id).all():
                inv_item = InvoiceItem(
                    invoice_id=invoice.id,
                    inventory_item_id=order_item.inventory_item_id,
                    quantity=order_item.quantity,
                    unit_price=order_item.unit_price,
                    subtotal=order_item.subtotal
                )
                db.session.add(inv_item)
                invoice_items.append(inv_item)
    
    db.session.commit()
    print(f"   ✓ {len(sales_orders)} órdenes de venta creadas")
    print(f"   ✓ {len(sales_order_items)} items de órdenes creados")
    print(f"   ✓ {len(invoices)} facturas creadas")
    print(f"   ✓ {len(invoice_items)} items de facturas creados")
    
    return sales_orders, invoices


def create_assignments(employees, inventory_items):
    """Crea asignaciones de items a empleados"""
    print("\n🔟 Creando Asignaciones...")
    
    assignments = []
    
    # Asignar 1-3 items a cada empleado
    for employee in employees[:15]:  # Primeros 15 empleados
        num_assignments = random.randint(1, 3)
        for _ in range(num_assignments):
            item = random.choice(inventory_items)
            
            assignment = Assignment(
                employee_id=employee.id,
                inventory_item_id=item.id,
                assignment_date=datetime.now() - timedelta(days=random.randint(1, 90)),
                return_date=None if random.random() < 0.7 else datetime.now() - timedelta(days=random.randint(1, 30)),
                notes=f"Asignado para trabajo de campo"
            )
            db.session.add(assignment)
            assignments.append(assignment)
    
    db.session.commit()
    print(f"   ✓ {len(assignments)} asignaciones creadas")
    
    return assignments


def print_summary():
    """Imprime resumen de la población"""
    print("\n" + "="*70)
    print(" 📊 RESUMEN DE POBLACIÓN DE BASE DE DATOS")
    print("="*70)
    
    print(f"\n📍 Geografía:")
    print(f"   - Estados: {State.query.count()}")
    print(f"   - Ciudades: {City.query.count()}")
    
    print(f"\n🏢 Organizacional:")
    print(f"   - Organizaciones: {Organization.query.count()}")
    print(f"   - Sucursales: {Branch.query.count()}")
    print(f"   - Personas: {Person.query.count()}")
    print(f"   - Empleados: {Employee.query.count()}")
    
    print(f"\n👥 Usuarios y Seguridad:")
    print(f"   - Roles: {Role.query.count()}")
    print(f"   - Usuarios: {User.query.count()}")
    
    print(f"\n📦 Inventario:")
    print(f"   - Marcas: {Brand.query.count()}")
    print(f"   - Categorías: {ItemCategory.query.count()}")
    print(f"   - Items: {InventoryItem.query.count()}")
    print(f"   - Asignaciones: {Assignment.query.count()}")
    
    print(f"\n💰 Ventas:")
    print(f"   - Cotizaciones: {Quote.query.count()}")
    print(f"   - Líneas de Cotización: {QuotationLine.query.count()}")
    print(f"   - Órdenes de Venta: {SalesOrder.query.count()}")
    print(f"   - Items de Órdenes: {SalesOrderItem.query.count()}")
    print(f"   - Facturas: {Invoice.query.count()}")
    print(f"   - Items de Facturas: {InvoiceItem.query.count()}")
    
    print(f"\n🎯 Metas:")
    print(f"   - Metas de Ventas: {SalesGoal.query.count()}")
    
    print("\n" + "="*70)
    print(" ✅ POBLACIÓN COMPLETADA EXITOSAMENTE")
    print("="*70)
    print("\n📝 Credenciales de usuarios nuevos:")
    print("   Username: [nombre][número] (ej: ana1, bruno2, etc.)")
    print("   Password: password123")
    print("\n🚀 Ahora puedes:")
    print("   1. Probar los endpoints en Swagger UI")
    print("   2. Ver analytics en /api/analytics/")
    print("   3. Desarrollar el frontend con datos reales")
    print("\n" + "="*70 + "\n")


def main():
    """Ejecuta la población completa"""
    print("="*70)
    print(" 🚀 SCRIPT DE POBLACIÓN COMPLETA DE BASE DE DATOS")
    print("="*70)
    print("\n✅ Este script agregará datos SIN BORRAR los existentes")
    print()
    
    app = create_app()
    with app.app_context():
        try:
            # Obtener datos existentes
            existing_cities = City.query.all()
            existing_branches = Branch.query.all()
            existing_persons = Person.query.all()
            existing_employees = Employee.query.all()
            
            print(f"📊 Datos existentes:")
            print(f"   - Ciudades: {len(existing_cities)}")
            print(f"   - Sucursales: {len(existing_branches)}")
            print(f"   - Personas: {len(existing_persons)}")
            print(f"   - Empleados: {len(existing_employees)}")
            print()
            
            # Paso 1: Geografía
            states, cities = create_states_and_cities()
            
            # Paso 2: Organizaciones
            organizations, branches = create_organizations_and_branches(cities if cities else existing_cities)
            
            # Paso 3: Personas y empleados
            persons, employees = create_persons_and_employees(branches if branches else existing_branches)
            
            # Paso 4: Usuarios y roles
            roles, users = create_roles_and_users(employees if employees else existing_employees)
            
            # Paso 5: Marcas y categorías
            brands, categories = create_brands_and_categories()
            
            # Paso 6: Inventario
            all_branches = Branch.query.all()
            inventory_items = create_inventory(brands, categories, all_branches)
            
            # Paso 7: Metas
            goals = create_sales_goals(all_branches, Employee.query.all())
            
            # Paso 8: Cotizaciones
            all_persons = Person.query.all()
            all_employees = Employee.query.all()
            quotes, quotation_lines = create_quotes_and_lines(all_persons, all_employees, inventory_items)
            
            # Paso 9: Órdenes y facturas
            sales_orders, invoices = create_sales_orders_and_invoices(quotes, quotation_lines, all_employees)
            
            # Paso 10: Asignaciones
            assignments = create_assignments(all_employees, inventory_items)
            
            # Resumen
            print_summary()
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()


if __name__ == "__main__":
    main()
