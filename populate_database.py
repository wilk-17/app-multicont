"""
Script para poblar la base de datos con el dataset completo (ABR-JUN y JUL-SEP)
Basado en el script SQL proporcionado pero adaptado al modelo actual de SQLAlchemy

Ejecutar: python populate_database.py
"""
import sys
from datetime import date, datetime
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
from app.entities.brand import Brand
from app.entities.item_category import ItemCategory
from app.entities.inventory_item import InventoryItem
from app.entities.assignment import Assignment
from app.entities.quote import Quote
from app.entities.quotation_line import QuotationLine
from app.entities.quote_item import QuoteItem
from app.entities.sales_order import SalesOrder
from app.entities.sales_order_item import SalesOrderItem
from app.entities.invoice import Invoice
from app.entities.invoice_item import InvoiceItem
from app.entities.sales_goal import SalesGoal


def clear_database():
    """Limpiar todas las tablas"""
    print("\n🗑️  Limpiando base de datos...")
    try:
        # Orden inverso de creación para respetar FKs
        db.session.query(SalesGoal).delete()
        db.session.query(UserRole).delete()
        db.session.query(Permission).delete()
        db.session.query(User).delete()
        db.session.query(Assignment).delete()
        db.session.query(InvoiceItem).delete()
        db.session.query(Invoice).delete()
        db.session.query(SalesOrderItem).delete()
        db.session.query(SalesOrder).delete()
        db.session.query(QuotationLine).delete()
        db.session.query(QuoteItem).delete()
        db.session.query(Quote).delete()
        db.session.query(InventoryItem).delete()
        db.session.query(ItemCategory).delete()
        db.session.query(Brand).delete()
        db.session.query(Employee).delete()
        db.session.query(Person).delete()
        db.session.query(Branch).delete()
        db.session.query(Organization).delete()
        db.session.query(City).delete()
        db.session.query(State).delete()
        db.session.query(Role).delete()
        
        db.session.commit()
        print("✅ Base de datos limpiada")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error al limpiar base de datos: {e}")
        raise


def populate_states_cities():
    """Poblar estados y ciudades"""
    print("\n📍 Creando Estados y Ciudades...")
    
    states_data = [
        ('Cundinamarca', 'CUN'),
        ('Santander', 'SAN'),
        ('Antioquia', 'ANT'),
        ('Valle del Cauca', 'VAC'),
        ('Atlántico', 'ATL')
    ]
    
    states = {}
    for desc, code in states_data:
        state = State(description=desc, code=code)
        db.session.add(state)
        db.session.flush()
        states[desc] = state
        print(f"  ✅ Estado: {desc} (ID: {state.id})")
    
    cities_data = [
        ('Bogotá', 'BOG', 'Cundinamarca'), ('Soacha', 'SOA', 'Cundinamarca'),
        ('Chía', 'CHI', 'Cundinamarca'), ('Zipaquirá', 'ZIP', 'Cundinamarca'),
        ('Bucaramanga', 'BGA', 'Santander'), ('Floridablanca', 'FLA', 'Santander'),
        ('Girón', 'GIR', 'Santander'), ('Piedecuesta', 'PDC', 'Santander'),
        ('Medellín', 'MED', 'Antioquia'), ('Envigado', 'ENV', 'Antioquia'),
        ('Bello', 'BEL', 'Antioquia'), ('Itagüí', 'ITA', 'Antioquia'),
        ('Cali', 'CLO', 'Valle del Cauca'), ('Palmira', 'PAL', 'Valle del Cauca'),
        ('Yumbo', 'YUM', 'Valle del Cauca'), ('Buga', 'BUG', 'Valle del Cauca'),
        ('Barranquilla', 'BAQ', 'Atlántico'), ('Soledad', 'SOL', 'Atlántico'),
        ('Malambo', 'MAL', 'Atlántico'), ('Puerto Colombia', 'PTC', 'Atlántico')
    ]
    
    cities = {}
    for desc, code, state_name in cities_data:
        city = City(description=desc, code=code, state_id=states[state_name].id)
        db.session.add(city)
        db.session.flush()
        cities[desc] = city
    
    print(f"  ✅ {len(cities)} ciudades creadas")
    db.session.commit()
    return states, cities


