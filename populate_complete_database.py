"""
Script de Población Completa - Dataset ABR-SEP 2025
Adaptado a la arquitectura Clean Architecture actual
Basado en el script SQL pero ajustado a los modelos existentes
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
from app.use_cases.assignment_handler import AssignmentHandler
from app.use_cases.brand_handler import BrandHandler
from app.use_cases.inventory_item_handler import InventoryItemHandler
from app.use_cases.quote_handler import QuoteHandler
from app.use_cases.quotation_line_handler import QuotationLineHandler
from app.use_cases.sales_order_handler import SalesOrderHandler
from app.use_cases.sales_order_item_handler import SalesOrderItemHandler
from app.use_cases.invoice_handler import InvoiceHandler
from app.use_cases.invoice_item_handler import InvoiceItemHandler

from datetime import date
from decimal import Decimal

app = create_app()

def populate():
    with app.app_context():
        print("="*80)
        print("POBLACIÓN COMPLETA DE BASE DE DATOS - Dataset ABR-SEP 2025")
        print("="*80)
        
        # ============================================================
        # 1. ESTADOS Y CIUDADES (5 estados, 20 ciudades)
        # ============================================================
        print("\n[1/12] Estados y Ciudades...")
        state_h = StateHandler()
        city_h = CityHandler()
        
        states_map = {}
        for code, desc in [('CUN','Cundinamarca'),('SAN','Santander'),('ANT','Antioquia'),('VAC','Valle del Cauca'),('ATL','Atlántico')]:
            s = state_h.create(description=desc, code=code)
            states_map[code] = s
            print(f"  + Estado: {desc}")
        
        cities_map = {}
        cities_data = [
            ('BOG','Bogotá','CUN'),('SOA','Soacha','CUN'),('CHI','Chía','CUN'),('ZIP','Zipaquirá','CUN'),
            ('BGA','Bucaramanga','SAN'),('FLA','Floridablanca','SAN'),('GIR','Girón','SAN'),('PDC','Piedecuesta','SAN'),
            ('MED','Medellín','ANT'),('ENV','Envigado','ANT'),('BEL','Bello','ANT'),('ITA','Itagüí','ANT'),
            ('CLO','Cali','VAC'),('PAL','Palmira','VAC'),('YUM','Yumbo','VAC'),('BUG','Buga','VAC'),
            ('BAQ','Barranquilla','ATL'),('SOL','Soledad','ATL'),('MAL','Malambo','ATL'),('PTC','Puerto Colombia','ATL')
        ]
        for code, desc, state_code in cities_data:
            c = city_h.create(description=desc, code=code, state_id=states_map[state_code].id)
            cities_map[code] = c
            print(f"  + Ciudad: {desc} ({state_code})")
        
        # ============================================================
        # 2. ORGANIZACIONES Y SUCURSALES (7 orgs, 5 branches multiCont)
        # ============================================================
        print("\n[2/12] Organizaciones y Sucursales...")
        org_h = OrganizationHandler()
        branch_h = BranchHandler()
        
        orgs = []
        for hist, curr in [
            ('multiCont','multiCont'),
            ('Automatiza Andina SAS','Automatiza Andina SAS'),
            ('ControlTech SAS','ControlTech SAS'),
            ('Industrias del Norte SA','Industrias del Norte SA'),
            ('Vallepack LTDA','Vallepack LTDA'),
            ('Caribe Foods SA','Caribe Foods SA'),
            ('Metalúrgica Antioquia SAS','Metalúrgica Antioquia SAS')
        ]:
            o = org_h.create(historical_name=hist, current_name=curr)
            orgs.append(o)
            print(f"  + Org {o.id}: {curr}")
        
        # Sucursales de multiCont (id=1)
        branches = []
        for city_code in ['BOG','BGA','MED','CLO','BAQ']:
            b = branch_h.create(organization_id=orgs[0].id, city_id=cities_map[city_code].id)
            branches.append(b)
            print(f"  + Branch {b.id}: {cities_map[city_code].description}")
        
        # ============================================================
        # 3. PERSONAS Y EMPLEADOS (20 personas, 10 empleados)
        # ============================================================
        print("\n[3/12] Personas y Empleados...")
        person_h = PersonHandler()
        employee_h = EmployeeHandler()
        
        persons_data = [
            ('CC3001','Ana','García','Cra 10 #1-23','300200001','BOG'),
            ('CC3002','Bruno','Pineda','Cll 12 #3-45','300200002','BGA'),
            ('CC3003','Carla','Mora','Cll 8 #9-10','300200003','MED'),
            ('CC3004','Diego','Luna','Cra 45 #12-34','300200004','CLO'),
            ('CC3005','Elena','Suárez','Av 7 #98-11','300200005','BAQ'),
            ('CC3006','Felipe','Cruz','Mz 4 Cs 5','300200006','SOA'),
            ('CC3007','Gloria','Vega','Cra 70 #20-30','300200007','FLA'),
            ('CC3008','Hugo','Ríos','Cll 25 #4-55','300200008','ENV'),
            ('CC3009','Irene','Quintero','Cll 30 #6-77','300200009','PAL'),
            ('CC3010','Jorge','Nieto','Cra 15 #5-22','300200010','SOL'),
            ('CC3011','Karen','Ortiz','Cll 72 #15-33','300200011','CHI'),
            ('CC3012','Luis','Pardo','Cra 8 #14-50','300200012','GIR'),
            ('CC3013','Marta','Rey','Cll 40 #9-21','300200013','BEL'),
            ('CC3014','Nicolás','Soto','Av 13 #45-60','300200014','YUM'),
            ('CC3015','Olga','Torres','Cra 9 #20-20','300200015','MAL'),
            ('CC3016','Pablo','Uribe','Cll 12 #23-12','300200016','ZIP'),
            ('CC3017','Raquel','Valencia','Cra 22 #33-44','300200017','PDC'),
            ('CC3018','Sergio','Weber','Cll 9 #10-11','300200018','ITA'),
            ('CC3019','Tatiana','Ximénez','Cll 1 #1-1','300200019','BUG'),
            ('CC3020','Ulises','Zárate','Cra 100 #50-60','300200020','PTC')
        ]
        
        persons = []
        for dni, fname, lname, addr, phone, city_code in persons_data:
            p = person_h.create(dni=dni, first_name=fname, last_name=lname, address=addr, phone=phone, city_id=cities_map[city_code].id)
            persons.append(p)
            print(f"  + Persona {p.id}: {fname} {lname}")
        
        # Empleados (primeros 10) asignados a branches
        employees = []
        branch_idx = [0,0,0,1,1,2,2,3,3,4]  # Distribución por sucursal
        for i in range(10):
            e = employee_h.create(person_id=persons[i].id, branch_id=branches[branch_idx[i]].id)
            employees.append(e)
            print(f"  + Empleado {e.id}: {persons[i].first_name} → Branch {branches[branch_idx[i]].id}")
        
        # ============================================================
        # 4. ROLES, USUARIOS Y PERMISOS
        # ============================================================
        print("\n[4/12] Roles, Usuarios y Permisos...")
        role_h = RoleHandler()
        user_h = UserHandler()
        perm_h = PermissionHandler()
        
        roles = {}
        for role_name in ['ADMIN','MANAGER','SALES']:
            r = role_h.create(name=role_name)
            roles[role_name] = r
            print(f"  + Rol: {role_name}")
        
        # Usuarios (8 primeros empleados)
        users_data = [
            ('ana',roles['SALES'].id),('bruno',roles['SALES'].id),('carla',roles['SALES'].id),
            ('diego',roles['SALES'].id),('elena',roles['SALES'].id),
            ('felipe',roles['MANAGER'].id),('gloria',roles['MANAGER'].id),('hugo',roles['ADMIN'].id)
        ]
        
        users = []
        for username, role_id in users_data:
            u = user_h.create(username=username, password=f'hash-{username}', role_id=role_id)
            users.append(u)
            print(f"  + User: {username}")
        
        # Permisos
        for perm_name in ['READ_REPORTS','WRITE_QUOTES','APPROVE_ORDERS','ADMIN_ALL']:
            perm_h.create(name=perm_name)
            print(f"  + Permiso: {perm_name}")
        
        # ============================================================
        # 5. ASIGNACIONES (se crearán después de inventario)
        # ============================================================
        print("\n[5/12] Asignaciones... (se crearán después del inventario)")
        
        # ============================================================
        # 6. MARCAS E INVENTARIO (6 marcas, 60 items)
        # ============================================================
        print("\n[6/12] Marcas e Inventario...")
        brand_h = BrandHandler()
        item_h = InventoryItemHandler()
        
        brands_data = [
            ('Omron','Japón','www.omron.com'),
            ('ING Multicontrol','Alemania','www.ing-multicontrol.com'),
            ('Gefran','Italia','www.gefran.com'),
            ('Weidmüller','Alemania','www.weidmuller.com'),
            ('Rice-Lake','USA','www.ricelake.com'),
            ('Optec','Colombia','www.optec.com.co')
        ]
        
        brands = []
        for name, country, web in brands_data:
            b = brand_h.create(name=name, country=country, website=web)
            brands.append(b)
            print(f"  + Marca {b.id}: {name}")
        
        # Inventario (10 items por marca)
        items_data = [
            # Omron
            ('OMR-PLC-NX1P2','Controlador PLC Omron NX1P2',4500000,10,0),
            ('OMR-SEN-E3Z','Sensor fotoeléctrico Omron E3Z',180000,50,0),
            ('OMR-INV-A1000','Variador Omron A1000',6000000,5,0),
            ('OMR-HMI-NA5','HMI Omron NA5 7"',2800000,15,0),
            ('OMR-IO-NX','Módulo I/O Omron NX',850000,20,0),
            ('OMR-ENC-E6B2','Encoder Omron E6B2',450000,25,0),
            ('OMR-REL-G2R','Relé electromecánico Omron G2R',35000,100,0),
            ('OMR-SSR-G3NA','Relé estado sólido Omron G3NA',185000,30,0),
            ('OMR-PSU-S8VK','Fuente 24V Omron S8VK',320000,40,0),
            ('OMR-SAF-F3SG','Cortina seguridad Omron F3SG',3200000,8,0),
            # ING Multicontrol
            ('ING-ARR-START','Arrancador suave ING',2750000,12,1),
            ('ING-CON-24V','Fuente 24V ING',380000,35,1),
            ('ING-PLC-MC200','PLC ING MC200',3800000,10,1),
            ('ING-HMI-MC7','HMI 7" ING',1900000,18,1),
            ('ING-VFD-MC500','Variador ING MC500',5200000,7,1),
            ('ING-IO-MOD8','Módulo I/O 8ch ING',620000,25,1),
            ('ING-REL-SAF','Relé seguridad ING',580000,22,1),
            ('ING-SWI-ETH5','Switch Ethernet 5p ING',490000,30,1),
            ('ING-ENC-INC','Encoder incremental ING',380000,28,1),
            ('ING-PSU-48V','Fuente 48V ING',520000,20,1),
            # Gefran
            ('GEF-TEMP-600','Controlador temp Gefran 600',1350000,15,2),
            ('GEF-INV-ADV','Inversor frecuencia Gefran',6500000,6,2),
            ('GEF-TRANS-LIN','Transductor lineal Gefran',2100000,10,2),
            ('GEF-SSR-GQ','Relé estado sólido Gefran GQ',285000,35,2),
            ('GEF-DRIVE-AX','Servo drive Gefran AX',7800000,5,2),
            ('GEF-PRES-TRX','Transductor presión Gefran',980000,18,2),
            ('GEF-AMP-LC','Amplificador celda carga Gefran',1450000,12,2),
            ('GEF-HMI-5','HMI 5" Gefran',1680000,14,2),
            ('GEF-RTD-PT100','Sonda RTD PT100 Gefran',220000,45,2),
            ('GEF-PSU-24','Fuente 24V Gefran',380000,30,2),
            # Weidmüller
            ('WEI-BOR-TER','Bornera Weidmüller',50000,200,3),
            ('WEI-SSR-IO','Módulo IO Weidmüller',250000,40,3),
            ('WEI-PSU-24','Fuente 24V Weidmüller',400000,35,3),
            ('WEI-REL-TER','Relé interfaz Weidmüller',85000,60,3),
            ('WEI-RAIL-DIN','Riel DIN Weidmüller',35000,150,3),
            ('WEI-SW-IND8','Switch industrial 8p Weidmüller',1250000,15,3),
            ('WEI-SURGE-SPD','Protección sobretensión Weidmüller',320000,28,3),
            ('WEI-CON-PUSHIN','Conector Push-In Weidmüller',18000,300,3),
            ('WEI-MARKZ-CARD','Tarjetas marcadoras Weidmüller',12000,500,3),
            ('WEI-TOOL-CRIMP','Herramienta crimpadora Weidmüller',450000,10,3),
            # Rice-Lake
            ('RCL-BAL-IND','Indicador pesaje Rice-Lake',4000000,8,4),
            ('RCL-CEL-CARGA','Celda carga Rice-Lake',1800000,12,4),
            ('RCL-PES-PLC','Módulo pesaje PLC Rice-Lake',3800000,6,4),
            ('RCL-JBOX-4','Caja conexiones 4 celdas Rice-Lake',580000,15,4),
            ('RCL-SCALE-PLT','Báscula plataforma Rice-Lake',5500000,5,4),
            ('RCL-TRX-ANALOG','Transmisor analógico Rice-Lake',720000,18,4),
            ('RCL-WEIGH-MOD','Módulo pesaje Rice-Lake',2900000,8,4),
            ('RCL-CHECK-CKW','Checkweigher Rice-Lake',12500000,3,4),
            ('RCL-PRN-TT','Impresora térmica Rice-Lake',950000,10,4),
            ('RCL-SW-LIC','Licencia software pesaje Rice-Lake',1800000,12,4),
            # Optec
            ('OPT-SEN-IND','Sensor inductivo Optec',220000,45,5),
            ('OPT-BARR-SEG','Barrera seguridad Optec',900000,12,5),
            ('OPT-HMI-7','Panel HMI 7" Optec',1200000,15,5),
            ('OPT-PE-SENS','Sensor fotoeléctrico Optec',195000,50,5),
            ('OPT-PROX-M18','Sensor proximidad M18 Optec',165000,60,5),
            ('OPT-IO-LINK','Módulo IO-Link Master Optec',850000,18,5),
            ('OPT-CAB-M12','Cable M12 Optec',45000,100,5),
            ('OPT-BRK-ANG','Soporte bracket angular Optec',28000,120,5),
            ('OPT-PB-LED','Pulsador iluminado Optec',75000,80,5),
            ('OPT-TWR-LIGHT','Torre luminosa Optec',320000,25,5)
        ]
        
        items = {}
        for name, desc, price, qty, brand_idx in items_data:
            i = item_h.create(name=name, description=desc, price=Decimal(str(price)), quantity=qty, brand_id=brands[brand_idx].id)
            items[name] = i
            print(f"  + Item {i.id}: {name}")
        
        print(f"\n  Total items creados: {len(items)}")
        
        # Asignaciones de items a empleados
        assign_h = AssignmentHandler()
        assignments_data = [
            (0, 'OMR-PLC-NX1P2', date(2025,4,1)),
            (1, 'ING-PLC-MC200', date(2025,4,1)),
            (3, 'GEF-TEMP-600', date(2025,4,1)),
            (5, 'RCL-BAL-IND', date(2025,5,1)),
            (7, 'OMR-INV-A1000', date(2025,5,1)),
            (9, 'RCL-CEL-CARGA', date(2025,6,1)),
            (0, 'WEI-PSU-24', date(2025,7,1)),
            (6, 'GEF-INV-ADV', date(2025,8,1)),
            (4, 'WEI-SSR-IO', date(2025,8,1)),
            (2, 'OPT-HMI-7', date(2025,9,1))
        ]
        for emp_idx, item_name, assg_date in assignments_data:
            a = assign_h.create(employee_id=employees[emp_idx].id, item_id=items[item_name].id, assigned_date=assg_date)
            print(f"  + Assignment: Emp {emp_idx+1} → {item_name}")
        
        # ============================================================
        # 7-12. TRANSACCIONES DE VENTAS (ABR-SEP 2025)
        # ============================================================
        print("\n[7/12] Cotizaciones Tanda 1 (ABR-JUN)...")
        quote_h = QuoteHandler()
        qline_h = QuotationLineHandler()
        so_h = SalesOrderHandler()
        soi_h = SalesOrderItemHandler()
        inv_h = InvoiceHandler()
        invi_h = InvoiceItemHandler()
        
        # TANDA 1: ABR-JUN
        quotes_t1 = []
        # Quote 1 - Ana (emp 0) - Automatiza Andina
        q1 = quote_h.create(customer_name='Automatiza Andina SAS', date=date(2025,4,8), total=Decimal('12800000'), employee_id=employees[0].id)
        quotes_t1.append(q1)
        qline_h.create(quote_id=q1.id, item_id=items['OMR-SEN-E3Z'].id, quantity=10, price=Decimal('180000'), description='Sensores')
        qline_h.create(quote_id=q1.id, item_id=items['WEI-PSU-24'].id, quantity=5, price=Decimal('400000'), description='Fuentes')
        qline_h.create(quote_id=q1.id, item_id=items['OPT-SEN-IND'].id, quantity=5, price=Decimal('220000'), description='Sensores inductivos')
        print(f"  + Quote {q1.id}: {q1.customer_name} - ${q1.total:,.0f}")
        
        # Quote 2 - Diego (emp 3) - ControlTech - ACCEPTED
        q2 = quote_h.create(customer_name='ControlTech SAS', date=date(2025,4,15), total=Decimal('18300000'), employee_id=employees[3].id)
        quotes_t1.append(q2)
        qline_h.create(quote_id=q2.id, item_id=items['OMR-PLC-NX1P2'].id, quantity=2, price=Decimal('4500000'), description='PLC')
        qline_h.create(quote_id=q2.id, item_id=items['GEF-TEMP-600'].id, quantity=3, price=Decimal('1350000'), description='Controladores temp')
        print(f"  + Quote {q2.id}: {q2.customer_name} - ${q2.total:,.0f} [ACCEPTED]")
        
        # Quote 3 - Felipe (emp 5) - Industrias del Norte
        q3 = quote_h.create(customer_name='Industrias del Norte SA', date=date(2025,5,3), total=Decimal('15700000'), employee_id=employees[5].id)
        quotes_t1.append(q3)
        qline_h.create(quote_id=q3.id, item_id=items['ING-PLC-MC200'].id, quantity=1, price=Decimal('3800000'), description='PLC')
        qline_h.create(quote_id=q3.id, item_id=items['GEF-INV-ADV'].id, quantity=1, price=Decimal('6500000'), description='Inversor')
        qline_h.create(quote_id=q3.id, item_id=items['RCL-BAL-IND'].id, quantity=1, price=Decimal('4000000'), description='Indicador')
        print(f"  + Quote {q3.id}: {q3.customer_name} - ${q3.total:,.0f}")
        
        # Quote 4 - Hugo (emp 7) - Vallepack - REJECTED
        q4 = quote_h.create(customer_name='Vallepack LTDA', date=date(2025,5,19), total=Decimal('6900000'), employee_id=employees[7].id)
        quotes_t1.append(q4)
        qline_h.create(quote_id=q4.id, item_id=items['OMR-INV-A1000'].id, quantity=1, price=Decimal('6000000'), description='Variador')
        qline_h.create(quote_id=q4.id, item_id=items['OPT-BARR-SEG'].id, quantity=1, price=Decimal('900000'), description='Barrera')
        print(f"  + Quote {q4.id}: {q4.customer_name} - ${q4.total:,.0f} [REJECTED]")
        
        # Quote 5 - Jorge (emp 9) - Caribe Foods - ACCEPTED
        q5 = quote_h.create(customer_name='Caribe Foods SA', date=date(2025,6,6), total=Decimal('22450000'), employee_id=employees[9].id)
        quotes_t1.append(q5)
        qline_h.create(quote_id=q5.id, item_id=items['RCL-CEL-CARGA'].id, quantity=3, price=Decimal('1800000'), description='Celdas')
        qline_h.create(quote_id=q5.id, item_id=items['WEI-SSR-IO'].id, quantity=10, price=Decimal('250000'), description='Módulos')
        qline_h.create(quote_id=q5.id, item_id=items['OMR-SEN-E3Z'].id, quantity=10, price=Decimal('180000'), description='Sensores')
        print(f"  + Quote {q5.id}: {q5.customer_name} - ${q5.total:,.0f} [ACCEPTED]")
        
        # Quote 6 - Bruno (emp 1) - Metalúrgica
        q6 = quote_h.create(customer_name='Metalúrgica Antioquia SAS', date=date(2025,6,21), total=Decimal('9950000'), employee_id=employees[1].id)
        quotes_t1.append(q6)
        qline_h.create(quote_id=q6.id, item_id=items['GEF-TRANS-LIN'].id, quantity=2, price=Decimal('2100000'), description='Transductores')
        qline_h.create(quote_id=q6.id, item_id=items['ING-CON-24V'].id, quantity=5, price=Decimal('380000'), description='Fuentes')
        print(f"  + Quote {q6.id}: {q6.customer_name} - ${q6.total:,.0f}")
        
        print(f"\n[8/12] Sales Orders Tanda 1...")
        # SO de Quote 2 (Diego)
        so1 = so_h.create(quote_id=q2.id, date=date(2025,4,20), total=Decimal('18300000'), employee_id=employees[3].id)
        soi_h.create(sales_order_id=so1.id, item_id=items['OMR-PLC-NX1P2'].id, quantity=2, unit_price=Decimal('4500000'))
        soi_h.create(sales_order_id=so1.id, item_id=items['GEF-TEMP-600'].id, quantity=3, unit_price=Decimal('1350000'))
        print(f"  + SO {so1.id}: Quote {so1.quote_id} - ${so1.total:,.0f}")
        
        # SO de Quote 5 (Jorge)
        so2 = so_h.create(quote_id=q5.id, date=date(2025,6,8), total=Decimal('22450000'), employee_id=employees[9].id)
        soi_h.create(sales_order_id=so2.id, item_id=items['RCL-CEL-CARGA'].id, quantity=3, unit_price=Decimal('1800000'))
        soi_h.create(sales_order_id=so2.id, item_id=items['WEI-SSR-IO'].id, quantity=10, unit_price=Decimal('250000'))
        soi_h.create(sales_order_id=so2.id, item_id=items['OMR-SEN-E3Z'].id, quantity=10, unit_price=Decimal('180000'))
        print(f"  + SO {so2.id}: Quote {so2.quote_id} - ${so2.total:,.0f}")
        
        print(f"\n[9/12] Facturas Tanda 1...")
        # Invoice de SO1
        inv1 = inv_h.create(sales_order_id=so1.id, date=date(2025,4,21), total=Decimal('18300000'), employee_id=employees[3].id)
        invi_h.create(invoice_id=inv1.id, item_id=items['OMR-PLC-NX1P2'].id, quantity=2, unit_price=Decimal('4500000'))
        invi_h.create(invoice_id=inv1.id, item_id=items['GEF-TEMP-600'].id, quantity=3, unit_price=Decimal('1350000'))
        print(f"  + Invoice {inv1.id}: SO {inv1.sales_order_id} - ${inv1.total:,.0f}")
        
        # Invoice de SO2
        inv2 = inv_h.create(sales_order_id=so2.id, date=date(2025,6,10), total=Decimal('22450000'), employee_id=employees[9].id)
        invi_h.create(invoice_id=inv2.id, item_id=items['RCL-CEL-CARGA'].id, quantity=3, unit_price=Decimal('1800000'))
        invi_h.create(invoice_id=inv2.id, item_id=items['WEI-SSR-IO'].id, quantity=10, unit_price=Decimal('250000'))
        invi_h.create(invoice_id=inv2.id, item_id=items['OMR-SEN-E3Z'].id, quantity=10, unit_price=Decimal('180000'))
        print(f"  + Invoice {inv2.id}: SO {inv2.sales_order_id} - ${inv2.total:,.0f}")
        
        # Facturas directas
        inv3 = inv_h.create(sales_order_id=so1.id, date=date(2025,4,30), total=Decimal('8600000'), employee_id=employees[0].id)
        invi_h.create(invoice_id=inv3.id, item_id=items['WEI-PSU-24'].id, quantity=5, unit_price=Decimal('400000'))
        invi_h.create(invoice_id=inv3.id, item_id=items['OPT-SEN-IND'].id, quantity=5, unit_price=Decimal('220000'))
        invi_h.create(invoice_id=inv3.id, item_id=items['OMR-SEN-E3Z'].id, quantity=10, unit_price=Decimal('180000'))
        print(f"  + Invoice {inv3.id}: Directa Ana - ${inv3.total:,.0f}")
        
        inv4 = inv_h.create(sales_order_id=so1.id, date=date(2025,6,25), total=Decimal('6900000'), employee_id=employees[1].id)
        invi_h.create(invoice_id=inv4.id, item_id=items['GEF-TRANS-LIN'].id, quantity=2, unit_price=Decimal('2100000'))
        invi_h.create(invoice_id=inv4.id, item_id=items['ING-CON-24V'].id, quantity=5, unit_price=Decimal('380000'))
        print(f"  + Invoice {inv4.id}: Directa Bruno - ${inv4.total:,.0f}")
        
        # TANDA 2: JUL-SEP
        print(f"\n[10/12] Cotizaciones Tanda 2 (JUL-SEP)...")
        quotes_t2 = []
        
        # Quote 7 - Hugo - Vallepack
        q7 = quote_h.create(customer_name='Vallepack LTDA', date=date(2025,7,5), total=Decimal('10400000'), employee_id=employees[7].id)
        quotes_t2.append(q7)
        qline_h.create(quote_id=q7.id, item_id=items['WEI-BOR-TER'].id, quantity=80, price=Decimal('50000'))
        qline_h.create(quote_id=q7.id, item_id=items['OMR-SEN-E3Z'].id, quantity=8, price=Decimal('180000'))
        print(f"  + Quote {q7.id}: {q7.customer_name} - ${q7.total:,.0f}")
        
        # Quote 8 - Jorge - Caribe Foods - ACCEPTED
        q8 = quote_h.create(customer_name='Caribe Foods SA', date=date(2025,7,18), total=Decimal('16900000'), employee_id=employees[9].id)
        quotes_t2.append(q8)
        qline_h.create(quote_id=q8.id, item_id=items['RCL-PES-PLC'].id, quantity=1, price=Decimal('3800000'))
        qline_h.create(quote_id=q8.id, item_id=items['OMR-INV-A1000'].id, quantity=1, price=Decimal('6000000'))
        qline_h.create(quote_id=q8.id, item_id=items['OPT-HMI-7'].id, quantity=1, price=Decimal('1200000'))
        print(f"  + Quote {q8.id}: {q8.customer_name} - ${q8.total:,.0f} [ACCEPTED]")
        
        # Quote 9 - Ana - Automatiza - ACCEPTED
        q9 = quote_h.create(customer_name='Automatiza Andina SAS', date=date(2025,8,8), total=Decimal('21600000'), employee_id=employees[0].id)
        quotes_t2.append(q9)
        qline_h.create(quote_id=q9.id, item_id=items['OMR-PLC-NX1P2'].id, quantity=3, price=Decimal('4500000'))
        qline_h.create(quote_id=q9.id, item_id=items['ING-CON-24V'].id, quantity=3, price=Decimal('380000'))
        print(f"  + Quote {q9.id}: {q9.customer_name} - ${q9.total:,.0f} [ACCEPTED]")
        
        # Quote 10 - Felipe - Metalúrgica
        q10 = quote_h.create(customer_name='Metalúrgica Antioquia SAS', date=date(2025,8,22), total=Decimal('13750000'), employee_id=employees[5].id)
        quotes_t2.append(q10)
        qline_h.create(quote_id=q10.id, item_id=items['ING-ARR-START'].id, quantity=2, price=Decimal('2750000'))
        qline_h.create(quote_id=q10.id, item_id=items['WEI-PSU-24'].id, quantity=5, price=Decimal('400000'))
        print(f"  + Quote {q10.id}: {q10.customer_name} - ${q10.total:,.0f}")
        
        # Quote 11 - Elena - ControlTech
        q11 = quote_h.create(customer_name='ControlTech SAS', date=date(2025,9,9), total=Decimal('7200000'), employee_id=employees[4].id)
        quotes_t2.append(q11)
        qline_h.create(quote_id=q11.id, item_id=items['WEI-SSR-IO'].id, quantity=8, price=Decimal('250000'))
        qline_h.create(quote_id=q11.id, item_id=items['OMR-SEN-E3Z'].id, quantity=8, price=Decimal('180000'))
        print(f"  + Quote {q11.id}: {q11.customer_name} - ${q11.total:,.0f}")
        
        # Quote 12 - Gloria - Industrias del Norte - ACCEPTED
        q12 = quote_h.create(customer_name='Industrias del Norte SA', date=date(2025,9,14), total=Decimal('19300000'), employee_id=employees[6].id)
        quotes_t2.append(q12)
        qline_h.create(quote_id=q12.id, item_id=items['GEF-INV-ADV'].id, quantity=1, price=Decimal('6500000'))
        qline_h.create(quote_id=q12.id, item_id=items['GEF-TEMP-600'].id, quantity=2, price=Decimal('1350000'))
        qline_h.create(quote_id=q12.id, item_id=items['RCL-BAL-IND'].id, quantity=1, price=Decimal('4000000'))
        print(f"  + Quote {q12.id}: {q12.customer_name} - ${q12.total:,.0f} [ACCEPTED]")
        
        print(f"\n[11/12] Sales Orders Tanda 2...")
        # SO de Quote 8 (Jorge)
        so3 = so_h.create(quote_id=q8.id, date=date(2025,7,20), total=Decimal('16900000'), employee_id=employees[9].id)
        soi_h.create(sales_order_id=so3.id, item_id=items['RCL-PES-PLC'].id, quantity=1, unit_price=Decimal('3800000'))
        soi_h.create(sales_order_id=so3.id, item_id=items['OMR-INV-A1000'].id, quantity=1, unit_price=Decimal('6000000'))
        soi_h.create(sales_order_id=so3.id, item_id=items['OPT-HMI-7'].id, quantity=1, unit_price=Decimal('1200000'))
        print(f"  + SO {so3.id}: Quote {so3.quote_id} - ${so3.total:,.0f}")
        
        # SO de Quote 7 (Hugo)
        so4 = so_h.create(quote_id=q7.id, date=date(2025,7,7), total=Decimal('10400000'), employee_id=employees[7].id)
        soi_h.create(sales_order_id=so4.id, item_id=items['WEI-BOR-TER'].id, quantity=80, unit_price=Decimal('50000'))
        soi_h.create(sales_order_id=so4.id, item_id=items['OMR-SEN-E3Z'].id, quantity=8, unit_price=Decimal('180000'))
        print(f"  + SO {so4.id}: Quote {so4.quote_id} - ${so4.total:,.0f}")
        
        # SO de Quote 9 (Ana)
        so5 = so_h.create(quote_id=q9.id, date=date(2025,8,10), total=Decimal('21600000'), employee_id=employees[0].id)
        soi_h.create(sales_order_id=so5.id, item_id=items['OMR-PLC-NX1P2'].id, quantity=3, unit_price=Decimal('4500000'))
        soi_h.create(sales_order_id=so5.id, item_id=items['ING-CON-24V'].id, quantity=3, unit_price=Decimal('380000'))
        print(f"  + SO {so5.id}: Quote {so5.quote_id} - ${so5.total:,.0f}")
        
        # SO de Quote 12 (Gloria)
        so6 = so_h.create(quote_id=q12.id, date=date(2025,9,16), total=Decimal('19300000'), employee_id=employees[6].id)
        soi_h.create(sales_order_id=so6.id, item_id=items['GEF-INV-ADV'].id, quantity=1, unit_price=Decimal('6500000'))
        soi_h.create(sales_order_id=so6.id, item_id=items['GEF-TEMP-600'].id, quantity=2, unit_price=Decimal('1350000'))
        soi_h.create(sales_order_id=so6.id, item_id=items['RCL-BAL-IND'].id, quantity=1, unit_price=Decimal('4000000'))
        print(f"  + SO {so6.id}: Quote {so6.quote_id} - ${so6.total:,.0f}")
        
        print(f"\n[12/12] Facturas Tanda 2...")
        # Invoice de SO3 (Jorge)
        inv5 = inv_h.create(sales_order_id=so3.id, date=date(2025,7,21), total=Decimal('16900000'), employee_id=employees[9].id)
        invi_h.create(invoice_id=inv5.id, item_id=items['RCL-PES-PLC'].id, quantity=1, unit_price=Decimal('3800000'))
        invi_h.create(invoice_id=inv5.id, item_id=items['OMR-INV-A1000'].id, quantity=1, unit_price=Decimal('6000000'))
        invi_h.create(invoice_id=inv5.id, item_id=items['OPT-HMI-7'].id, quantity=1, unit_price=Decimal('1200000'))
        print(f"  + Invoice {inv5.id}: SO {inv5.sales_order_id} - ${inv5.total:,.0f}")
        
        # Invoice de SO4 (Hugo)
        inv6 = inv_h.create(sales_order_id=so4.id, date=date(2025,7,8), total=Decimal('10400000'), employee_id=employees[7].id)
        invi_h.create(invoice_id=inv6.id, item_id=items['WEI-BOR-TER'].id, quantity=80, unit_price=Decimal('50000'))
        invi_h.create(invoice_id=inv6.id, item_id=items['OMR-SEN-E3Z'].id, quantity=8, unit_price=Decimal('180000'))
        print(f"  + Invoice {inv6.id}: SO {inv6.sales_order_id} - ${inv6.total:,.0f}")
        
        # Invoice de SO5 (Ana)
        inv7 = inv_h.create(sales_order_id=so5.id, date=date(2025,8,11), total=Decimal('21600000'), employee_id=employees[0].id)
        invi_h.create(invoice_id=inv7.id, item_id=items['OMR-PLC-NX1P2'].id, quantity=3, unit_price=Decimal('4500000'))
        invi_h.create(invoice_id=inv7.id, item_id=items['ING-CON-24V'].id, quantity=3, unit_price=Decimal('380000'))
        print(f"  + Invoice {inv7.id}: SO {inv7.sales_order_id} - ${inv7.total:,.0f}")
        
        # Invoice de SO6 (Gloria)
        inv8 = inv_h.create(sales_order_id=so6.id, date=date(2025,9,17), total=Decimal('19300000'), employee_id=employees[6].id)
        invi_h.create(invoice_id=inv8.id, item_id=items['GEF-INV-ADV'].id, quantity=1, unit_price=Decimal('6500000'))
        invi_h.create(invoice_id=inv8.id, item_id=items['GEF-TEMP-600'].id, quantity=2, unit_price=Decimal('1350000'))
        invi_h.create(invoice_id=inv8.id, item_id=items['RCL-BAL-IND'].id, quantity=1, unit_price=Decimal('4000000'))
        print(f"  + Invoice {inv8.id}: SO {inv8.sales_order_id} - ${inv8.total:,.0f}")
        
        # Facturas directas T2
        inv9 = inv_h.create(sales_order_id=so3.id, date=date(2025,8,25), total=Decimal('9150000'), employee_id=employees[5].id)
        invi_h.create(invoice_id=inv9.id, item_id=items['ING-ARR-START'].id, quantity=2, unit_price=Decimal('2750000'))
        invi_h.create(invoice_id=inv9.id, item_id=items['WEI-PSU-24'].id, quantity=5, unit_price=Decimal('400000'))
        invi_h.create(invoice_id=inv9.id, item_id=items['OMR-SEN-E3Z'].id, quantity=5, unit_price=Decimal('180000'))
        print(f"  + Invoice {inv9.id}: Directa Felipe - ${inv9.total:,.0f}")
        
        inv10 = inv_h.create(sales_order_id=so3.id, date=date(2025,9,20), total=Decimal('6440000'), employee_id=employees[4].id)
        invi_h.create(invoice_id=inv10.id, item_id=items['WEI-SSR-IO'].id, quantity=8, unit_price=Decimal('250000'))
        invi_h.create(invoice_id=inv10.id, item_id=items['OMR-SEN-E3Z'].id, quantity=8, unit_price=Decimal('180000'))
        print(f"  + Invoice {inv10.id}: Directa Elena - ${inv10.total:,.0f}")
        
        # ============================================================
        # RESUMEN FINAL
        # ============================================================
        total_invoiced = sum([inv1.total, inv2.total, inv3.total, inv4.total, inv5.total, inv6.total, inv7.total, inv8.total, inv9.total, inv10.total])
        
        print("\n" + "="*80)
        print("✅ POBLACIÓN COMPLETADA CON ÉXITO")
        print("="*80)
        print(f"\n📊 RESUMEN DATASET ABR-SEP 2025:")
        print(f"  • Estados: 5")
        print(f"  • Ciudades: 20")
        print(f"  • Organizaciones: 7")
        print(f"  • Sucursales multiCont: 5")
        print(f"  • Personas: 20")
        print(f"  • Empleados: 10")
        print(f"  • Usuarios: 8")
        print(f"  • Roles: 3")
        print(f"  • Marcas: 6")
        print(f"  • Items inventario: 60")
        print(f"  • Cotizaciones: 12 (6 ABR-JUN + 6 JUL-SEP)")
        print(f"  • Sales Orders: 6")
        print(f"  • Facturas: 10")
        print(f"\n💰 Total Facturado: ${total_invoiced:,.0f} COP")
        print(f"📅 Período: Abril - Septiembre 2025")
        print("\n¡Base de datos lista para análisis!")
        print("="*80)

if __name__ == "__main__":
    populate()
