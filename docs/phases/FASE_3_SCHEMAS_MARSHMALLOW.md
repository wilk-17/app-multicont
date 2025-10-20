# Fase 3: Schemas de Validación Marshmallow - Resumen de Implementación

## 📦 Schemas Creados

Se han implementado **6 módulos de schemas** con un total de **20+ schemas de validación** para los modelos principales del sistema.

### 1. Quote Schema (`app/schemas/quote_schema.py`)
**Schemas implementados:**
- `QuotationLineSchema` - Validación de líneas de cotización
- `QuoteCreateSchema` - Validación para crear cotizaciones
- `QuoteUpdateSchema` - Validación para actualizar cotizaciones
- `QuoteResponseSchema` - Serialización de respuestas

**Validaciones clave:**
- `customer_name`: Length(min=3, max=200), no vacío
- `date`: No puede ser fecha futura
- `quantity`: Range(min=1)
- `unit_price`: Range(min=0), formato Decimal

**Instancias globales:**
```python
quote_create_schema = QuoteCreateSchema()
quote_update_schema = QuoteUpdateSchema()
quote_response_schema = QuoteResponseSchema()
quotes_response_schema = QuoteResponseSchema(many=True)
```

---

### 2. Invoice Schema (`app/schemas/invoice_schema.py`)
**Schemas implementados:**
- `InvoiceItemSchema` - Validación de items de factura
- `InvoiceCreateSchema` - Validación para crear facturas
- `InvoiceUpdateSchema` - Validación para actualizar facturas
- `InvoiceResponseSchema` - Serialización de respuestas

**Validaciones clave:**
- `customer_name`: Length(min=3, max=200), requerido
- `invoice_date`: No puede ser fecha futura
- `total`: Range(min=0), formato Decimal
- `items`: Lista anidada de InvoiceItemSchema
- `inventory_item_id`, `employee_id`, `sales_order_id`: Range(min=1)

**Instancias globales:**
```python
invoice_create_schema = InvoiceCreateSchema()
invoice_update_schema = InvoiceUpdateSchema()
invoice_response_schema = InvoiceResponseSchema()
invoices_response_schema = InvoiceResponseSchema(many=True)
```

---

### 3. Inventory Item Schema (`app/schemas/inventory_item_schema.py`)
**Schemas implementados:**
- `InventoryItemCreateSchema` - Validación para crear items
- `InventoryItemUpdateSchema` - Validación para actualizar items
- `StockOperationSchema` - Validación para operaciones de stock (agregar/quitar)
- `InventoryItemResponseSchema` - Serialización de respuestas

**Validaciones clave:**
- `name`: Length(min=3, max=200), no vacío
- `description`: Length(max=500), opcional
- `price`: Range(min=0), formato Decimal
- `quantity`: Range(min=0), no negativa
- `category_id`: Range(min=1), requerido
- `brand_id`, `branch_id`: Range(min=1), opcionales
- `amount` (StockOperation): Range(min=1)

**Instancias globales:**
```python
inventory_item_create_schema = InventoryItemCreateSchema()
inventory_item_update_schema = InventoryItemUpdateSchema()
stock_operation_schema = StockOperationSchema()
inventory_item_response_schema = InventoryItemResponseSchema()
inventory_items_response_schema = InventoryItemResponseSchema(many=True)
```

---

### 4. Sales Order Schema (`app/schemas/sales_order_schema.py`)
**Schemas implementados:**
- `SalesOrderItemSchema` - Validación de items de orden
- `SalesOrderCreateSchema` - Validación para crear órdenes
- `SalesOrderUpdateSchema` - Validación para actualizar órdenes
- `SalesOrderResponseSchema` - Serialización de respuestas

**Validaciones clave:**
- `customer_name`: Length(min=3, max=200), no vacío
- `order_date`: No puede ser fecha futura
- `total`: Range(min=0), formato Decimal
- `status`: OneOf(['pending', 'confirmed', 'cancelled', 'delivered'])
- `items`: Lista anidada de SalesOrderItemSchema

**Instancias globales:**
```python
sales_order_create_schema = SalesOrderCreateSchema()
sales_order_update_schema = SalesOrderUpdateSchema()
sales_order_response_schema = SalesOrderResponseSchema()
sales_orders_response_schema = SalesOrderResponseSchema(many=True)
```

