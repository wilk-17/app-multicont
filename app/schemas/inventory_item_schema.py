"""
InventoryItem Schemas - Validación de datos para items de inventario
Marshmallow schemas para validar requests de inventario
"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class InventoryItemCreateSchema(Schema):
    """
    Schema para crear item de inventario.
    """
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=200)
    )
    description = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=500)
    )
    price = fields.Decimal(
        required=True,
        as_string=True,
        validate=validate.Range(min=0)
    )
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )
    category_id = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    brand_id = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1)
    )
    
    @validates('name')
    def validate_name(self, value):
        """Valida que el nombre no esté vacío."""
        if not value or not value.strip():
            raise ValidationError("El nombre no puede estar vacío")
    
    @validates('quantity')
    def validate_quantity(self, value):
        """Valida que la cantidad sea no negativa."""
        if value < 0:
            raise ValidationError("La cantidad no puede ser negativa")


class InventoryItemUpdateSchema(Schema):
    """Schema para actualizar item de inventario."""
    name = fields.Str(validate=validate.Length(min=3, max=200))
    description = fields.Str(allow_none=True, validate=validate.Length(max=500))
    price = fields.Decimal(as_string=True, validate=validate.Range(min=0))
    quantity = fields.Int(validate=validate.Range(min=0))
    category_id = fields.Int(validate=validate.Range(min=1))
    brand_id = fields.Int(allow_none=True, validate=validate.Range(min=1))


class StockOperationSchema(Schema):
    """Schema para operaciones de stock (agregar/quitar)."""
    amount = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    reason = fields.Str(
        required=False,
        validate=validate.Length(max=200)
    )


class InventoryItemResponseSchema(Schema):
    """Schema para respuesta de item de inventario."""
    id = fields.Str()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    price = fields.Decimal(as_string=True)
    quantity = fields.Int()
    category_id = fields.Str()
    brand_id = fields.Str(allow_none=True)
    status = fields.Str()
    is_low_stock = fields.Boolean()


# Instancias
inventory_item_create_schema = InventoryItemCreateSchema()
inventory_item_update_schema = InventoryItemUpdateSchema()
stock_operation_schema = StockOperationSchema()
inventory_item_response_schema = InventoryItemResponseSchema()
inventory_items_response_schema = InventoryItemResponseSchema(many=True)