def populate_organizations_branches(cities):
    """Poblar organizaciones y sucursales"""
    print("\n🏢 Creando Organizaciones y Sucursales...")
    
    orgs_data = [
        ('multiCont', 'multiCont'),
        ('Automatiza Andina SAS', 'Automatiza Andina SAS'),
        ('ControlTech SAS', 'ControlTech SAS'),
        ('Industrias del Norte SA', 'Industrias del Norte SA'),
        ('Vallepack LTDA', 'Vallepack LTDA'),
        ('Caribe Foods SA', 'Caribe Foods SA'),
        ('Metalúrgica Antioquia SAS', 'Metalúrgica Antioquia SAS')
    ]
    
    orgs = {}
    for hist, curr in orgs_data:
        org = Organization(historical_name=hist, current_name=curr)
        db.session.add(org)
        db.session.flush()
        orgs[curr] = org
        print(f"  ✅ Organización: {curr} (ID: {org.id})")
    
    # Sucursales de multiCont en las 5 ciudades principales
    branches = []
    multicont = orgs['multiCont']
    cities_for_branches = ['Bogotá', 'Bucaramanga', 'Medellín', 'Cali', 'Barranquilla']
    
    for city_name in cities_for_branches:
        branch = Branch(organization_id=multicont.id, city_id=cities[city_name].id)
        db.session.add(branch)
        db.session.flush()
        branches.append(branch)
        print(f"  ✅ Sucursal en {city_name} (ID: {branch.id})")
    
    db.session.commit()
    return orgs, branches


def populate_persons_employees(cities, branches):
    """Poblar personas y empleados"""
    print("\n👥 Creando Personas y Empleados...")
    
    persons_data = [
        ('CC3001', 'Ana', 'García', 'Cra 10 #1-23', '300200001', 'Bogotá'),
        ('CC3002', 'Bruno', 'Pineda', 'Cll 12 #3-45', '300200002', 'Bucaramanga'),
        ('CC3003', 'Carla', 'Mora', 'Cll 8 #9-10', '300200003', 'Medellín'),
        ('CC3004', 'Diego', 'Luna', 'Cra 45 #12-34', '300200004', 'Cali'),
        ('CC3005', 'Elena', 'Suárez', 'Av 7 #98-11', '300200005', 'Barranquilla'),
        ('CC3006', 'Felipe', 'Cruz', 'Mz 4 Cs 5', '300200006', 'Soacha'),
        ('CC3007', 'Gloria', 'Vega', 'Cra 70 #20-30', '300200007', 'Floridablanca'),
        ('CC3008', 'Hugo', 'Ríos', 'Cll 25 #4-55', '300200008', 'Envigado'),
        ('CC3009', 'Irene', 'Quintero', 'Cll 30 #6-77', '300200009', 'Palmira'),
        ('CC3010', 'Jorge', 'Nieto', 'Cra 15 #5-22', '300200010', 'Soledad'),
        ('CC3011', 'Karen', 'Ortiz', 'Cll 72 #15-33', '300200011', 'Chía'),
        ('CC3012', 'Luis', 'Pardo', 'Cra 8 #14-50', '300200012', 'Girón'),
        ('CC3013', 'Marta', 'Rey', 'Cll 40 #9-21', '300200013', 'Bello'),
        ('CC3014', 'Nicolás', 'Soto', 'Av 13 #45-60', '300200014', 'Yumbo'),
        ('CC3015', 'Olga', 'Torres', 'Cra 9 #20-20', '300200015', 'Malambo'),
        ('CC3016', 'Pablo', 'Uribe', 'Cll 12 #23-12', '300200016', 'Zipaquirá'),
        ('CC3017', 'Raquel', 'Valencia', 'Cra 22 #33-44', '300200017', 'Piedecuesta'),
        ('CC3018', 'Sergio', 'Weber', 'Cll 9 #10-11', '300200018', 'Itagüí'),
        ('CC3019', 'Tatiana', 'Ximénez', 'Cll 1 #1-1', '300200019', 'Buga'),
        ('CC3020', 'Ulises', 'Zárate', 'Cra 100 #50-60', '300200020', 'Puerto Colombia')
    ]
    
    persons = []
    employees = []
    
    for dni, first, last, addr, phone, city_name in persons_data:
        person = Person(
            dni=dni,
            first_name=first,
            last_name=last,
            address=addr,
            phone=phone,
            city_id=cities[city_name].id
        )
        db.session.add(person)
        db.session.flush()
        persons.append(person)
    
    # Primeros 15 como empleados
    for i, person in enumerate(persons[:15]):
        # Asignar a sucursales de forma distribuida
        branch_idx = i % len(branches)
        employee = Employee(person_id=person.id, branch_id=branches[branch_idx].id)
        db.session.add(employee)
        db.session.flush()
        employees.append(employee)
        print(f"  ✅ Empleado: {person.first_name} {person.last_name} - Sucursal {branches[branch_idx].id}")
    
    db.session.commit()
    return persons, employees


