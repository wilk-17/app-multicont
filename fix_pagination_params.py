"""
Script para corregir el error parse_pagination_params(request) -> parse_pagination_params()
"""
import os
import re

# Directorio de APIs
api_dir = "app/api"

# Archivos a corregir
files_to_fix = [
    "employee_api.py",
    "assignment_api.py",
    "branch_api.py",
    "city_api.py",
    "inventory_item_api.py",
    "sales_order_api.py",
    "user_api.py",
    "person_api.py",
    "item_category_api.py",
    "brand_api.py",
    "sales_goal_api.py",
    "invoice_api.py",
    "organization_api.py",
    "permission_api.py",
    "user_role_api.py",
    "state_api.py",
    "sales_order_item_api.py",
    "role_api.py",
    "quote_item_api.py",
    "quotation_line_api.py",
    "invoice_item_api.py"
]

fixed_count = 0
error_count = 0

print("="*80)
print("CORRIGIENDO ERROR parse_pagination_params(request)")
print("="*80 + "\n")

for filename in files_to_fix:
    filepath = os.path.join(api_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"SKIP: {filename} - No existe")
        continue
    
    try:
        # Leer archivo
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Contar ocurrencias antes
        before_count = content.count('parse_pagination_params(request)')
        
        if before_count == 0:
            print(f"SKIP: {filename} - No necesita corrección")
            continue
        
        # Reemplazar
        new_content = content.replace(
            'parse_pagination_params(request)',
            'parse_pagination_params()'
        )
        
        # Contar ocurrencias después
        after_count = new_content.count('parse_pagination_params(request)')
        
        # Guardar
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        replacements = before_count - after_count
        print(f"OK  : {filename} - {replacements} reemplazo(s)")
        fixed_count += 1
        
    except Exception as e:
        print(f"ERROR: {filename} - {e}")
        error_count += 1

print("\n" + "="*80)
print(f"RESUMEN: {fixed_count} archivos corregidos, {error_count} errores")
print("="*80)
