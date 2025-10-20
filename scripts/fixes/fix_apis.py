"""
Script para actualizar todas las APIs eliminando el parámetro 'status' obsoleto
y mejorando la documentación Swagger
"""
import os
import re

# Lista de archivos API a actualizar
api_files = [
    'app/api/employee_api.py',
    'app/api/assignment_api.py',
    'app/api/branch_api.py',
    'app/api/city_api.py',
    'app/api/inventory_item_api.py',
    'app/api/quote_api.py',
    'app/api/sales_order_api.py',
    'app/api/user_role_api.py',
    'app/api/state_api.py',
    'app/api/sales_order_item_api.py',
    'app/api/role_api.py',
    'app/api/quote_item_api.py',
    'app/api/quotation_line_api.py',
    'app/api/permission_api.py',
    'app/api/organization_api.py',
    'app/api/invoice_item_api.py',
    'app/api/invoice_api.py'
]

def fix_api_file(filepath):
    """Actualiza un archivo API eliminando el parámetro status"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Eliminar la línea que obtiene el parámetro status
    content = re.sub(
        r'\s+status = request\.args\.get\(\'status\', None, type=str\)\n',
        '\n',
        content
    )
    
    # Eliminar el parámetro status del handler.list_all
    content = re.sub(
        r'handler\.list_all\(page=page, per_page=per_page, status=status\)',
        'handler.list_all(page=page, per_page=per_page)',
        content
    )
    
    # Escribir el contenido actualizado
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'✅ Actualizado: {filepath}')

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for api_file in api_files:
        filepath = os.path.join(base_dir, api_file)
        if os.path.exists(filepath):
            try:
                fix_api_file(filepath)
            except Exception as e:
                print(f'❌ Error en {api_file}: {e}')
        else:
            print(f'⚠️  No encontrado: {filepath}')
    
    print('\n✅ Proceso completado!')

if __name__ == '__main__':
    main()
