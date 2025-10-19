"""
Quote Schemas - Validación de datos para cotizaciones
Marshmallow schemas para validar requests de cotizaciones
"""
from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from datetime import date


class QuotationLineSchema(Schema):
    """Schema para líneas de cotización."""
    id = fields.Int(dump_only=True)
    quote_id = fields.Int(dump_only=True)
    inventory_item_id = fields.Int(required=True, validate=validate.Range(min=1))
    quantity = fields.Int(required=True, validate=validate.Range(min=1, error="La cantidad debe ser al menos 1"))
    unit_price = fields.Decimal(required=True, as_string=True, validate=validate.Range(min=0))
    total = fields.Decimal(dump_only=True, as_string=True)


class QuoteCreateSchema(Schema):
    """
    Schema para crear cotización.
    Valida todos los campos requeridos y formatos.
    """
    customer_name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=200, error="El nombre debe tener entre 3 y 200 caracteres")
    )
    date = fields.Date(required=True)
    employee_id = fields.Int(required=False, allow_none=True, validate=validate.Range(min=1))
    items = fields.List(
        fields.Nested(QuotationLineSchema),
        required=False,
        validate=validate.Length(min=0, error="Debe incluir al menos 0 items")
    )
    
    @validates('date')
    def validate_date(self, value):
        """Valida que la fecha no sea futura."""
        if value > date.today():
            raise ValidationError("La fecha no puede ser futura")
    
    @validates('customer_name')
    def validate_customer_name(self, value):
        """Valida que el nombre del cliente no esté vacío."""
        if not value or value.strip() == '':
            raise ValidationError("El nombre del cliente no puede estar vacío")


class QuoteUpdateSchema(Schema):
    """
    Schema para actualizar cotización.
    Todos los campos son opcionales.
    """
    customer_name = fields.Str(
        validate=validate.Length(min=3, max=200)
    )
    date = fields.Date()
    employee_id = fields.Int(allow_none=True, validate=validate.Range(min=1))
    total = fields.Decimal(as_string=True, validate=validate.Range(min=0))
    
    @validates('date')
    def validate_date(self, value):
        """Valida que la fecha no sea futura."""
        if value and value > date.today():
            raise ValidationError("La fecha no puede ser futura")


class QuoteResponseSchema(Schema):
    """Schema para respuesta de cotización."""
    id = fields.Str()
    customer_name = fields.Str()
    date = fields.Date()
    total = fields.Decimal(as_string=True)
    employee_id = fields.Str(allow_none=True)
    creation_date = fields.DateTime(dump_only=True)
    update_date = fields.DateTime(dump_only=True)


# Instancias reutilizables
quote_create_schema = QuoteCreateSchema()
quote_update_schema = QuoteUpdateSchema()
quote_response_schema = QuoteResponseSchema()
quotes_response_schema = QuoteResponseSchema(many=True)
