# 🧪 GUÍA DE TESTING - Sistema de Autenticación JWT + RBAC

## 📌 RESUMEN DEL SISTEMA

### ✅ Implementación Completada:
1. **JWT Authentication** con bcrypt (contraseñas hasheadas)
2. **17 permisos** poblados en base de datos
3. **8 usuarios** listos para testing:
   - `ana` (ADMIN) - Acceso total
   - `bruno`, `carla` (MANAGER) - Acceso limitado
   - `diego`, `elena`, `felipe`, `gloria`, `hugo` (SALES) - Solo lectura + crear cotizaciones

4. **Endpoints de autenticación**:
   - `POST /api/auth/login` - Login y obtener tokens
   - `POST /api/auth/refresh` - Renovar access token
   - `GET /api/auth/me` - Info del usuario actual
   - `GET /api/auth/validate` - Validar token
   - `POST /api/auth/logout` - Cerrar sesión

---

## 🚀 PASO A PASO: Cómo Probar en Swagger

### PASO 1: Abrir Swagger UI
```
URL: http://127.0.0.1:5000/api/docs/
```

### PASO 2: Login y Obtener Token

1. **Buscar endpoint**: `POST /api/auth/login`
2. **Click en "Try it out"**
3. **Completar el JSON**:

```json
{
  "username": "ana",
  "password": "ana123"
}
```

4. **Click "Execute"**
5. **Copiar el `access_token`** de la respuesta:

```json
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVz...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVz...",
    "user": {
      "id": "1",
      "username": "ana",
      "role": "ADMIN",
      "role_id": "1"
    }
  },
  "message": "Bienvenido, ana!"
}
```

### PASO 3: Autorizar en Swagger

1. **Click en botón "Authorize" 🔒** (arriba a la derecha en Swagger UI)
2. **En el campo "Value"**, pegar **SOLO el token** (sin "Bearer "):
   ```
   eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVz...
   ```
3. **Click "Authorize"**
4. **Click "Close"**

✅ **Ahora todos los endpoints protegidos usarán este token automáticamente**

### PASO 4: Probar Endpoints

#### ✅ Ejemplo 1: Listar Items de Inventario
```
GET /api/inventory_items/
```
- **Todos los roles** pueden verlo (requiere `inventory:read`)
- ✅ ADMIN: 200 OK
- ✅ MANAGER: 200 OK
- ✅ SALES: 200 OK

#### ✅ Ejemplo 2: Crear Item de Inventario
```
POST /api/inventory_items/
```
Body:
```json
{
  "name": "Laptop Dell XPS 15",
  "brand_id": 1,
  "item_category_id": 1,
  "quantity": 10,
  "price": 3500000.00,
  "status": "active"
}
```

**Resultado esperado**:
- ✅ ADMIN (ana): 201 Created - Puede crear
- ✅ MANAGER (bruno): 201 Created - Puede crear
- ❌ SALES (diego): 403 Forbidden - NO puede crear

#### ✅ Ejemplo 3: Eliminar Usuario
```
DELETE /api/users/5
```

**Resultado esperado**:
- ✅ ADMIN (ana): 200 OK - Puede eliminar usuarios
- ❌ MANAGER (bruno): 403 Forbidden - NO puede eliminar usuarios
- ❌ SALES (diego): 403 Forbidden - NO puede eliminar usuarios

#### ✅ Ejemplo 4: Crear Cotización
```
POST /api/quotes/
```
Body:
```json
{
  "person_id": 1,
  "issue_date": "2025-01-15",
  "total_amount": 5000000.00,
  "status": "pending"
}
```

**Resultado esperado**:
- ✅ ADMIN (ana): 201 Created
- ✅ MANAGER (bruno): 201 Created
- ✅ SALES (diego): 201 Created - **SALES puede crear cotizaciones**

#### ✅ Ejemplo 5: Eliminar Inventario
```
DELETE /api/inventory_items/10
```

**Resultado esperado**:
- ✅ ADMIN (ana): 200 OK - Tiene `inventory:delete`
- ❌ MANAGER (bruno): 403 Forbidden - **NO** tiene `inventory:delete`
- ❌ SALES (diego): 403 Forbidden - NO tiene permiso

---

## 📊 MATRIZ DE PERMISOS POR ROL

