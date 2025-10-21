"""
Comprehensive population script for Multicont - Mechatronics dataset

Creates:
 - >15 organizations (includes 'ING Multicontrol') across different cities/departments
 - 5 branches for ING Multicontrol (Bogotá, Medellín, Cali, Ibagué, Cartagena)
 - Minimum 14 employees distributed across those 5 branches
 - 6 mechatronics brands and a representative inventory for each
 - Sales / invoices / quotes spread across Q1, Q2 and Q3 for realistic time-series

Usage:
    python scripts/setup/populate_mechatronics_complete.py [--reset]

Options:
    --reset   : delete seeded data first (idempotent run)

This script is idempotent (checks by unique keys) and wrapped in transactions.
"""
import sys
import os
from datetime import datetime, date
from random import choice, randint, seed

seed(42)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import text
from app import create_app, db
from app.entities.state import State
from app.entities.city import City
from app.entities.organization import Organization
from app.entities.branch import Branch
from app.entities.person import Person
from app.entities.employee import Employee
from app.entities.brand import Brand
from app.entities.item_category import ItemCategory
from app.entities.inventory_item import InventoryItem
from app.entities.role import Role
from app.entities.user import User
from app.entities.user_role import UserRole
from app.entities.quote import Quote
from app.entities.quotation_line import QuotationLine
from app.entities.sales_order import SalesOrder
from app.entities.sales_order_item import SalesOrderItem
from app.entities.invoice import Invoice
from app.entities.invoice_item import InvoiceItem

from werkzeug.security import generate_password_hash


MECH_BRANDS = [
    'OMRON',
    'ING Multicontrol',
    'Gefran',
    'Weidmüller',
    'Rice Lake',
    'Optec'
]

CITIES_TO_CREATE = [
    # (state_code, state_name, city_code, city_name, department)
    ('CUN', 'Cundinamarca', 'BOG', 'Bogotá'),
    ('ANT', 'Antioquia', 'MED', 'Medellín'),
    ('VAL', 'Valle del Cauca', 'CAL', 'Cali'),
    ('TOL', 'Tolima', 'IBA', 'Ibagué'),
    ('CAR', 'Bolívar', 'CTG', 'Cartagena'),
]

ADDITIONAL_LOCATIONS = [
    ('ATL', 'Atlántico', 'BAR', 'Barranquilla'),
    ('SAN', 'Santander', 'BDA', 'Bucaramanga'),
    ('CUN', 'Cundinamarca', 'FAC', 'Facatativá'),
    ('ANT', 'Antioquia', 'RND', 'Rionegro'),
    ('VAL', 'Valle del Cauca', 'PTO', 'Palmira'),
    ('NAR', 'Nariño', 'PPT', 'Pasto'),
    ('CAQ', 'Cauca', 'POP', 'Popayán'),
    ('BOY', 'Boyacá', 'TUN', 'Tunja'),
    ('MAG', 'Magdalena', 'SMR', 'Santa Marta'),
    ('CHO', 'Chocó', 'QUI', 'Quibdó'),
]


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='Populate database with mechatronics dataset')
    parser.add_argument('--reset', action='store_true', help='Delete seeded data before populating')
    return parser.parse_args()


