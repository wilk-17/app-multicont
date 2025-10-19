# 🏢 MODELO DE NEGOCIO - Control de Acceso por Roles (RBAC)

## 📊 ARQUITECTURA DEL SISTEMA

### **Jerarquía Organizacional**
```
ORGANIZATION (Empresa)
    ↓
BRANCH (Sucursal)
    ↓
EMPLOYEE (Empleado)
    ↓
ASSIGNMENT (Asignación de Items)
```

### **Flujo de Ventas**
```
QUOTE (Cotización) → Creada por SALES o MANAGER
    ↓
SALES_ORDER (Orden de Venta) → Aprobada por MANAGER o ADMIN
    ↓
INVOICE (Factura) → Generada por MANAGER o ADMIN
    ↓
INVOICE_ITEMS (Items facturados)
```

---

## 👥 ROLES Y PERMISOS DEL SISTEMA

### **🔴 ADMIN (Nivel 3 - Acceso Total)**
**Usuario de testing**: `ana` / `ana123`

**Puede hacer TODO:**
- ✅ **CRUD completo** en TODOS los modelos
- ✅ Crear, editar y **ELIMINAR** usuarios
- ✅ Crear, editar y **ELIMINAR** inventario
- ✅ Crear, editar y **ELIMINAR** organizaciones/sucursales
- ✅ Generar cotizaciones, órdenes y facturas
- ✅ Ver todos los reportes y analytics
- ✅ Gestionar roles y permisos

**Endpoints exclusivos de ADMIN:**
```http
DELETE /api/users/{id}           # Solo ADMIN puede eliminar usuarios
DELETE /api/inventory_items/{id} # Solo ADMIN puede eliminar inventario
DELETE /api/organizations/{id}   # Solo ADMIN puede eliminar organizaciones
DELETE /api/branches/{id}        # Solo ADMIN puede eliminar sucursales
```

---

### **🟡 MANAGER (Nivel 2 - Gestión Operativa)**
**Usuarios de testing**: `bruno` / `bruno123`, `carla` / `carla123`

**Puede hacer:**
- ✅ **VER** todos los datos (inventario, ventas, usuarios, reportes)
- ✅ **CREAR y EDITAR** inventario (pero NO eliminar)
- ✅ **CREAR y EDITAR** organizaciones/sucursales (pero NO eliminar)
- ✅ **CREAR** cotizaciones
- ✅ **APROBAR** cotizaciones y crear órdenes de venta
- ✅ **GENERAR** facturas
- ✅ **VER** usuarios (pero NO crear/editar/eliminar)
- ✅ Exportar reportes

**Restricciones de MANAGER:**
```http
❌ DELETE /api/users/{id}           # NO puede eliminar usuarios
❌ DELETE /api/inventory_items/{id} # NO puede eliminar inventario
❌ POST /api/users/                 # NO puede crear usuarios
❌ PUT /api/users/{id}              # NO puede editar usuarios
```

**Endpoints permitidos para MANAGER:**
```http
✅ GET /api/inventory_items/        # Ver inventario
✅ POST /api/inventory_items/       # Crear items
✅ PUT /api/inventory_items/{id}    # Editar items
❌ DELETE /api/inventory_items/{id} # NO puede eliminar

✅ GET /api/quotes/                 # Ver cotizaciones
✅ POST /api/quotes/                # Crear cotizaciones
✅ PUT /api/quotes/{id}             # Editar cotizaciones
✅ POST /api/sales_orders/          # Crear órdenes de venta
✅ POST /api/invoices/              # Generar facturas

✅ GET /api/users/                  # Ver usuarios
❌ POST /api/users/                 # NO puede crear usuarios
❌ DELETE /api/users/{id}           # NO puede eliminar usuarios
```

---

### **🟢 SALES (Nivel 1 - Ventas)**
**Usuarios de testing**: `diego`, `elena`, `felipe`, `gloria`, `hugo` (todos con password `{username}123`)

**Puede hacer:**
- ✅ **VER** inventario (para consultar disponibilidad)
- ✅ **VER** cotizaciones y ventas propias
- ✅ **CREAR** cotizaciones
- ✅ Ver dashboard de ventas
- ✅ Consultar productos y precios

**Restricciones de SALES:**
```http
❌ NO puede crear/editar/eliminar inventario
❌ NO puede aprobar cotizaciones
❌ NO puede crear órdenes de venta
❌ NO puede generar facturas
❌ NO puede ver/gestionar usuarios
❌ NO puede ver reportes detallados
❌ NO puede eliminar nada
```

