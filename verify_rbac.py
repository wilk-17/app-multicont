"""
Script de Verificación de Control de Acceso (RBAC)
Verifica que TODOS los endpoints tengan los decoradores correctos según el modelo de negocio
"""
import os
import re

# Definición de control de acceso esperado por endpoint
EXPECTED_ACCESS_CONTROL = {
    # USUARIOS - Solo ADMIN gestiona usuarios
    'user_api.py': {
        'GET /': ['TODOS'],  # Requiere JWT pero ADMIN y MANAGER pueden ver
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],  # Solo ADMIN y MANAGER pueden crear usuarios
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']  # Solo ADMIN puede eliminar
    },
    
    # ROLES - ADMIN y MANAGER gestionan
    'role_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # ORGANIZACIONES - ADMIN y MANAGER gestionan
    'organization_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # SUCURSALES - ADMIN y MANAGER gestionan
    'branch_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # INVENTARIO - TODOS ven, ADMIN y MANAGER crean/editan, solo ADMIN elimina
    'inventory_item_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']  # Solo ADMIN elimina inventario
    },
    
    # COTIZACIONES - TODOS pueden crear, solo ADMIN y MANAGER editan/eliminan
    'quote_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['TODOS'],  # ¡SALES puede crear cotizaciones!
        'PUT /<id>': ['ADMIN', 'MANAGER'],  # Solo ADMIN/MANAGER editan
        'DELETE /<id>': ['ADMIN']
    },
    
    # ÓRDENES DE VENTA - Solo ADMIN y MANAGER
    'sales_order_api.py': {
        'GET /': ['ADMIN', 'MANAGER'],  # SALES NO ve órdenes
        'GET /<id>': ['ADMIN', 'MANAGER'],
        'POST /': ['ADMIN', 'MANAGER'],  # Solo ADMIN/MANAGER crean órdenes
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # FACTURAS - Solo ADMIN y MANAGER
    'invoice_api.py': {
        'GET /': ['ADMIN', 'MANAGER'],
        'GET /<id>': ['ADMIN', 'MANAGER'],
        'POST /': ['ADMIN', 'MANAGER'],  # Solo ADMIN/MANAGER facturan
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # PERSONAS - ADMIN y MANAGER gestionan
    'person_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # EMPLEADOS - ADMIN y MANAGER gestionan
    'employee_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # ASIGNACIONES - ADMIN y MANAGER gestionan
    'assignment_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # CATEGORÍAS - ADMIN y MANAGER gestionan
    'item_category_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # MARCAS - ADMIN y MANAGER gestionan
    'brand_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # PERMISOS - Solo ADMIN gestiona
    'permission_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN'],  # Solo ADMIN crea permisos
        'PUT /<id>': ['ADMIN'],
        'DELETE /<id>': ['ADMIN']
    },
    
    # UBICACIONES - ADMIN y MANAGER gestionan
    'city_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    },
    
    'state_api.py': {
        'GET /': ['TODOS'],
        'GET /<id>': ['TODOS'],
        'POST /': ['ADMIN', 'MANAGER'],
        'PUT /<id>': ['ADMIN', 'MANAGER'],
        'DELETE /<id>': ['ADMIN']
    }
}

