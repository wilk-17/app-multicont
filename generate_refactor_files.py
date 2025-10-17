"""
Script para generar automáticamente Handlers y APIs para todos los modelos.
Ejecutar: python generate_refactor_files.py
"""
import os

BASE_PATH = "app"

# Template para Handlers
HANDLER_TEMPLATE = '''"""
{model}Handler - Use Case Layer
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.{model_lower} import {model}

class {model}Handler:
    """Handler para gestionar operaciones con {model_plural}."""
    
    def create(self, **kwargs) -> {model}:
        """Crea un nuevo {model_singular}."""
        try:
            obj = {model}(**kwargs)
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {{str(e)}}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear {model_singular}: {{str(e)}}")
    
    def get(self, id: int) -> Optional[{model}]:
        """Obtiene un {model_singular} por ID."""
        return {model}.query.get(id)
    
    def list_all(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """Lista {model_plural} con paginación."""
        query = {model}.query
        if status and hasattr({model}, 'status'):
            query = query.filter_by(status=status)
        query = query.order_by({model}.creation_date.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        return {{
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }}
    
    def update(self, id: int, **kwargs) -> {model}:
        """Actualiza un {model_singular}."""
        obj = {model}.query.get(id)
        if not obj:
            raise ValueError(f"{model} con ID '{{id}}' no existe")
        try:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar: {{str(e)}}")
    
    def delete(self, id: int) -> bool:
        """Elimina un {model_singular}."""
        obj = {model}.query.get(id)
        if not obj:
            return False
        try:
            db.session.delete(obj)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al eliminar: {{str(e)}}")
    
    def count(self, status: Optional[str] = None) -> int:
        """Cuenta {model_plural}."""
        query = {model}.query
        if status and hasattr({model}, 'status'):
            query = query.filter_by(status=status)
        return query.count()
'''

# Template para APIs
API_TEMPLATE = '''"""
{model} API - REST Endpoints
"""
from flask import Blueprint, request, jsonify
from app.use_cases.{model_lower}_handler import {model}Handler

{model_lower}_api = Blueprint('{model_lower}_api', __name__, url_prefix='/api/{model_path}')
handler = {model}Handler()

@{model_lower}_api.route('/', methods=['GET'])
def get_all():
    """Lista todos los {model_plural} con paginación"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', None, type=str)
        result = handler.list_all(page=page, per_page=per_page, status=status)
        return jsonify({{
            'success': True,
            'data': {{
                'items': [item.to_dict() for item in result['items']],
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'total_pages': result['total_pages']
            }}
        }}), 200
    except Exception as e:
        return jsonify({{'success': False, 'error': str(e)}}), 500

@{model_lower}_api.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    """Obtiene un {model_singular} por ID"""
    try:
        obj = handler.get(id)
        if obj:
            return jsonify({{'success': True, 'data': obj.to_dict()}}), 200
        return jsonify({{'success': False, 'error': 'No encontrado'}}), 404
    except Exception as e:
        return jsonify({{'success': False, 'error': str(e)}}), 500

@{model_lower}_api.route('/', methods=['POST'])
def create():
    """Crea un nuevo {model_singular}"""
    try:
        data = request.get_json()
        obj = handler.create(**data)
        return jsonify({{'success': True, 'message': 'Creado exitosamente', 'data': obj.to_dict()}}), 201
    except ValueError as e:
        return jsonify({{'success': False, 'error': str(e)}}), 400
    except Exception as e:
        return jsonify({{'success': False, 'error': str(e)}}), 500

@{model_lower}_api.route('/<int:id>', methods=['PUT'])
def update(id):
    """Actualiza un {model_singular}"""
    try:
        data = request.get_json()
        obj = handler.update(id, **data)
        return jsonify({{'success': True, 'message': 'Actualizado exitosamente', 'data': obj.to_dict()}}), 200
    except ValueError as e:
        return jsonify({{'success': False, 'error': str(e)}}), 404
    except Exception as e:
        return jsonify({{'success': False, 'error': str(e)}}), 500

@{model_lower}_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """Elimina un {model_singular}"""
    try:
        deleted = handler.delete(id)
        if deleted:
            return jsonify({{'success': True, 'message': 'Eliminado exitosamente'}}), 200
        return jsonify({{'success': False, 'error': 'No encontrado'}}), 404
    except Exception as e:
        return jsonify({{'success': False, 'error': str(e)}}), 500
'''

# Modelos a generar (omitimos User que ya está hecho)
MODELS_TO_GENERATE = [
    ('Role', 'roles', 'rol'),
    ('Person', 'persons', 'persona'),
    ('Organization', 'organizations', 'organización'),
    ('Branch', 'branches', 'sucursal'),
    ('State', 'states', 'estado'),
    ('City', 'cities', 'ciudad'),
    ('Employee', 'employees', 'empleado'),
    ('Permission', 'permissions', 'permiso'),
    ('UserRole', 'user_roles', 'rol de usuario'),
    ('ItemCategory', 'item_categories', 'categoría'),
    ('InventoryItem', 'inventory_items', 'item de inventario'),
    ('Assignment', 'assignments', 'asignación'),
    ('Quote', 'quotes', 'cotización'),
    ('QuotationLine', 'quotation_lines', 'línea de cotización'),
    ('QuoteItem', 'quote_items', 'item de cotización'),
    ('SalesOrder', 'sales_orders', 'orden de venta'),
    ('SalesOrderItem', 'sales_order_items', 'item de orden de venta'),
    ('Invoice', 'invoices', 'factura'),
    ('InvoiceItem', 'invoice_items', 'item de factura'),
]

def generate_files():
    """Genera todos los handlers y APIs"""
    use_cases_dir = os.path.join(BASE_PATH, 'use_cases')
    api_dir = os.path.join(BASE_PATH, 'api')
    
    for model, plural_path, singular_es in MODELS_TO_GENERATE:
        model_lower = ''.join(['_' + c.lower() if c.isupper() and i > 0 else c.lower() 
                               for i, c in enumerate(model)]).lstrip('_')
        
        # Generar Handler
        handler_content = HANDLER_TEMPLATE.format(
            model=model,
            model_lower=model_lower,
            model_plural=plural_path.replace('_', ' '),
            model_singular=singular_es
        )
        handler_path = os.path.join(use_cases_dir, f'{model_lower}_handler.py')
        with open(handler_path, 'w', encoding='utf-8') as f:
            f.write(handler_content)
        print(f"✓ Creado: {handler_path}")
        
        # Generar API
        api_content = API_TEMPLATE.format(
            model=model,
            model_lower=model_lower,
            model_path=plural_path,
            model_plural=plural_path.replace('_', ' '),
            model_singular=singular_es
        )
        api_path = os.path.join(api_dir, f'{model_lower}_api.py')
        with open(api_path, 'w', encoding='utf-8') as f:
            f.write(api_content)
        print(f"✓ Creado: {api_path}")

if __name__ == '__main__':
    print("Generando handlers y APIs...")
    generate_files()
    print("\n¡Archivos generados exitosamente!")
    print(f"Total: {len(MODELS_TO_GENERATE) * 2} archivos creados")