def delete_seeded(session):
    """Attempt an ordered deletion of data created by this script. Uses ORM delete for portability.
    This is conservative and only deletes records that match our seeded markers (brand names and organization name patterns).
    """
    print('⏳ Resetting seeded data (best-effort) ...')
    try:
        # invoice items/orders/quotes first
        session.execute(text('DELETE FROM invoice_item'))
        session.execute(text('DELETE FROM invoice'))
        session.execute(text('DELETE FROM sales_order_item'))
        session.execute(text('DELETE FROM sales_order'))
        session.execute(text('DELETE FROM quotation_line'))
        session.execute(text('DELETE FROM quote'))

        # assignments, employees, persons
        session.execute(text('DELETE FROM employee'))
        session.execute(text('DELETE FROM person'))

        # inventory and categories and brands
        session.execute(text("DELETE FROM inventory_item WHERE name ILIKE 'OMR_%' OR name ILIKE 'RC_%' OR name ILIKE 'GF_%' OR name ILIKE 'WM_%' OR name ILIKE 'RL_%' OR brand_id IN (SELECT id FROM brand WHERE name IN ('OMRON','ING Multicontrol','Gefran','Weidmüller','Rice Lake','Optec'))"))
        session.execute(text("DELETE FROM brand WHERE name IN ('OMRON','ING Multicontrol','Gefran','Weidmüller','Rice Lake','Optec')"))

        # branches and organizations created by this script
        session.execute(text("DELETE FROM branch WHERE id IN (SELECT b.id FROM branch b JOIN organization o ON o.id = b.organization_id WHERE o.current_name ILIKE '%Multicontrol%' OR o.current_name ILIKE '%SeedCo%')"))
        session.execute(text("DELETE FROM organization WHERE current_name ILIKE '%Multicontrol%' OR current_name ILIKE 'SeedCo %'"))

        # cities & states created by this run (conservative: we won't drop states that have other data)
        session.execute(text("DELETE FROM city WHERE code IN ('BOG','MED','CAL','IBA','CTG')"))
        # roles/users created by seeding
        session.execute(text("DELETE FROM user_role WHERE user_id IN (SELECT id FROM \"user\" WHERE username ILIKE 'seed_%')"))
        session.execute(text("DELETE FROM \"user\" WHERE username ILIKE 'seed_%'"))
        session.execute(text("DELETE FROM role WHERE name ILIKE 'SEED_%'"))

        session.commit()
        print('✅ Reset completed (best-effort).')
    except Exception as e:
        session.rollback()
        print('⚠️ Reset encountered an error (continuing):', e)


def get_or_create_state(session, code, description):
    state = session.query(State).filter_by(code=code).first()
    if not state:
        state = State(description=description, code=code)
        session.add(state)
        session.flush()
        print(f"   Created state: {description} ({code})")
    return state


def get_or_create_city(session, code, description, state_id):
    city = session.query(City).filter_by(code=code).first()
    if not city:
        city = City(description=description, state_id=state_id, code=code)
        session.add(city)
        session.flush()
        print(f"   Created city: {description} ({code})")
    return city


def seed_brands(session):
    existing = {b.name for b in session.query(Brand).filter(Brand.name.in_(MECH_BRANDS)).all()}
    for name in MECH_BRANDS:
        if name not in existing:
            brand = Brand(name=name, description=f'Marca {name} (seeded)')
            session.add(brand)
            print(f"   Brand created: {name}")
    session.flush()


def seed_organizations_and_branches(session):
    # Create ING Multicontrol as required
    ing = session.query(Organization).filter(Organization.current_name=='ING Multicontrol').first()
    if not ing:
        ing = Organization(historical_name='ING Multicontrol S.A.S. (seed)', current_name='ING Multicontrol')
        session.add(ing)
        session.flush()
        print('   Created organization: ING Multicontrol')

    # Create additional organizations (>15 total). We'll create 16 in total including ING
    total_needed = 16
    existing_orgs = session.query(Organization).count()
    to_create = max(0, total_needed - existing_orgs)

    for i in range(to_create):
        name = f'SeedCo {i+1}'
        org = Organization(historical_name=name + ' (hist)', current_name=name)
        session.add(org)
    session.flush()
    print(f'   Ensured >={total_needed} organizations present (including ING Multicontrol)')

    # Create branches for ING Multicontrol in the 5 required cities
    branch_map = {}
    for state_code, state_name, city_code, city_name in CITIES_TO_CREATE:
        state = get_or_create_state(session, state_code, state_name)
        city = get_or_create_city(session, city_code, city_name, state.id)

        # branch unique by organization+city
        branch = session.query(Branch).filter_by(organization_id=ing.id, city_id=city.id).first()
        if not branch:
            branch = Branch(organization_id=ing.id, city_id=city.id)
            session.add(branch)
            session.flush()
            print(f'   Created branch for ING Multicontrol in {city_name}')
        branch_map[city_code] = branch

    # Also create at least one branch for several other organizations to spread companies across cities
    other_orgs = session.query(Organization).filter(Organization.current_name != 'ING Multicontrol').limit(10).all()
    idx = 0
    for org in other_orgs:
        # rotate locations from additional list
        loc = ADDITIONAL_LOCATIONS[idx % len(ADDITIONAL_LOCATIONS)]
        state = get_or_create_state(session, loc[0], loc[1])
        city = get_or_create_city(session, loc[2], loc[3], state.id)
        existing = session.query(Branch).filter_by(organization_id=org.id, city_id=city.id).first()
        if not existing:
            b = Branch(organization_id=org.id, city_id=city.id)
            session.add(b)
        idx += 1

    session.flush()
    return branch_map


