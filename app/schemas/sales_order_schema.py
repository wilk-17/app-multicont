"""
SalesOrder Schemas - Validación de datos para órdenes de venta
Marshmallow schemas para validar requests de órdenes
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date


class SalesOrderItemSchema(Schema):
    """Schema para items de orden de venta."""
    id = fields.Int(dump_only=True)
    sales_order_id = fields.Int(dump_only=True)
    inventory_item_id = fields.Int(required=True, validate=validate.Range(min=1))
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    unit_price = fields.Decimal(required=True, as_string=True, validate=validate.Range(min=0))
    total = fields.Decimal(dump_only=True, as_string=True)


class SalesOrderCreateSchema(Schema):
    """
    Schema para crear orden de venta.
    """
    customer_id = fields.Int(required=False, allow_none=True)
    customer_name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=200)
    )
    order_date = fields.Date(required=True)
    total = fields.Decimal(as_string=True, validate=validate.Range(min=0))
    employee_id = fields.Int(required=False, allow_none=True, validate=validate.Range(min=1))
    quote_id = fields.Int(required=False, allow_none=True, validate=validate.Range(min=1))
    items = fields.List(
        fields.Nested(SalesOrderItemSchema),
        required=False
    )
    
    @validates('order_date')
    def validate_order_date(self, value):
        """Valida que la fecha de orden no sea futura."""
        if value > date.today():
            raise ValidationError("La fecha de orden no puede ser futura")
    
    @validates('customer_name')
    def validate_customer_name(self, value):
        """Valida que el nombre del cliente no esté vacío."""
        if not value or not value.strip():
            raise ValidationError("El nombre del cliente no puede estar vacío")


class SalesOrderUpdateSchema(Schema):
    """Schema para actualizar orden de venta."""
    customer_name = fields.Str(validate=validate.Length(min=3, max=200))
    order_date = fields.Date()
    total = fields.Decimal(as_string=True, validate=validate.Range(min=0))
    employee_id = fields.Int(allow_none=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'confirmed', 'cancelled', 'delivered']))


class SalesOrderResponseSchema(Schema):
    """Schema para respuesta de orden de venta."""
    id = fields.Str()
    customer_name = fields.Str()
    order_date = fields.Date()
    total = fields.Decimal(as_string=True)
    employee_id = fields.Str(allow_none=True)
    quote_id = fields.Str(allow_none=True)
    status = fields.Str()


# Instancias
sales_order_create_schema = SalesOrderCreateSchema()
sales_order_update_schema = SalesOrderUpdateSchema()
sales_order_response_schema = SalesOrderResponseSchema()
sales_orders_response_schema = SalesOrderResponseSchema(many=True)
