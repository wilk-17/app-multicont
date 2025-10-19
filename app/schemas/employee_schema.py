"""
Employee Schemas - Validación de datos para empleados
Marshmallow schemas para validar requests de empleados
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class EmployeeCreateSchema(Schema):
    """
    Schema para crear empleado.
    """
    first_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    last_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    email = fields.Email(required=True)
    phone = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=20)
    )
    position = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=100)
    )
    hire_date = fields.Date(required=True)
    salary = fields.Decimal(
        required=False,
        allow_none=True,
        as_string=True,
        validate=validate.Range(min=0)
    )
    branch_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    person_id = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1)
    )
    
    @validates('first_name')
    def validate_first_name(self, value):
        """Valida que el nombre no esté vacío y contenga solo letras."""
        if not value or not value.strip():
            raise ValidationError("El nombre no puede estar vacío")
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise ValidationError("El nombre solo puede contener letras y espacios")
    
    @validates('last_name')
    def validate_last_name(self, value):
        """Valida que el apellido no esté vacío y contenga solo letras."""
        if not value or not value.strip():
            raise ValidationError("El apellido no puede estar vacío")
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise ValidationError("El apellido solo puede contener letras y espacios")


class EmployeeUpdateSchema(Schema):
    """Schema para actualizar empleado."""
    first_name = fields.Str(validate=validate.Length(min=2, max=100))
    last_name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    phone = fields.Str(allow_none=True, validate=validate.Length(max=20))
    position = fields.Str(validate=validate.Length(min=2, max=100))
    hire_date = fields.Date()
    salary = fields.Decimal(allow_none=True, as_string=True, validate=validate.Range(min=0))
    branch_id = fields.Int(validate=validate.Range(min=1))
    person_id = fields.Int(allow_none=True, validate=validate.Range(min=1))
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'on_leave', 'terminated']))


class EmployeeResponseSchema(Schema):
    """Schema para respuesta de empleado."""
    id = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()
    phone = fields.Str(allow_none=True)
    position = fields.Str()
    hire_date = fields.Date()
    salary = fields.Decimal(as_string=True, allow_none=True)
    branch_id = fields.Str()
    person_id = fields.Str(allow_none=True)
    status = fields.Str()


# Instancias
employee_create_schema = EmployeeCreateSchema()
employee_update_schema = EmployeeUpdateSchema()
employee_response_schema = EmployeeResponseSchema()
employees_response_schema = EmployeeResponseSchema(many=True)