| Permiso | ADMIN (ana) | MANAGER (bruno/carla) | SALES (diego/elena/etc) |
|---------|-------------|----------------------|-------------------------|
| **INVENTORY** | | | |
| inventory:read | ✅ | ✅ | ✅ |
| inventory:write | ✅ | ✅ | ❌ |
| inventory:delete | ✅ | ❌ | ❌ |
| inventory:manage | ✅ | ❌ | ❌ |
| **SALES** | | | |
| sales:read | ✅ | ✅ | ✅ |
| sales:create_quote | ✅ | ✅ | ✅ |
| sales:approve_quote | ✅ | ✅ | ❌ |
| sales:create_order | ✅ | ✅ | ❌ |
| sales:create_invoice | ✅ | ✅ | ❌ |
| sales:delete | ✅ | ✅ | ❌ |
| **REPORTS** | | | |
| reports:read | ✅ | ✅ | ❌ |
| reports:export | ✅ | ✅ | ❌ |
| dashboard:view | ✅ | ✅ | ✅ |
| **USERS** | | | |
| users:read | ✅ | ✅ | ❌ |
| users:write | ✅ | ❌ | ❌ |
| users:delete | ✅ | ❌ | ❌ |
| **ADMIN** | | | |
| admin:all | ✅ | ❌ | ❌ |

---

## 🧪 ESCENARIOS DE TESTING COMPLETOS

### 🔹 ESCENARIO 1: Usuario ADMIN (ana)
**Password**: `ana123`

**Testing Steps**:
1. Login con `ana` / `ana123`
2. ✅ GET `/api/inventory_items/` → 200 OK
3. ✅ POST `/api/inventory_items/` → 201 Created
4. ✅ PUT `/api/inventory_items/1` → 200 OK
5. ✅ DELETE `/api/inventory_items/1` → 200 OK
6. ✅ GET `/api/users/` → 200 OK
7. ✅ DELETE `/api/users/5` → 200 OK
8. ✅ POST `/api/quotes/` → 201 Created
9. ✅ POST `/api/sales_orders/` → 201 Created
10. ✅ POST `/api/invoices/` → 201 Created

**Resultado**: ✅ **ADMIN tiene acceso total a todos los endpoints**

---

### 🔹 ESCENARIO 2: Usuario MANAGER (bruno)
**Password**: `bruno123`

**Testing Steps**:
1. Login con `bruno` / `bruno123`
2. ✅ GET `/api/inventory_items/` → 200 OK (tiene `inventory:read`)
3. ✅ POST `/api/inventory_items/` → 201 Created (tiene `inventory:write`)
4. ✅ PUT `/api/inventory_items/1` → 200 OK (tiene `inventory:write`)
5. ❌ DELETE `/api/inventory_items/1` → **403 Forbidden** (NO tiene `inventory:delete`)
6. ✅ GET `/api/users/` → 200 OK (tiene `users:read`)
7. ❌ DELETE `/api/users/5` → **403 Forbidden** (NO tiene `users:delete`)
8. ✅ POST `/api/quotes/` → 201 Created (tiene `sales:create_quote`)
9. ✅ POST `/api/sales_orders/` → 201 Created (tiene `sales:create_order`)
10. ✅ POST `/api/invoices/` → 201 Created (tiene `sales:create_invoice`)

**Resultado**: ✅ **MANAGER puede hacer casi todo excepto eliminar inventario y gestionar usuarios**

---

### 🔹 ESCENARIO 3: Usuario SALES (diego)
**Password**: `diego123`

**Testing Steps**:
1. Login con `diego` / `diego123`
2. ✅ GET `/api/inventory_items/` → 200 OK (tiene `inventory:read`)
3. ❌ POST `/api/inventory_items/` → **403 Forbidden** (NO tiene `inventory:write`)
4. ❌ DELETE `/api/inventory_items/1` → **403 Forbidden** (NO tiene `inventory:delete`)
5. ❌ GET `/api/users/` → **403 Forbidden** (NO tiene `users:read`)
6. ✅ GET `/api/quotes/` → 200 OK (tiene `sales:read`)
7. ✅ POST `/api/quotes/` → 201 Created (tiene `sales:create_quote`)
8. ❌ POST `/api/sales_orders/` → **403 Forbidden** (NO tiene `sales:create_order`)
9. ❌ POST `/api/invoices/` → **403 Forbidden** (NO tiene `sales:create_invoice`)
10. ❌ DELETE `/api/quotes/1` → **403 Forbidden** (NO tiene `sales:delete`)

**Resultado**: ✅ **SALES solo puede VER y CREAR COTIZACIONES, nada más**

---