**Endpoints permitidos para SALES:**
```http
✅ GET /api/inventory_items/        # Ver inventario (solo lectura)
✅ GET /api/inventory_items/{id}    # Ver detalle de producto
❌ POST /api/inventory_items/       # NO puede crear
❌ PUT /api/inventory_items/{id}    # NO puede editar
❌ DELETE /api/inventory_items/{id} # NO puede eliminar

✅ GET /api/quotes/                 # Ver cotizaciones
✅ POST /api/quotes/                # Crear cotizaciones
❌ PUT /api/quotes/{id}             # NO puede editar (solo MANAGER+)
❌ DELETE /api/quotes/{id}          # NO puede eliminar

❌ POST /api/sales_orders/          # NO puede crear órdenes
❌ POST /api/invoices/              # NO puede generar facturas

❌ GET /api/users/                  # NO puede ver usuarios
```

---

## 🔐 CONTROL DE ACCESO POR ENDPOINT

### **Tabla de Permisos por Modelo**

| Modelo | GET (Ver) | POST (Crear) | PUT (Editar) | DELETE (Eliminar) |
|--------|-----------|--------------|--------------|-------------------|
| **Users** | ADMIN, MANAGER | **ADMIN** | **ADMIN** | **ADMIN** |
| **Roles** | ADMIN, MANAGER | ADMIN, MANAGER | ADMIN, MANAGER | **ADMIN** |
| **Organizations** | ADMIN, MANAGER, SALES | ADMIN, MANAGER | ADMIN, MANAGER | **ADMIN** |
| **Branches** | ADMIN, MANAGER, SALES | ADMIN, MANAGER | ADMIN, MANAGER | **ADMIN** |
| **Inventory Items** | **TODOS** | ADMIN, MANAGER | ADMIN, MANAGER | **ADMIN** |
| **Quotes** | **TODOS** | **TODOS** | ADMIN, MANAGER | **ADMIN** |
| **Sales Orders** | ADMIN, MANAGER | ADMIN, MANAGER | ADMIN, MANAGER | **ADMIN** |
| **Invoices** | ADMIN, MANAGER | ADMIN, MANAGER | ADMIN, MANAGER | **ADMIN** |
| **Persons** | ADMIN, MANAGER | ADMIN, MANAGER | ADMIN, MANAGER | **ADMIN** |
| **Employees** | ADMIN, MANAGER | ADMIN, MANAGER | ADMIN, MANAGER | **ADMIN** |
| **Assignments** | ADMIN, MANAGER | ADMIN, MANAGER | ADMIN, MANAGER | **ADMIN** |

---

## 🎯 CASOS DE USO POR ROL

### **Caso 1: Vendedor (SALES) crea una cotización**

1. **Login** como `diego` / `diego123`
   ```http
   POST /api/auth/login
   {
     "username": "diego",
     "password": "diego123"
   }
   ```

2. **Consultar inventario** disponible
   ```http
   GET /api/inventory_items/?status=active
   → ✅ 200 OK (puede ver productos)
   ```

3. **Crear cotización** para cliente
   ```http
   POST /api/quotes/
   {
     "person_id": 1,
     "issue_date": "2025-10-19",
     "total_amount": 5000000.00,
     "status": "pending"
   }
   → ✅ 201 Created (SALES puede crear cotizaciones)
   ```

4. **Intentar aprobar cotización** (crear orden de venta)
   ```http
   POST /api/sales_orders/
   {
     "quote_id": 1,
     ...
   }
   → ❌ 403 Forbidden (SALES NO puede crear órdenes)
   ```

**Resultado**: SALES puede consultar y cotizar, pero NO puede aprobar ventas.

---

### **Caso 2: Manager (MANAGER) aprueba cotización y genera factura**

1. **Login** como `bruno` / `bruno123`
   ```http
   POST /api/auth/login
   {
     "username": "bruno",
     "password": "bruno123"
   }
   ```

2. **Ver cotizaciones pendientes**
   ```http
   GET /api/quotes/?status=pending
   → ✅ 200 OK (MANAGER puede ver todas las cotizaciones)
   ```

3. **Aprobar cotización** (crear orden de venta)
   ```http
   POST /api/sales_orders/
   {
     "quote_id": 1,
     "order_date": "2025-10-19",
     "total_amount": 5000000.00,
     "status": "pending"
   }
   → ✅ 201 Created (MANAGER puede crear órdenes)
   ```

4. **Generar factura**
   ```http
   POST /api/invoices/
   {
     "sales_order_id": 1,
     "issue_date": "2025-10-19",
     "total_amount": 5000000.00,
     "status": "pending"
   }
   → ✅ 201 Created (MANAGER puede facturar)
   ```

5. **Intentar eliminar inventario**
   ```http
   DELETE /api/inventory_items/10
   → ❌ 403 Forbidden (MANAGER NO puede eliminar inventario)
   ```