---

### 5. User Schema (`app/schemas/user_schema.py`)
**Schemas implementados:**
- `UserCreateSchema` - Validación para crear usuarios (con validación de contraseña fuerte)
- `UserUpdateSchema` - Validación para actualizar usuarios
- `PasswordChangeSchema` - Validación para cambiar contraseña
- `UserResponseSchema` - Serialización de respuestas

**Validaciones clave:**
- `username`: Length(min=4, max=50), alfanumérico con guiones
- `email`: Formato email válido
- `password`: **Validación robusta de contraseña fuerte**:
  - Mínimo 8 caracteres
  - Al menos 1 mayúscula
  - Al menos 1 minúscula
  - Al menos 1 número
  - Al menos 1 carácter especial (!@#$%^&*...)
- `status`: OneOf(['active', 'inactive', 'suspended'])

**Validador de contraseña (regex):**
```python
@validates('password')
def validate_password(self, value):
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
```

**Instancias globales:**
```python
user_create_schema = UserCreateSchema()
user_update_schema = UserUpdateSchema()
password_change_schema = PasswordChangeSchema()
user_response_schema = UserResponseSchema()
users_response_schema = UserResponseSchema(many=True)
```

---

### 6. Employee Schema (`app/schemas/employee_schema.py`)
**Schemas implementados:**
- `EmployeeCreateSchema` - Validación para crear empleados
- `EmployeeUpdateSchema` - Validación para actualizar empleados
- `EmployeeResponseSchema` - Serialización de respuestas

**Validaciones clave:**
- `first_name`, `last_name`: Length(min=2, max=100), solo letras (incluyendo acentos)
- `email`: Formato email válido
- `position`: Length(min=2, max=100)
- `hire_date`: Formato fecha válido
- `salary`: Range(min=0), formato Decimal
- `branch_id`: Range(min=1), requerido
- `status`: OneOf(['active', 'inactive', 'on_leave', 'terminated'])

**Validador de nombres (regex):**
```python
@validates('first_name')
def validate_first_name(self, value):
    if not value or not value.strip():
        raise ValidationError("El nombre no puede estar vacío")
    
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
        raise ValidationError("El nombre solo puede contener letras y espacios")
```

**Instancias globales:**
```python
employee_create_schema = EmployeeCreateSchema()
employee_update_schema = EmployeeUpdateSchema()
employee_response_schema = EmployeeResponseSchema()
employees_response_schema = EmployeeResponseSchema(many=True)
```

---

## 🔧 Arquitectura del Módulo Schemas

```
app/schemas/
├── __init__.py               # Exporta todas las instancias de schemas
├── quote_schema.py           # 4 schemas para cotizaciones
├── invoice_schema.py         # 4 schemas para facturas
├── inventory_item_schema.py  # 4 schemas para inventario
├── sales_order_schema.py     # 4 schemas para órdenes de venta
├── user_schema.py            # 4 schemas para usuarios
└── employee_schema.py        # 3 schemas para empleados
```

**Archivo `__init__.py`** centraliza todas las importaciones:
```python
from .quote_schema import quote_create_schema, quote_update_schema, ...
from .invoice_schema import invoice_create_schema, invoice_update_schema, ...
from .inventory_item_schema import inventory_item_create_schema, ...
from .sales_order_schema import sales_order_create_schema, ...
from .user_schema import user_create_schema, password_change_schema, ...
from .employee_schema import employee_create_schema, ...
```

Esto permite importar directamente:
```python
from app.schemas import quote_create_schema, user_create_schema
```

---

## 📝 Ejemplo de Integración en API Endpoint

### Antes (Sin Validación):
```python
# app/api/quote_api.py
@quote_api.route('/', methods=['POST'])
def create_quote():
    data = request.get_json()
    # No hay validación, cualquier dato pasa
    quote = handler.create(**data)
    return jsonify({'success': True, 'data': quote.to_dict()}), 201
```

**Problemas:**
- ❌ No valida tipos de datos
- ❌ No valida longitud de strings
- ❌ No valida rangos numéricos
- ❌ Permite fechas futuras
- ❌ Permite nombres vacíos

---

### Después (Con Marshmallow):
```python
# app/api/quote_api.py
from marshmallow import ValidationError
from app.schemas import quote_create_schema, quote_response_schema

@quote_api.route('/', methods=['POST'])
def create_quote():
    """
    Crear nueva cotización con validación automática
    ---
    tags:
      - Quotes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - customer_name
            - date
          properties:
            customer_name:
              type: string
              minLength: 3
              maxLength: 200
            date:
              type: string
              format: date
            employee_id:
              type: integer
            items:
              type: array
              items:
                type: object
                properties:
                  inventory_item_id:
                    type: integer
                  quantity:
                    type: integer
                    minimum: 1
                  unit_price:
                    type: number
                    minimum: 0
    responses:
      201:
        description: Cotización creada exitosamente
      400:
        description: Datos de validación incorrectos
      500:
        description: Error del servidor
    """
    try:
        # 1. Validar datos de entrada
        validated_data = quote_create_schema.load(request.get_json())
        
        # 2. Crear cotización con datos validados
        quote = handler.create(**validated_data)
        
        # 3. Serializar respuesta
        result = quote_response_schema.dump(quote)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Cotización creada exitosamente'
        }), 201
        
    except ValidationError as e:
        # Errores de validación de Marshmallow
        return jsonify({
            'success': False,
            'errors': e.messages,
            'message': 'Datos de validación incorrectos'
        }), 400
        
    except ValueError as e:
        # Errores de lógica de negocio
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        # Errores inesperados
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
```

**Beneficios:**
- ✅ Validación automática de tipos
- ✅ Validación de longitud y rangos
- ✅ Validación de fechas (no futuras)
- ✅ Validación de nombres (no vacíos)
- ✅ Mensajes de error descriptivos
- ✅ Respuestas consistentes en formato JSON

---

## 🔍 Ejemplo de Respuesta de Error

Cuando se intenta crear una cotización con datos inválidos:

**Request:**
```json
POST /api/quotes/
{
    "customer_name": "AB",
    "date": "2025-12-31",
    "items": [
        {
            "inventory_item_id": 0,
            "quantity": -5,
            "unit_price": -100
        }
    ]
}
```

**Response (HTTP 400):**
```json
{
    "success": false,
    "errors": {
        "customer_name": [
            "Length must be between 3 and 200."
        ],
        "date": [
            "La fecha no puede ser futura"
        ],
        "items": {
            "0": {
                "inventory_item_id": [
                    "Must be greater than or equal to 1."
                ],
                "quantity": [
                    "Must be greater than or equal to 1."
                ],
                "unit_price": [
                    "Must be greater than or equal to 0."
                ]
            }
        }
    },
    "message": "Datos de validación incorrectos"
}
```

**Ventajas:**
- Mensajes descriptivos para cada campo
- Estructura jerárquica para objetos anidados
- HTTP 400 indica error del cliente
- Formato JSON consistente

---

## 🚀 Próximos Pasos (Fase 3 - Continuación)

### 1. Integrar schemas en todos los endpoints API (Alta Prioridad)
- [ ] Actualizar `app/api/quote_api.py` con `quote_create_schema`, `quote_update_schema`
- [ ] Actualizar `app/api/invoice_api.py` con `invoice_create_schema`, `invoice_update_schema`
- [ ] Actualizar `app/api/inventory_item_api.py` con `inventory_item_create_schema`, `stock_operation_schema`
- [ ] Actualizar `app/api/sales_order_api.py` con `sales_order_create_schema`, `sales_order_update_schema`
- [ ] Actualizar `app/api/user_api.py` con `user_create_schema`, `password_change_schema`
- [ ] Actualizar `app/api/employee_api.py` con `employee_create_schema`, `employee_update_schema`

### 2. Lógica de negocio avanzada en handlers (Alta Prioridad)
- [ ] `QuoteHandler.create_with_items()` - Crear cotización con líneas de items, calcular total automático
- [ ] `QuoteHandler.convert_to_sales_order()` - Convertir cotización aprobada en orden de venta
- [ ] `InvoiceHandler.create_from_order()` - Generar factura desde orden de venta
- [ ] `InventoryItemHandler.add_stock(item_id, amount)` - Agregar stock con validación
- [ ] `InventoryItemHandler.remove_stock(item_id, amount)` - Quitar stock con validación (suficiente stock)
- [ ] `InventoryItemHandler.check_low_stock()` - Alertas de stock bajo

### 3. Métodos de dominio en entities (Prioridad Media)
- [ ] `InventoryItem.add_stock(amount)` - Aumentar cantidad
- [ ] `InventoryItem.remove_stock(amount)` - Disminuir cantidad con validación
- [ ] `InventoryItem.is_low_stock()` - Verificar si está bajo en stock
- [ ] `Quote.calculate_total()` - Calcular total desde líneas de items
- [ ] `Quote.can_be_converted()` - Verificar si puede convertirse a orden
- [ ] `User.update_password(new_password)` - Actualizar contraseña hasheada
- [ ] `Invoice.mark_as_paid()` - Marcar factura como pagada
- [ ] `Invoice.is_overdue()` - Verificar si está vencida

---

## 📊 Estadísticas de Implementación

| Métrica | Valor |
|---------|-------|
| **Módulos de schemas** | 6 |
| **Schemas totales** | 23 |
| **Líneas de código** | ~700 |
| **Validaciones implementadas** | 50+ |
| **Modelos cubiertos** | 6 principales (Quote, Invoice, InventoryItem, SalesOrder, User, Employee) |
| **Dependencias instaladas** | marshmallow 3.22.0, Flask-SQLAlchemy 3.1.1, Flask-Migrate 4.0.5, Flasgger 0.9.7.1, python-dotenv 1.0.0 |

---

## ✅ Checklist de Progreso - Fase 3

- [x] Crear `quote_schema.py` con 4 schemas
- [x] Crear `invoice_schema.py` con 4 schemas
- [x] Crear `inventory_item_schema.py` con 4 schemas (incluyendo `StockOperationSchema`)
- [x] Crear `sales_order_schema.py` con 4 schemas
- [x] Crear `user_schema.py` con 4 schemas (incluyendo validación de contraseña fuerte)
- [x] Crear `employee_schema.py` con 3 schemas
- [x] Crear `app/schemas/__init__.py` para centralizar importaciones
- [x] Instalar `marshmallow==3.22.0` y dependencias
- [ ] Integrar schemas en endpoints de `quote_api.py`
- [ ] Integrar schemas en endpoints de `invoice_api.py`
- [ ] Integrar schemas en endpoints de `inventory_item_api.py`
- [ ] Integrar schemas en endpoints de `sales_order_api.py`
- [ ] Integrar schemas en endpoints de `user_api.py`
- [ ] Integrar schemas en endpoints de `employee_api.py`
- [ ] Implementar lógica de negocio avanzada en handlers
- [ ] Agregar métodos de dominio en entities
- [ ] Documentar cambios en `RESUMEN_MEJORAS_APLICADAS.md`

**Progreso actual: 35% de Fase 3 completado**

---

## 🎯 Impacto de los Schemas

### Antes:
```python
# Ejemplo de error silencioso
data = {
    "customer_name": "",  # ❌ Nombre vacío
    "date": "2030-01-01",  # ❌ Fecha futura
    "quantity": -10        # ❌ Cantidad negativa
}
quote = handler.create(**data)  # Se crea con datos inválidos
```

### Después:
```python
# Error detectado automáticamente
try:
    validated_data = quote_create_schema.load(data)
except ValidationError as e:
    # e.messages contiene todos los errores
    print(e.messages)
    # {
    #     "customer_name": ["Length must be between 3 and 200."],
    #     "date": ["La fecha no puede ser futura"],
    #     "quantity": ["Must be greater than or equal to 1."]
    # }
```

**Resultado:**
- 🛡️ **Integridad de datos garantizada**
- 🚫 **Datos inválidos bloqueados antes de llegar a la base de datos**
- 📋 **Mensajes de error claros para el frontend**
- ⚡ **Validación automática sin código adicional en cada endpoint**

---

**Fecha de implementación**: 2025-01-22  
**Estado**: ✅ Schemas creados y dependencias instaladas  
**Próximo objetivo**: Integrar schemas en todos los endpoints API
