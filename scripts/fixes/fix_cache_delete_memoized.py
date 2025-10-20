"""
Script para eliminar las líneas problemáticas de cache.delete_memoized(get_by_id, id)
y cache.delete_memoized(get_all)
"""
import os
import re

api_dir = "app/api"

# Todos los archivos API
api_files = [
    "employee_api.py", "assignment_api.py", "branch_api.py", "city_api.py",
    "inventory_item_api.py", "quote_api.py", "sales_order_api.py", "user_api.py",
    "person_api.py", "item_category_api.py", "brand_api.py", "sales_goal_api.py",
    "invoice_api.py", "organization_api.py", "permission_api.py", "user_role_api.py",
    "state_api.py", "sales_order_item_api.py", "role_api.py", "quote_item_api.py",
    "quotation_line_api.py", "invoice_item_api.py"
]

print("="*80)
print("ELIMINANDO LÍNEAS PROBLEMÁTICAS DE CACHE")
print("="*80 + "\n")

fixed_count = 0
total_lines_removed = 0

for filename in api_files:
    filepath = os.path.join(api_dir, filename)
    
    if not os.path.exists(filepath):
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        lines_removed_in_file = 0
        
        for line in lines:
            # Eliminar líneas que contengan cache.delete_memoized(get_by_id
            # o cache.delete_memoized(get_all)
            if 'cache.delete_memoized(get_by_id' in line:
                lines_removed_in_file += 1
                total_lines_removed += 1
                continue
            elif 'cache.delete_memoized(get_all)' in line:
                lines_removed_in_file += 1
                total_lines_removed += 1
                continue
            else:
                new_lines.append(line)
        
        if lines_removed_in_file > 0:
            # Guardar archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            print(f"OK  : {filename} - {lines_removed_in_file} línea(s) eliminada(s)")
            fixed_count += 1
        else:
            print(f"SKIP: {filename} - Sin cambios")
            
    except Exception as e:
        print(f"ERROR: {filename} - {e}")

print("\n" + "="*80)
print(f"RESUMEN: {fixed_count} archivos modificados")
print(f"Total de líneas eliminadas: {total_lines_removed}")
print("="*80)
print("\nNOTA: El cache expirará automáticamente según el timeout configurado.")
print("No es necesario invalidar manualmente el cache en cada operación.")
