"""
Script para poblar la base de datos con datos realistas
Adaptado a la estructura ACTUAL de los modelos del proyecto

Fecha: 20 de Octubre de 2025
Versión: 2.0.0 - Adaptado a modelos actuales
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
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
from datetime import date, datetime
from decimal import Decimal
import random

def clear_database():
    """Limpia todas las tablas en orden correcto (respetando FKs)"""
    print("🗑️  Limpiando base de datos...")
    
    # Orden correcto: de más dependiente a menos dependiente
    db.session.query(UserRole).delete()
    db.session.query(Permission).delete()
    db.session.query(Assignment).delete()
    db.session.query(InvoiceItem).delete()
    db.session.query(Invoice).delete()
    db.session.query(SalesOrderItem).delete()
    db.session.query(SalesOrder).delete()
    db.session.query(QuoteItem).delete()
    db.session.query(QuotationLine).delete()
    db.session.query(Quote).delete()
    db.session.query(ItemCategory).delete()
    db.session.query(InventoryItem).delete()
    db.session.query(User).delete()
    db.session.query(Employee).delete()
    db.session.query(Person).delete()
    db.session.query(Branch).delete()
    db.session.query(Organization).delete()
    db.session.query(City).delete()
    db.session.query(State).delete()
    db.session.query(Role).delete()
    
    db.session.commit()
    print("✅ Base de datos limpiada")

def populate_states_cities():
    """Poblar estados y ciudades de Colombia"""
    print("\n📍 Poblando estados y ciudades...")
    
    states_data = [
        ('Cundinamarca', 'CUN'),
        ('Santander', 'SAN'),
        ('Antioquia', 'ANT'),
        ('Valle del Cauca', 'VAC'),
        ('Atlántico', 'ATL')
    ]
    
    states = []
    for desc, code in states_data:
        state = State(description=desc, code=code)
        db.session.add(state)
        states.append((desc, state))
    
    db.session.flush()
    
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
    
    states_dict = {name: state for name, state in states}
    cities = []
    for desc, code, state_name in cities_data:
        state = states_dict[state_name]
        city = City(description=desc, code=code, state_id=state.id)
        db.session.add(city)
        cities.append(city)
    
    db.session.commit()
    print(f"✅ {len(states)} estados y {len(cities)} ciudades creadas")
    return cities

def populate_organizations_branches(cities):
    """Poblar organizaciones y sucursales"""
    print("\n🏢 Poblando organizaciones y sucursales...")
    
    orgs_data = [
        ('multiCont', 'multiCont'),
        ('Automatiza Andina SAS', 'Automatiza Andina SAS'),
        ('ControlTech SAS', 'ControlTech SAS'),
        ('Industrias del Norte SA', 'Industrias del Norte SA'),
        ('Vallepack LTDA', 'Vallepack LTDA'),
        ('Caribe Foods SA', 'Caribe Foods SA'),
        ('Metalúrgica Antioquia SAS', 'Metalúrgica Antioquia SAS')
    ]
    
    orgs = []
    for hist, curr in orgs_data:
        org = Organization(historical_name=hist, current_name=curr)
        db.session.add(org)
        orgs.append(org)
    
    db.session.flush()
    
    # Sucursales de multiCont (org 1) en 5 ciudades principales
    branches = []
    branch_cities = [0, 4, 8, 12, 16]  # Bogotá, Bucaramanga, Medellín, Cali, Barranquilla
    for city_idx in branch_cities:
        branch = Branch(organization_id=orgs[0].id, city_id=cities[city_idx].id)
        db.session.add(branch)
        branches.append(branch)
    
    db.session.commit()
    print(f"✅ {len(orgs)} organizaciones y {len(branches)} sucursales creadas")
    return orgs, branches

def populate_people_employees(cities, branches):
    """Poblar personas y empleados - SIN campo status (no existe en modelo actual)"""
    print("\n👥 Poblando personas y empleados...")
    
    people_data = [
        ('CC3001', 'Ana', 'García', 'Cra 10 #1-23', '300200001', 0, 0),
        ('CC3002', 'Bruno', 'Pineda', 'Cll 12 #3-45', '300200002', 4, 0),
        ('CC3003', 'Carla', 'Mora', 'Cll 8 #9-10', '300200003', 8, 0),
        ('CC3004', 'Diego', 'Luna', 'Cra 45 #12-34', '300200004', 12, 1),
        ('CC3005', 'Elena', 'Suárez', 'Av 7 #98-11', '300200005', 16, 1),
        ('CC3006', 'Felipe', 'Cruz', 'Mz 4 Cs 5', '300200006', 1, 2),
        ('CC3007', 'Gloria', 'Vega', 'Cra 70 #20-30', '300200007', 5, 2),
        ('CC3008', 'Hugo', 'Ríos', 'Cll 25 #4-55', '300200008', 9, 3),
        ('CC3009', 'Irene', 'Quintero', 'Cll 30 #6-77', '300200009', 13, 3),
        ('CC3010', 'Jorge', 'Nieto', 'Cra 15 #5-22', '300200010', 17, 4),
        ('CC3011', 'Karen', 'Ortiz', 'Cll 72 #15-33', '300200011', 2, 0),
        ('CC3012', 'Luis', 'Pardo', 'Cra 8 #14-50', '300200012', 6, 1),
        ('CC3013', 'Marta', 'Rey', 'Cll 40 #9-21', '300200013', 10, 2),
        ('CC3014', 'Nicolás', 'Soto', 'Av 13 #45-60', '300200014', 14, 3),
        ('CC3015', 'Olga', 'Torres', 'Cra 9 #20-20', '300200015', 18, 4),
        ('CC3016', 'Pablo', 'Uribe', 'Cll 12 #23-12', '300200016', 3, 0),
        ('CC3017', 'Raquel', 'Valencia', 'Cra 22 #33-44', '300200017', 7, 1),
        ('CC3018', 'Sergio', 'Weber', 'Cll 9 #10-11', '300200018', 11, 2),
        ('CC3019', 'Tatiana', 'Ximénez', 'Cll 1 #1-1', '300200019', 15, 3),
        ('CC3020', 'Ulises', 'Zárate', 'Cra 100 #50-60', '300200020', 19, 4)
    ]
    
    people = []
    employees = []
    for dni, first, last, addr, phone, city_idx, branch_idx in people_data:
        person = Person(
            dni=dni,
            first_name=first,
            last_name=last,
            address=addr,
            phone=phone,
            city_id=cities[city_idx].id
        )
        db.session.add(person)
        people.append(person)
    
    db.session.flush()
    
    # Crear empleados con branch_id (requerido en modelo actual)
    for i, (_, _, _, _, _, _, branch_idx) in enumerate(people_data):
        employee = Employee(
            person_id=people[i].id,
            branch_id=branches[branch_idx].id
        )
        db.session.add(employee)
        employees.append(employee)
    
    db.session.commit()
    print(f"✅ {len(people)} personas y {len(employees)} empleados creados")
    return people, employees

def populate_users_roles_permissions(people):
    """Poblar usuarios, roles y permisos con bcrypt"""
    print("\n🔐 Poblando usuarios, roles y permisos...")
    
    # Roles
    roles_data = ['ADMIN', 'MANAGER', 'SALES', 'VIEWER']
    roles = {}
    for role_name in roles_data:
        role = Role(name=role_name)  # Modelo actual: name, no description
        db.session.add(role)
        roles[role_name] = role
    
    db.session.flush()
    
    # Usuarios (primeros 10 personas) - Modelo actual tiene username, no login
    users_data = [
        ('ana', 'password123', 0, 'SALES'),
        ('bruno', 'password123', 1, 'SALES'),
        ('carla', 'password123', 2, 'SALES'),
        ('diego', 'password123', 3, 'SALES'),
        ('elena', 'password123', 4, 'SALES'),
        ('felipe', 'password123', 5, 'MANAGER'),
        ('gloria', 'password123', 6, 'MANAGER'),
        ('hugo', 'password123', 7, 'ADMIN'),
        ('irene', 'password123', 8, 'VIEWER'),
        ('jorge', 'password123', 9, 'VIEWER')
    ]
    
    users = {}
    for username, pwd, person_idx, role_name in users_data:
        user = User(
            username=username,
            password=hash_password(pwd),
            role_id=roles[role_name].id
        )
        db.session.add(user)
        users[username] = user
    
    db.session.flush()
    
    # Permisos - Modelo actual: name (sin role_id)
    permissions_data = [
        'READ_REPORTS',
        'WRITE_QUOTES',
        'APPROVE_ORDERS',
        'ADMIN_ALL',
        'VIEW_ONLY'
    ]
    
    for perm_name in permissions_data:
        permission = Permission(name=perm_name)  # Modelo actual: solo name
        db.session.add(permission)
    
    # User-Role assignments
    for username, _, _, role_name in users_data:
        user_role = UserRole(user_id=users[username].id, role_id=roles[role_name].id)
        db.session.add(user_role)
    
    db.session.commit()
    print(f"✅ {len(users)} usuarios, {len(roles)} roles y permisos creados")
    return users, roles

def populate_inventory():
    """Poblar inventario con 60 items (6 marcas × 10) - CON precio y cantidad"""
    print("\n📦 Poblando inventario...")
    
    # 60 items de inventario con precios realistas
    items_data = [
        # Omron (10) - Precios en COP
        ('OMR-PLC-NX1P2', 'Controlador PLC Omron NX1P2', 'Omron', 4500000, 5),
        ('OMR-SEN-E3Z', 'Sensor fotoeléctrico Omron E3Z', 'Omron', 180000, 50),
        ('OMR-INV-A1000', 'Variador Omron A1000', 'Omron', 6000000, 3),
        ('OMR-HMI-NA5', 'HMI Omron NA5 7"', 'Omron', 2200000, 8),
        ('OMR-IO-NX', 'Módulo I/O Omron NX', 'Omron', 850000, 12),
        ('OMR-ENC-E6B2', 'Encoder Omron E6B2', 'Omron', 420000, 20),
        ('OMR-REL-G2R', 'Relé electromecánico Omron G2R', 'Omron', 35000, 100),
        ('OMR-SSR-G3NA', 'Relé de estado sólido Omron G3NA', 'Omron', 180000, 30),
        ('OMR-PSU-S8VK', 'Fuente 24V Omron S8VK', 'Omron', 320000, 15),
        ('OMR-SAF-F3SG', 'Cortina de seguridad Omron F3SG', 'Omron', 5500000, 2),
        # ING Multicontrol (10)
        ('ING-ARR-START', 'Arrancador suave ING Multicontrol', 'ING Multicontrol', 2750000, 6),
        ('ING-CON-24V', 'Fuente de poder 24V ING Multicontrol', 'ING Multicontrol', 380000, 25),
        ('ING-PLC-MC200', 'PLC ING Multicontrol MC200', 'ING Multicontrol', 3800000, 4),
        ('ING-HMI-MC7', 'HMI 7" ING Multicontrol', 'ING Multicontrol', 1850000, 7),
        ('ING-VFD-MC500', 'Variador ING Multicontrol MC500', 'ING Multicontrol', 4200000, 5),
        ('ING-IO-MOD8', 'Módulo I/O 8ch ING Multicontrol', 'ING Multicontrol', 650000, 18),
        ('ING-REL-SAF', 'Relé de seguridad ING Multicontrol', 'ING Multicontrol', 380000, 22),
        ('ING-SWI-ETH5', 'Switch Ethernet 5p ING Multicontrol', 'ING Multicontrol', 520000, 10),
        ('ING-ENC-INC', 'Encoder incremental ING Multicontrol', 'ING Multicontrol', 450000, 15),
        ('ING-PSU-48V', 'Fuente 48V ING Multicontrol', 'ING Multicontrol', 580000, 12),
        # Gefran (10)
        ('GEF-TEMP-600', 'Controlador de temperatura Gefran 600', 'Gefran', 1350000, 10),
        ('GEF-INV-ADV', 'Inversor de frecuencia Gefran ADV', 'Gefran', 6500000, 3),
        ('GEF-TRANS-LIN', 'Transductor lineal Gefran', 'Gefran', 2100000, 8),
        ('GEF-SSR-GQ', 'Relé de estado sólido Gefran GQ', 'Gefran', 420000, 20),
        ('GEF-DRIVE-AX', 'Servo drive Gefran AX', 'Gefran', 7800000, 2),
        ('GEF-PRES-TRX', 'Transductor de presión Gefran', 'Gefran', 1200000, 12),
        ('GEF-AMP-LC', 'Amplificador para celda de carga Gefran', 'Gefran', 980000, 9),
        ('GEF-HMI-5', 'HMI 5" Gefran', 'Gefran', 1650000, 6),
        ('GEF-RTD-PT100', 'Sonda RTD PT100 Gefran', 'Gefran', 280000, 40),
        ('GEF-PSU-24', 'Fuente 24V Gefran', 'Gefran', 350000, 18),
        # Weidmüller (10)
        ('WEI-BOR-TER', 'Bornera Weidmüller Terminal', 'Weidmüller', 50000, 200),
        ('WEI-SSR-IO', 'Módulo IO Weidmüller SSR', 'Weidmüller', 250000, 30),
        ('WEI-PSU-24', 'Fuente 24V Weidmüller', 'Weidmüller', 400000, 20),
        ('WEI-REL-TER', 'Relé interfaz Weidmüller', 'Weidmüller', 85000, 60),
        ('WEI-RAIL-DIN', 'Riel DIN Weidmüller', 'Weidmüller', 25000, 150),
        ('WEI-SW-IND8', 'Switch industrial 8p Weidmüller', 'Weidmüller', 1200000, 8),
        ('WEI-SURGE-SPD', 'Protección contra sobretensión Weidmüller SPD', 'Weidmüller', 320000, 25),
        ('WEI-CON-PUSHIN', 'Conector Push-In Weidmüller', 'Weidmüller', 15000, 300),
        ('WEI-MARKZ-CARD', 'Tarjetas marcadoras Weidmüller', 'Weidmüller', 45000, 100),
        ('WEI-TOOL-CRIMP', 'Herramienta crimpadora Weidmüller', 'Weidmüller', 850000, 5),
        # Rice-Lake (10)
        ('RCL-BAL-IND', 'Indicador de pesaje Rice-Lake', 'Rice-Lake', 4000000, 4),
        ('RCL-CEL-CARGA', 'Celda de carga Rice-Lake', 'Rice-Lake', 1800000, 10),
        ('RCL-PES-PLC', 'Módulo de pesaje para PLC Rice-Lake', 'Rice-Lake', 3800000, 5),
        ('RCL-JBOX-4', 'Caja de conexiones 4 celdas Rice-Lake', 'Rice-Lake', 650000, 12),
        ('RCL-SCALE-PLT', 'Báscula de plataforma Rice-Lake', 'Rice-Lake', 12000000, 2),
        ('RCL-TRX-ANALOG', 'Transmisor analógico Rice-Lake', 'Rice-Lake', 950000, 8),
        ('RCL-WEIGH-MOD', 'Módulo de pesaje Rice-Lake', 'Rice-Lake', 2200000, 6),
        ('RCL-CHECK-CKW', 'Checkweigher Rice-Lake', 'Rice-Lake', 15000000, 1),
        ('RCL-PRN-TT', 'Impresora térmica Rice-Lake', 'Rice-Lake', 2500000, 3),
        ('RCL-SW-LIC', 'Licencia software pesaje Rice-Lake', 'Rice-Lake', 3200000, 10),
        # Optec (10)
        ('OPT-SEN-IND', 'Sensor inductivo Optec', 'Optec', 220000, 45),
        ('OPT-BARR-SEG', 'Barrera de seguridad Optec', 'Optec', 900000, 8),
        ('OPT-HMI-7', 'Panel HMI 7" Optec', 'Optec', 1200000, 10),
        ('OPT-PE-SENS', 'Sensor fotoeléctrico Optec', 'Optec', 195000, 50),
        ('OPT-PROX-M18', 'Sensor de proximidad M18 Optec', 'Optec', 180000, 55),
        ('OPT-IO-LINK', 'Módulo IO-Link Master Optec', 'Optec', 850000, 12),
        ('OPT-CAB-M12', 'Cable M12 Optec', 'Optec', 35000, 200),
        ('OPT-BRK-ANG', 'Soporte/bracket angular Optec', 'Optec', 15000, 150),
        ('OPT-PB-LED', 'Pulsador iluminado Optec', 'Optec', 85000, 80),
        ('OPT-TWR-LIGHT', 'Torre luminosa Optec', 'Optec', 280000, 25)
    ]
    
    items_dict = {}
    for code, desc, brand, price, qty in items_data:
        # Modelo actual: name (no product_description), price, quantity
        item = InventoryItem(
            name=desc,
            code=code,
            price=Decimal(str(price)),
            quantity=qty
        )
        db.session.add(item)
        items_dict[code] = item
    
    db.session.flush()
    
    # Categorías (brand)
    for code, _, brand, _, _ in items_data:
        category = ItemCategory(item_code=code, category_type='brand', category_value=brand)
        db.session.add(category)
    
    db.session.commit()
    print(f"✅ {len(items_data)} items de inventario creados")
    return items_dict

def populate_quotes_orders_invoices_q2(employees, items_dict):
    """Poblar cotizaciones, órdenes y facturas Q2 (ABR-JUN 2025)"""
    print("\n💰 Poblando transacciones Q2 (ABR-JUN)...")
    
    # Quotes Q2 - Modelo actual: customer_name, date, total, employee_id
    quotes_data = [
        ('Automatiza Andina SAS', '2025-04-08', 12800000, 0),  # emp1 (Ana)
        ('ControlTech SAS', '2025-04-15', 18300000, 3),         # emp4 (Diego)
        ('Industrias del Norte SA', '2025-05-03', 15700000, 5), # emp6 (Felipe)
        ('Vallepack LTDA', '2025-05-19', 6900000, 7),           # emp8 (Hugo)
        ('Caribe Foods SA', '2025-06-06', 22450000, 9),         # emp10 (Jorge)
        ('Metalúrgica Antioquia SAS', '2025-06-21', 9950000, 1) # emp2 (Bruno)
    ]
    
    quotes = []
    for customer, date_str, total, emp_idx in quotes_data:
        quote = Quote(
            customer_name=customer,
            date=date.fromisoformat(date_str),
            total=Decimal(str(total)),
            employee_id=employees[emp_idx].id
        )
        db.session.add(quote)
        quotes.append(quote)
    
    db.session.flush()
    
    # Quote items - Modelo actual: quote_id, item_id (no item_code), quantity, price
    quote_items_data = [
        (0, 'OMR-SEN-E3Z', 10, 180000), (0, 'WEI-PSU-24', 5, 400000), (0, 'OPT-SEN-IND', 5, 220000),
        (1, 'OMR-PLC-NX1P2', 2, 4500000), (1, 'GEF-TEMP-600', 3, 1350000),
        (2, 'ING-PLC-MC200', 1, 3800000), (2, 'GEF-INV-ADV', 1, 6500000), (2, 'RCL-BAL-IND', 1, 4000000),
        (3, 'OMR-INV-A1000', 1, 6000000), (3, 'OPT-BARR-SEG', 1, 900000),
        (4, 'RCL-CEL-CARGA', 3, 1800000), (4, 'WEI-SSR-IO', 10, 250000), (4, 'OMR-SEN-E3Z', 10, 180000),
        (5, 'GEF-TRANS-LIN', 2, 2100000), (5, 'ING-CON-24V', 5, 380000)
    ]
    
    for quote_idx, item_code, qty, price in quote_items_data:
        item = items_dict[item_code]
        quote_item = QuoteItem(
            quote_id=quotes[quote_idx].id,
            item_id=item.id,  # Modelo actual usa item_id, no item_code
            quantity=qty,
            price=Decimal(str(price))
        )
        db.session.add(quote_item)
    
    db.session.commit()
    
    # Sales Orders Q2 - Modelo actual: quote_id, date, total, employee_id
    orders_data = [
        (1, '2025-04-20', 18300000, 3),  # Quote 2
        (4, '2025-06-08', 22450000, 9)   # Quote 5
    ]
    
    orders = []
    for quote_idx, date_str, total, emp_idx in orders_data:
        order = SalesOrder(
            quote_id=quotes[quote_idx].id,
            date=date.fromisoformat(date_str),
            total=Decimal(str(total)),
            employee_id=employees[emp_idx].id
        )
        db.session.add(order)
        orders.append(order)
    
    db.session.flush()
    
    # Sales Order Items
    order_items_data = [
        (0, 'OMR-PLC-NX1P2', 2, 4500000), (0, 'GEF-TEMP-600', 3, 1350000),
        (1, 'RCL-CEL-CARGA', 3, 1800000), (1, 'WEI-SSR-IO', 10, 250000), (1, 'OMR-SEN-E3Z', 10, 180000)
    ]
    
    for order_idx, item_code, qty, price in order_items_data:
        item = items_dict[item_code]
        order_item = SalesOrderItem(
            sales_order_id=orders[order_idx].id,
            item_id=item.id,
            quantity=qty,
            price=Decimal(str(price))
        )
        db.session.add(order_item)
    
    db.session.commit()
    
    # Invoices Q2 - Modelo actual: sales_order_id, date, total, employee_id
    invoices_data = [
        (0, '2025-04-21', 18300000, 3),  # Order 1
        (1, '2025-06-10', 22450000, 9),  # Order 2
        # Facturas sin orden (directas)
        (None, '2025-04-30', 8600000, 0),   # Ana
        (None, '2025-06-25', 6900000, 1)    # Bruno
    ]
    
    invoices = []
    for order_idx, date_str, total, emp_idx in invoices_data:
        invoice = Invoice(
            sales_order_id=orders[order_idx].id if order_idx is not None else orders[0].id,  # Modelo requiere sales_order_id
            date=date.fromisoformat(date_str),
            total=Decimal(str(total)),
            employee_id=employees[emp_idx].id
        )
        db.session.add(invoice)
        invoices.append(invoice)
    
    db.session.flush()
    
    # Invoice Items
    invoice_items_data = [
        (0, 'OMR-PLC-NX1P2', 2, 4500000), (0, 'GEF-TEMP-600', 3, 1350000),
        (1, 'RCL-CEL-CARGA', 3, 1800000), (1, 'WEI-SSR-IO', 10, 250000), (1, 'OMR-SEN-E3Z', 10, 180000),
        (2, 'WEI-PSU-24', 5, 400000), (2, 'OPT-SEN-IND', 5, 220000), (2, 'OMR-SEN-E3Z', 10, 180000),
        (3, 'GEF-TRANS-LIN', 2, 2100000), (3, 'ING-CON-24V', 5, 380000)
    ]
    
    for inv_idx, item_code, qty, price in invoice_items_data:
        item = items_dict[item_code]
        invoice_item = InvoiceItem(
            invoice_id=invoices[inv_idx].id,
            item_id=item.id,
            quantity=qty,
            price=Decimal(str(price))
        )
        db.session.add(invoice_item)
    
    db.session.commit()
    print(f"✅ Q2: {len(quotes)} cotizaciones, {len(orders)} órdenes, {len(invoices)} facturas")
    return quotes, orders, invoices

def populate_quotes_orders_invoices_q3(employees, items_dict):
    """Poblar cotizaciones, órdenes y facturas Q3 (JUL-SEP 2025)"""
    print("\n💰 Poblando transacciones Q3 (JUL-SEP)...")
    
    # Quotes Q3
    quotes_data = [
        ('Vallepack LTDA', '2025-07-05', 10400000, 7),          # emp8
        ('Caribe Foods SA', '2025-07-18', 16900000, 9),         # emp10
        ('Automatiza Andina SAS', '2025-08-08', 21600000, 0),   # emp1
        ('Metalúrgica Antioquia SAS', '2025-08-22', 13750000, 5), # emp6
        ('ControlTech SAS', '2025-09-09', 7200000, 4),          # emp5
        ('Industrias del Norte SA', '2025-09-14', 19300000, 6)  # emp7
    ]
    
    quotes = []
    for customer, date_str, total, emp_idx in quotes_data:
        quote = Quote(
            customer_name=customer,
            date=date.fromisoformat(date_str),
            total=Decimal(str(total)),
            employee_id=employees[emp_idx].id
        )
        db.session.add(quote)
        quotes.append(quote)
    
    db.session.flush()
    
    # Quote items Q3
    quote_items_data = [
        (0, 'WEI-BOR-TER', 80, 50000), (0, 'OMR-SEN-E3Z', 8, 180000),
        (1, 'RCL-PES-PLC', 1, 3800000), (1, 'OMR-INV-A1000', 1, 6000000), (1, 'OPT-HMI-7', 1, 1200000),
        (2, 'OMR-PLC-NX1P2', 3, 4500000), (2, 'ING-CON-24V', 3, 380000),
        (3, 'ING-ARR-START', 2, 2750000), (3, 'WEI-PSU-24', 5, 400000),
        (4, 'WEI-SSR-IO', 8, 250000), (4, 'OMR-SEN-E3Z', 8, 180000),
        (5, 'GEF-INV-ADV', 1, 6500000), (5, 'GEF-TEMP-600', 2, 1350000), (5, 'RCL-BAL-IND', 1, 4000000)
    ]
    
    for quote_idx, item_code, qty, price in quote_items_data:
        item = items_dict[item_code]
        quote_item = QuoteItem(
            quote_id=quotes[quote_idx].id,
            item_id=item.id,
            quantity=qty,
            price=Decimal(str(price))
        )
        db.session.add(quote_item)
    
    db.session.commit()
    
    # Sales Orders Q3
    orders_data = [
        (1, '2025-07-20', 16900000, 9),  # Quote 2 (idx 1)
        (0, '2025-07-07', 10400000, 7),  # Quote 1 (idx 0)
        (2, '2025-08-10', 21600000, 0),  # Quote 3 (idx 2)
        (5, '2025-09-16', 19300000, 6)   # Quote 6 (idx 5)
    ]
    
    orders = []
    for quote_idx, date_str, total, emp_idx in orders_data:
        order = SalesOrder(
            quote_id=quotes[quote_idx].id,
            date=date.fromisoformat(date_str),
            total=Decimal(str(total)),
            employee_id=employees[emp_idx].id
        )
        db.session.add(order)
        orders.append(order)
    
    db.session.flush()
    
    # Sales Order Items Q3
    order_items_data = [
        (0, 'RCL-PES-PLC', 1, 3800000), (0, 'OMR-INV-A1000', 1, 6000000), (0, 'OPT-HMI-7', 1, 1200000),
        (1, 'WEI-BOR-TER', 80, 50000), (1, 'OMR-SEN-E3Z', 8, 180000),
        (2, 'OMR-PLC-NX1P2', 3, 4500000), (2, 'ING-CON-24V', 3, 380000),
        (3, 'GEF-INV-ADV', 1, 6500000), (3, 'GEF-TEMP-600', 2, 1350000), (3, 'RCL-BAL-IND', 1, 4000000)
    ]
    
    for order_idx, item_code, qty, price in order_items_data:
        item = items_dict[item_code]
        order_item = SalesOrderItem(
            sales_order_id=orders[order_idx].id,
            item_id=item.id,
            quantity=qty,
            price=Decimal(str(price))
        )
        db.session.add(order_item)
    
    db.session.commit()
    
    # Invoices Q3
    invoices_data = [
        (0, '2025-07-21', 16900000, 9),  # Order 1
        (1, '2025-07-08', 10400000, 7),  # Order 2
        (2, '2025-08-11', 21600000, 0),  # Order 3
        (3, '2025-09-17', 19300000, 6),  # Order 4
        # Facturas sin orden (directas)
        (0, '2025-08-25', 9150000, 5),
        (0, '2025-09-20', 6440000, 4)
    ]
    
    invoices = []
    for order_idx, date_str, total, emp_idx in invoices_data:
        invoice = Invoice(
            sales_order_id=orders[order_idx].id,
            date=date.fromisoformat(date_str),
            total=Decimal(str(total)),
            employee_id=employees[emp_idx].id
        )
        db.session.add(invoice)
        invoices.append(invoice)
    
    db.session.flush()
    
    # Invoice Items Q3
    invoice_items_data = [
        (0, 'RCL-PES-PLC', 1, 3800000), (0, 'OMR-INV-A1000', 1, 6000000), (0, 'OPT-HMI-7', 1, 1200000),
        (1, 'WEI-BOR-TER', 80, 50000), (1, 'OMR-SEN-E3Z', 8, 180000),
        (2, 'OMR-PLC-NX1P2', 3, 4500000), (2, 'ING-CON-24V', 3, 380000),
        (3, 'GEF-INV-ADV', 1, 6500000), (3, 'GEF-TEMP-600', 2, 1350000), (3, 'RCL-BAL-IND', 1, 4000000),
        (4, 'ING-ARR-START', 2, 2750000), (4, 'WEI-PSU-24', 5, 400000), (4, 'OMR-SEN-E3Z', 5, 180000),
        (5, 'WEI-SSR-IO', 8, 250000), (5, 'OMR-SEN-E3Z', 8, 180000)
    ]
    
    for inv_idx, item_code, qty, price in invoice_items_data:
        item = items_dict[item_code]
        invoice_item = InvoiceItem(
            invoice_id=invoices[inv_idx].id,
            item_id=item.id,
            quantity=qty,
            price=Decimal(str(price))
        )
        db.session.add(invoice_item)
    
    db.session.commit()
    print(f"✅ Q3: {len(quotes)} cotizaciones, {len(orders)} órdenes, {len(invoices)} facturas")
    return quotes, orders, invoices

def populate_assignments(employees, items_dict):
    """Poblar asignaciones de items a empleados"""
    print("\n📌 Poblando asignaciones...")
    
    # Asignar algunos items a empleados (modelo actual: employee_id, item_id, assigned_date, status)
    assignments_data = [
        (0, 'OMR-PLC-NX1P2', '2025-04-01', 'active'),
        (0, 'OMR-HMI-NA5', '2025-04-01', 'active'),
        (3, 'ING-PLC-MC200', '2025-05-01', 'active'),
        (5, 'GEF-TEMP-600', '2025-06-01', 'active'),
        (7, 'RCL-BAL-IND', '2025-07-01', 'active'),
        (9, 'OPT-HMI-7', '2025-08-01', 'active')
    ]
    
    for emp_idx, item_code, date_str, status in assignments_data:
        item = items_dict[item_code]
        assignment = Assignment(
            employee_id=employees[emp_idx].id,
            item_id=item.id,
            assigned_date=date.fromisoformat(date_str),
            status=status
        )
        db.session.add(assignment)
    
    db.session.commit()
    print(f"✅ {len(assignments_data)} asignaciones creadas")

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("  POBLANDO BASE DE DATOS - DATASET COMPLETO 2025")
    print("  Adaptado a estructura ACTUAL de modelos del proyecto")
    print("="*70 + "\n")
    
    app = create_app()
    with app.app_context():
        try:
            # 1. Limpiar BD
            clear_database()
            
            # 2. Catálogos base
            cities = populate_states_cities()
            orgs, branches = populate_organizations_branches(cities)
            people, employees = populate_people_employees(cities, branches)
            users, roles = populate_users_roles_permissions(people)
            items_dict = populate_inventory()
            
            # 3. Q2 (ABR-JUN)
            quotes_q2, orders_q2, invoices_q2 = populate_quotes_orders_invoices_q2(employees, items_dict)
            
            # 4. Q3 (JUL-SEP)
            quotes_q3, orders_q3, invoices_q3 = populate_quotes_orders_invoices_q3(employees, items_dict)
            
            # 5. Asignaciones
            populate_assignments(employees, items_dict)
            
            print("\n" + "="*70)
            print("  ✅ BASE DE DATOS POBLADA EXITOSAMENTE")
            print("="*70 + "\n")
            
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
            print(f"  • Items inventario: {InventoryItem.query.count()}")
            print(f"  • Cotizaciones: {Quote.query.count()}")
            print(f"  • Órdenes de venta: {SalesOrder.query.count()}")
            print(f"  • Facturas: {Invoice.query.count()}")
            print(f"  • Asignaciones: {Assignment.query.count()}")
            print()
            
            # Credenciales de usuarios
            print("🔐 CREDENCIALES DE USUARIOS:")
            print("  • ana / password123 (SALES)")
            print("  • bruno / password123 (SALES)")
            print("  • felipe / password123 (MANAGER)")
            print("  • hugo / password123 (ADMIN)")
            print()
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
