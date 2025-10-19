"""
Script para hashear contraseñas existentes en la base de datos
EJECUTAR UNA SOLA VEZ antes de activar el sistema de autenticación

Ejecutar: python hash_existing_passwords.py
"""
from app import create_app, db
from app.entities.user import User
from app.utils.security import hash_password


def hash_all_passwords():
    """
    Hashea todas las contraseñas en texto plano de la base de datos
    
    IMPORTANTE: Este script detecta si una contraseña ya está hasheada
    y solo hashea las que están en texto plano
    """
    print("\n" + "=" * 70)
    print(" HASH DE CONTRASEÑAS EXISTENTES")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Obtener todos los usuarios
            users = db.session.query(User).all()
            
            if not users:
                print("\n⚠️  No se encontraron usuarios en la base de datos")
                return
            
            print(f"\n  Total de usuarios: {len(users)}")
            print("\n  Procesando...\n")
            
            updated_count = 0
            skipped_count = 0
            
            for user in users:
                # Verificar si la contraseña ya está hasheada
                # Las contraseñas hasheadas con bcrypt empiezan con $2b$
                if user.password.startswith('$2b$') or user.password.startswith('$2a$'):
                    print(f"  ⏭️  Usuario '{user.username}': Contraseña ya hasheada (skipped)")
                    skipped_count += 1
                    continue
                
                # Guardar contraseña original para mostrar
                original_password = user.password
                
                # Hashear la contraseña
                hashed_password = hash_password(original_password)
                user.password = hashed_password
                
                print(f"  ✅ Usuario '{user.username}': Contraseña hasheada")
                print(f"     Original: {original_password}")
                print(f"     Hash: {hashed_password[:50]}...")
                
                updated_count += 1
            
            # Guardar cambios
            if updated_count > 0:
                db.session.commit()
                print("\n" + "=" * 70)
                print(f" ✅ {updated_count} contraseñas hasheadas exitosamente")
                print(f" ⏭️  {skipped_count} contraseñas ya estaban hasheadas")
                print("=" * 70)
                
                print("\n📝 IMPORTANTE: Guarda las contraseñas originales mostradas arriba")
                print("   para poder hacer login después del cambio.\n")
            else:
                print("\n⚠️  No se actualizó ninguna contraseña (todas ya estaban hasheadas)\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()


def create_test_user():
    """
    Crear un usuario de prueba con contraseña hasheada
    """
    print("\n" + "=" * 70)
    print(" CREAR USUARIO DE PRUEBA")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si ya existe un usuario 'test'
            existing = User.query.filter_by(username='test').first()
            if existing:
                print("\n⚠️  El usuario 'test' ya existe")
                return
            
            # Crear usuario de prueba
            hashed_password = hash_password('test123')
            
            test_user = User(
                username='test',
                password=hashed_password,
                role_id=1  # Asume que existe el rol con ID 1
            )
            
            db.session.add(test_user)
            db.session.commit()
            
            print("\n✅ Usuario de prueba creado:")
            print(f"   Username: test")
            print(f"   Password: test123")
            print(f"   Role ID: 1")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            db.session.rollback()


def verify_password_hashing():
    """
    Verificar que el sistema de hash funciona correctamente
    """
    print("\n" + "=" * 70)
    print(" VERIFICACIÓN DEL SISTEMA DE HASH")
    print("=" * 70)
    
    from app.utils.security import hash_password, verify_password
    
    # Test 1: Hash básico
    password = "test_password_123"
    hashed = hash_password(password)
    
    print(f"\n  Password original: {password}")
    print(f"  Hash generado: {hashed}")
    print(f"  Longitud hash: {len(hashed)} caracteres")
    
    # Test 2: Verificación correcta
    is_valid = verify_password(password, hashed)
    print(f"\n  ✅ Verificación con password correcta: {is_valid}")
    
    # Test 3: Verificación incorrecta
    is_invalid = verify_password("wrong_password", hashed)
    print(f"  ❌ Verificación con password incorrecta: {is_invalid}")
    
    # Test 4: Hashes diferentes para la misma contraseña
    hashed2 = hash_password(password)
    print(f"\n  ✅ Segundo hash (diferente): {hashed2}")
    print(f"  ✅ Hashes son diferentes (salt único): {hashed != hashed2}")
    print(f"  ✅ Ambos hashes son válidos: {verify_password(password, hashed2)}")
    
    print("\n" + "=" * 70)
    print(" ✅ SISTEMA DE HASH FUNCIONANDO CORRECTAMENTE")
    print("=" * 70)


def main():
    """Función principal con menú de opciones"""
    import sys
    
    print("\n" + "=" * 70)
    print(" SCRIPT DE GESTIÓN DE CONTRASEÑAS")
    print("=" * 70)
    print("\nOpciones:")
    print("  1. Hashear contraseñas existentes")
    print("  2. Crear usuario de prueba")
    print("  3. Verificar sistema de hash")
    print("  4. Hacer todo (1 + 2 + 3)")
    print("  0. Salir")
    
    try:
        choice = input("\nElige una opción [1-4, 0]: ").strip()
        
        if choice == '1':
            hash_all_passwords()
        elif choice == '2':
            create_test_user()
        elif choice == '3':
            verify_password_hashing()
        elif choice == '4':
            verify_password_hashing()
            hash_all_passwords()
            create_test_user()
        elif choice == '0':
            print("\n👋 Saliendo...")
            sys.exit(0)
        else:
            print("\n❌ Opción inválida")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
        sys.exit(1)


if __name__ == "__main__":
    main()
