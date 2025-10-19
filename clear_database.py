"""
Script para BORRAR TODOS LOS DATOS de la base de datos
⚠️ ADVERTENCIA: Esta operación es IRREVERSIBLE
⚠️ Se eliminarán TODOS los registros de TODAS las tablas
"""
import sys
from app import create_app, db
from sqlalchemy import text

def confirm_deletion():
    """Solicitar confirmación del usuario antes de borrar datos."""
    print("\n" + "="*70)
    print("⚠️  ADVERTENCIA: BORRADO COMPLETO DE BASE DE DATOS")
    print("="*70)
    print("\nEsta operación eliminará TODOS los datos de las siguientes tablas:")
    print("  - Users (usuarios)")
    print("  - Roles (roles)")
    print("  - Permissions (permisos)")
    print("  - Organizations (organizaciones)")
    print("  - Branches (sucursales)")
    print("  - Employees (empleados)")
    print("  - Persons (personas)")
    print("  - Inventory Items (items de inventario)")
    print("  - Item Categories (categorías)")
    print("  - Brands (marcas)")
    print("  - Quotes (cotizaciones)")
    print("  - Sales Orders (órdenes de venta)")
    print("  - Invoices (facturas)")
    print("  - Sales Goals (metas de venta)")
    print("  - Assignments (asignaciones)")
    print("  - States y Cities (ubicaciones)")
    print("  - Y todas las tablas relacionadas...")
    print("\n⚠️  ESTA OPERACIÓN NO SE PUEDE DESHACER")
    print("="*70)
    
    response = input("\n¿Estás SEGURO de que deseas continuar? (escribe 'BORRAR TODO'): ")
    return response == "BORRAR TODO"

def delete_all_data():
    """Eliminar todos los datos de todas las tablas."""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n🔍 Verificando conexión a la base de datos...")
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"📊 Base de datos: {db_uri.split('@')[-1] if '@' in db_uri else db_uri}")
            
            # Confirmar con el usuario
            if not confirm_deletion():
                print("\n❌ Operación cancelada por el usuario.")
                print("No se eliminó ningún dato.")
                return
            
            print("\n🗑️  Iniciando borrado de datos...")
            print("-" * 70)
            
            # Lista de tablas en orden de dependencias (de hijos a padres)
            # Primero las tablas con FK, luego las tablas base
            tables_to_clear = [
                # Tablas de relaciones muchos a muchos y detalles
                'user_role',
                'assignment',
                'quotation_line',
                'quote_item',
                'sales_order_item',
                'invoice_item',
                
                # Tablas con FK a otras tablas
                'sales_goal',
                'quote',
                'sales_order',
                'invoice',
                'inventory_item',
                'employee',
                'person',
                'city',
                'branch',
                
                # Tablas base
                'state',
                'brand',
                'item_category',
                'permission',
                'role',
                'user',
                'organization',
            ]
            
            deleted_counts = {}
            
            # Usar TRUNCATE CASCADE que es más efectivo para PostgreSQL
            # TRUNCATE es más rápido y maneja automáticamente las FK
            print("✓ Usando TRUNCATE CASCADE para eliminar todos los datos")
            
            # Obtener todas las tablas de la base de datos
            inspector = db.inspect(db.engine)
            all_tables = inspector.get_table_names()
            
            # Eliminar datos tabla por tabla con TRUNCATE
            for table_name in all_tables:
                # Saltar la tabla de migraciones de alembic
                if table_name == 'alembic_version':
                    continue
                    
                try:
                    # Usar TRUNCATE con CASCADE para eliminar datos y resetear secuencias
                    # RESTART IDENTITY resetea los auto_increment
                    # CASCADE elimina datos en tablas dependientes
                    
                    # Escapar 'user' que es palabra reservada en PostgreSQL
                    table_quoted = f'"{table_name}"' if table_name == 'user' else table_name
                    
                    db.session.execute(text(f"TRUNCATE TABLE {table_quoted} RESTART IDENTITY CASCADE;"))
                    print(f"  ✓ {table_name:25} : datos eliminados y secuencia reseteada")
                    deleted_counts[table_name] = 1  # Marcamos como procesado
                        
                except Exception as e:
                    print(f"  ⚠️  Error en {table_name}: {e}")
            
            # Commit de todos los cambios
            db.session.commit()
            
            print("\n✓ Las secuencias ya fueron reseteadas automáticamente con TRUNCATE RESTART IDENTITY")
            
            print("\n" + "="*70)
            print("✅ BORRADO COMPLETO EXITOSO")
            print("="*70)
            
            total_processed = len(deleted_counts)
            print(f"\n📊 Resumen:")
            print(f"   - Total de tablas procesadas: {total_processed}")
            print(f"   - Secuencias de IDs reseteadas automáticamente")
            print(f"   - Base de datos completamente vacía")
            
            print("\n✓ La base de datos está ahora completamente vacía.")
            print("✓ Los IDs volverán a empezar desde 1.")
            print("\n💡 Puedes ejecutar los seeders para insertar datos de prueba:")
            print("   python seed_data.py")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR durante el borrado: {e}")
            print("⚠️  Se hizo rollback de los cambios.")
            sys.exit(1)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  SCRIPT DE BORRADO COMPLETO DE BASE DE DATOS")
    print("="*70)
    
    delete_all_data()
    
    print("\n✓ Script finalizado.")
    print("="*70 + "\n")