def populate_users_roles(persons, employees):
    """Poblar usuarios, roles y permisos"""
    print("\n🔐 Creando Usuarios, Roles y Permisos...")
    
    # Crear roles
    roles_data = ['ADMIN', 'MANAGER', 'SALES']
    roles = {}
    for role_name in roles_data:
        role = Role(name=role_name)
        db.session.add(role)
        db.session.flush()
        roles[role_name] = role
        print(f"  ✅ Rol: {role_name} (ID: {role.id})")
    
    # Crear usuarios (primeros 10 personas)
    users_data = [
        ('ana', 'hash-ana', 0, 'SALES'),
        ('bruno', 'hash-bruno', 1, 'SALES'),
        ('carla', 'hash-carla', 2, 'SALES'),
        ('diego', 'hash-diego', 3, 'SALES'),
        ('elena', 'hash-elena', 4, 'SALES'),
        ('felipe', 'hash-felipe', 5, 'MANAGER'),
        ('gloria', 'hash-gloria', 6, 'MANAGER'),
        ('hugo', 'hash-hugo', 7, 'ADMIN'),
        ('irene', 'hash-irene', 8, 'SALES'),
        ('jorge', 'hash-jorge', 9, 'SALES')
    ]
    
    users = {}
    for username, password, person_idx, role_name in users_data:
        user = User(
            username=username,
            password=password,
            role_id=roles[role_name].id
        )
        db.session.add(user)
        db.session.flush()
        users[username] = user
        print(f"  ✅ Usuario: {username} ({role_name}) - ID: {user.id}")
    
    # Crear permisos
    permissions_data = [
        'READ_REPORTS',
        'WRITE_QUOTES',
        'APPROVE_ORDERS',
        'ADMIN_ALL'
    ]
    
    for perm_name in permissions_data:
        perm = Permission(name=perm_name)
        db.session.add(perm)
    
    # Crear user_roles (relación muchos a muchos)
    for username, role_name in [('ana', 'SALES'), ('bruno', 'SALES'), ('carla', 'SALES'),
                                  ('diego', 'SALES'), ('elena', 'SALES'), ('felipe', 'MANAGER'),
                                  ('gloria', 'MANAGER'), ('hugo', 'ADMIN')]:
        user_role = UserRole(user_id=users[username].id, role_id=roles[role_name].id)
        db.session.add(user_role)
    
    db.session.commit()
    return users, roles


def populate_brands():
    """Poblar marcas"""
    print("\n🏷️  Creando Marcas...")
    
    brands_data = [
        ('Omron', 'Fabricante japonés de automatización industrial'),
        ('ING Multicontrol', 'Soluciones de control industrial'),
        ('Gefran', 'Sensores y controles industriales italianos'),
        ('Weidmüller', 'Conexiones y componentes eléctricos alemanes'),
        ('Rice-Lake', 'Sistemas de pesaje industrial'),
        ('Optec', 'Sensores y dispositivos ópticos')
    ]
    
    brands = {}
    for name, desc in brands_data:
        brand = Brand(name=name, description=desc)
        db.session.add(brand)
        db.session.flush()
        brands[name] = brand
        print(f"  ✅ Marca: {name} (ID: {brand.id})")
    
    db.session.commit()
    return brands


