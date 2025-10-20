"""
Script para revisar el estado completo de la base de datos
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from sqlalchemy import inspect, text

def check_database():
    """Revisa el estado completo de la base de datos"""
    app = create_app()
    
    with app.app_context():
        print("="*80)
        print("REVISIÓN COMPLETA DE LA BASE DE DATOS")
        print("="*80)
        
        # Obtener inspector
        inspector = inspect(db.engine)
        
        # 1. Listar todas las tablas
        print("\n1. TABLAS EN LA BASE DE DATOS:")
        print("-"*80)
        tables = inspector.get_table_names()
        if tables:
            for i, table in enumerate(sorted(tables), 1):
                print(f"   {i:2d}. {table}")
        else:
            print("   ⚠️  NO HAY TABLAS EN LA BASE DE DATOS")
        
        print(f"\n   Total de tablas: {len(tables)}")
        
        # 2. Verificar tablas específicas importantes
        print("\n2. VERIFICACIÓN DE TABLAS CRÍTICAS:")
        print("-"*80)
        critical_tables = ['user', 'role', 'organization', 'branch', 'employee', 
                          'inventory_item', 'quote', 'sales_order', 'invoice']
        
        for table in critical_tables:
            exists = table in tables
            status = "✓ EXISTE" if exists else "✗ NO EXISTE"
            print(f"   {status:12} - {table}")
        
        # 3. Contar registros en cada tabla
        print("\n3. CANTIDAD DE REGISTROS POR TABLA:")
        print("-"*80)
        
        for table in sorted(tables):
            try:
                result = db.session.execute(text(f'SELECT COUNT(*) FROM "{table}"'))
                count = result.scalar()
                print(f"   {table:30} - {count:5d} registros")
            except Exception as e:
                print(f"   {table:30} - ERROR: {str(e)[:40]}")
        
        # 4. Verificar datos en tabla 'role'
        if 'role' in tables:
            print("\n4. CONTENIDO DE LA TABLA 'role':")
            print("-"*80)
            try:
                result = db.session.execute(text('SELECT id, name, description FROM "role"'))
                roles = result.fetchall()
                if roles:
                    for role in roles:
                        print(f"   ID: {role[0]:2d} | Name: {role[1]:15s} | Desc: {role[2] or 'N/A'}")
                else:
                    print("   ⚠️  Tabla 'role' está vacía")
            except Exception as e:
                print(f"   ERROR: {e}")
        
        # 5. Verificar datos en tabla 'user'
        if 'user' in tables:
            print("\n5. CONTENIDO DE LA TABLA 'user':")
            print("-"*80)
            try:
                result = db.session.execute(text('SELECT id, username, role_id FROM "user"'))
                users = result.fetchall()
                if users:
                    for user in users:
                        print(f"   ID: {user[0]:2d} | Username: {user[1]:15s} | Role ID: {user[2]}")
                else:
                    print("   ⚠️  Tabla 'user' está vacía")
            except Exception as e:
                print(f"   ERROR: {e}")
        
        # 6. Verificar datos en tabla 'organization'
        if 'organization' in tables:
            print("\n6. CONTENIDO DE LA TABLA 'organization':")
            print("-"*80)
            try:
                result = db.session.execute(text('SELECT id, historical_name, current_name FROM "organization" LIMIT 5'))
                orgs = result.fetchall()
                if orgs:
                    for org in orgs:
                        print(f"   ID: {org[0]:2d} | Historical: {org[1][:30]:30s} | Current: {org[2][:30]:30s}")
                else:
                    print("   ⚠️  Tabla 'organization' está vacía")
            except Exception as e:
                print(f"   ERROR: {e}")
        
        # 7. Verificar datos en tabla 'branch'
        if 'branch' in tables:
            print("\n7. CONTENIDO DE LA TABLA 'branch':")
            print("-"*80)
            try:
                result = db.session.execute(text('SELECT id, organization_id, city_id FROM "branch" LIMIT 5'))
                branches = result.fetchall()
                if branches:
                    for branch in branches:
                        print(f"   ID: {branch[0]:2d} | Org ID: {branch[1]:3d} | City ID: {branch[2]:3d}")
                else:
                    print("   ⚠️  Tabla 'branch' está vacía")
            except Exception as e:
                print(f"   ERROR: {e}")
        
        # 8. Verificar datos en tabla 'employee'
        if 'employee' in tables:
            print("\n8. CONTENIDO DE LA TABLA 'employee':")
            print("-"*80)
            try:
                result = db.session.execute(text('SELECT id, person_id, branch_id FROM "employee" LIMIT 5'))
                employees = result.fetchall()
                if employees:
                    for emp in employees:
                        print(f"   ID: {emp[0]:2d} | Person ID: {emp[1]:3d} | Branch ID: {emp[2]:3d}")
                else:
                    print("   ⚠️  Tabla 'employee' está vacía")
            except Exception as e:
                print(f"   ERROR: {e}")
        
        # 9. Verificar datos en tabla 'inventory_item'
        if 'inventory_item' in tables:
            print("\n9. CONTENIDO DE LA TABLA 'inventory_item':")
            print("-"*80)
            try:
                result = db.session.execute(text('SELECT id, name, price, quantity FROM "inventory_item" LIMIT 5'))
                items = result.fetchall()
                if items:
                    for item in items:
                        print(f"   ID: {item[0]:2d} | Name: {item[1][:30]:30s} | Price: ${float(item[2]):10.2f} | Qty: {item[3]:3d}")
                else:
                    print("   ⚠️  Tabla 'inventory_item' está vacía")
            except Exception as e:
                print(f"   ERROR: {e}")
        
        # 10. Verificar estado de migraciones
        print("\n10. ESTADO DE MIGRACIONES (alembic_version):")
        print("-"*80)
        try:
            result = db.session.execute(text('SELECT version_num FROM alembic_version'))
            version = result.scalar()
            print(f"   Versión actual: {version}")
        except Exception as e:
            print(f"   ERROR: {e}")
        
        print("\n" + "="*80)
        print("REVISIÓN COMPLETADA")
        print("="*80 + "\n")

if __name__ == '__main__':
    try:
        check_database()
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