**Resultado**: MANAGER puede todo el flujo de ventas, pero NO puede eliminar recursos críticos.

---

### **Caso 3: Admin (ADMIN) gestiona todo el sistema**

1. **Login** como `ana` / `ana123`
   ```http
   POST /api/auth/login
   {
     "username": "ana",
     "password": "ana123"
   }
   ```

2. **Crear nuevo usuario MANAGER**
   ```http
   POST /api/users/
   {
     "username": "nuevo_manager",
     "password": "password123",
     "role_id": 2
   }
   → ✅ 201 Created (ADMIN puede crear usuarios)
   ```

3. **Eliminar inventario obsoleto**
   ```http
   DELETE /api/inventory_items/99
   → ✅ 200 OK (ADMIN puede eliminar inventario)
   ```

4. **Eliminar usuario inactivo**
   ```http
   DELETE /api/users/10
   → ✅ 200 OK (ADMIN puede eliminar usuarios)
   ```

**Resultado**: ADMIN tiene control total sobre TODOS los recursos.

---

## 🧪 TESTING EN SWAGGER - Escenarios Completos

### **📋 Escenario 1: Flujo de Venta Completo (Multi-rol)**

#### **Paso 1: SALES crea cotización**
```
1. Login: diego / diego123
2. GET /api/inventory_items/ → Ver productos disponibles
3. POST /api/quotes/ → Crear cotización para cliente
   {
     "person_id": 1,
     "issue_date": "2025-10-19",
     "total_amount": 8500000.00,
     "status": "pending"
   }
   → ✅ 201 Created (cotización ID: 100)
```

#### **Paso 2: MANAGER aprueba y factura**
```
1. Logout → Login: bruno / bruno123
2. GET /api/quotes/100 → Ver cotización creada por diego
3. POST /api/sales_orders/ → Aprobar cotización
   {
     "quote_id": 100,
     "order_date": "2025-10-19",
     "total_amount": 8500000.00,
     "status": "approved"
   }
   → ✅ 201 Created (orden ID: 50)
4. POST /api/invoices/ → Generar factura
   {
     "sales_order_id": 50,
     "issue_date": "2025-10-19",
     "total_amount": 8500000.00,
     "status": "paid"
   }
   → ✅ 201 Created (factura ID: 30)
```

#### **Paso 3: ADMIN audita y gestiona**
```
1. Logout → Login: ana / ana123
2. GET /api/sales_analytics/summary → Ver métricas de venta
3. GET /api/invoices/30 → Revisar factura
4. PUT /api/inventory_items/X → Actualizar stock
   → ✅ 200 OK (ADMIN puede ajustar inventario)
```

---

### **📋 Escenario 2: Control de Permisos (Testing de Restricciones)**

#### **Test 1: SALES intenta crear inventario**
```
Login: diego / diego123
POST /api/inventory_items/
{
  "name": "Laptop HP",
  "brand_id": 1,
  "item_category_id": 1,
  "quantity": 10,
  "price": 2500000.00
}
→ ❌ 403 Forbidden
   {
     "success": false,
     "error": "No tienes permiso para realizar esta acción",
     "required_role": ["ADMIN", "MANAGER"],
     "your_role": "SALES"
   }
```

#### **Test 2: MANAGER intenta eliminar usuario**
```
Login: bruno / bruno123
DELETE /api/users/5
→ ❌ 403 Forbidden
   {
     "success": false,
     "error": "No tienes permiso para realizar esta acción",
     "required_role": ["ADMIN"],
     "your_role": "MANAGER"
   }
```

#### **Test 3: MANAGER intenta eliminar inventario**
```
Login: bruno / bruno123
DELETE /api/inventory_items/10
→ ❌ 403 Forbidden
   {
     "success": false,
     "error": "No tienes permiso para realizar esta acción",
     "required_role": ["ADMIN"],
     "your_role": "MANAGER"
   }
```

#### **Test 4: Sin autenticación**
```
NO hacer login (o hacer logout)
GET /api/inventory_items/
→ ❌ 401 Unauthorized
   {
     "msg": "Missing Authorization Header"
   }
```

---

## 🔒 IMPLEMENTACIÓN TÉCNICA

### **Decoradores de Protección**

Cada endpoint está protegido con decoradores:

```python
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role

# 1. TODOS pueden ver (requiere autenticación)
@blueprint.route('/', methods=['GET'])
@jwt_required()
def get_all():
    ...

# 2. ADMIN y MANAGER pueden crear/editar
@blueprint.route('/', methods=['POST'])
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def create():
    ...

# 3. SOLO ADMIN puede eliminar
@blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@require_role('ADMIN')
def delete(id):
    ...
```