def populate_inventory(brands):
    """Poblar inventario y categorías"""
    print("\n📦 Creando Inventario...")
    
    # Datos: (código, descripción, marca, precio unitario estimado)
    inventory_data = [
        ('OMR-PLC-NX1P2', 'Controlador PLC Omron NX1P2', 'Omron', 4500000),
        ('OMR-SEN-E3Z', 'Sensor fotoeléctrico Omron E3Z', 'Omron', 180000),
        ('OMR-INV-A1000', 'Variador Omron A1000', 'Omron', 6000000),
        ('OMR-HMI-NA5', 'HMI Omron NA5 7"', 'Omron', 1800000),
        ('OMR-IO-NX', 'Módulo I/O Omron NX', 'Omron', 950000),
        ('OMR-ENC-E6B2', 'Encoder Omron E6B2', 'Omron', 420000),
        ('OMR-REL-G2R', 'Relé electromecánico Omron G2R', 'Omron', 85000),
        ('OMR-SSR-G3NA', 'Relé de estado sólido Omron G3NA', 'Omron', 320000),
        ('OMR-PSU-S8VK', 'Fuente 24V Omron S8VK', 'Omron', 450000),
        ('OMR-SAF-F3SG', 'Cortina de seguridad Omron F3SG', 'Omron', 2800000),
        ('ING-ARR-START', 'Arrancador suave ING Multicontrol', 'ING Multicontrol', 2750000),
        ('ING-CON-24V', 'Fuente de poder 24V ING Multicontrol', 'ING Multicontrol', 380000),
        ('ING-PLC-MC200', 'PLC ING Multicontrol MC200', 'ING Multicontrol', 3800000),
        ('ING-HMI-MC7', 'HMI 7" ING Multicontrol', 'ING Multicontrol', 1500000),
        ('ING-VFD-MC500', 'Variador ING Multicontrol MC500', 'ING Multicontrol', 5200000),
        ('ING-IO-MOD8', 'Módulo I/O 8ch ING Multicontrol', 'ING Multicontrol', 680000),
        ('ING-REL-SAF', 'Relé de seguridad ING Multicontrol', 'ING Multicontrol', 540000),
        ('ING-SWI-ETH5', 'Switch Ethernet 5p ING Multicontrol', 'ING Multicontrol', 750000),
        ('ING-ENC-INC', 'Encoder incremental ING Multicontrol', 'ING Multicontrol', 490000),
        ('ING-PSU-48V', 'Fuente 48V ING Multicontrol', 'ING Multicontrol', 620000),
        ('GEF-TEMP-600', 'Controlador de temperatura Gefran 600', 'Gefran', 1350000),
        ('GEF-INV-ADV', 'Inversor de frecuencia Gefran ADV', 'Gefran', 6500000),
        ('GEF-TRANS-LIN', 'Transductor lineal Gefran', 'Gefran', 2100000),
        ('GEF-SSR-GQ', 'Relé de estado sólido Gefran GQ', 'Gefran', 380000),
        ('GEF-DRIVE-AX', 'Servo drive Gefran AX', 'Gefran', 7200000),
        ('GEF-PRES-TRX', 'Transductor de presión Gefran', 'Gefran', 1650000),
        ('GEF-AMP-LC', 'Amplificador para celda de carga Gefran', 'Gefran', 1980000),
        ('GEF-HMI-5', 'HMI 5" Gefran', 'Gefran', 1100000),
        ('GEF-RTD-PT100', 'Sonda RTD PT100 Gefran', 'Gefran', 220000),
        ('GEF-PSU-24', 'Fuente 24V Gefran', 'Gefran', 410000),
        ('WEI-BOR-TER', 'Bornera Weidmüller Terminal', 'Weidmüller', 50000),
        ('WEI-SSR-IO', 'Módulo IO Weidmüller SSR', 'Weidmüller', 250000),
        ('WEI-PSU-24', 'Fuente 24V Weidmüller', 'Weidmüller', 400000),
        ('WEI-REL-TER', 'Relé interfaz Weidmüller', 'Weidmüller', 180000),
        ('WEI-RAIL-DIN', 'Riel DIN Weidmüller', 'Weidmüller', 35000),
        ('WEI-SW-IND8', 'Switch industrial 8p Weidmüller', 'Weidmüller', 890000),
        ('WEI-SURGE-SPD', 'Protección contra sobretensión Weidmüller SPD', 'Weidmüller', 520000),
        ('WEI-CON-PUSHIN', 'Conector Push-In Weidmüller', 'Weidmüller', 28000),
        ('WEI-MARKZ-CARD', 'Tarjetas marcadoras Weidmüller', 'Weidmüller', 45000),
        ('WEI-TOOL-CRIMP', 'Herramienta crimpadora Weidmüller', 'Weidmüller', 1200000),
        ('RCL-BAL-IND', 'Indicador de pesaje Rice-Lake', 'Rice-Lake', 4000000),
        ('RCL-CEL-CARGA', 'Celda de carga Rice-Lake', 'Rice-Lake', 1800000),
        ('RCL-PES-PLC', 'Módulo de pesaje para PLC Rice-Lake', 'Rice-Lake', 3800000),
        ('RCL-JBOX-4', 'Caja de conexiones 4 celdas Rice-Lake', 'Rice-Lake', 650000),
        ('RCL-SCALE-PLT', 'Báscula de plataforma Rice-Lake', 'Rice-Lake', 9500000),
        ('RCL-TRX-ANALOG', 'Transmisor analógico Rice-Lake', 'Rice-Lake', 2200000),
        ('RCL-WEIGH-MOD', 'Módulo de pesaje Rice-Lake', 'Rice-Lake', 2800000),
        ('RCL-CHECK-CKW', 'Checkweigher Rice-Lake', 'Rice-Lake', 15000000),
        ('RCL-PRN-TT', 'Impresora térmica Rice-Lake', 'Rice-Lake', 1500000),
        ('RCL-SW-LIC', 'Licencia software pesaje Rice-Lake', 'Rice-Lake', 4500000),
        ('OPT-SEN-IND', 'Sensor inductivo Optec', 'Optec', 220000),
        ('OPT-BARR-SEG', 'Barrera de seguridad Optec', 'Optec', 900000),
        ('OPT-HMI-7', 'Panel HMI 7" Optec', 'Optec', 1200000),
        ('OPT-PE-SENS', 'Sensor fotoeléctrico Optec', 'Optec', 195000),
        ('OPT-PROX-M18', 'Sensor de proximidad M18 Optec', 'Optec', 165000),
        ('OPT-IO-LINK', 'Módulo IO-Link Master Optec', 'Optec', 780000),
        ('OPT-CAB-M12', 'Cable M12 Optec', 'Optec', 95000),
        ('OPT-BRK-ANG', 'Soporte/bracket angular Optec', 'Optec', 42000),
        ('OPT-PB-LED', 'Pulsador iluminado Optec', 'Optec', 120000),
        ('OPT-TWR-LIGHT', 'Torre luminosa Optec', 'Optec', 280000)
    ]
    
    items = {}
    for code, desc, brand_name, price in inventory_data:
        item = InventoryItem(
            name=desc,
            description=desc,
            quantity=100,  # Stock inicial
            price=price,
            brand_id=brands[brand_name].id
        )
        db.session.add(item)
        db.session.flush()
        items[code] = item
    
    print(f"  ✅ {len(items)} items de inventario creados")
    
    # Crear categorías
    for code, brand_name in [(code, data[2]) for code, *data in inventory_data]:
        category = ItemCategory(name=brand_name)
        db.session.add(category)
    
    db.session.commit()
    return items


