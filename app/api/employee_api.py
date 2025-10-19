"""
Employee API - REST Endpoints con validación Marshmallow
Gestiona empleados con relaciones a sucursales y validación automática.
"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.use_cases.employee_handler import EmployeeHandler
from app.schemas import (
    employee_create_schema,
    employee_update_schema,
    employee_response_schema,
    employees_response_schema
)
from app.api.helpers import (
    parse_pagination_params,
    success_response,
    error_response,
    paginated_response
)
from app import cache

employee_api = Blueprint('employee_api', __name__, url_prefix='/api/employees')
handler = EmployeeHandler()

@employee_api.route('/', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_all():
    """
    Lista todos los empleados con paginación y eager loading (Branch)
    ---
    tags:
      - Empleados
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: status
        in: query
        type: string
        enum: [active, inactive]
    responses:
      200:
        description: Lista de empleados con info de sucursal
      500:
        description: Error del servidor
    """
    try:
        page, per_page = parse_pagination_params(request)
        status = request.args.get('status')
        
        # Usar eager loading para evitar N+1 queries
        result = handler.list_all_with_branch(page=page, per_page=per_page, status=status)
        serialized_items = employees_response_schema.dump(result['items'])
        
        return paginated_response(
            items=serialized_items,
            total=result['total'],
            page=result['page'],
            per_page=result['per_page'],
            total_pages=result['total_pages']
        )
    except Exception as e:
        return error_response(str(e), 500)

@employee_api.route('/<int:id>', methods=['GET'])
@cache.cached(timeout=300)
def get_by_id(id):
    """
    Obtiene un empleado por ID
    ---
    tags:
      - Empleados
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Empleado encontrado
      404:
        description: Empleado no encontrado
    """
    try:
        obj = handler.get(id)
        if obj:
            result = employee_response_schema.dump(obj)
            return success_response(result)
        return error_response('Empleado no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)

@employee_api.route('/', methods=['POST'])
def create():
    """
    Crea un nuevo empleado
    ---
    tags:
      - Empleados
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - person_id
            - branch_id
            - position
          properties:
            person_id:
              type: integer
              example: 1
            branch_id:
              type: integer
              example: 1
            position:
              type: string
              example: "Gerente de Ventas"
            salary:
              type: number
              example: 3500.00
            hire_date:
              type: string
              format: date
              example: "2024-01-15"
    responses:
      201:
        description: Empleado creado
      400:
        description: Datos inválidos
    """
    try:
        validated_data = employee_create_schema.load(request.get_json())
        obj = handler.create(**validated_data)
        cache.delete_memoized(get_all)
        
        result = employee_response_schema.dump(obj)
        return success_response(
            data=result,
            message='Empleado creado exitosamente',
            status_code=201
        )
    except ValidationError as e:
        return error_response('Datos de validación incorrectos', 400, errors=e.messages)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@employee_api.route('/<int:id>', methods=['PUT'])
def update(id):
    """
    Actualiza un empleado
    ---
    tags:
      - Empleados
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          type: object
    responses:
      200:
        description: Empleado actualizado
      404:
        description: No encontrado
    """
    try:
        validated_data = employee_update_schema.load(request.get_json())
        if not validated_data:
            return error_response('No se proporcionaron datos para actualizar', 400)
        
        obj = handler.update(id, **validated_data)
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        
        result = employee_response_schema.dump(obj)
        return success_response(data=result, message='Empleado actualizado exitosamente')
    except ValidationError as e:
        return error_response('Datos de validación incorrectos', 400, errors=e.messages)
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Error interno del servidor', 500)

@employee_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Elimina un empleado
    ---
    tags:
      - Empleados
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Eliminado exitosamente
      404:
        description: No encontrado
    """
    try:
        deleted = handler.delete(id)
        cache.delete_memoized(get_all)
        cache.delete_memoized(get_by_id, id)
        
        if deleted:
            return success_response(message='Empleado eliminado exitosamente')
        return error_response('Empleado no encontrado', 404)
    except Exception as e:
        return error_response(str(e), 500)
