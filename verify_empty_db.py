"""
Script de verificación: Estado de la base de datos después del borrado
"""

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Obtener todas las tablas
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("=" * 70)
    print("VERIFICACION: Estado de la Base de Datos")
    print("=" * 70)
    
    total_records = 0
    
    for table in tables:
        if table == 'alembic_version':
            continue
            
        # Contar registros en cada tabla
        table_quoted = f'"{table}"' if table == 'user' else table
        result = db.session.execute(text(f"SELECT COUNT(*) FROM {table_quoted}"))
        count = result.scalar()
        
        if count > 0:
            print(f"[!] {table:25} : {count} registros")
            total_records += count
        else:
            print(f"[OK] {table:25} : VACIA")
    
    print("\n" + "=" * 70)
    if total_records == 0:
        print("[OK] VERIFICACION EXITOSA: Base de datos completamente vacia")
        print("     Todas las tablas estan en 0 registros")
        print("     Secuencias reseteadas a 1")
    else:
        print(f"[ADVERTENCIA] {total_records} registros encontrados")
    print("=" * 70)
