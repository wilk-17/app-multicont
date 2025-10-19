"""
Invoice Schemas - Validación de datos para facturas
Marshmallow schemas para validar requests de facturas
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date


class InvoiceItemSchema(Schema):
    """Schema para items de factura."""
    id = fields.Int(dump_only=True)
    invoice_id = fields.Int(dump_only=True)
    inventory_item_id = fields.Int(required=True, validate=validate.Range(min=1))
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    unit_price = fields.Decimal(required=True, as_string=True, validate=validate.Range(min=0))
    total = fields.Decimal(dump_only=True, as_string=True)


class InvoiceCreateSchema(Schema):
    """
    Schema para crear factura.
    """
    customer_id = fields.Int(required=False, allow_none=True)
    customer_name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=200)
    )
    invoice_date = fields.Date(required=True)
    total = fields.Decimal(as_string=True, validate=validate.Range(min=0))
    employee_id = fields.Int(required=False, allow_none=True, validate=validate.Range(min=1))
    sales_order_id = fields.Int(required=False, allow_none=True, validate=validate.Range(min=1))
    items = fields.List(
        fields.Nested(InvoiceItemSchema),
        required=False
    )
    
    @validates('invoice_date')
    def validate_invoice_date(self, value):
        """Valida que la fecha de factura no sea futura."""
        if value > date.today():
            raise ValidationError("La fecha de factura no puede ser futura")


class InvoiceUpdateSchema(Schema):
    """Schema para actualizar factura."""
    customer_name = fields.Str(validate=validate.Length(min=3, max=200))
    invoice_date = fields.Date()
    total = fields.Decimal(as_string=True, validate=validate.Range(min=0))
    employee_id = fields.Int(allow_none=True)


class InvoiceResponseSchema(Schema):
    """Schema para respuesta de factura."""
    id = fields.Str()
    customer_name = fields.Str()
    invoice_date = fields.Date()
    total = fields.Decimal(as_string=True)
    employee_id = fields.Str(allow_none=True)
    sales_order_id = fields.Str(allow_none=True)


# Instancias
invoice_create_schema = InvoiceCreateSchema()
invoice_update_schema = InvoiceUpdateSchema()
invoice_response_schema = InvoiceResponseSchema()
invoices_response_schema = InvoiceResponseSchema(many=True)