### 🔹 ESCENARIO 4: Sin Autenticación
**Testing Steps**:
1. **NO hacer login** (o click "Logout" en Swagger)
2. ❌ GET `/api/inventory_items/` → **401 Unauthorized**
3. ❌ POST `/api/inventory_items/` → **401 Unauthorized**
4. ❌ GET `/api/users/` → **401 Unauthorized**

**Resultado**: ✅ **Sin token, ningún endpoint funciona**

---

## 🛠️ CÓMO AGREGAR PROTECCIÓN A ENDPOINTS

Los endpoints actuales **NO están protegidos todavía**. Para protegerlos:

### Ejemplo: Proteger endpoint de inventario

**ANTES** (sin protección):
```python
@inventory_item_api.route('/', methods=['POST'])
def create():
    # Cualquiera puede crear
    ...
```

**DESPUÉS** (con protección):
```python
from flask_jwt_extended import jwt_required
from app.services.authorization_service import require_permission

@inventory_item_api.route('/', methods=['POST'])
@jwt_required()  # Requiere estar autenticado
@require_permission('inventory:write')  # Requiere permiso específico
def create():
    # Solo usuarios con inventory:write pueden crear
    ...
```

### Proteger DELETE con rol específico:
```python
from app.services.authorization_service import admin_required

@inventory_item_api.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required()  # Solo ADMIN
def delete(id):
    ...
```

---

## 📝 RESPUESTAS ESPERADAS

### ✅ 200 OK - Operación exitosa
```json
{
  "success": true,
  "data": { ... },
  "message": "Operación exitosa"
}
```

### ✅ 201 Created - Recurso creado
```json
{
  "success": true,
  "data": { "id": "123", "name": "..." },
  "message": "Creado exitosamente"
}
```

### ❌ 401 Unauthorized - No autenticado
```json
{
  "msg": "Missing Authorization Header"
}
```

### ❌ 403 Forbidden - Sin permisos
```json
{
  "success": false,
  "error": "No tienes permiso para realizar esta acción. Permiso requerido: inventory:write",
  "required_permission": "inventory:write",
  "your_role": "SALES"
}
```

### ❌ 404 Not Found - Recurso no existe
```json
{
  "success": false,
  "error": "Recurso no encontrado"
}
```

---

## 🔄 RENOVAR TOKEN (Refresh)

Cuando el access_token expire (24 horas), usa el refresh_token:

1. **Endpoint**: `POST /api/auth/refresh`
2. **Autorizar con refresh_token** (en lugar de access_token)
3. **Respuesta**:
```json
{
  "success": true,
  "data": {
    "access_token": "nuevo_token_aqui..."
  },
  "message": "Token renovado exitosamente"
}
```

---

## ✅ CHECKLIST DE TESTING

### Testing Básico:
- [ ] Login con usuario ADMIN → Obtener token
- [ ] Autorizar en Swagger con token
- [ ] Listar recursos (GET) → 200 OK
- [ ] Crear recurso (POST) → 201 Created
- [ ] Logout → Probar endpoint sin token → 401

### Testing de Permisos:
- [ ] Login como ADMIN → Eliminar recurso → 200 OK
- [ ] Login como MANAGER → Eliminar inventario → 403 Forbidden
- [ ] Login como SALES → Crear inventario → 403 Forbidden
- [ ] Login como SALES → Crear cotización → 201 Created

### Testing de Tokens:
- [ ] Usar access_token → Funciona
- [ ] Usar token inválido → 401/422
- [ ] Renovar token con refresh_token → 200 OK
- [ ] Validar token con `/api/auth/validate` → 200 OK

---

## 🎯 PRÓXIMOS PASOS

1. ✅ **Sistema completamente funcional** para testing
2. ⏳ **Proteger endpoints existentes** con decoradores (paso 4)
3. ⏳ **Crear relación Role-Permission** en BD (opcional)
4. ⏳ **Implementar token blacklist** para logout real
5. ⏳ **Rate limiting** para prevenir brute force
6. ⏳ **Logs de auditoría** de acciones

---

## 📞 SOPORTE

### Usuario de Testing Recomendado:
```
Username: ana
Password: ana123
Rol: ADMIN
Permisos: Todos (17 permisos)
```

### Otros Usuarios:
```
bruno/bruno123 - MANAGER
diego/diego123 - SALES
elena/elena123 - SALES
```

---

**✨ Sistema listo para pruebas en Swagger UI: http://127.0.0.1:5000/api/docs/**
