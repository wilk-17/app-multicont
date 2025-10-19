"""
Script para poblar la tabla de permisos con los 16 permisos definidos en ROLE_PERMISSIONS
Estos permisos corresponden al sistema RBAC implementado
"""
from app import create_app, db
from app.entities.permission import Permission

def populate_permissions():
    """Pobla la tabla de permisos con todos los permisos del sistema"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("POBLANDO TABLA DE PERMISOS")
        print("=" * 60)
        
        # Definición de permisos según ROLE_PERMISSIONS matrix
        permissions_data = [
            # INVENTORY PERMISSIONS (4)
            {'name': 'inventory:read', 'description': 'Ver inventario y productos'},
            {'name': 'inventory:write', 'description': 'Crear y editar productos en inventario'},
            {'name': 'inventory:delete', 'description': 'Eliminar productos del inventario'},
            {'name': 'inventory:manage', 'description': 'Gestión completa de inventario'},
            
            # SALES PERMISSIONS (6)
            {'name': 'sales:read', 'description': 'Ver cotizaciones, órdenes y ventas'},
            {'name': 'sales:create_quote', 'description': 'Crear cotizaciones'},
            {'name': 'sales:approve_quote', 'description': 'Aprobar cotizaciones'},
            {'name': 'sales:create_order', 'description': 'Crear órdenes de venta'},
            {'name': 'sales:create_invoice', 'description': 'Crear facturas'},
            {'name': 'sales:delete', 'description': 'Eliminar cotizaciones, órdenes y facturas'},
            
            # REPORTS PERMISSIONS (3)
            {'name': 'reports:read', 'description': 'Ver reportes y métricas'},
            {'name': 'reports:export', 'description': 'Exportar reportes'},
            {'name': 'dashboard:view', 'description': 'Acceder al dashboard principal'},
            
            # USERS PERMISSIONS (3)
            {'name': 'users:read', 'description': 'Ver usuarios del sistema'},
            {'name': 'users:write', 'description': 'Crear y editar usuarios'},
            {'name': 'users:delete', 'description': 'Eliminar usuarios'},
            
            # ADMIN PERMISSION (1)
            {'name': 'admin:all', 'description': 'Acceso completo a todas las funcionalidades'}
        ]
        
        print(f"\n✓ Definidos {len(permissions_data)} permisos\n")
        
        created_count = 0
        existing_count = 0
        
        for perm_data in permissions_data:
            # Verificar si ya existe
            existing = Permission.query.filter_by(name=perm_data['name']).first()
            
            if existing:
                print(f"   [SKIP] {perm_data['name']} - Ya existe")
                existing_count += 1
            else:
                # Crear nuevo permiso
                permission = Permission(
                    name=perm_data['name']
                )
                db.session.add(permission)
                print(f"   [OK] {perm_data['name']}")
                print(f"        {perm_data['description']}\n")
                created_count += 1
        
        # Commit cambios
        try:
            db.session.commit()
            print("=" * 60)
            print(f"✅ ÉXITO: {created_count} permisos creados, {existing_count} ya existían")
            print("=" * 60)
            
            # Mostrar matriz de permisos por rol
            print("\n📋 MATRIZ DE PERMISOS POR ROL:")
            print("=" * 60)
            
            role_permissions = {
                'ADMIN': [
                    'inventory:read', 'inventory:write', 'inventory:delete', 'inventory:manage',
                    'sales:read', 'sales:create_quote', 'sales:approve_quote',
                    'sales:create_order', 'sales:create_invoice', 'sales:delete',
                    'reports:read', 'reports:export', 'dashboard:view',
                    'users:read', 'users:write', 'users:delete',
                    'admin:all'
                ],
                'MANAGER': [
                    'inventory:read', 'inventory:write',
                    'sales:read', 'sales:create_quote', 'sales:approve_quote',
                    'sales:create_order', 'sales:create_invoice', 'sales:delete',
                    'reports:read', 'reports:export', 'dashboard:view',
                    'users:read'
                ],
                'SALES': [
                    'inventory:read',
                    'sales:read', 'sales:create_quote',
                    'dashboard:view'
                ]
            }
            
            for role, perms in role_permissions.items():
                print(f"\n🔹 {role} ({len(perms)} permisos):")
                print("-" * 60)
                for perm in perms:
                    # Buscar descripción
                    desc = next((p['description'] for p in permissions_data if p['name'] == perm), '')
                    print(f"   ✓ {perm:<25} {desc}")
            
            print("\n" + "=" * 60)
            print("💡 PRÓXIMOS PASOS:")
            print("1. Los permisos están poblados en la base de datos")
            print("2. El sistema RBAC usa estos permisos para controlar acceso")
            print("3. Los decoradores @require_permission() validan contra estos permisos")
            print("4. Ahora puedes proteger endpoints con decoradores")
            print("5. Ejemplo: @require_permission('inventory:write')")
            print("=" * 60 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR al poblar permisos: {e}")
            raise

if __name__ == '__main__':
    populate_permissions()