def populate_sales_data_q2(employees, orgs, branches, cities, items):
    """Poblar datos de ventas Q2 (Abril-Junio)"""
    print("\n💰 Creando datos de ventas Q2 (Abril-Junio)...")
    
    # Mapeo de empleados por índice (del script SQL original)
    emp_map = {1: employees[0], 4: employees[3], 6: employees[5], 
               8: employees[7], 10: employees[9] if len(employees) > 9 else employees[0], 
               2: employees[1]}
    
    # QUOTES Q2
    quotes_q2 = [
        (date(2025, 4, 8), 12800000, emp_map[1], branches[0], cities['Bogotá']),
        (date(2025, 4, 15), 18300000, emp_map[4], branches[1], cities['Bucaramanga']),
        (date(2025, 5, 3), 15700000, emp_map[6], branches[2], cities['Medellín']),
        (date(2025, 5, 19), 6900000, emp_map[8], branches[3], cities['Cali']),
        (date(2025, 6, 6), 22450000, emp_map[10], branches[4], cities['Barranquilla']),
        (date(2025, 6, 21), 9950000, emp_map[2], branches[0], cities['Chía'])
    ]
    
    quotes = []
    for quote_date, total, employee, branch, city in quotes_q2:
        quote = Quote(
            customer_name=f"Cliente-{len(quotes)+1}",
            date=quote_date,
            total=total,
            employee_id=employee.id
        )
        db.session.add(quote)
        db.session.flush()
        quotes.append(quote)
    
    print(f"  ✅ {len(quotes)} cotizaciones Q2 creadas")
    
    # INVOICES Q2 (simplificado - crear facturas directas)
    invoices_q2_data = [
        (date(2025, 4, 21), 18300000, emp_map[4]),
        (date(2025, 6, 10), 22450000, emp_map[10]),
        (date(2025, 4, 30), 8600000, emp_map[1]),
        (date(2025, 6, 25), 6900000, emp_map[2])
    ]
    
    invoices = []
    for inv_date, total, employee in invoices_q2_data:
        # Crear sales_order primero (simplificado)
        so = SalesOrder(
            quote_id=quotes[len(invoices)].id if len(invoices) < len(quotes) else quotes[0].id,
            date=inv_date,
            total=total,
            employee_id=employee.id
        )
        db.session.add(so)
        db.session.flush()
        
        invoice = Invoice(
            sales_order_id=so.id,
            date=inv_date,
            total=total,
            employee_id=employee.id
        )
        db.session.add(invoice)
        db.session.flush()
        invoices.append(invoice)
    
    print(f"  ✅ {len(invoices)} facturas Q2 creadas")
    db.session.commit()
    return quotes, invoices


