"""
User Schemas - Validación de datos para usuarios
Marshmallow schemas para validar requests de usuarios con validación de contraseñas
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class UserCreateSchema(Schema):
    """
    Schema para crear usuario con validación de contraseña fuerte.
    """
    username = fields.Str(
        required=True,
        validate=validate.Length(min=4, max=50)
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=100)
    )
    full_name = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=200)
    )
    phone = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=20)
    )
    employee_id = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1)
    )
    
    @validates('username')
    def validate_username(self, value):
        """Valida que el username no esté vacío y sea alfanumérico."""
        if not value or not value.strip():
            raise ValidationError("El nombre de usuario no puede estar vacío")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            raise ValidationError("El nombre de usuario solo puede contener letras, números, guiones y guiones bajos")
    
    @validates('password')
    def validate_password(self, value):
        """
        Valida que la contraseña sea fuerte:
        - Al menos 8 caracteres
        - Al menos una mayúscula
        - Al menos una minúscula
        - Al menos un número
        - Al menos un carácter especial
        """
        if len(value) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")
        
        if not re.search(r'[A-Z]', value):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula")
        
        if not re.search(r'[a-z]', value):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula")
        
        if not re.search(r'\d', value):
            raise ValidationError("La contraseña debe contener al menos un número")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("La contraseña debe contener al menos un carácter especial (!@#$%^&*...)")


class UserUpdateSchema(Schema):
    """Schema para actualizar usuario."""
    username = fields.Str(validate=validate.Length(min=4, max=50))
    email = fields.Email()
    full_name = fields.Str(allow_none=True, validate=validate.Length(max=200))
    phone = fields.Str(allow_none=True, validate=validate.Length(max=20))
    employee_id = fields.Int(allow_none=True, validate=validate.Range(min=1))
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'suspended']))


class PasswordChangeSchema(Schema):
    """Schema para cambiar contraseña."""
    current_password = fields.Str(required=True, load_only=True)
    new_password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=100)
    )
    confirm_password = fields.Str(required=True, load_only=True)
    
    @validates('new_password')
    def validate_new_password(self, value):
        """Valida que la nueva contraseña sea fuerte."""
        if len(value) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres")
        
        if not re.search(r'[A-Z]', value):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula")
        
        if not re.search(r'[a-z]', value):
            raise ValidationError("La contraseña debe contener al menos una letra minúscula")
        
        if not re.search(r'\d', value):
            raise ValidationError("La contraseña debe contener al menos un número")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("La contraseña debe contener al menos un carácter especial")


class UserResponseSchema(Schema):
    """Schema para respuesta de usuario."""
    id = fields.Str()
    username = fields.Str()
    email = fields.Str()
    full_name = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)
    employee_id = fields.Str(allow_none=True)
    status = fields.Str()
    creation_date = fields.DateTime()


# Instancias
user_create_schema = UserCreateSchema()
user_update_schema = UserUpdateSchema()
password_change_schema = PasswordChangeSchema()
user_response_schema = UserResponseSchema()
users_response_schema = UserResponseSchema(many=True)