def check_decorator_in_file(filepath, expected_roles):
    """Verifica si un archivo tiene los decoradores correctos"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {
        'GET /': {'found': False, 'correct': False},
        'GET /<id>': {'found': False, 'correct': False},
        'POST /': {'found': False, 'correct': False},
        'PUT /<id>': {'found': False, 'correct': False},
        'DELETE /<id>': {'found': False, 'correct': False}
    }
    
    # Buscar cada endpoint
    for endpoint, required_roles in expected_roles.items():
        # Buscar patrón del endpoint
        if endpoint == 'GET /':
            pattern = r"@.*\.route\('/'\s*,\s*methods=\['GET'\]\)(.*?)def\s+\w+"
        elif endpoint == 'GET /<id>':
            pattern = r"@.*\.route\('/<int:id>'\s*,\s*methods=\['GET'\]\)(.*?)def\s+\w+"
        elif endpoint == 'POST /':
            pattern = r"@.*\.route\('/'\s*,\s*methods=\['POST'\]\)(.*?)def\s+\w+"
        elif endpoint == 'PUT /<id>':
            pattern = r"@.*\.route\('/<int:id>'\s*,\s*methods=\['PUT'\]\)(.*?)def\s+\w+"
        elif endpoint == 'DELETE /<id>':
            pattern = r"@.*\.route\('/<int:id>'\s*,\s*methods=\['DELETE'\]\)(.*?)def\s+\w+"
        
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            decorators = match.group(1)
            results[endpoint]['found'] = True
            
            # Verificar si tiene @jwt_required()
            has_jwt = '@jwt_required()' in decorators
            
            # Verificar @require_role según lo esperado
            if required_roles == ['TODOS']:
                # Solo debe tener @jwt_required(), sin @require_role
                results[endpoint]['correct'] = has_jwt and '@require_role' not in decorators
            elif required_roles == ['ADMIN']:
                # Debe tener @require_role('ADMIN')
                results[endpoint]['correct'] = has_jwt and "@require_role('ADMIN')" in decorators
            elif required_roles == ['ADMIN', 'MANAGER']:
                # Debe tener @require_role('ADMIN', 'MANAGER')
                results[endpoint]['correct'] = has_jwt and (
                    "@require_role('ADMIN', 'MANAGER')" in decorators or
                    "@require_role(\"ADMIN\", \"MANAGER\")" in decorators
                )
            else:
                results[endpoint]['correct'] = has_jwt
    
    return results

def verify_all_apis():
    """Verifica todos los archivos API"""
    
    base_path = "c:/Users/wilke/app-multicont/app/api"
    
    print("=" * 80)
    print("VERIFICACIÓN DE CONTROL DE ACCESO (RBAC)")
    print("=" * 80)
    print()
    
    total_endpoints = 0
    correct_endpoints = 0
    issues = []
    
    for filename, expected_roles in EXPECTED_ACCESS_CONTROL.items():
        filepath = os.path.join(base_path, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️  {filename} - Archivo no encontrado")
            continue
        
        print(f"\n📄 {filename}")
        print("-" * 80)
        
        results = check_decorator_in_file(filepath, expected_roles)
        
        for endpoint, result in results.items():
            total_endpoints += 1
            expected = expected_roles.get(endpoint, [])
            
            if result['found']:
                if result['correct']:
                    print(f"   ✅ {endpoint:<15} - Correcto (requiere: {', '.join(expected)})")
                    correct_endpoints += 1
                else:
                    status = "❌"
                    print(f"   {status} {endpoint:<15} - INCORRECTO (esperado: {', '.join(expected)})")
                    issues.append({
                        'file': filename,
                        'endpoint': endpoint,
                        'expected': expected
                    })
            else:
                print(f"   ⚠️  {endpoint:<15} - No encontrado")
                issues.append({
                    'file': filename,
                    'endpoint': endpoint,
                    'expected': expected,
                    'issue': 'Endpoint no encontrado'
                })
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 80)
    print(f"Total de endpoints verificados: {total_endpoints}")
    print(f"Endpoints correctos: {correct_endpoints}")
    print(f"Endpoints con problemas: {len(issues)}")
    print(f"Porcentaje de cumplimiento: {(correct_endpoints/total_endpoints*100):.1f}%")
    
    if issues:
        print("\n" + "=" * 80)
        print("⚠️  PROBLEMAS DETECTADOS")
        print("=" * 80)
        for issue in issues:
            print(f"\n📝 {issue['file']} - {issue['endpoint']}")
            print(f"   Esperado: {', '.join(issue['expected'])}")
            if 'issue' in issue:
                print(f"   Problema: {issue['issue']}")
    else:
        print("\n✅ ¡TODOS LOS ENDPOINTS TIENEN CONTROL DE ACCESO CORRECTO!")
    
    print("\n" + "=" * 80)
    print("MODELO DE NEGOCIO - RESUMEN DE ROLES")
    print("=" * 80)
    print("""
🔴 ADMIN (ana):
   - Acceso TOTAL a todos los endpoints
   - Único que puede ELIMINAR recursos críticos

🟡 MANAGER (bruno, carla):
   - Gestión operativa completa (CRUD excepto DELETE crítico)
   - Puede crear órdenes de venta y facturas
   - NO puede eliminar inventario/usuarios/organizaciones

🟢 SALES (diego, elena, felipe, gloria, hugo):
   - VER inventario (solo lectura)
   - CREAR cotizaciones
   - NO puede crear órdenes ni facturas
   - NO puede gestionar usuarios/organizaciones
    """)

if __name__ == '__main__':
    verify_all_apis()
