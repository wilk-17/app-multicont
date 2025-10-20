"""
Script para hashear las contraseñas de los 8 usuarios existentes
Actualiza los passwords de 'hash-{username}' a hashes bcrypt reales
"""
from app import create_app, db
from app.entities.user import User
from app.utils.security import hash_password

def hash_all_passwords():
    """Hashea las contraseñas de todos los usuarios"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("ACTUALIZANDO CONTRASEÑAS DE USUARIOS")
        print("=" * 60)
        
        # Obtener todos los usuarios
        users = User.query.all()
        
        if not users:
            print("❌ No hay usuarios en la base de datos")
            return
        
        print(f"\n✓ Encontrados {len(users)} usuarios\n")
        
        # Mapeo de usuarios a contraseñas simples para testing
        # En producción, estos deberían ser passwords fuertes
        password_mapping = {
            'ana': 'ana123',
            'bruno': 'bruno123',
            'carla': 'carla123',
            'diego': 'diego123',
            'elena': 'elena123',
            'felipe': 'felipe123',
            'gloria': 'gloria123',
            'hugo': 'hugo123'
        }
        
        updated_count = 0
        
        for user in users:
            # Si el password ya está hasheado con bcrypt, skip
            if user.password.startswith('$2b$'):
                print(f"   [SKIP] {user.username} - Ya tiene hash bcrypt")
                continue
            
            # Obtener password simple del mapeo
            plain_password = password_mapping.get(user.username, f'{user.username}123')
            
            # Hashear password
            hashed = hash_password(plain_password)
            
            # Actualizar en base de datos
            user.password = hashed
            
            print(f"   [OK] {user.username}")
            print(f"        Password: {plain_password}")
            print(f"        Hash: {hashed[:50]}...\n")
            
            updated_count += 1
        
        # Commit cambios
        try:
            db.session.commit()
            print("=" * 60)
            print(f"✅ ÉXITO: {updated_count} contraseñas actualizadas")
            print("=" * 60)
            print("\n📋 USUARIOS PARA TESTING EN SWAGGER:")
            print("-" * 60)
            print(f"{'Usuario':<15} {'Password':<15} {'Rol':<10}")
            print("-" * 60)
            
            for user in users:
                from app.entities.role import Role
                role = Role.query.get(user.role_id)
                role_name = role.name if role else 'UNKNOWN'
                plain_pass = password_mapping.get(user.username, f'{user.username}123')
                print(f"{user.username:<15} {plain_pass:<15} {role_name:<10}")
            
            print("-" * 60)
            print("\n💡 INSTRUCCIONES:")
            print("1. Ir a http://127.0.0.1:5000/api/docs/")
            print("2. Probar POST /api/auth/login con username y password")
            print("3. Copiar 'access_token' de la respuesta")
            print("4. Click en botón 'Authorize' arriba a la derecha")
            print("5. Pegar token en el campo (sin 'Bearer', solo el token)")
            print("6. Probar endpoints protegidos\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR al actualizar contraseñas: {e}")
            raise

if __name__ == '__main__':
    hash_all_passwords()
