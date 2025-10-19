"""
Script de población completa de base de datos
Dataset: Abril-Septiembre 2025 (6 meses)
Basado en Clean Architecture con handlers
Llena TODOS los campos sin valores nulos
"""

from app import create_app, db
from app.use_cases.state_handler import StateHandler
from app.use_cases.city_handler import CityHandler
from app.use_cases.organization_handler import OrganizationHandler
from app.use_cases.branch_handler import BranchHandler
from app.use_cases.person_handler import PersonHandler
from app.use_cases.employee_handler import EmployeeHandler
from app.use_cases.user_handler import UserHandler
from app.use_cases.role_handler import RoleHandler
from app.use_cases.permission_handler import PermissionHandler
from app.use_cases.user_role_handler import UserRoleHandler
from app.use_cases.assignment_handler import AssignmentHandler
from app.use_cases.brand_handler import BrandHandler
from app.use_cases.inventory_item_handler import InventoryItemHandler
from app.use_cases.quote_handler import QuoteHandler
from app.use_cases.quote_item_handler import QuoteItemHandler
from app.use_cases.quotation_line_handler import QuotationLineHandler
from app.use_cases.sales_order_handler import SalesOrderHandler
from app.use_cases.sales_order_item_handler import SalesOrderItemHandler
from app.use_cases.invoice_handler import InvoiceHandler
from app.use_cases.invoice_item_handler import InvoiceItemHandler

from datetime import date, datetime
from decimal import Decimal

app = create_app()

# Instanciar handlers
state_handler = StateHandler()
city_handler = CityHandler()
org_handler = OrganizationHandler()
branch_handler = BranchHandler()
person_handler = PersonHandler()
employee_handler = EmployeeHandler()
user_handler = UserHandler()
role_handler = RoleHandler()
permission_handler = PermissionHandler()
user_role_handler = UserRoleHandler()
assignment_handler = AssignmentHandler()
brand_handler = BrandHandler()
inventory_handler = InventoryItemHandler()
quote_handler = QuoteHandler()
quote_item_handler = QuoteItemHandler()
quotation_line_handler = QuotationLineHandler()
sales_order_handler = SalesOrderHandler()
sales_order_item_handler = SalesOrderItemHandler()
invoice_handler = InvoiceHandler()
invoice_item_handler = InvoiceItemHandler()

