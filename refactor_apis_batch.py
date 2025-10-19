"""
Script de Refactorización Masiva de APIs
==========================================
Aplica helpers, caching y documentación Swagger a TODAS las APIs pendientes.

Ejecutar: python refactor_apis_batch.py
"""

import os
import re
from typing import List, Tuple

# APIs a refactorizar (18 total)
APIS_TO_REFACTOR = [
    'branch_api',
    'person_api',
    'role_api',
    'permission_api',
    'item_category_api',
    'brand_api',
    'quotation_line_api',
    'quote_item_api',
    'invoice_item_api',
    'sales_order_item_api',
    'state_api',
    'city_api',
    'assignment_api',
    'user_role_api',
    'sales_goal_api',
    'user_api',
    'auth_api',
    'dashboard_api',  # Si existe
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.join(BASE_DIR, 'app', 'api')


def add_imports(content: str) -> str:
    """Agrega imports de helpers y caching si no existen."""
    
    # Verificar si ya tiene los imports
    if 'from app.api.helpers import' in content:
        print("  ✓ Ya tiene imports de helpers")
        return content
    
    # Buscar la línea después de los imports de Flask
    lines = content.split('\n')
    insert_index = None
    
    for i, line in enumerate(lines):
        if line.startswith('from flask import') or line.startswith('from flask_jwt_extended'):
            insert_index = i + 1
        elif insert_index and not line.startswith('from') and not line.startswith('import'):
            break
    
    if insert_index is None:
        insert_index = 5  # Default
    
    # Insertar imports
    new_imports = [
        'from app.api.helpers import (',
        '    parse_pagination_params,',
        '    success_response,',
        '    error_response,',
        '    paginated_response',
        ')',
        'from app import cache'
    ]
    
    for i, imp in enumerate(new_imports):
        lines.insert(insert_index + i, imp)
    
    print("  ✓ Imports agregados")
    return '\n'.join(lines)


def add_caching_to_get_all(content: str) -> str:
    """Agrega @cache.cached() a endpoint GET /"""
    
    # Buscar el endpoint GET all
    pattern = r"@\w+_api\.route\('/'\s*,\s*methods=\['GET'\]\)\s*\n@jwt_required\(\)"
    
    if '@cache.cached(timeout=300, query_string=True)' in content:
        print("  ✓ Ya tiene caching en GET all")
        return content
    
    # Agregar decorator de cache
    replacement = r"@\g<0>\n@cache.cached(timeout=300, query_string=True)"
    content = re.sub(pattern, replacement, content)
    
    print("  ✓ Caching agregado a GET all")
    return content


def add_caching_to_get_by_id(content: str) -> str:
    """Agrega @cache.cached() a endpoint GET /<id>"""
    
    pattern = r"@\w+_api\.route\('/<int:id>'\s*,\s*methods=\['GET'\]\)\s*\n@jwt_required\(\)"
    
    if len(re.findall(r'@cache\.cached\(timeout=300', content)) >= 2:
        print("  ✓ Ya tiene caching en GET by ID")
        return content
    
    replacement = r"@\g<0>\n@cache.cached(timeout=300)"
    content = re.sub(pattern, replacement, content)
    
    print("  ✓ Caching agregado a GET by ID")
    return content


def add_cache_invalidation(content: str, api_name: str) -> str:
    """Agrega cache.delete_memoized() en POST, PUT, DELETE"""
    
    if 'cache.delete_memoized' in content:
        print("  ✓ Ya tiene invalidación de cache")
        return content
    
    # Buscar función get_all para invalidar
    lines = content.split('\n')
    modified = False
    
    for i, line in enumerate(lines):
        # En POST (create)
        if 'def create():' in line or 'def create(' in line:
            # Buscar el try: y agregar antes del handler.create()
            for j in range(i, min(i + 20, len(lines))):
                if 'handler.create(' in lines[j] or 'obj = handler.create' in lines[j]:
                    indent = len(lines[j]) - len(lines[j].lstrip())
                    lines.insert(j, ' ' * indent + '# Invalidar cache')
                    lines.insert(j + 1, ' ' * indent + 'cache.delete_memoized(get_all)')
                    modified = True
                    break
        
        # En PUT (update)
        if 'def update(' in line:
            for j in range(i, min(i + 20, len(lines))):
                if 'handler.update(' in lines[j] or 'obj = handler.update' in lines[j]:
                    indent = len(lines[j]) - len(lines[j].lstrip())
                    lines.insert(j, ' ' * indent + '# Invalidar cache')
                    lines.insert(j + 1, ' ' * indent + 'cache.delete_memoized(get_all)')
                    lines.insert(j + 2, ' ' * indent + 'cache.delete_memoized(get_by_id, id)')
                    modified = True
                    break
        
        # En DELETE
        if 'def delete(' in line:
            for j in range(i, min(i + 20, len(lines))):
                if 'handler.delete(' in lines[j] or 'deleted = handler.delete' in lines[j]:
                    indent = len(lines[j]) - len(lines[j].lstrip())
                    lines.insert(j, ' ' * indent + '# Invalidar cache')
                    lines.insert(j + 1, ' ' * indent + 'cache.delete_memoized(get_all)')
                    lines.insert(j + 2, ' ' * indent + 'cache.delete_memoized(get_by_id, id)')
                    modified = True
                    break
    
    if modified:
        print("  ✓ Invalidación de cache agregada")
    return '\n'.join(lines)


def replace_pagination_with_helper(content: str) -> str:
    """Reemplaza extracción manual de page/per_page con helper"""
    
    if 'parse_pagination_params' in content:
        print("  ✓ Ya usa parse_pagination_params")
        return content
    
    # Reemplazar patrón manual
    pattern = r"page = request\.args\.get\('page',\s*1,\s*type=int\)\s*\n\s*per_page = request\.args\.get\('per_page',\s*10,\s*type=int\)"
    replacement = "page, per_page = parse_pagination_params(request)"
    
    content = re.sub(pattern, replacement, content)
    print("  ✓ parse_pagination_params aplicado")
    return content


def replace_responses_with_helpers(content: str) -> str:
    """Reemplaza jsonify manual con success_response/error_response"""
    
    if 'success_response' in content and 'error_response' in content:
        print("  ✓ Ya usa helpers de respuesta")
        return content
    
    # Patrón éxito con datos
    content = re.sub(
        r"return jsonify\(\{'success':\s*True,\s*'data':\s*(.+?)\}\),\s*200",
        r"return success_response(\1)",
        content
    )
    
    # Patrón éxito con mensaje
    content = re.sub(
        r"return jsonify\(\{'success':\s*True,\s*'message':\s*'(.+?)'\}\),\s*200",
        r"return success_response(message='\1')",
        content
    )
    
    # Patrón error
    content = re.sub(
        r"return jsonify\(\{'success':\s*False,\s*'error':\s*(.+?)\}\),\s*(\d+)",
        r"return error_response(\1, \2)",
        content
    )
    
    print("  ✓ Helpers de respuesta aplicados")
    return content


def add_swagger_docs(content: str, api_name: str) -> str:
    """Agrega documentación Swagger básica a cada endpoint"""
    
    if '---' in content and 'swagger:' in content:
        print("  ✓ Ya tiene documentación Swagger")
        return content
    
    # Determinar nombre del recurso
    resource_name = api_name.replace('_api', '').replace('_', ' ').title()
    resource_name_plural = resource_name + 's' if not resource_name.endswith('s') else resource_name
    
    # Agregar docstrings con formato Swagger
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # GET all
        if 'def get_all():' in line:
            indent = len(line) - len(line.lstrip())
            swagger_doc = f'''    """Lista todos los {resource_name_plural}
    ---
    tags:
      - {resource_name}
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
    responses:
      200:
        description: Lista paginada de {resource_name_plural}
      500:
        description: Error interno del servidor
    """'''
            lines[i + 1] = swagger_doc
        
        # GET by ID
        elif 'def get_by_id(id):' in line:
            swagger_doc = f'''    """Obtiene un {resource_name} por ID
    ---
    tags:
      - {resource_name}
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: {resource_name} encontrado
      404:
        description: {resource_name} no encontrado
    """'''
            lines[i + 1] = swagger_doc
        
        # POST
        elif 'def create():' in line or 'def create(' in line:
            swagger_doc = f'''    """Crea un nuevo {resource_name}
    ---
    tags:
      - {resource_name}
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
    responses:
      201:
        description: {resource_name} creado exitosamente
      400:
        description: Datos inválidos
    """'''
            lines[i + 1] = swagger_doc
        
        # PUT
        elif 'def update(' in line:
            swagger_doc = f'''    """Actualiza un {resource_name}
    ---
    tags:
      - {resource_name}
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
    responses:
      200:
        description: {resource_name} actualizado
      404:
        description: {resource_name} no encontrado
    """'''
            lines[i + 1] = swagger_doc
        
        # DELETE
        elif 'def delete(' in line:
            swagger_doc = f'''    """Elimina un {resource_name}
    ---
    tags:
      - {resource_name}
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: {resource_name} eliminado
      404:
        description: {resource_name} no encontrado
    """'''
            lines[i + 1] = swagger_doc
    
    print("  ✓ Documentación Swagger agregada")
    return '\n'.join(lines)


def refactor_api_file(api_name: str) -> bool:
    """Refactoriza un archivo de API completo"""
    
    file_path = os.path.join(API_DIR, f'{api_name}.py')
    
    if not os.path.exists(file_path):
        print(f"⚠️  {api_name}.py NO EXISTE - saltando")
        return False
    
    print(f"\n🔧 Refactorizando {api_name}.py...")
    
    # Leer contenido
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Aplicar transformaciones
    content = add_imports(content)
    content = replace_pagination_with_helper(content)
    content = replace_responses_with_helpers(content)
    content = add_caching_to_get_all(content)
    content = add_caching_to_get_by_id(content)
    content = add_cache_invalidation(content, api_name)
    content = add_swagger_docs(content, api_name)
    
    # Escribir archivo refactorizado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {api_name}.py REFACTORIZADO")
    return True


def main():
    """Ejecuta refactorización masiva de todas las APIs"""
    
    print("=" * 70)
    print("REFACTORIZACIÓN MASIVA DE APIs".center(70))
    print("=" * 70)
    print(f"\n📋 APIs a refactorizar: {len(APIS_TO_REFACTOR)}\n")
    
    refactored_count = 0
    skipped_count = 0
    
    for api_name in APIS_TO_REFACTOR:
        success = refactor_api_file(api_name)
        if success:
            refactored_count += 1
        else:
            skipped_count += 1
    
    print("\n" + "=" * 70)
    print(f"✅ REFACTORIZACIÓN COMPLETA".center(70))
    print("=" * 70)
    print(f"\n📊 Resultado:")
    print(f"   ✅ APIs refactorizadas: {refactored_count}")
    print(f"   ⚠️  APIs saltadas: {skipped_count}")
    print(f"\n🎉 Total: {refactored_count}/{len(APIS_TO_REFACTOR)} completadas!")
    print("\n🚀 Próximo paso: git add, git commit, git push\n")


if __name__ == '__main__':
    main()