def populate_sales_data_q3(employees, branches, cities, items):
    """Poblar datos de ventas Q3 (Julio-Septiembre)"""
    print("\n💰 Creando datos de ventas Q3 (Julio-Septiembre)...")
    
    emp_map = {1: employees[0], 4: employees[3], 5: employees[4],
               6: employees[5], 7: employees[6], 8: employees[7], 
               10: employees[9] if len(employees) > 9 else employees[0]}
    
    # QUOTES Q3
    quotes_q3 = [
        (date(2025, 7, 5), 10400000, emp_map[8], branches[3], cities['Cali']),
        (date(2025, 7, 18), 16900000, emp_map[10], branches[4], cities['Barranquilla']),
        (date(2025, 8, 8), 21600000, emp_map[1], branches[0], cities['Bogotá']),
        (date(2025, 8, 22), 13750000, emp_map[6], branches[2], cities['Medellín']),
        (date(2025, 9, 9), 7200000, emp_map[5], branches[1], cities['Floridablanca']),
        (date(2025, 9, 14), 19300000, emp_map[7], branches[2], cities['Medellín'])
    ]
    
    quotes = []
    for quote_date, total, employee, branch, city in quotes_q3:
        quote = Quote(
            customer_name=f"Cliente-Q3-{len(quotes)+1}",
            date=quote_date,
            total=total,
            employee_id=employee.id
        )
        db.session.add(quote)
        db.session.flush()
        quotes.append(quote)
    
    print(f"  ✅ {len(quotes)} cotizaciones Q3 creadas")
    
    # INVOICES Q3
    invoices_q3_data = [
        (date(2025, 7, 21), 16900000, emp_map[10]),
        (date(2025, 7, 8), 10400000, emp_map[8]),
        (date(2025, 8, 11), 21600000, emp_map[1]),
        (date(2025, 9, 17), 19300000, emp_map[7]),
        (date(2025, 8, 25), 9150000, emp_map[6]),
        (date(2025, 9, 20), 6440000, emp_map[5])
    ]
    
    invoices = []
    for inv_date, total, employee in invoices_q3_data:
        so = SalesOrder(
            quote_id=quotes[len(invoices)].id if len(invoices) < len(quotes) else quotes[0].id,
            date=inv_date,
            total=total,
            employee_id=employee.id
        )
        db.session.add(so)
        db.session.flush()
        
        invoice = Invoice(
            sales_order_id=so.id,
            date=inv_date,
            total=total,
            employee_id=employee.id
        )
        db.session.add(invoice)
        db.session.flush()
        invoices.append(invoice)
    
    print(f"  ✅ {len(invoices)} facturas Q3 creadas")
    db.session.commit()
    return quotes, invoices


