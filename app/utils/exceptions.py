"""
Custom Exceptions - Excepciones personalizadas para la aplicación
Permite manejo consistente de errores en toda la API
"""


class AppException(Exception):
    """
    Excepción base de la aplicación.
    Todas las excepciones custom heredan de esta.
    """
    status_code = 500
    message = "Error interno del servidor"

    def __init__(self, message=None, **kwargs):
        super().__init__()
        if message:
            self.message = message
        self.details = kwargs

    def to_dict(self):
        """Convierte la excepción a dict para JSON response."""
        response = {
            'success': False,
            'error': self.message
        }
        if self.details:
            response['details'] = self.details
        return response


class NotFoundException(AppException):
    """Recurso no encontrado (404)."""
    status_code = 404
    message = "Recurso no encontrado"


class ValidationException(AppException):
    """Datos inválidos o validación fallida (400)."""
    status_code = 400
    message = "Datos inválidos"

    def __init__(self, errors=None, message=None):
        super().__init__(message)
        self.errors = errors or {}

    def to_dict(self):
        response = super().to_dict()
        if self.errors:
            response['errors'] = self.errors
        return response


class UnauthorizedException(AppException):
    """Usuario no autenticado (401)."""
    status_code = 401
    message = "No autorizado. Token inválido o expirado"


class ForbiddenException(AppException):
    """Usuario autenticado pero sin permisos (403)."""
    status_code = 403
    message = "Acceso denegado. Permisos insuficientes"


class ConflictException(AppException):
    """Conflicto con el estado actual (409)."""
    status_code = 409
    message = "Conflicto con el estado actual del recurso"


class BusinessRuleException(AppException):
    """Violación de regla de negocio (422)."""
    status_code = 422
    message = "Operación viola reglas de negocio"


class InsufficientStockException(BusinessRuleException):
    """Stock insuficiente para completar operación."""
    message = "Stock insuficiente"

    def __init__(self, item_name, available, requested):
        super().__init__(
            f"Stock insuficiente para '{item_name}'. Disponible: {available}, Solicitado: {requested}"
        )
        self.item_name = item_name
        self.available = available
        self.requested = requested

    def to_dict(self):
        response = super().to_dict()
        response['details'] = {
            'item_name': self.item_name,
            'available': self.available,
            'requested': self.requested
        }
        return response


class DuplicateException(ConflictException):
    """Intento de crear recurso duplicado."""
    message = "El recurso ya existe"

    def __init__(self, resource, field, value):
        super().__init__(
            f"{resource} con {field}='{value}' ya existe"
        )
        self.resource = resource
        self.field = field
        self.value = value


class DatabaseException(AppException):
    """Error de base de datos."""
    status_code = 500
    message = "Error al acceder a la base de datos"

    def __init__(self, original_error=None):
        super().__init__()
        self.original_error = str(original_error) if original_error else None

    def to_dict(self):
        response = super().to_dict()
        # No exponer detalles de BD en producción
        if self.original_error and not self._is_production():
            response['details'] = {'database_error': self.original_error}
        return response

    @staticmethod
    def _is_production():
        """Verifica si estamos en producción."""
        import os
        return os.getenv('FLASK_ENV') == 'production'