def seed_persons_and_employees(session, branch_map):
    """Create at least 14 employees across the 5 specific branches (Bogotá, Medellín, Cali, Ibagué, Cartagena).
    We'll name users as 'seed_emp_01'.. and create Person + Employee rows.
    """
    employees_needed = 14
    created = 0
    persons = []
    # ensure branch_map has entries for the 5 city codes
    city_codes = ['BOG','MED','CAL','IBA','CTG']
    # distribute employees as evenly as possible
    per_branch = [employees_needed // len(city_codes)] * len(city_codes)
    for i in range(employees_needed % len(city_codes)):
        per_branch[i] += 1

    for idx, city_code in enumerate(city_codes):
        branch = branch_map.get(city_code)
        count = per_branch[idx]
        for j in range(count):
            seq = created + 1
            username = f'seed_emp_{seq:02d}'
            # person unique by dni
            dni = f'EMP{10000+seq}'
            person = session.query(Person).filter_by(dni=dni).first()
            if not person:
                person = Person(first_name=f'Emp{seq}', last_name='Seed', dni=dni, phone=f'+57 300 {1000000+seq}', city_id=branch.city_id)
                session.add(person)
                session.flush()
            # create employee row
            existing_emp = session.query(Employee).filter_by(person_id=person.id, branch_id=branch.id).first()
            if not existing_emp:
                emp = Employee(person_id=person.id, branch_id=branch.id)
                session.add(emp)
                created += 1
            else:
                created += 1

    # commit persons & employees
    session.flush()
    print(f'   Created/ensured {created} employees across 5 branches')


def seed_item_categories(session):
    cat_names = ['IC', 'AT', 'SAFETY', 'PESAJE', 'ACCESSORIES']
    for name in cat_names:
        # ItemCategory only has 'name' field
        exists = session.query(ItemCategory).filter_by(name=name).first()
        if not exists:
            c = ItemCategory(name=name)
            session.add(c)
    session.flush()


def seed_inventory(session):
    # ensure our brands
    seed_brands(session)
    # ensure categories
    seed_item_categories(session)

    # build a representative inventory using brand objects
    brand_objs = {b.name: b for b in session.query(Brand).filter(Brand.name.in_(MECH_BRANDS)).all()}
    categories = session.query(ItemCategory).all()
    cat_map = {c.name if hasattr(c,'name') else str(c.id): c.id for c in categories}

    # small helper to add item if missing
    def add_item(sku_prefix, name, brand_name, category_code, price_range=(100000,2000000), qty_range=(1,50)):
        brand_obj = brand_objs.get(brand_name)
        if not brand_obj:
            return
        
        # Check if item already exists
        exists = session.query(InventoryItem).filter(
            InventoryItem.name==name, 
            InventoryItem.brand_id==brand_obj.id
        ).first()
        if exists:
            return
        
        price = randint(*price_range)
        qty = randint(*qty_range)
        brand_id = brand_obj.id
        category_id = None
        
        # pick category id by code if available
        for c in categories:
            if getattr(c,'name',None) == category_code or getattr(c,'code',None) == category_code:
                category_id = c.id
                break
        
        # Create item with correct constructor signature
        item = InventoryItem(
            name=name, 
            price=price, 
            quantity=qty, 
            description=f'{name} - {brand_name}', 
            category_id=category_id, 
            brand_id=brand_id
        )
        session.add(item)

    # Use representative items inspired by the sample list (abbreviated names)
    # OMRON items
    add_item('OMR', 'E2FMX5B1M1 - Sensor Inductivo 18mm', 'OMRON', 'IC', (40000,120000), (5,30))
    add_item('OMR', 'R7DBP04H - Drive para servo 200V 400W', 'OMRON', 'AT', (800000,2000000), (1,6))
    add_item('OMR', 'R88MG40030HS2 - Servomotor 200V 400W', 'OMRON', 'AT', (600000,1800000), (1,8))
    add_item('OMR', 'E32CC200 - Fibra Optica Autoreflex', 'OMRON', 'IC', (30000,90000), (10,80))

    # ING Multicontrol items (our company brand)
    add_item('ING', 'ING-MC-PLC-1000 - PLC Industria Basico', 'ING Multicontrol', 'AT', (200000,1000000), (2,15))
    add_item('ING', 'ING-MC-ENC-01 - Encoder Incremental', 'ING Multicontrol', 'IC', (50000,250000), (5,25))

    # Gefran - sensors / controllers
    add_item('GF', 'GF-TEMP-CTRL-48 - Control de Temperatura 48x48', 'Gefran', 'IC', (120000,450000), (3,20))
    add_item('GF', 'GF-LOAD-RL - Relé de Monitoreo', 'Gefran', 'SAFETY', (80000,220000), (2,10))

    # Weidmüller - connectivity
    add_item('WM', 'WM-CON-M12-4P - Conector M12 4p', 'Weidmüller', 'IC', (5000,25000), (20,200))
    add_item('WM', 'WM-PS-24V-10A - Fuente 24V 10A', 'Weidmüller', 'IC', (120000,600000), (2,20))

    # Rice Lake - pesaje
    add_item('RL', 'RLM87031 - Celda de carga monopunto 200kg', 'Rice Lake', 'PESAJE', (250000,1200000), (1,10))
    add_item('RL', 'RL-SUM-10CH - Caja sumadora 10 canales', 'Rice Lake', 'PESAJE', (400000,1600000), (1,5))

    # Optec - power / control
    add_item('OP', 'OP-TA48-25 - Relé Estado Solido 25A', 'Optec', 'IC', (45000,180000), (2,30))
    add_item('OP', 'OP-TV24A25 - Dimmer control fase', 'Optec', 'IC', (70000,250000), (1,10))

    session.flush()
    print('   Inventory seeded (representative items created)')


def seed_quarterly_sales(session):
    """Create quotes/orders/invoices spread across Q1, Q2, Q3 for realism.
    We'll pick random inventory items and create small transactions dated in the correct ranges.
    """
    def date_in_range(year, month_start, month_end):
        m = randint(month_start, month_end)
        d = randint(1, 28)
        return date(year, m, d)

    # pick some users to attribute sales to; if not found create seeded sales user
    sales_user = session.query(User).filter_by(username='seed_sales').first()
    if not sales_user:
        role_sales = session.query(Role).filter_by(name='SALES').first()
        if not role_sales:
            role_sales = Role(name='SALES')
            session.add(role_sales)
            session.flush()
        # User requires (username, password, role_id)
        sales_user = User(username='seed_sales', password=generate_password_hash('salespass'), role_id=role_sales.id)
        session.add(sales_user)
        session.flush()

    items = session.query(InventoryItem).limit(20).all()
    if not items:
        print('   No inventory items found for sales seeding; skipping')
        return

    # Get first employee for linking
    first_employee = session.query(Employee).first()
    if not first_employee:
        print('   No employees found for sales seeding; skipping')
        return

    def create_transaction(transaction_date, suffix):
        # Quote: (customer_name, date, total=0, employee_id=None)
        q = Quote(
            customer_name=f'Cliente {suffix}',
            date=transaction_date,
            total=0,
            employee_id=first_employee.id
        )
        session.add(q)
        session.flush()
        
        # add 1-3 quotation lines
        # QuotationLine: (quote_id, item_id, quantity, price, description=None)
        total = 0
        for _ in range(randint(1,3)):
            it = choice(items)
            qty = randint(1,5)
            price = float(it.price)
            subtotal = price * qty
            total += subtotal
            line = QuotationLine(
                quote_id=q.id,
                item_id=it.id,
                quantity=qty,
                price=price,
                description=f'{it.name} x{qty}'
            )
            session.add(line)
        q.total = total
        session.flush()
        
        # Convert to sales order
        # SalesOrder: (quote_id, date, total=0, employee_id=None)
        so = SalesOrder(
            quote_id=q.id,
            date=transaction_date,
            total=total,
            employee_id=first_employee.id
        )
        session.add(so)
        session.flush()
        
        # Add sales order items
        # SalesOrderItem: (sales_order_id, item_id, quantity)
        for line in session.query(QuotationLine).filter_by(quote_id=q.id).all():
            soi = SalesOrderItem(
                sales_order_id=so.id,
                item_id=line.item_id,
                quantity=line.quantity
            )
            session.add(soi)
        session.flush()
        
        # Create invoice
        # Invoice: (sales_order_id, date, total=0, quotation_line_id=None, employee_id=None)
        inv = Invoice(
            sales_order_id=so.id,
            date=transaction_date,
            total=total,
            employee_id=first_employee.id
        )
        session.add(inv)
        session.flush()
        
        # Add invoice items
        # InvoiceItem: (invoice_id, item_id, quantity, price)
        for soi in session.query(SalesOrderItem).filter_by(sales_order_id=so.id).all():
            item = session.query(InventoryItem).get(soi.item_id)
            ii = InvoiceItem(
                invoice_id=inv.id,
                item_id=soi.item_id,
                quantity=soi.quantity,
                price=float(item.price)
            )
            session.add(ii)
        session.flush()

    year = datetime.utcnow().year
    # Q1: Jan-Mar
    for i in range(3):
        d = date_in_range(year, 1, 3)
        create_transaction(d, f'Q1-{i+1}')
    # Q2: Apr-Jun
    for i in range(3):
        d = date_in_range(year, 4, 6)
        create_transaction(d, f'Q2-{i+1}')
    # Q3: Jul-Sep
    for i in range(3):
        d = date_in_range(year, 7, 9)
        create_transaction(d, f'Q3-{i+1}')

    print('   Quarterly sales data (Q1-Q3) created')


def main():
    args = parse_args()
    app = create_app()

    with app.app_context():
        session = db.session
        if args.reset:
            delete_seeded(session)

        try:
            # wrap all seeding in a transaction and commit at the end
            # seed_brands returns None, just call it directly
            seed_brands(session)
            
            # 1. ensure states/cities and organizations + branches
            branch_map = seed_organizations_and_branches(session)
            # 2. persons & employees
            seed_persons_and_employees(session, branch_map)
            # 3. inventory
            seed_inventory(session)
            # 4. quarterly sales
            seed_quarterly_sales(session)
            session.commit()
            print('\n🎉 Database population complete — mechatronics dataset seeded.')
        except Exception as e:
            session.rollback()
            print('❌ Population failed:', e)
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    main()