def populate_sales_goals(employees, branches):
    """Crear metas de ventas"""
    print("\n🎯 Creando Metas de Ventas...")
    
    # Metas mensuales para vendedores top (primeros 5)
    for i, employee in enumerate(employees[:5]):
        goal = SalesGoal(
            employee_id=employee.id,
            period_type='monthly',
            start_date=date(2025, 10, 1),
            end_date=date(2025, 10, 31),
            target_amount=15000000 + (i * 5000000),  # Metas escalonadas
            created_by_user_id=1
        )
        db.session.add(goal)
        print(f"  ✅ Meta mensual empleado {employee.id}: ${ goal.target_amount:,.0f}")
    
    # Meta trimestral para cada sucursal
    for i, branch in enumerate(branches[:3]):
        goal = SalesGoal(
            branch_id=branch.id,
            period_type='quarterly',
            start_date=date(2025, 10, 1),
            end_date=date(2025, 12, 31),
            target_amount=80000000 + (i * 20000000),
            created_by_user_id=1
        )
        db.session.add(goal)
        print(f"  ✅ Meta trimestral sucursal {branch.id}: ${goal.target_amount:,.0f}")
    
    db.session.commit()


def main():
    """Función principal"""
    print("=" * 70)
    print("POBLACIÓN DE BASE DE DATOS - MULTICONT")
    print("Dataset completo: Abril-Septiembre 2025")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        try:
            # 1. Limpiar
            clear_database()
            
            # 2. Catálogos base
            states, cities = populate_states_cities()
            orgs, branches = populate_organizations_branches(cities)
            
            # 3. Personas y empleados
            persons, employees = populate_persons_employees(cities, branches)
            
            # 4. Usuarios y roles
            users, roles = populate_users_roles(persons, employees)
            
            # 5. Marcas e inventario
            brands = populate_brands()
            items = populate_inventory(brands)
            
            # 6. Datos de ventas Q2
            quotes_q2, invoices_q2 = populate_sales_data_q2(
                employees, orgs, branches, cities, items
            )
            
            # 7. Datos de ventas Q3
            quotes_q3, invoices_q3 = populate_sales_data_q3(
                employees, branches, cities, items
            )
            
            # 8. Metas de ventas
            populate_sales_goals(employees, branches)
            
            print("\n" + "=" * 70)
            print("✅ BASE DE DATOS POBLADA EXITOSAMENTE")
            print("=" * 70)
            print(f"\n📊 Resumen:")
            print(f"  - Estados: {len(states)}")
            print(f"  - Ciudades: {len(cities)}")
            print(f"  - Organizaciones: {len(orgs)}")
            print(f"  - Sucursales: {len(branches)}")
            print(f"  - Personas: {len(persons)}")
            print(f"  - Empleados: {len(employees)}")
            print(f"  - Usuarios: {len(users)}")
            print(f"  - Marcas: {len(brands)}")
            print(f"  - Items inventario: {len(items)}")
            print(f"  - Cotizaciones: {len(quotes_q2) + len(quotes_q3)}")
            print(f"  - Facturas: {len(invoices_q2) + len(invoices_q3)}")
            print(f"\n🎯 Ahora puedes probar los endpoints de analytics:")
            print(f"  GET /api/analytics/invoicing/by_employee?start_date=2025-04-01&end_date=2025-09-30")
            print(f"  GET /api/analytics/goals/vs_actual?period_type=monthly")
            print(f"  GET /api/analytics/sales/summary?start_date=2025-04-01&end_date=2025-09-30")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            sys.exit(1)


if __name__ == "__main__":
    main()
