"""
Script para corregir paginated_response en todos los archivos API
"""
import os
import re

api_dir = "app/api"

# Lista de archivos API (excluyendo helpers y auth)
api_files = [
    "employee_api.py", "assignment_api.py", "branch_api.py", "city_api.py",
    "sales_order_api.py", "user_api.py", "person_api.py", "item_category_api.py",
    "brand_api.py", "sales_goal_api.py", "invoice_api.py", "organization_api.py",
    "permission_api.py", "user_role_api.py", "state_api.py", "sales_order_item_api.py",
    "role_api.py", "quote_item_api.py", "quotation_line_api.py", "invoice_item_api.py",
    "quote_api.py"  # Agregar quote_api también
]

print("="*80)
print("CORRIGIENDO LLAMADAS A paginated_response()")
print("="*80 + "\n")

fixed_count = 0

for filename in api_files:
    filepath = os.path.join(api_dir, filename)
    
    if not os.path.exists(filepath):
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar el patrón de paginated_response con múltiples parámetros
        # El patrón puede variar pero generalmente es:
        # paginated_response(
        #     items=...,
        #     total=...,
        #     page=...,
        #     per_page=...,
        #     total_pages=...
        # )
        
        # Patrón simplificado para la corrección específica
        pattern = r'return paginated_response\(\s*items=([^,]+),\s*total=result\[\'total\'\],\s*page=result\[\'page\'\],\s*per_page=result\[\'per_page\'\],\s*total_pages=result\[\'total_pages\'\]\s*\)'
        
        replacement = r'''paginated_data = {
            'items': \1,
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'total_pages': result['total_pages']
        }
        
        return paginated_response(paginated_data)'''
        
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"OK  : {filename}")
            fixed_count += 1
        else:
            print(f"SKIP: {filename} - Sin cambios necesarios")
            
    except Exception as e:
        print(f"ERROR: {filename} - {e}")

print("\n" + "="*80)
print(f"RESUMEN: {fixed_count} archivos corregidos")
print("="*80)
