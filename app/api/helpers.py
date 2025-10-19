"""
Funciones helper reutilizables para APIs.

Contiene utilidades para:
- Paginación de queries
- Formateo de respuestas JSON
- Parsing de parámetros de request
- Validaciones comunes
"""

from flask import request, jsonify


def paginate_query(query, page=1, per_page=10):
    """
    Pagina una query SQLAlchemy.
    
    Args:
        query: SQLAlchemy query object
        page (int): Número de página (default: 1)
        per_page (int): Items por página (default: 10)
    
    Returns:
        dict: {
            'items': [instances],
            'total': int,
            'page': int,
            'per_page': int,
            'total_pages': int
        }
    """
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'items': paginated.items,
        'total': paginated.total,
        'page': paginated.page,
        'per_page': paginated.per_page,
        'total_pages': paginated.pages
    }


def success_response(data=None, message="Operación exitosa", status_code=200):
    """
    Genera respuesta JSON de éxito estándar.
    
    Args:
        data: Datos a retornar (dict, list, object con to_dict())
        message (str): Mensaje descriptivo
        status_code (int): Código HTTP (default: 200)
    
    Returns:
        tuple: (jsonify response, status_code)
    """
    response = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        # Si el objeto tiene to_dict(), usarlo
        if hasattr(data, 'to_dict'):
            response['data'] = data.to_dict()
        # Si es lista de objetos con to_dict()
        elif isinstance(data, list) and len(data) > 0 and hasattr(data[0], 'to_dict'):
            response['data'] = [item.to_dict() for item in data]
        # Sino, usar data directamente
        else:
            response['data'] = data
    
    return jsonify(response), status_code


def error_response(error_message, status_code=400, error_code=None):
    """
    Genera respuesta JSON de error estándar.
    
    Args:
        error_message (str): Descripción del error
        status_code (int): Código HTTP (default: 400)
        error_code (str): Código de error custom (opcional)
    
    Returns:
        tuple: (jsonify response, status_code)
    """
    response = {
        'success': False,
        'error': error_message
    }
    
    if error_code:
        response['error_code'] = error_code
    
    return jsonify(response), status_code


def paginated_response(paginated_data, message="Listado exitoso", status_code=200):
    """
    Genera respuesta JSON paginada estándar.
    
    Args:
        paginated_data (dict): Dict con 'items', 'total', 'page', etc.
        message (str): Mensaje descriptivo
        status_code (int): Código HTTP (default: 200)
    
    Returns:
        tuple: (jsonify response, status_code)
    """
    items = paginated_data.get('items', [])
    
    # Convertir items a dict si tienen to_dict()
    if items and hasattr(items[0], 'to_dict'):
        items_dict = [item.to_dict() for item in items]
    else:
        items_dict = items
    
    response = {
        'success': True,
        'message': message,
        'data': {
            'items': items_dict,
            'pagination': {
                'total': paginated_data.get('total', 0),
                'page': paginated_data.get('page', 1),
                'per_page': paginated_data.get('per_page', 10),
                'total_pages': paginated_data.get('total_pages', 0)
            }
        }
    }
    
    return jsonify(response), status_code


def parse_pagination_params(default_per_page=10, max_per_page=100):
    """
    Parsea parámetros de paginación del request.
    
    Args:
        default_per_page (int): Valor default para per_page
        max_per_page (int): Máximo permitido para per_page
    
    Returns:
        tuple: (page, per_page)
    """
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1
    
    try:
        per_page = int(request.args.get('per_page', default_per_page))
        if per_page < 1:
            per_page = default_per_page
        elif per_page > max_per_page:
            per_page = max_per_page
    except (ValueError, TypeError):
        per_page = default_per_page
    
    return page, per_page


def parse_status_filter():
    """
    Parsea el parámetro 'status' del request.
    
    Returns:
        str or None: Status a filtrar o None
    """
    return request.args.get('status', None)


def parse_filters(*allowed_filters):
    """
    Parsea múltiples filtros del request.
    
    Args:
        *allowed_filters: Nombres de filtros permitidos
    
    Returns:
        dict: Diccionario con filtros {key: value}
    """
    filters = {}
    for filter_name in allowed_filters:
        value = request.args.get(filter_name)
        if value is not None:
            filters[filter_name] = value
    
    return filters


def validate_required_fields(data, required_fields):
    """
    Valida que todos los campos requeridos estén presentes.
    
    Args:
        data (dict): Datos a validar
        required_fields (list): Lista de campos requeridos
    
    Returns:
        tuple: (is_valid: bool, missing_fields: list)
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            missing_fields.append(field)
    
    return len(missing_fields) == 0, missing_fields


def safe_int(value, default=None):
    """
    Convierte un valor a int de forma segura.
    
    Args:
        value: Valor a convertir
        default: Valor por defecto si falla
    
    Returns:
        int or default: Valor convertido o default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=None):
    """
    Convierte un valor a float de forma segura.
    
    Args:
        value: Valor a convertir
        default: Valor por defecto si falla
    
    Returns:
        float or default: Valor convertido o default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
