#!/usr/bin/env python3
"""
Fix imports - Agrega el import de require_role donde falte
"""

import os
import re

API_DIR = 'app/api'

files_to_fix = [
    'branch_api.py',
    'sales_order_api.py',
    'brand_api.py',
    'sales_goal_api.py',
    'organization_api.py',
    'permission_api.py',
    'invoice_api.py',
    'role_api.py'
]

def fix_file(filepath):
    """Agrega import de require_role si usa el decorador pero no lo importa"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Si usa @require_role pero no tiene el import
    if '@require_role' in content and 'from app.utils.decorators import require_role' not in content:
        # Buscar la línea con jwt_required import
        if 'from flask_jwt_extended import jwt_required' in content:
            # Agregar import después de jwt_required
            content = content.replace(
                'from flask_jwt_extended import jwt_required',
                'from flask_jwt_extended import jwt_required\nfrom app.utils.decorators import require_role'
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
    
    return False

def main():
    print("🔧 Corrigiendo imports faltantes...")
    
    fixed_count = 0
    for filename in files_to_fix:
        filepath = os.path.join(API_DIR, filename)
        if os.path.exists(filepath):
            if fix_file(filepath):
                print(f"   ✓ {filename}")
                fixed_count += 1
            else:
                print(f"   ⏭️  {filename} (ya correcto o no necesita)")
    
    print(f"\n✅ {fixed_count} archivos corregidos")

if __name__ == "__main__":
    main()
