#!/usr/bin/env python3
"""
Script para agregar protección JWT a endpoints críticos
Agrega decoradores @jwt_required() y @require_role() automáticamente
"""

import os
import re

# Configuración de protección por API
PROTECTION_CONFIG = {
    'role_api.py': {
        'imports': "from flask_jwt_extended import jwt_required\nfrom app.utils.decorators import require_role",
        'endpoints': {
            'POST': '@jwt_required()\n@require_role(\'ADMIN\')',
            'PUT': '@jwt_required()\n@require_role(\'ADMIN\')',
            'DELETE': '@jwt_required()\n@require_role(\'ADMIN\')',
            'GET': None  # GET methods are public for roles
        }
    },
    'permission_api.py': {
        'imports': "from flask_jwt_extended import jwt_required\nfrom app.utils.decorators import require_role",
        'endpoints': {
            'POST': '@jwt_required()\n@require_role(\'ADMIN\')',
            'PUT': '@jwt_required()\n@require_role(\'ADMIN\')',
            'DELETE': '@jwt_required()\n@require_role(\'ADMIN\')',
            'GET': None
        }
    },
    'sales_goal_api.py': {
        'imports': "from flask_jwt_extended import jwt_required\nfrom app.utils.decorators import require_role",
        'endpoints': {
            'POST': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'PUT': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'DELETE': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'GET': '@jwt_required()'
        }
    },
    'brand_api.py': {
        'imports': "from flask_jwt_extended import jwt_required\nfrom app.utils.decorators import require_role",
        'endpoints': {
            'POST': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'PUT': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'DELETE': '@jwt_required()\n@require_role(\'ADMIN\')',
            'GET': '@jwt_required()'
        }
    },
    'sales_analytics_api.py': {
        'imports': "from flask_jwt_extended import jwt_required",
        'endpoints': {
            'GET': '@jwt_required()',
            'POST': '@jwt_required()',
            'PUT': None,
            'DELETE': None
        }
    },
    'invoice_api.py': {
        'imports': "from flask_jwt_extended import jwt_required\nfrom app.utils.decorators import require_role",
        'endpoints': {
            'POST': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'PUT': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'DELETE': '@jwt_required()\n@require_role(\'ADMIN\')',
            'GET': '@jwt_required()'
        }
    },
    'sales_order_api.py': {
        'imports': "from flask_jwt_extended import jwt_required\nfrom app.utils.decorators import require_role",
        'endpoints': {
            'POST': '@jwt_required()',
            'PUT': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'DELETE': '@jwt_required()\n@require_role(\'ADMIN\')',
            'GET': '@jwt_required()'
        }
    },
    'quote_api.py': {
        'imports': "from flask_jwt_extended import jwt_required",
        'endpoints': {
            'POST': '@jwt_required()',
            'PUT': '@jwt_required()',
            'DELETE': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'GET': '@jwt_required()'
        }
    },
    'organization_api.py': {
        'imports': "from flask_jwt_extended import jwt_required\nfrom app.utils.decorators import require_role",
        'endpoints': {
            'POST': '@jwt_required()\n@require_role(\'ADMIN\')',
            'PUT': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'DELETE': '@jwt_required()\n@require_role(\'ADMIN\')',
            'GET': '@jwt_required()'
        }
    },
    'branch_api.py': {
        'imports': "from flask_jwt_extended import jwt_required\nfrom app.utils.decorators import require_role",
        'endpoints': {
            'POST': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'PUT': '@jwt_required()\n@require_role(\'ADMIN\', \'MANAGER\')',
            'DELETE': '@jwt_required()\n@require_role(\'ADMIN\')',
            'GET': '@jwt_required()'
        }
    }
}


def add_imports_to_file(filepath, imports_str):
    """Agrega imports si no existen"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar si ya tiene los imports
    if 'jwt_required' in content:
        print(f"   ⏭️  Ya tiene imports JWT")
        return content
    
    # Buscar la línea después de los imports existentes
    lines = content.split('\n')
    insert_index = 0
    
    for i, line in enumerate(lines):
        if line.startswith('from ') or line.startswith('import '):
            insert_index = i + 1
    
    # Insertar imports
    lines.insert(insert_index, imports_str)
    new_content = '\n'.join(lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"   ✓ Imports agregados")
    return new_content


def protect_endpoints_in_file(filepath, method_decorators):
    """Agrega decoradores a métodos HTTP"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    protected_count = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Buscar decorador de ruta con método HTTP
        if '@' in line and '.route(' in line and 'methods=' in line:
            # Extraer el método HTTP
            method_match = re.search(r"methods=\['(\w+)'\]", line)
            if method_match:
                method = method_match.group(1)
                
                # Verificar si debe protegerse
                if method in method_decorators and method_decorators[method]:
                    # Verificar si ya tiene @jwt_required
                    if i + 1 < len(lines) and '@jwt_required' not in lines[i + 1]:
                        # Agregar decoradores antes de la definición de función
                        decorator = method_decorators[method]
                        new_lines.append(decorator)
                        protected_count += 1
        
        i += 1
    
    if protected_count > 0:
        new_content = '\n'.join(new_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"   ✓ {protected_count} endpoints protegidos")
    else:
        print(f"   ⏭️  Endpoints ya protegidos")


def main():
    print("="*70)
    print(" 🔒 PROTECCIÓN AUTOMÁTICA DE ENDPOINTS")
    print("="*70)
    print()
    
    api_dir = 'app/api'
    total_files = 0
    total_protected = 0
    
    for filename, config in PROTECTION_CONFIG.items():
        filepath = os.path.join(api_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️  {filename}: Archivo no encontrado")
            continue
        
        print(f"📄 {filename}")
        total_files += 1
        
        # Agregar imports
        add_imports_to_file(filepath, config['imports'])
        
        # Proteger endpoints
        protect_endpoints_in_file(filepath, config['endpoints'])
        
        print()
    
    print("="*70)
    print(f" ✅ PROTECCIÓN COMPLETADA")
    print("="*70)
    print(f"\n📊 Resumen:")
    print(f"   - Archivos procesados: {total_files}")
    print(f"   - Configuraciones aplicadas: {len(PROTECTION_CONFIG)}")
    print()
    print("🔐 Endpoints ahora protegidos por:")
    print("   - JWT Token (Bearer Authentication)")
    print("   - Roles (ADMIN, MANAGER, SALES)")
    print()
    print("📚 Próximo paso:")
    print("   - Probar endpoints en Swagger UI")
    print("   - Usar 'Authorize' con token de login")
    print()


if __name__ == "__main__":
    main()