### **Validación de Tokens JWT**

```python
# El token JWT contiene:
{
  "identity": "1",           # User ID
  "role": "ADMIN",           # Role name
  "permissions": [           # Lista de permisos
    "inventory:read",
    "inventory:write",
    "inventory:delete",
    ...
  ],
  "exp": 1729468800          # Expiración (24h)
}
```

---

## 📊 MATRIZ DE ENDPOINTS COMPLETA

### **Usuarios (Users)**
| Endpoint | ADMIN | MANAGER | SALES |
|----------|-------|---------|-------|
| `GET /api/users/` | ✅ | ✅ | ❌ |
| `GET /api/users/{id}` | ✅ | ✅ | ❌ |
| `POST /api/users/` | ✅ | ❌ | ❌ |
| `PUT /api/users/{id}` | ✅ | ❌ | ❌ |
| `DELETE /api/users/{id}` | ✅ | ❌ | ❌ |

### **Inventario (Inventory Items)**
| Endpoint | ADMIN | MANAGER | SALES |
|----------|-------|---------|-------|
| `GET /api/inventory_items/` | ✅ | ✅ | ✅ |
| `GET /api/inventory_items/{id}` | ✅ | ✅ | ✅ |
| `POST /api/inventory_items/` | ✅ | ✅ | ❌ |
| `PUT /api/inventory_items/{id}` | ✅ | ✅ | ❌ |
| `DELETE /api/inventory_items/{id}` | ✅ | ❌ | ❌ |

### **Cotizaciones (Quotes)**
| Endpoint | ADMIN | MANAGER | SALES |
|----------|-------|---------|-------|
| `GET /api/quotes/` | ✅ | ✅ | ✅ |
| `GET /api/quotes/{id}` | ✅ | ✅ | ✅ |
| `POST /api/quotes/` | ✅ | ✅ | ✅ |
| `PUT /api/quotes/{id}` | ✅ | ✅ | ❌ |
| `DELETE /api/quotes/{id}` | ✅ | ❌ | ❌ |

### **Órdenes de Venta (Sales Orders)**
| Endpoint | ADMIN | MANAGER | SALES |
|----------|-------|---------|-------|
| `GET /api/sales_orders/` | ✅ | ✅ | ❌ |
| `GET /api/sales_orders/{id}` | ✅ | ✅ | ❌ |
| `POST /api/sales_orders/` | ✅ | ✅ | ❌ |
| `PUT /api/sales_orders/{id}` | ✅ | ✅ | ❌ |
| `DELETE /api/sales_orders/{id}` | ✅ | ❌ | ❌ |

### **Facturas (Invoices)**
| Endpoint | ADMIN | MANAGER | SALES |
|----------|-------|---------|-------|
| `GET /api/invoices/` | ✅ | ✅ | ❌ |
| `GET /api/invoices/{id}` | ✅ | ✅ | ❌ |
| `POST /api/invoices/` | ✅ | ✅ | ❌ |
| `PUT /api/invoices/{id}` | ✅ | ✅ | ❌ |
| `DELETE /api/invoices/{id}` | ✅ | ❌ | ❌ |

---

## ✅ VERIFICACIÓN DE IMPLEMENTACIÓN

### **Checklist de Seguridad:**
- [x] Todos los endpoints tienen `@jwt_required()`
- [x] Endpoints de creación tienen `@require_role('ADMIN', 'MANAGER')`
- [x] Endpoints de eliminación tienen `@require_role('ADMIN')`
- [x] Documentación Swagger especifica `security: - Bearer: []`
- [x] Respuestas HTTP 401 (no autenticado) y 403 (sin permisos) implementadas
- [x] 8 usuarios de testing con roles asignados
- [x] 17 permisos poblados en base de datos

### **Checklist de Modelo de Negocio:**
- [x] SALES puede ver inventario y crear cotizaciones
- [x] MANAGER puede aprobar cotizaciones y generar facturas
- [x] ADMIN puede eliminar y gestionar todo
- [x] Flujo de ventas: Quote → Sales Order → Invoice
- [x] Jerarquía: Organization → Branch → Employee → Assignment

---

## 🎯 CONCLUSIÓN

**Modelo de negocio implementado con RBAC completo:**

✅ **3 roles** con permisos diferenciados  
✅ **90+ endpoints** protegidos con JWT + decoradores  
✅ **Flujo de ventas** controlado por roles  
✅ **Testing en Swagger** con autenticación Bearer  
✅ **Documentación completa** de permisos y restricciones  

**Swagger UI**: http://127.0.0.1:5000/api/docs/

**Sistema listo para manipular CUALQUIER operación según el rol del usuario.**