def populate_database():
    with app.app_context():
        print("="*70)
        print("POBLACIÓN COMPLETA DE BASE DE DATOS")
        print("Dataset: Abril-Septiembre 2025")
        print("="*70)
        
        # ============================================================
        # 1. ESTADOS Y CIUDADES
        # ============================================================
        print("\n[1/15] Creando Estados y Ciudades...")
        states_data = [
            {'description': 'Cundinamarca', 'code': 'CUN'},
            {'description': 'Santander', 'code': 'SAN'},
            {'description': 'Antioquia', 'code': 'ANT'},
            {'description': 'Valle del Cauca', 'code': 'VAC'},
            {'description': 'Atlántico', 'code': 'ATL'}
        ]
        
        states = {}
        for state_data in states_data:
            state = state_handler.create(**state_data)
            states[state_data['code']] = state
            print(f"  ✓ Estado: {state.description}")
        
        cities_data = [
            # Cundinamarca
            {'description': 'Bogotá', 'code': 'BOG', 'state_id': states['CUN'].id},
            {'description': 'Soacha', 'code': 'SOA', 'state_id': states['CUN'].id},
            {'description': 'Chía', 'code': 'CHI', 'state_id': states['CUN'].id},
            {'description': 'Zipaquirá', 'code': 'ZIP', 'state_id': states['CUN'].id},
            # Santander
            {'description': 'Bucaramanga', 'code': 'BGA', 'state_id': states['SAN'].id},
            {'description': 'Floridablanca', 'code': 'FLA', 'state_id': states['SAN'].id},
            {'description': 'Girón', 'code': 'GIR', 'state_id': states['SAN'].id},
            {'description': 'Piedecuesta', 'code': 'PDC', 'state_id': states['SAN'].id},
            # Antioquia
            {'description': 'Medellín', 'code': 'MED', 'state_id': states['ANT'].id},
            {'description': 'Envigado', 'code': 'ENV', 'state_id': states['ANT'].id},
            {'description': 'Bello', 'code': 'BEL', 'state_id': states['ANT'].id},
            {'description': 'Itagüí', 'code': 'ITA', 'state_id': states['ANT'].id},
            # Valle del Cauca
            {'description': 'Cali', 'code': 'CLO', 'state_id': states['VAC'].id},
            {'description': 'Palmira', 'code': 'PAL', 'state_id': states['VAC'].id},
            {'description': 'Yumbo', 'code': 'YUM', 'state_id': states['VAC'].id},
            {'description': 'Buga', 'code': 'BUG', 'state_id': states['VAC'].id},
            # Atlántico
            {'description': 'Barranquilla', 'code': 'BAQ', 'state_id': states['ATL'].id},
            {'description': 'Soledad', 'code': 'SOL', 'state_id': states['ATL'].id},
            {'description': 'Malambo', 'code': 'MAL', 'state_id': states['ATL'].id},
            {'description': 'Puerto Colombia', 'code': 'PTC', 'state_id': states['ATL'].id}
        ]
        
        cities = {}
        for idx, city_data in enumerate(cities_data, 1):
            city = city_handler.create(**city_data)
            cities[city_data['code']] = city
            print(f"  ✓ Ciudad {idx}: {city.description}")
        
        # ============================================================
        # 2. ORGANIZACIONES Y SUCURSALES
        # ============================================================
        print("\n[2/15] Creando Organizaciones y Sucursales...")
        orgs_data = [
            {'historical_name': 'multiCont', 'current_name': 'multiCont'},
            {'historical_name': 'Automatiza Andina SAS', 'current_name': 'Automatiza Andina SAS'},
            {'historical_name': 'ControlTech SAS', 'current_name': 'ControlTech SAS'},
            {'historical_name': 'Industrias del Norte SA', 'current_name': 'Industrias del Norte SA'},
            {'historical_name': 'Vallepack LTDA', 'current_name': 'Vallepack LTDA'},
            {'historical_name': 'Caribe Foods SA', 'current_name': 'Caribe Foods SA'},
            {'historical_name': 'Metalúrgica Antioquia SAS', 'current_name': 'Metalúrgica Antioquia SAS'}
        ]
        
        orgs = []
        for org_data in orgs_data:
            org = org_handler.create(**org_data)
            orgs.append(org)
            print(f"  ✓ Organización {org.id}: {org.current_name}")
        
        # Sucursales de multiCont (id=1) en 5 ciudades principales
        branches_data = [
            {'organization_id': orgs[0].id, 'city_id': cities['BOG'].id},  # Bogotá
            {'organization_id': orgs[0].id, 'city_id': cities['BGA'].id},  # Bucaramanga
            {'organization_id': orgs[0].id, 'city_id': cities['MED'].id},  # Medellín
            {'organization_id': orgs[0].id, 'city_id': cities['CLO'].id},  # Cali
            {'organization_id': orgs[0].id, 'city_id': cities['BAQ'].id}   # Barranquilla
        ]
        
        branches = []
        for branch_data in branches_data:
            branch = branch_handler.create(**branch_data)
            branches.append(branch)
            city = city_handler.get(branch.city_id)
            print(f"  ✓ Sucursal {branch.id}: {city.description}")
        
        # ============================================================
        # 3. PERSONAS Y EMPLEADOS
        # ============================================================
        print("\n[3/15] Creando Personas y Empleados...")
        persons_data = [
            {'dni': 'CC3001', 'first_name': 'Ana', 'last_name': 'García', 'address': 'Cra 10 #1-23', 'phone': '300200001', 'city_id': cities['BOG'].id},
            {'dni': 'CC3002', 'first_name': 'Bruno', 'last_name': 'Pineda', 'address': 'Cll 12 #3-45', 'phone': '300200002', 'city_id': cities['BGA'].id},
            {'dni': 'CC3003', 'first_name': 'Carla', 'last_name': 'Mora', 'address': 'Cll 8 #9-10', 'phone': '300200003', 'city_id': cities['MED'].id},
            {'dni': 'CC3004', 'first_name': 'Diego', 'last_name': 'Luna', 'address': 'Cra 45 #12-34', 'phone': '300200004', 'city_id': cities['CLO'].id},
            {'dni': 'CC3005', 'first_name': 'Elena', 'last_name': 'Suárez', 'address': 'Av 7 #98-11', 'phone': '300200005', 'city_id': cities['BAQ'].id},
            {'dni': 'CC3006', 'first_name': 'Felipe', 'last_name': 'Cruz', 'address': 'Mz 4 Cs 5', 'phone': '300200006', 'city_id': cities['SOA'].id},
            {'dni': 'CC3007', 'first_name': 'Gloria', 'last_name': 'Vega', 'address': 'Cra 70 #20-30', 'phone': '300200007', 'city_id': cities['FLA'].id},
            {'dni': 'CC3008', 'first_name': 'Hugo', 'last_name': 'Ríos', 'address': 'Cll 25 #4-55', 'phone': '300200008', 'city_id': cities['ENV'].id},
            {'dni': 'CC3009', 'first_name': 'Irene', 'last_name': 'Quintero', 'address': 'Cll 30 #6-77', 'phone': '300200009', 'city_id': cities['PAL'].id},
            {'dni': 'CC3010', 'first_name': 'Jorge', 'last_name': 'Nieto', 'address': 'Cra 15 #5-22', 'phone': '300200010', 'city_id': cities['SOL'].id},
            {'dni': 'CC3011', 'first_name': 'Karen', 'last_name': 'Ortiz', 'address': 'Cll 72 #15-33', 'phone': '300200011', 'city_id': cities['CHI'].id},
            {'dni': 'CC3012', 'first_name': 'Luis', 'last_name': 'Pardo', 'address': 'Cra 8 #14-50', 'phone': '300200012', 'city_id': cities['GIR'].id},
            {'dni': 'CC3013', 'first_name': 'Marta', 'last_name': 'Rey', 'address': 'Cll 40 #9-21', 'phone': '300200013', 'city_id': cities['BEL'].id},
            {'dni': 'CC3014', 'first_name': 'Nicolás', 'last_name': 'Soto', 'address': 'Av 13 #45-60', 'phone': '300200014', 'city_id': cities['YUM'].id},
            {'dni': 'CC3015', 'first_name': 'Olga', 'last_name': 'Torres', 'address': 'Cra 9 #20-20', 'phone': '300200015', 'city_id': cities['MAL'].id},
            {'dni': 'CC3016', 'first_name': 'Pablo', 'last_name': 'Uribe', 'address': 'Cll 12 #23-12', 'phone': '300200016', 'city_id': cities['ZIP'].id},
            {'dni': 'CC3017', 'first_name': 'Raquel', 'last_name': 'Valencia', 'address': 'Cra 22 #33-44', 'phone': '300200017', 'city_id': cities['PDC'].id},
            {'dni': 'CC3018', 'first_name': 'Sergio', 'last_name': 'Weber', 'address': 'Cll 9 #10-11', 'phone': '300200018', 'city_id': cities['ITA'].id},
            {'dni': 'CC3019', 'first_name': 'Tatiana', 'last_name': 'Ximénez', 'address': 'Cll 1 #1-1', 'phone': '300200019', 'city_id': cities['BUG'].id},
            {'dni': 'CC3020', 'first_name': 'Ulises', 'last_name': 'Zárate', 'address': 'Cra 100 #50-60', 'phone': '300200020', 'city_id': cities['PTC'].id}
        ]
        
        persons = []
        for person_data in persons_data:
            person = person_handler.create(**person_data)
            persons.append(person)
            print(f"  ✓ Persona {person.id}: {person.first_name} {person.last_name}")
        
        # Crear 10 empleados (primeros 10 personas) asignados a sucursales
        employees = []
        branch_assignments = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4]  # índice de branches
        
        for i in range(10):
            employee = employee_handler.create(
                person_id=persons[i].id,
                branch_id=branches[branch_assignments[i]].id
            )
            employees.append(employee)
            city = city_handler.get(branches[branch_assignments[i]].city_id)
            print(f"  ✓ Empleado {employee.id}: {persons[i].first_name} {persons[i].last_name} - {city.description}")
        
        # ============================================================
        # 4. USUARIOS, ROLES Y PERMISOS
        # ============================================================
        print("\n[4/15] Creando Usuarios, Roles y Permisos...")
        
        # Primero crear roles
        roles_data = [
            {'description': 'ADMIN'},
            {'description': 'MANAGER'},
            {'description': 'SALES'}
        ]
        
        roles = {}
        for role_data in roles_data:
            role = role_handler.create(**role_data)
            roles[role_data['description']] = role
            print(f"  ✓ Rol: {role.description}")
        
        # Crear usuarios para los primeros 8 empleados (necesitan role_id)
        users_data = [
            {'username': 'ana', 'password': 'hash-ana', 'role_id': roles['SALES'].id},
            {'username': 'bruno', 'password': 'hash-bruno', 'role_id': roles['SALES'].id},
            {'username': 'carla', 'password': 'hash-carla', 'role_id': roles['SALES'].id},
            {'username': 'diego', 'password': 'hash-diego', 'role_id': roles['SALES'].id},
            {'username': 'elena', 'password': 'hash-elena', 'role_id': roles['SALES'].id},
            {'username': 'felipe', 'password': 'hash-felipe', 'role_id': roles['MANAGER'].id},
            {'username': 'gloria', 'password': 'hash-gloria', 'role_id': roles['MANAGER'].id},
            {'username': 'hugo', 'password': 'hash-hugo', 'role_id': roles['ADMIN'].id}
        ]
        
        users = []
        for user_data in users_data:
            user = user_handler.create(**user_data)
            users.append(user)
            print(f"  ✓ Usuario: {user.username}")
        
        # Permisos (los roles ya fueron creados arriba)
        permissions_data = [
            {'description': 'READ_REPORTS', 'role_id': roles['MANAGER'].id},
            {'description': 'WRITE_QUOTES', 'role_id': roles['SALES'].id},
            {'description': 'APPROVE_ORDERS', 'role_id': roles['MANAGER'].id},
            {'description': 'ADMIN_ALL', 'role_id': roles['ADMIN'].id}
        ]
        
        for perm_data in permissions_data:
            perm = permission_handler.create(**perm_data)
            print(f"  ✓ Permiso: {perm.description}")
        
        # ============================================================
        # 5. ASIGNACIONES (ya los empleados tienen branch_id)
        # ============================================================
        print("\n[5/15] Creando Asignaciones...")
        # Los empleados ya están asignados a branches via branch_id
        # Ahora creamos asignaciones adicionales a organization
        assignments_data = []
        for i, employee in enumerate(employees):
            assignment = assignment_handler.create(
                organization_id=orgs[0].id,
                branch_id=employee.branch_id,
                employee_id=employee.id
            )
            assignments_data.append(assignment)
            person = person_handler.get(employee.person_id)
            branch = branch_handler.get(employee.branch_id)
            city = city_handler.get(branch.city_id)
            print(f"  ✓ Assignment {assignment.id}: {person.first_name} → {city.description}")
        
        # ============================================================
        # 6. MARCAS
        # ============================================================
        print("\n[6/15] Creando Marcas...")
        brands_data = [
            {'name': 'Omron', 'country': 'Japón', 'website': 'www.omron.com'},
            {'name': 'ING Multicontrol', 'country': 'Alemania', 'website': 'www.ing-multicontrol.com'},
            {'name': 'Gefran', 'country': 'Italia', 'website': 'www.gefran.com'},
            {'name': 'Weidmüller', 'country': 'Alemania', 'website': 'www.weidmuller.com'},
            {'name': 'Rice-Lake', 'country': 'USA', 'website': 'www.ricelake.com'},
            {'name': 'Optec', 'country': 'Colombia', 'website': 'www.optec.com.co'}
        ]
        
        brands = []
        for brand_data in brands_data:
            brand = brand_handler.create(**brand_data)
            brands.append(brand)
            print(f"  ✓ Marca {brand.id}: {brand.name}")
        
        # ============================================================
        # 7. INVENTARIO (60 items = 6 marcas × 10 productos)
        # ============================================================
        print("\n[7/15] Creando Items de Inventario...")
        
        inventory_items_data = [
            # Omron (10 productos)
            {'name': 'OMR-PLC-NX1P2', 'description': 'Controlador PLC Omron NX1P2', 'price': Decimal('4500000'), 'quantity': 10, 'brand_id': brands[0].id},
            {'name': 'OMR-SEN-E3Z', 'description': 'Sensor fotoeléctrico Omron E3Z', 'price': Decimal('180000'), 'quantity': 50, 'brand_id': brands[0].id},
            {'name': 'OMR-INV-A1000', 'description': 'Variador Omron A1000', 'price': Decimal('6000000'), 'quantity': 5, 'brand_id': brands[0].id},
            {'name': 'OMR-HMI-NA5', 'description': 'HMI Omron NA5 7"', 'price': Decimal('2800000'), 'quantity': 15, 'brand_id': brands[0].id},
            {'name': 'OMR-IO-NX', 'description': 'Módulo I/O Omron NX', 'price': Decimal('850000'), 'quantity': 20, 'brand_id': brands[0].id},
            {'name': 'OMR-ENC-E6B2', 'description': 'Encoder Omron E6B2', 'price': Decimal('450000'), 'quantity': 25, 'brand_id': brands[0].id},
            {'name': 'OMR-REL-G2R', 'description': 'Relé electromecánico Omron G2R', 'price': Decimal('35000'), 'quantity': 100, 'brand_id': brands[0].id},
            {'name': 'OMR-SSR-G3NA', 'description': 'Relé de estado sólido Omron G3NA', 'price': Decimal('185000'), 'quantity': 30, 'brand_id': brands[0].id},
            {'name': 'OMR-PSU-S8VK', 'description': 'Fuente 24V Omron S8VK', 'price': Decimal('320000'), 'quantity': 40, 'brand_id': brands[0].id},
            {'name': 'OMR-SAF-F3SG', 'description': 'Cortina de seguridad Omron F3SG', 'price': Decimal('3200000'), 'quantity': 8, 'brand_id': brands[0].id},
            # ING Multicontrol (10 productos)
            {'name': 'ING-ARR-START', 'description': 'Arrancador suave ING Multicontrol', 'price': Decimal('2750000'), 'quantity': 12, 'brand_id': brands[1].id},
            {'name': 'ING-CON-24V', 'description': 'Fuente de poder 24V ING Multicontrol', 'price': Decimal('380000'), 'quantity': 35, 'brand_id': brands[1].id},
            {'name': 'ING-PLC-MC200', 'description': 'PLC ING Multicontrol MC200', 'price': Decimal('3800000'), 'quantity': 10, 'brand_id': brands[1].id},
            {'name': 'ING-HMI-MC7', 'description': 'HMI 7" ING Multicontrol', 'price': Decimal('1900000'), 'quantity': 18, 'brand_id': brands[1].id},
            {'name': 'ING-VFD-MC500', 'description': 'Variador ING Multicontrol MC500', 'price': Decimal('5200000'), 'quantity': 7, 'brand_id': brands[1].id},
            {'name': 'ING-IO-MOD8', 'description': 'Módulo I/O 8ch ING Multicontrol', 'price': Decimal('620000'), 'quantity': 25, 'brand_id': brands[1].id},
            {'name': 'ING-REL-SAF', 'description': 'Relé de seguridad ING Multicontrol', 'price': Decimal('580000'), 'quantity': 22, 'brand_id': brands[1].id},
            {'name': 'ING-SWI-ETH5', 'description': 'Switch Ethernet 5p ING Multicontrol', 'price': Decimal('490000'), 'quantity': 30, 'brand_id': brands[1].id},
            {'name': 'ING-ENC-INC', 'description': 'Encoder incremental ING Multicontrol', 'price': Decimal('380000'), 'quantity': 28, 'brand_id': brands[1].id},
            {'name': 'ING-PSU-48V', 'description': 'Fuente 48V ING Multicontrol', 'price': Decimal('520000'), 'quantity': 20, 'brand_id': brands[1].id},
            # Gefran (10 productos)
            {'name': 'GEF-TEMP-600', 'description': 'Controlador de temperatura Gefran 600', 'price': Decimal('1350000'), 'quantity': 15, 'brand_id': brands[2].id},
            {'name': 'GEF-INV-ADV', 'description': 'Inversor de frecuencia Gefran ADV', 'price': Decimal('6500000'), 'quantity': 6, 'brand_id': brands[2].id},
            {'name': 'GEF-TRANS-LIN', 'description': 'Transductor lineal Gefran', 'price': Decimal('2100000'), 'quantity': 10, 'brand_id': brands[2].id},
            {'name': 'GEF-SSR-GQ', 'description': 'Relé de estado sólido Gefran GQ', 'price': Decimal('285000'), 'quantity': 35, 'brand_id': brands[2].id},
            {'name': 'GEF-DRIVE-AX', 'description': 'Servo drive Gefran AX', 'price': Decimal('7800000'), 'quantity': 5, 'brand_id': brands[2].id},
            {'name': 'GEF-PRES-TRX', 'description': 'Transductor de presión Gefran', 'price': Decimal('980000'), 'quantity': 18, 'brand_id': brands[2].id},
            {'name': 'GEF-AMP-LC', 'description': 'Amplificador para celda de carga Gefran', 'price': Decimal('1450000'), 'quantity': 12, 'brand_id': brands[2].id},
            {'name': 'GEF-HMI-5', 'description': 'HMI 5" Gefran', 'price': Decimal('1680000'), 'quantity': 14, 'brand_id': brands[2].id},
            {'name': 'GEF-RTD-PT100', 'description': 'Sonda RTD PT100 Gefran', 'price': Decimal('220000'), 'quantity': 45, 'brand_id': brands[2].id},
            {'name': 'GEF-PSU-24', 'description': 'Fuente 24V Gefran', 'price': Decimal('380000'), 'quantity': 30, 'brand_id': brands[2].id},
            # Weidmüller (10 productos)
            {'name': 'WEI-BOR-TER', 'description': 'Bornera Weidmüller Terminal', 'price': Decimal('50000'), 'quantity': 200, 'brand_id': brands[3].id},
            {'name': 'WEI-SSR-IO', 'description': 'Módulo IO Weidmüller SSR', 'price': Decimal('250000'), 'quantity': 40, 'brand_id': brands[3].id},
            {'name': 'WEI-PSU-24', 'description': 'Fuente 24V Weidmüller', 'price': Decimal('400000'), 'quantity': 35, 'brand_id': brands[3].id},
            {'name': 'WEI-REL-TER', 'description': 'Relé interfaz Weidmüller', 'price': Decimal('85000'), 'quantity': 60, 'brand_id': brands[3].id},
            {'name': 'WEI-RAIL-DIN', 'description': 'Riel DIN Weidmüller', 'price': Decimal('35000'), 'quantity': 150, 'brand_id': brands[3].id},
            {'name': 'WEI-SW-IND8', 'description': 'Switch industrial 8p Weidmüller', 'price': Decimal('1250000'), 'quantity': 15, 'brand_id': brands[3].id},
            {'name': 'WEI-SURGE-SPD', 'description': 'Protección contra sobretensión Weidmüller SPD', 'price': Decimal('320000'), 'quantity': 28, 'brand_id': brands[3].id},
            {'name': 'WEI-CON-PUSHIN', 'description': 'Conector Push-In Weidmüller', 'price': Decimal('18000'), 'quantity': 300, 'brand_id': brands[3].id},
            {'name': 'WEI-MARKZ-CARD', 'description': 'Tarjetas marcadoras Weidmüller', 'price': Decimal('12000'), 'quantity': 500, 'brand_id': brands[3].id},
            {'name': 'WEI-TOOL-CRIMP', 'description': 'Herramienta crimpadora Weidmüller', 'price': Decimal('450000'), 'quantity': 10, 'brand_id': brands[3].id},
            # Rice-Lake (10 productos)
            {'name': 'RCL-BAL-IND', 'description': 'Indicador de pesaje Rice-Lake', 'price': Decimal('4000000'), 'quantity': 8, 'brand_id': brands[4].id},
            {'name': 'RCL-CEL-CARGA', 'description': 'Celda de carga Rice-Lake', 'price': Decimal('1800000'), 'quantity': 12, 'brand_id': brands[4].id},
            {'name': 'RCL-PES-PLC', 'description': 'Módulo de pesaje para PLC Rice-Lake', 'price': Decimal('3800000'), 'quantity': 6, 'brand_id': brands[4].id},
            {'name': 'RCL-JBOX-4', 'description': 'Caja de conexiones 4 celdas Rice-Lake', 'price': Decimal('580000'), 'quantity': 15, 'brand_id': brands[4].id},
            {'name': 'RCL-SCALE-PLT', 'description': 'Báscula de plataforma Rice-Lake', 'price': Decimal('5500000'), 'quantity': 5, 'brand_id': brands[4].id},
            {'name': 'RCL-TRX-ANALOG', 'description': 'Transmisor analógico Rice-Lake', 'price': Decimal('720000'), 'quantity': 18, 'brand_id': brands[4].id},
            {'name': 'RCL-WEIGH-MOD', 'description': 'Módulo de pesaje Rice-Lake', 'price': Decimal('2900000'), 'quantity': 8, 'brand_id': brands[4].id},
            {'name': 'RCL-CHECK-CKW', 'description': 'Checkweigher Rice-Lake', 'price': Decimal('12500000'), 'quantity': 3, 'brand_id': brands[4].id},
            {'name': 'RCL-PRN-TT', 'description': 'Impresora térmica Rice-Lake', 'price': Decimal('950000'), 'quantity': 10, 'brand_id': brands[4].id},
            {'name': 'RCL-SW-LIC', 'description': 'Licencia software pesaje Rice-Lake', 'price': Decimal('1800000'), 'quantity': 12, 'brand_id': brands[4].id},
            # Optec (10 productos)
            {'name': 'OPT-SEN-IND', 'description': 'Sensor inductivo Optec', 'price': Decimal('220000'), 'quantity': 45, 'brand_id': brands[5].id},
            {'name': 'OPT-BARR-SEG', 'description': 'Barrera de seguridad Optec', 'price': Decimal('900000'), 'quantity': 12, 'brand_id': brands[5].id},
            {'name': 'OPT-HMI-7', 'description': 'Panel HMI 7" Optec', 'price': Decimal('1200000'), 'quantity': 15, 'brand_id': brands[5].id},
            {'name': 'OPT-PE-SENS', 'description': 'Sensor fotoeléctrico Optec', 'price': Decimal('195000'), 'quantity': 50, 'brand_id': brands[5].id},
            {'name': 'OPT-PROX-M18', 'description': 'Sensor de proximidad M18 Optec', 'price': Decimal('165000'), 'quantity': 60, 'brand_id': brands[5].id},
            {'name': 'OPT-IO-LINK', 'description': 'Módulo IO-Link Master Optec', 'price': Decimal('850000'), 'quantity': 18, 'brand_id': brands[5].id},
            {'name': 'OPT-CAB-M12', 'description': 'Cable M12 Optec', 'price': Decimal('45000'), 'quantity': 100, 'brand_id': brands[5].id},
            {'name': 'OPT-BRK-ANG', 'description': 'Soporte/bracket angular Optec', 'price': Decimal('28000'), 'quantity': 120, 'brand_id': brands[5].id},
            {'name': 'OPT-PB-LED', 'description': 'Pulsador iluminado Optec', 'price': Decimal('75000'), 'quantity': 80, 'brand_id': brands[5].id},
            {'name': 'OPT-TWR-LIGHT', 'description': 'Torre luminosa Optec', 'price': Decimal('320000'), 'quantity': 25, 'brand_id': brands[5].id}
        ]
        
        items = []
        for item_data in inventory_items_data:
            item = inventory_handler.create(**item_data)
            items.append(item)
            print(f"  ✓ Item {item.id}: {item.name} (${item.price:,.0f})")
        
        print(f"\n  Total de items creados: {len(items)}")
        
        # Helper function para buscar items por nombre
        def find_item(name):
            return next(item for item in items if item.name == name)
        
        # ============================================================
        # 8. QUOTATION LINES (Líneas base para órdenes)
        # ============================================================
        print("\n[8/15] Creando Quotation Lines...")
        quotation_lines_data = [
            {'item_code': find_item('OMR-PLC-NX1P2').name, 'quantity': 2},
            {'item_code': find_item('GEF-TEMP-600').name, 'quantity': 2},
            {'item_code': find_item('ING-PLC-MC200').name, 'quantity': 1},
            {'item_code': find_item('OMR-INV-A1000').name, 'quantity': 1},
            {'item_code': find_item('WEI-SSR-IO').name, 'quantity': 5},
            {'item_code': find_item('RCL-CEL-CARGA').name, 'quantity': 2},
            {'item_code': find_item('GEF-TRANS-LIN').name, 'quantity': 1},
            {'item_code': find_item('RCL-PES-PLC').name, 'quantity': 1}
        ]
        
        q_lines = []
        for qline_data in quotation_lines_data:
            qline = quotation_line_handler.create(**qline_data)
            q_lines.append(qline)
            print(f"  ✓ QuotationLine {qline.id}: {qline.item_code} x{qline.quantity}")
        
        # ============================================================
        # 9. TANDA 1: COTIZACIONES ABRIL-JUNIO 2025
        # ============================================================
        print("\n[9/15] Creando Cotizaciones Tanda 1 (ABR-JUN)...")
        
        quotes_t1_data = [
            {
                'customer_name': 'Automatiza Andina SAS',
                'date': date(2025, 4, 8),
                'total': Decimal('12800000'),
                'employee_id': employees[0].id  # Ana (Bogotá)
            },
            {
                'customer_name': 'ControlTech SAS',
                'date': date(2025, 4, 15),
                'total': Decimal('18300000'),
                'employee_id': employees[3].id  # Diego (Bucaramanga)
            },
            {
                'customer_name': 'Industrias del Norte SA',
                'date': date(2025, 5, 3),
                'total': Decimal('15700000'),
                'employee_id': employees[5].id  # Felipe (Medellín)
            },
            {
                'customer_name': 'Vallepack LTDA',
                'date': date(2025, 5, 19),
                'total': Decimal('6900000'),
                'employee_id': employees[7].id  # Hugo (Cali)
            },
            {
                'customer_name': 'Caribe Foods SA',
                'date': date(2025, 6, 6),
                'total': Decimal('22450000'),
                'employee_id': employees[9].id  # Jorge (Barranquilla)
            },
            {
                'customer_name': 'Metalúrgica Antioquia SAS',
                'date': date(2025, 6, 21),
                'total': Decimal('9950000'),
                'employee_id': employees[1].id  # Bruno (Bucaramanga)
            }
        ]
        
        quotes_t1 = []
        for q_data in quotes_t1_data:
            quote = quote_handler.create(**q_data)
            quotes_t1.append(quote)
            print(f"  ✓ Quote {quote.id}: {quote.customer_name} - ${quote.total:,.0f}")
        
        # ============================================================
        # 10. QUOTE ITEMS TANDA 1
        # ============================================================
        print("\n[10/15] Creando Quote Items Tanda 1...")
        
        quote_items_t1 = [
            # Quote 1 (Ana - $12,800,000)
            {'quote_id': quotes_t1[0].id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 10, 'unit_price': Decimal('180000')},
            {'quote_id': quotes_t1[0].id, 'item_code': find_item('WEI-PSU-24').name, 'quantity': 5, 'unit_price': Decimal('400000')},
            {'quote_id': quotes_t1[0].id, 'item_code': find_item('OPT-SEN-IND').name, 'quantity': 5, 'unit_price': Decimal('220000')},
            # Quote 2 (Diego - $18,300,000) - ACCEPTED
            {'quote_id': quotes_t1[1].id, 'item_code': find_item('OMR-PLC-NX1P2').name, 'quantity': 2, 'unit_price': Decimal('4500000')},
            {'quote_id': quotes_t1[1].id, 'item_code': find_item('GEF-TEMP-600').name, 'quantity': 3, 'unit_price': Decimal('1350000')},
            # Quote 3 (Felipe - $15,700,000)
            {'quote_id': quotes_t1[2].id, 'item_code': find_item('ING-PLC-MC200').name, 'quantity': 1, 'unit_price': Decimal('3800000')},
            {'quote_id': quotes_t1[2].id, 'item_code': find_item('GEF-INV-ADV').name, 'quantity': 1, 'unit_price': Decimal('6500000')},
            {'quote_id': quotes_t1[2].id, 'item_code': find_item('RCL-BAL-IND').name, 'quantity': 1, 'unit_price': Decimal('4000000')},
            # Quote 4 (Hugo - $6,900,000) - REJECTED
            {'quote_id': quotes_t1[3].id, 'item_code': find_item('OMR-INV-A1000').name, 'quantity': 1, 'unit_price': Decimal('6000000')},
            {'quote_id': quotes_t1[3].id, 'item_code': find_item('OPT-BARR-SEG').name, 'quantity': 1, 'unit_price': Decimal('900000')},
            # Quote 5 (Jorge - $22,450,000) - ACCEPTED
            {'quote_id': quotes_t1[4].id, 'item_code': find_item('RCL-CEL-CARGA').name, 'quantity': 3, 'unit_price': Decimal('1800000')},
            {'quote_id': quotes_t1[4].id, 'item_code': find_item('WEI-SSR-IO').name, 'quantity': 10, 'unit_price': Decimal('250000')},
            {'quote_id': quotes_t1[4].id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 10, 'unit_price': Decimal('180000')},
            # Quote 6 (Bruno - $9,950,000)
            {'quote_id': quotes_t1[5].id, 'item_code': find_item('GEF-TRANS-LIN').name, 'quantity': 2, 'unit_price': Decimal('2100000')},
            {'quote_id': quotes_t1[5].id, 'item_code': find_item('ING-CON-24V').name, 'quantity': 5, 'unit_price': Decimal('380000')}
        ]
        
        for qi_data in quote_items_t1:
            qi = quote_item_handler.create(**qi_data)
            print(f"  ✓ QuoteItem: Quote {qi.quote_id} - {qi.item_code} x{qi.quantity}")
        
        # ============================================================
        # 11. SALES ORDERS TANDA 1
        # ============================================================
        print("\n[11/15] Creando Sales Orders Tanda 1...")
        
        # SO de Quote 2 (Diego - ControlTech)
        so1 = sales_order_handler.create(
            quote_id=quotes_t1[1].id,
            date=date(2025, 4, 20),
            total=Decimal('18300000'),
            employee_id=employees[3].id
        )
        print(f"  ✓ SalesOrder {so1.id}: Quote {so1.quote_id} - ${so1.total:,.0f}")
        
        # Items de SO1
        so1_items = [
            {'sales_order_id': so1.id, 'item_code': find_item('OMR-PLC-NX1P2').name, 'quantity': 2, 'unit_price': Decimal('4500000')},
            {'sales_order_id': so1.id, 'item_code': find_item('GEF-TEMP-600').name, 'quantity': 3, 'unit_price': Decimal('1350000')}
        ]
        for soi_data in so1_items:
            soi = sales_order_item_handler.create(**soi_data)
            print(f"    - Item: {soi.item_code} x{soi.quantity}")
        
        # SO de Quote 5 (Jorge - Caribe Foods)
        so2 = sales_order_handler.create(
            quote_id=quotes_t1[4].id,
            date=date(2025, 6, 8),
            total=Decimal('22450000'),
            employee_id=employees[9].id
        )
        print(f"  ✓ SalesOrder {so2.id}: Quote {so2.quote_id} - ${so2.total:,.0f}")
        
        # Items de SO2
        so2_items = [
            {'sales_order_id': so2.id, 'item_code': find_item('RCL-CEL-CARGA').name, 'quantity': 3, 'unit_price': Decimal('1800000')},
            {'sales_order_id': so2.id, 'item_code': find_item('WEI-SSR-IO').name, 'quantity': 10, 'unit_price': Decimal('250000')},
            {'sales_order_id': so2.id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 10, 'unit_price': Decimal('180000')}
        ]
        for soi_data in so2_items:
            soi = sales_order_item_handler.create(**soi_data)
            print(f"    - Item: {soi.item_code} x{soi.quantity}")
        
        # ============================================================
        # 12. FACTURAS TANDA 1
        # ============================================================
        print("\n[12/15] Creando Facturas Tanda 1...")
        
        invoices_t1_data = [
            # Factura de SO1 (Diego)
            {
                'sales_order_id': so1.id,
                'date': date(2025, 4, 21),
                'total': Decimal('18300000'),
                'quotation_line_id': q_lines[1].id,
                'employee_id': employees[3].id
            },
            # Factura de SO2 (Jorge)
            {
                'sales_order_id': so2.id,
                'date': date(2025, 6, 10),
                'total': Decimal('22450000'),
                'quotation_line_id': q_lines[4].id,
                'employee_id': employees[9].id
            },
            # Factura directa sin SO (Ana)
            {
                'sales_order_id': so1.id,  # Requerido por modelo
                'date': date(2025, 4, 30),
                'total': Decimal('8600000'),
                'employee_id': employees[0].id
            },
            # Factura directa sin SO (Bruno)
            {
                'sales_order_id': so1.id,  # Requerido por modelo
                'date': date(2025, 6, 25),
                'total': Decimal('6900000'),
                'employee_id': employees[1].id
            }
        ]
        
        invoices_t1 = []
        for inv_data in invoices_t1_data:
            invoice = invoice_handler.create(**inv_data)
            invoices_t1.append(invoice)
            print(f"  ✓ Invoice {invoice.id}: ${invoice.total:,.0f} - Emp {invoice.employee_id}")
        
        # Invoice Items
        invoice_items_t1 = [
            # Invoice 1 (de SO1)
            {'invoice_id': invoices_t1[0].id, 'item_code': find_item('OMR-PLC-NX1P2').name, 'quantity': 2, 'unit_price': Decimal('4500000')},
            {'invoice_id': invoices_t1[0].id, 'item_code': find_item('GEF-TEMP-600').name, 'quantity': 3, 'unit_price': Decimal('1350000')},
            # Invoice 2 (de SO2)
            {'invoice_id': invoices_t1[1].id, 'item_code': find_item('RCL-CEL-CARGA').name, 'quantity': 3, 'unit_price': Decimal('1800000')},
            {'invoice_id': invoices_t1[1].id, 'item_code': find_item('WEI-SSR-IO').name, 'quantity': 10, 'unit_price': Decimal('250000')},
            {'invoice_id': invoices_t1[1].id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 10, 'unit_price': Decimal('180000')},
            # Invoice 3 (directa Ana)
            {'invoice_id': invoices_t1[2].id, 'item_code': find_item('WEI-PSU-24').name, 'quantity': 5, 'unit_price': Decimal('400000')},
            {'invoice_id': invoices_t1[2].id, 'item_code': find_item('OPT-SEN-IND').name, 'quantity': 5, 'unit_price': Decimal('220000')},
            {'invoice_id': invoices_t1[2].id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 10, 'unit_price': Decimal('180000')},
            # Invoice 4 (directa Bruno)
            {'invoice_id': invoices_t1[3].id, 'item_code': find_item('GEF-TRANS-LIN').name, 'quantity': 2, 'unit_price': Decimal('2100000')},
            {'invoice_id': invoices_t1[3].id, 'item_code': find_item('ING-CON-24V').name, 'quantity': 5, 'unit_price': Decimal('380000')}
        ]
        
        for ii_data in invoice_items_t1:
            ii = invoice_item_handler.create(**ii_data)
            print(f"    - Item: Invoice {ii.invoice_id} - {ii.item_code} x{ii.quantity}")
        
        # ============================================================
        # 13. TANDA 2: COTIZACIONES JUL-SEP 2025
        # ============================================================
        print("\n[13/15] Creando Cotizaciones Tanda 2 (JUL-SEP)...")
        
        quotes_t2_data = [
            {
                'customer_name': 'Vallepack LTDA',
                'date': date(2025, 7, 5),
                'total': Decimal('10400000'),
                'employee_id': employees[7].id  # Hugo
            },
            {
                'customer_name': 'Caribe Foods SA',
                'date': date(2025, 7, 18),
                'total': Decimal('16900000'),
                'employee_id': employees[9].id  # Jorge
            },
            {
                'customer_name': 'Automatiza Andina SAS',
                'date': date(2025, 8, 8),
                'total': Decimal('21600000'),
                'employee_id': employees[0].id  # Ana
            },
            {
                'customer_name': 'Metalúrgica Antioquia SAS',
                'date': date(2025, 8, 22),
                'total': Decimal('13750000'),
                'employee_id': employees[5].id  # Felipe
            },
            {
                'customer_name': 'ControlTech SAS',
                'date': date(2025, 9, 9),
                'total': Decimal('7200000'),
                'employee_id': employees[4].id  # Elena
            },
            {
                'customer_name': 'Industrias del Norte SA',
                'date': date(2025, 9, 14),
                'total': Decimal('19300000'),
                'employee_id': employees[6].id  # Gloria
            }
        ]
        
        quotes_t2 = []
        for q_data in quotes_t2_data:
            quote = quote_handler.create(**q_data)
            quotes_t2.append(quote)
            print(f"  ✓ Quote {quote.id}: {quote.customer_name} - ${quote.total:,.0f}")
        
        # Quote Items Tanda 2
        quote_items_t2 = [
            # Quote 7 (Hugo - $10,400,000)
            {'quote_id': quotes_t2[0].id, 'item_code': find_item('WEI-BOR-TER').name, 'quantity': 80, 'unit_price': Decimal('50000')},
            {'quote_id': quotes_t2[0].id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 8, 'unit_price': Decimal('180000')},
            # Quote 8 (Jorge - $16,900,000) - ACCEPTED
            {'quote_id': quotes_t2[1].id, 'item_code': find_item('RCL-PES-PLC').name, 'quantity': 1, 'unit_price': Decimal('3800000')},
            {'quote_id': quotes_t2[1].id, 'item_code': find_item('OMR-INV-A1000').name, 'quantity': 1, 'unit_price': Decimal('6000000')},
            {'quote_id': quotes_t2[1].id, 'item_code': find_item('OPT-HMI-7').name, 'quantity': 1, 'unit_price': Decimal('1200000')},
            # Quote 9 (Ana - $21,600,000) - ACCEPTED
            {'quote_id': quotes_t2[2].id, 'item_code': find_item('OMR-PLC-NX1P2').name, 'quantity': 3, 'unit_price': Decimal('4500000')},
            {'quote_id': quotes_t2[2].id, 'item_code': find_item('ING-CON-24V').name, 'quantity': 3, 'unit_price': Decimal('380000')},
            # Quote 10 (Felipe - $13,750,000)
            {'quote_id': quotes_t2[3].id, 'item_code': find_item('ING-ARR-START').name, 'quantity': 2, 'unit_price': Decimal('2750000')},
            {'quote_id': quotes_t2[3].id, 'item_code': find_item('WEI-PSU-24').name, 'quantity': 5, 'unit_price': Decimal('400000')},
            # Quote 11 (Elena - $7,200,000)
            {'quote_id': quotes_t2[4].id, 'item_code': find_item('WEI-SSR-IO').name, 'quantity': 8, 'unit_price': Decimal('250000')},
            {'quote_id': quotes_t2[4].id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 8, 'unit_price': Decimal('180000')},
            # Quote 12 (Gloria - $19,300,000) - ACCEPTED
            {'quote_id': quotes_t2[5].id, 'item_code': find_item('GEF-INV-ADV').name, 'quantity': 1, 'unit_price': Decimal('6500000')},
            {'quote_id': quotes_t2[5].id, 'item_code': find_item('GEF-TEMP-600').name, 'quantity': 2, 'unit_price': Decimal('1350000')},
            {'quote_id': quotes_t2[5].id, 'item_code': find_item('RCL-BAL-IND').name, 'quantity': 1, 'unit_price': Decimal('4000000')}
        ]
        
        for qi_data in quote_items_t2:
            qi = quote_item_handler.create(**qi_data)
            print(f"  ✓ QuoteItem: Quote {qi.quote_id} - {qi.item_code}")
        
        # ============================================================
        # 14. SALES ORDERS TANDA 2
        # ============================================================
        print("\n[14/15] Creando Sales Orders Tanda 2...")
        
        # SO de Quote 8 (Jorge)
        so3 = sales_order_handler.create(
            quote_id=quotes_t2[1].id,
            date=date(2025, 7, 20),
            total=Decimal('16900000'),
            employee_id=employees[9].id
        )
        print(f"  ✓ SalesOrder {so3.id}: ${so3.total:,.0f}")
        
        so3_items = [
            {'sales_order_id': so3.id, 'item_code': find_item('RCL-PES-PLC').name, 'quantity': 1, 'unit_price': Decimal('3800000')},
            {'sales_order_id': so3.id, 'item_code': find_item('OMR-INV-A1000').name, 'quantity': 1, 'unit_price': Decimal('6000000')},
            {'sales_order_id': so3.id, 'item_code': find_item('OPT-HMI-7').name, 'quantity': 1, 'unit_price': Decimal('1200000')}
        ]
        for soi_data in so3_items:
            soi = sales_order_item_handler.create(**soi_data)
            print(f"    - {soi.item_code} x{soi.quantity}")
        
        # SO de Quote 7 (Hugo)
        so4 = sales_order_handler.create(
            quote_id=quotes_t2[0].id,
            date=date(2025, 7, 7),
            total=Decimal('10400000'),
            employee_id=employees[7].id
        )
        print(f"  ✓ SalesOrder {so4.id}: ${so4.total:,.0f}")
        
        so4_items = [
            {'sales_order_id': so4.id, 'item_code': find_item('WEI-BOR-TER').name, 'quantity': 80, 'unit_price': Decimal('50000')},
            {'sales_order_id': so4.id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 8, 'unit_price': Decimal('180000')}
        ]
        for soi_data in so4_items:
            soi = sales_order_item_handler.create(**soi_data)
            print(f"    - {soi.item_code} x{soi.quantity}")
        
        # SO de Quote 9 (Ana)
        so5 = sales_order_handler.create(
            quote_id=quotes_t2[2].id,
            date=date(2025, 8, 10),
            total=Decimal('21600000'),
            employee_id=employees[0].id
        )
        print(f"  ✓ SalesOrder {so5.id}: ${so5.total:,.0f}")
        
        so5_items = [
            {'sales_order_id': so5.id, 'item_code': find_item('OMR-PLC-NX1P2').name, 'quantity': 3, 'unit_price': Decimal('4500000')},
            {'sales_order_id': so5.id, 'item_code': find_item('ING-CON-24V').name, 'quantity': 3, 'unit_price': Decimal('380000')}
        ]
        for soi_data in so5_items:
            soi = sales_order_item_handler.create(**soi_data)
            print(f"    - {soi.item_code} x{soi.quantity}")
        
        # SO de Quote 12 (Gloria)
        so6 = sales_order_handler.create(
            quote_id=quotes_t2[5].id,
            date=date(2025, 9, 16),
            total=Decimal('19300000'),
            employee_id=employees[6].id
        )
        print(f"  ✓ SalesOrder {so6.id}: ${so6.total:,.0f}")
        
        so6_items = [
            {'sales_order_id': so6.id, 'item_code': find_item('GEF-INV-ADV').name, 'quantity': 1, 'unit_price': Decimal('6500000')},
            {'sales_order_id': so6.id, 'item_code': find_item('GEF-TEMP-600').name, 'quantity': 2, 'unit_price': Decimal('1350000')},
            {'sales_order_id': so6.id, 'item_code': find_item('RCL-BAL-IND').name, 'quantity': 1, 'unit_price': Decimal('4000000')}
        ]
        for soi_data in so6_items:
            soi = sales_order_item_handler.create(**soi_data)
            print(f"    - {soi.item_code} x{soi.quantity}")
        
        # ============================================================
        # 15. FACTURAS TANDA 2
        # ============================================================
        print("\n[15/15] Creando Facturas Tanda 2...")
        
        invoices_t2_data = [
            # Factura de SO3 (Jorge)
            {'sales_order_id': so3.id, 'date': date(2025, 7, 21), 'total': Decimal('16900000'), 'employee_id': employees[9].id, 'quotation_line_id': q_lines[5].id},
            # Factura de SO4 (Hugo)
            {'sales_order_id': so4.id, 'date': date(2025, 7, 8), 'total': Decimal('10400000'), 'employee_id': employees[7].id, 'quotation_line_id': q_lines[0].id},
            # Factura de SO5 (Ana)
            {'sales_order_id': so5.id, 'date': date(2025, 8, 11), 'total': Decimal('21600000'), 'employee_id': employees[0].id, 'quotation_line_id': q_lines[2].id},
            # Factura de SO6 (Gloria)
            {'sales_order_id': so6.id, 'date': date(2025, 9, 17), 'total': Decimal('19300000'), 'employee_id': employees[6].id, 'quotation_line_id': q_lines[7].id},
            # Factura directa (Felipe)
            {'sales_order_id': so3.id, 'date': date(2025, 8, 25), 'total': Decimal('9150000'), 'employee_id': employees[5].id},
            # Factura directa (Elena)
            {'sales_order_id': so3.id, 'date': date(2025, 9, 20), 'total': Decimal('6440000'), 'employee_id': employees[4].id}
        ]
        
        invoices_t2 = []
        for inv_data in invoices_t2_data:
            invoice = invoice_handler.create(**inv_data)
            invoices_t2.append(invoice)
            print(f"  ✓ Invoice {invoice.id}: ${invoice.total:,.0f}")
        
        # Invoice Items Tanda 2
        invoice_items_t2 = [
            # Invoice 5 (de SO3 - Jorge)
            {'invoice_id': invoices_t2[0].id, 'item_code': find_item('RCL-PES-PLC').name, 'quantity': 1, 'unit_price': Decimal('3800000')},
            {'invoice_id': invoices_t2[0].id, 'item_code': find_item('OMR-INV-A1000').name, 'quantity': 1, 'unit_price': Decimal('6000000')},
            {'invoice_id': invoices_t2[0].id, 'item_code': find_item('OPT-HMI-7').name, 'quantity': 1, 'unit_price': Decimal('1200000')},
            # Invoice 6 (de SO4 - Hugo)
            {'invoice_id': invoices_t2[1].id, 'item_code': find_item('WEI-BOR-TER').name, 'quantity': 80, 'unit_price': Decimal('50000')},
            {'invoice_id': invoices_t2[1].id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 8, 'unit_price': Decimal('180000')},
            # Invoice 7 (de SO5 - Ana)
            {'invoice_id': invoices_t2[2].id, 'item_code': find_item('OMR-PLC-NX1P2').name, 'quantity': 3, 'unit_price': Decimal('4500000')},
            {'invoice_id': invoices_t2[2].id, 'item_code': find_item('ING-CON-24V').name, 'quantity': 3, 'unit_price': Decimal('380000')},
            # Invoice 8 (de SO6 - Gloria)
            {'invoice_id': invoices_t2[3].id, 'item_code': find_item('GEF-INV-ADV').name, 'quantity': 1, 'unit_price': Decimal('6500000')},
            {'invoice_id': invoices_t2[3].id, 'item_code': find_item('GEF-TEMP-600').name, 'quantity': 2, 'unit_price': Decimal('1350000')},
            {'invoice_id': invoices_t2[3].id, 'item_code': find_item('RCL-BAL-IND').name, 'quantity': 1, 'unit_price': Decimal('4000000')},
            # Invoice 9 (directa Felipe)
            {'invoice_id': invoices_t2[4].id, 'item_code': find_item('ING-ARR-START').name, 'quantity': 2, 'unit_price': Decimal('2750000')},
            {'invoice_id': invoices_t2[4].id, 'item_code': find_item('WEI-PSU-24').name, 'quantity': 5, 'unit_price': Decimal('400000')},
            {'invoice_id': invoices_t2[4].id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 5, 'unit_price': Decimal('180000')},
            # Invoice 10 (directa Elena)
            {'invoice_id': invoices_t2[5].id, 'item_code': find_item('WEI-SSR-IO').name, 'quantity': 8, 'unit_price': Decimal('250000')},
            {'invoice_id': invoices_t2[5].id, 'item_code': find_item('OMR-SEN-E3Z').name, 'quantity': 8, 'unit_price': Decimal('180000')}
        ]
        
        for ii_data in invoice_items_t2:
            ii = invoice_item_handler.create(**ii_data)
            print(f"    - {ii.item_code} x{ii.quantity}")
        
        # ============================================================
        # RESUMEN FINAL
        # ============================================================
        print("\n" + "="*70)
        print("✅ POBLACIÓN COMPLETADA CON ÉXITO")
        print("="*70)
        
        total_invoiced = sum(inv.total for inv in invoices_t1 + invoices_t2)
        
        print(f"\n📊 RESUMEN DEL DATASET:")
        print(f"  • Estados: {len(states)}")
        print(f"  • Ciudades: {len(cities)}")
        print(f"  • Organizaciones: {len(orgs)}")
        print(f"  • Sucursales multiCont: {len(branches)}")
        print(f"  • Personas: {len(persons)}")
        print(f"  • Empleados: {len(employees)}")
        print(f"  • Usuarios: {len(users)}")
        print(f"  • Roles: 3 (ADMIN, MANAGER, SALES)")
        print(f"  • Asignaciones: {len(assignments_data)}")
        print(f"  • Marcas: {len(brands)}")
        print(f"  • Items de inventario: {len(items)}")
        print(f"  • Quotation Lines: {len(q_lines)}")
        print(f"  • Cotizaciones: {len(quotes_t1) + len(quotes_t2)}")
        print(f"  • Sales Orders: 6")
        print(f"  • Facturas: {len(invoices_t1) + len(invoices_t2)}")
        print(f"\n💰 Total Facturado: ${total_invoiced:,.0f} COP")
        print(f"📅 Período: Abril - Septiembre 2025")
        print("\n¡Base de datos lista para análisis y reportes!")
        print("="*70)

if __name__ == "__main__":
    populate_database()
