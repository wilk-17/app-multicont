#!/usr/bin/env python3
"""
Script de Activación Automática del Sistema de Autenticación
Ejecuta todas las tareas necesarias para activar el sistema JWT
"""

import sys
from app import create_app, db
from app.entities.user import User
from app.entities.role import Role
from app.utils.security import hash_password, verify_password

def verify_bcrypt():
    """Verifica que bcrypt funciona correctamente"""
    print("\n" + "="*70)
    print(" 🔐 VERIFICANDO SISTEMA BCRYPT")
    print("="*70)
    
    test_password = "test123"
    print(f"\n1. Hasheando contraseña de prueba: '{test_password}'")
    hashed = hash_password(test_password)
    print(f"   ✓ Hash generado: {hashed[:30]}...")
    
    print(f"\n2. Verificando contraseña correcta...")
    if verify_password(test_password, hashed):
        print("   ✓ Verificación exitosa")
    else:
        print("   ✗ ERROR: La verificación falló")
        return False
    
    print(f"\n3. Verificando contraseña incorrecta...")
    if not verify_password("wrong_password", hashed):
        print("   ✓ Rechazo correcto de contraseña incorrecta")
    else:
        print("   ✗ ERROR: No rechazó contraseña incorrecta")
        return False
    
    print("\n✅ Sistema bcrypt funciona correctamente")
    return True


def hash_existing_passwords():
    """Hashea todas las contraseñas existentes en la base de datos"""
    print("\n" + "="*70)
    print(" 🔑 HASHEANDO CONTRASEÑAS EXISTENTES")
    print("="*70)
    
    app = create_app()
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("\n⚠️  No hay usuarios en la base de datos")
            return
        
        print(f"\n📋 Se encontraron {len(users)} usuarios")
        print("\n⚠️  IMPORTANTE: Guarda estas contraseñas originales para testing:")
        print("-" * 70)
        
        original_passwords = []
        updated_count = 0
        
        for user in users:
            # Detectar si ya está hasheada (bcrypt comienza con $2b$)
            if user.password and user.password.startswith('$2b$'):
                print(f"   ⏭️  {user.username}: Ya tiene hash bcrypt - SALTANDO")
                continue
            
            # Guardar contraseña original
            original_password = user.password or "admin123"
            original_passwords.append({
                'username': user.username,
                'password': original_password
            })
            
            # Hashear
            new_hash = hash_password(original_password)
            user.password = new_hash
            updated_count += 1
            
            print(f"   ✓ {user.username}: '{original_password}' → HASHEADO")
        
        if updated_count > 0:
            db.session.commit()
            print(f"\n✅ {updated_count} contraseñas hasheadas exitosamente")
            
            print("\n" + "="*70)
            print(" 📝 CREDENCIALES PARA TESTING")
            print("="*70)
            for cred in original_passwords:
                print(f"   Usuario: {cred['username']}")
                print(f"   Password: {cred['password']}")
                print()
        else:
            print("\n✅ Todas las contraseñas ya estaban hasheadas")


def create_test_user():
    """Crea un usuario de prueba para testing"""
    print("\n" + "="*70)
    print(" 👤 CREANDO USUARIO DE PRUEBA")
    print("="*70)
    
    app = create_app()
    with app.app_context():
        # Verificar si ya existe
        existing_user = User.query.filter_by(username='testuser').first()
        if existing_user:
            print("\n⚠️  El usuario 'testuser' ya existe - SALTANDO")
            return
        
        # Obtener rol ADMIN
        admin_role = Role.query.filter_by(name='ADMIN').first()
        if not admin_role:
            print("\n⚠️  No se encontró el rol ADMIN. Creando roles...")
            # Crear roles básicos
            admin_role = Role(name='ADMIN', description='Administrador del sistema')
            manager_role = Role(name='MANAGER', description='Gerente')
            sales_role = Role(name='SALES', description='Vendedor')
            
            db.session.add_all([admin_role, manager_role, sales_role])
            db.session.commit()
            print("   ✓ Roles creados")
        
        # Crear usuario de prueba
        test_user = User(
            username='testuser',
            password=hash_password('test123'),
            role_id=admin_role.id
        )
        
        db.session.add(test_user)
        db.session.commit()
        
        print("\n✅ Usuario de prueba creado exitosamente")
        print("\n📝 Credenciales:")
        print("   Usuario: testuser")
        print("   Password: test123")
        print("   Rol: ADMIN")


def main():
    """Ejecuta todas las tareas de activación"""
    print("\n" + "="*70)
    print(" 🚀 ACTIVACIÓN AUTOMÁTICA DEL SISTEMA DE AUTENTICACIÓN")
    print("="*70)
    print("\nEste script ejecutará:")
    print("  1. Verificación del sistema bcrypt")
    print("  2. Hash de contraseñas existentes")
    print("  3. Creación de usuario de prueba")
    print("\n" + "="*70)
    
    try:
        # Paso 1: Verificar bcrypt
        if not verify_bcrypt():
            print("\n❌ ERROR: Sistema bcrypt no funciona correctamente")
            sys.exit(1)
        
        # Paso 2: Hashear contraseñas existentes
        hash_existing_passwords()
        
        # Paso 3: Crear usuario de prueba
        create_test_user()
        
        # Resumen final
        print("\n" + "="*70)
        print(" ✅ ACTIVACIÓN COMPLETADA")
        print("="*70)
        print("\n🎉 El sistema de autenticación está listo para usar")
        print("\n📚 Próximos pasos:")
        print("   1. Probar login: python test_auth_system.py")
        print("   2. Ver docs: http://127.0.0.1:5000/api/docs/")
        print("   3. Proteger endpoints críticos (ver EJEMPLO_PROTEGER_ENDPOINTS.py)")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR durante la activación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
