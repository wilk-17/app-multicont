"""
SalesGoal API - REST endpoints para metas de ventas
"""
from flask import Blueprint, request, jsonify
from app.use_cases.sales_goal_handler import SalesGoalHandler

sales_goal_api = Blueprint('sales_goal_api', __name__, url_prefix='/api/sales_goals')
handler = SalesGoalHandler()


@sales_goal_api.route('/', methods=['GET'])
def list_sales_goals():
    """
    Listar metas de ventas con filtros
    ---
    tags:
      - SalesGoal
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: period_type
        in: query
        type: string
        enum: [monthly, quarterly, yearly]
      - name: employee_id
        in: query
        type: integer
      - name: branch_id
        in: query
        type: integer
    responses:
      200:
        description: Lista de metas de ventas
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    period_type = request.args.get('period_type', None, type=str)
    employee_id = request.args.get('employee_id', None, type=int)
    branch_id = request.args.get('branch_id', None, type=int)
    
    try:
        result = handler.list_all(
            page=page, 
            per_page=per_page, 
            period_type=period_type,
            employee_id=employee_id,
            branch_id=branch_id
        )
        return jsonify({
            'success': True,
            'data': {
                'items': [item.to_dict() for item in result['items']],
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'total_pages': result['total_pages']
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@sales_goal_api.route('/<int:id>', methods=['GET'])
def get_sales_goal(id):
    """
    Obtener meta por ID
    ---
    tags:
      - SalesGoal
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Meta encontrada
      404:
        description: Meta no encontrada
    """
    goal = handler.get(id)
    if goal:
        return jsonify({'success': True, 'data': goal.to_dict()}), 200
    return jsonify({'success': False, 'error': 'SalesGoal not found'}), 404


@sales_goal_api.route('/current', methods=['GET'])
def get_current_goals():
    """
    Obtener metas activas para la fecha actual o especificada
    ---
    tags:
      - SalesGoal
    parameters:
      - name: reference_date
        in: query
        type: string
        format: date
        description: Fecha de referencia (YYYY-MM-DD), default hoy
    responses:
      200:
        description: Metas activas
    """
    reference_date = request.args.get('reference_date', None, type=str)
    
    try:
        goals = handler.get_current_goals(reference_date=reference_date)
        return jsonify({
            'success': True,
            'data': [goal.to_dict() for goal in goals]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@sales_goal_api.route('/employee/<int:employee_id>', methods=['GET'])
def get_goals_by_employee(employee_id):
    """
    Obtener todas las metas de un empleado
    ---
    tags:
      - SalesGoal
    parameters:
      - name: employee_id
        in: path
        type: integer
        required: true
      - name: period_type
        in: query
        type: string
        enum: [monthly, quarterly, yearly]
    responses:
      200:
        description: Metas del empleado
    """
    period_type = request.args.get('period_type', None, type=str)
    
    try:
        goals = handler.get_goals_by_employee(employee_id, period_type=period_type)
        return jsonify({
            'success': True,
            'data': [goal.to_dict() for goal in goals]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@sales_goal_api.route('/branch/<int:branch_id>', methods=['GET'])
def get_goals_by_branch(branch_id):
    """
    Obtener todas las metas de una sucursal
    ---
    tags:
      - SalesGoal
    parameters:
      - name: branch_id
        in: path
        type: integer
        required: true
      - name: period_type
        in: query
        type: string
        enum: [monthly, quarterly, yearly]
    responses:
      200:
        description: Metas de la sucursal
    """
    period_type = request.args.get('period_type', None, type=str)
    
    try:
        goals = handler.get_goals_by_branch(branch_id, period_type=period_type)
        return jsonify({
            'success': True,
            'data': [goal.to_dict() for goal in goals]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@sales_goal_api.route('/', methods=['POST'])
def create_sales_goal():
    """
    Crear nueva meta de ventas
    ---
    tags:
      - SalesGoal
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - period_type
            - start_date
            - end_date
            - target_amount
          properties:
            employee_id:
              type: integer
              example: 1
            branch_id:
              type: integer
              example: 1
            period_type:
              type: string
              enum: [monthly, quarterly, yearly]
              example: monthly
            start_date:
              type: string
              format: date
              example: "2025-10-01"
            end_date:
              type: string
              format: date
              example: "2025-10-31"
            target_amount:
              type: number
              example: 50000.00
            created_by_user_id:
              type: integer
              example: 1
    responses:
      201:
        description: Meta creada exitosamente
      400:
        description: Datos inválidos
    """
    data = request.get_json()
    
    # Validar campos requeridos
    required_fields = ['period_type', 'start_date', 'end_date', 'target_amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Field "{field}" is required'}), 400
    
    try:
        goal = handler.create(
            period_type=data['period_type'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            target_amount=data['target_amount'],
            employee_id=data.get('employee_id'),
            branch_id=data.get('branch_id'),
            created_by_user_id=data.get('created_by_user_id')
        )
        return jsonify({
            'success': True,
            'data': goal.to_dict(),
            'message': 'SalesGoal created successfully'
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@sales_goal_api.route('/<int:id>', methods=['PUT'])
def update_sales_goal(id):
    """
    Actualizar meta de ventas
    ---
    tags:
      - SalesGoal
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            period_type:
              type: string
              enum: [monthly, quarterly, yearly]
            start_date:
              type: string
              format: date
            end_date:
              type: string
              format: date
            target_amount:
              type: number
            employee_id:
              type: integer
            branch_id:
              type: integer
    responses:
      200:
        description: Meta actualizada exitosamente
      400:
        description: Datos inválidos
      404:
        description: Meta no encontrada
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    try:
        goal = handler.update(id, **data)
        return jsonify({
            'success': True,
            'data': goal.to_dict(),
            'message': 'SalesGoal updated successfully'
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@sales_goal_api.route('/<int:id>', methods=['DELETE'])
def delete_sales_goal(id):
    """
    Eliminar meta de ventas
    ---
    tags:
      - SalesGoal
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Meta eliminada exitosamente
      404:
        description: Meta no encontrada
    """
    try:
        handler.delete(id)
        return jsonify({
            'success': True,
            'message': 'SalesGoal deleted successfully'
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@sales_goal_api.route('/count', methods=['GET'])
def count_sales_goals():
    """
    Contar metas con filtros
    ---
    tags:
      - SalesGoal
    parameters:
      - name: employee_id
        in: query
        type: integer
      - name: branch_id
        in: query
        type: integer
    responses:
      200:
        description: Total de metas
    """
    employee_id = request.args.get('employee_id', None, type=int)
    branch_id = request.args.get('branch_id', None, type=int)
    
    try:
        total = handler.count(employee_id=employee_id, branch_id=branch_id)
        return jsonify({'success': True, 'data': {'total': total}}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
