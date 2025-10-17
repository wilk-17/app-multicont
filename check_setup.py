"""
Script de verificación pre-inicio
Verifica que todas las dependencias y configuraciones estén correctas antes de ejecutar la aplicación
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("  ⚠️  Se recomienda Python 3.9+")
        return False
    return True

def check_virtual_env():
    """Verificar que estamos en un entorno virtual"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print(f"✓ Entorno virtual activo: {sys.prefix}")
        return True
    else:
        print("✗ No estás en un entorno virtual")
        print("  Ejecuta: .\\venv\\Scripts\\Activate.ps1")
        return False

def check_dependencies():
    """Verificar dependencias principales"""
    required = {
        'flask': '2.3.3',
        'sqlalchemy': '2.0.20',
        'flask_sqlalchemy': '3.0.5',
        'flask_migrate': '4.0.5',
        'flasgger': '0.9.7.1',
        'psycopg2': '2.9.7'
    }
    
    all_ok = True
    for package, expected_version in required.items():
        try:
            mod = __import__(package)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✓ {package}: {version}")
        except ImportError:
            print(f"✗ {package}: NO INSTALADO")
            all_ok = False
    
    if not all_ok:
        print("\n  Ejecuta: pip install -r requirements.txt")
    return all_ok

def check_env_file():
    """Verificar archivo .env"""
    env_path = Path('.env')
    if env_path.exists():
        print(f"✓ Archivo .env encontrado")
        
        # Leer y verificar variables críticas
        with open(env_path, 'r') as f:
            content = f.read()
            
        critical_vars = ['DATABASE_URL', 'SECRET_KEY']
        missing = []
        for var in critical_vars:
            if var not in content:
                missing.append(var)
        
        if missing:
            print(f"  ⚠️  Variables faltantes: {', '.join(missing)}")
            return False
        
        # Verificar valores de ejemplo no cambiados
        if 'YOUR_PASSWORD_HERE' in content:
            print("  ⚠️  DATABASE_URL tiene password de ejemplo")
            return False
        
        if 'change-this-to-a-random-secret-key' in content:
            print("  ⚠️  SECRET_KEY no ha sido cambiada")
            return False
            
        return True
    else:
        print("✗ Archivo .env NO encontrado")
        print("  Copia .env.example a .env y configura tus credenciales")
        return False

def check_database_connection():
    """Verificar conexión a base de datos"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            print("✗ DATABASE_URL no configurada")
            return False
        
        # Intentar conexión básica
        from sqlalchemy import create_engine
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print(f"✓ Conexión a base de datos OK")
            return True
            
    except Exception as e:
        print(f"✗ Error de conexión a base de datos: {str(e)}")
        print("  Verifica que PostgreSQL esté corriendo")
        print("  Verifica las credenciales en .env")
        return False

def check_migrations():
    """Verificar estado de migraciones"""
    migrations_dir = Path('migrations')
    if migrations_dir.exists():
        versions_dir = migrations_dir / 'versions'
        if versions_dir.exists():
            migrations = list(versions_dir.glob('*.py'))
            if migrations:
                print(f"✓ Migraciones encontradas: {len(migrations)}")
                return True
        print("⚠️  No hay archivos de migración")
        print("  Ejecuta: flask db migrate -m 'Initial migration'")
        return False
    else:
        print("⚠️  Directorio migrations no existe")
        print("  Ejecuta: flask db init")
        return False

def main():
    print("=" * 60)
    print("🔍 VERIFICACIÓN PRE-INICIO - Multicont Flask API")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_env),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Database Connection", check_database_connection),
        ("Migrations", check_migrations),
    ]
    
    results = {}
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results[name] = False
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for name, result in results.items():
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    print(f"\nTotal: {passed}/{total} verificaciones pasadas")
    
    if passed == total:
        print("\n✅ ¡Todo listo! Puedes ejecutar la aplicación con:")
        print("   python run.py")
    else:
        print("\n⚠️  Hay problemas que resolver antes de ejecutar la aplicación")
        print("   Revisa los errores anteriores")
    
    print()
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
