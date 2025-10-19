# 🔐 Guía de Autenticación y Autorización - multiCont API

## 📋 Sistema de Roles y Permisos (RBAC)

### **Arquitectura del Sistema**

```
Usuario → Rol → Permisos → Recursos
```

### **Roles Definidos**

| Rol | Nivel | Descripción | Permisos |
|-----|-------|-------------|----------|
| **ADMIN** | 3 | Administrador total del sistema | Todos los permisos (CRUD completo en todos los modelos) |
| **MANAGER** | 2 | Gerente de ventas | Lectura de todo, escritura en ventas, aprobación de órdenes |
| **SALES** | 1 | Vendedor | Lectura limitada, crear cotizaciones, ver inventario |

### **Permisos por Recurso**

#### **Inventario (Inventory Items)**
- `inventory:read` - Ver productos y stock
- `inventory:write` - Crear/editar productos
- `inventory:delete` - Eliminar productos
- `inventory:manage` - Gestión completa

#### **Ventas (Quotes, Orders, Invoices)**
- `sales:read` - Ver cotizaciones, órdenes y facturas
- `sales:create_quote` - Crear cotizaciones
- `sales:approve_quote` - Aprobar cotizaciones
- `sales:create_order` - Crear órdenes de venta
- `sales:create_invoice` - Crear facturas
- `sales:delete` - Eliminar registros de ventas

#### **Reportes y Métricas**
- `reports:read` - Ver reportes y métricas
- `reports:export` - Exportar reportes
- `dashboard:view` - Acceder al dashboard

#### **Usuarios y Administración**
- `users:read` - Ver usuarios
- `users:write` - Crear/editar usuarios
- `users:delete` - Eliminar usuarios
- `admin:all` - Acceso administrativo completo

### **Matriz de Permisos por Rol**

| Permiso | ADMIN | MANAGER | SALES |
|---------|-------|---------|-------|
| `inventory:read` | ✅ | ✅ | ✅ |
| `inventory:write` | ✅ | ✅ | ❌ |
| `inventory:delete` | ✅ | ❌ | ❌ |
| `sales:read` | ✅ | ✅ | ✅ (solo propias) |
| `sales:create_quote` | ✅ | ✅ | ✅ |
| `sales:approve_quote` | ✅ | ✅ | ❌ |
| `sales:create_order` | ✅ | ✅ | ❌ |
| `sales:create_invoice` | ✅ | ✅ | ❌ |
| `sales:delete` | ✅ | ✅ | ❌ |
| `reports:read` | ✅ | ✅ | ✅ (limitado) |
| `reports:export` | ✅ | ✅ | ❌ |
| `dashboard:view` | ✅ | ✅ | ✅ |
| `users:read` | ✅ | ✅ | ❌ |
| `users:write` | ✅ | ❌ | ❌ |
| `users:delete` | ✅ | ❌ | ❌ |
| `admin:all` | ✅ | ❌ | ❌ |

---

## 🚀 Implementación - Pasos a Seguir

### **PASO 1: Configuración Inicial**

1. ✅ Verificar Flask-JWT-Extended instalado
2. ⏳ Crear servicio de autenticación
3. ⏳ Implementar decoradores de autorización
4. ⏳ Proteger endpoints con permisos
5. ⏳ Poblar permisos en base de datos
6. ⏳ Crear usuarios de prueba

### **PASO 2: Endpoints de Autenticación**

#### **POST /api/auth/login**
```json
Request:
{
  "username": "ana",
  "password": "password123"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "1",
    "username": "ana",
    "role": "ADMIN"
  }
}
```

#### **POST /api/auth/refresh**
```json
Request:
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### **GET /api/auth/me**
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Response:
{
  "id": "1",
  "username": "ana",
  "role": "ADMIN",
  "permissions": ["inventory:read", "inventory:write", ...]
}
```

#### **POST /api/auth/logout**
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Response:
{
  "message": "Logout exitoso"
}
```

---

## 🧪 Pruebas en Swagger

### **Escenario 1: Login como ADMIN**

1. **POST /api/auth/login**
   ```json
   {
     "username": "ana",
     "password": "hash-ana"
   }
   ```
   ✅ **Resultado Esperado**: Token de acceso + rol ADMIN

2. **GET /api/inventory/**
   - Header: `Authorization: Bearer {token}`
   - ✅ **Resultado**: Lista completa de productos

3. **POST /api/inventory/**
   - Header: `Authorization: Bearer {token}`
   - Body: Nuevo producto
   - ✅ **Resultado**: Producto creado exitosamente

4. **DELETE /api/inventory/1**
   - Header: `Authorization: Bearer {token}`
   - ✅ **Resultado**: Producto eliminado (200 OK)

### **Escenario 2: Login como MANAGER**

1. **POST /api/auth/login**
   ```json
   {
     "username": "bruno",
     "password": "hash-bruno"
   }
   ```
   ✅ **Resultado Esperado**: Token de acceso + rol MANAGER

2. **GET /api/inventory/**
   - ✅ **Resultado**: Lista completa de productos

3. **POST /api/quotes/**
   - ✅ **Resultado**: Cotización creada

4. **POST /api/sales-orders/**
   - ✅ **Resultado**: Orden de venta creada

5. **DELETE /api/inventory/1**
   - ❌ **Resultado**: 403 Forbidden (No tiene permiso)

6. **DELETE /api/users/5**
   - ❌ **Resultado**: 403 Forbidden (No tiene permiso)

### **Escenario 3: Login como SALES**

1. **POST /api/auth/login**
   ```json
   {
     "username": "diego",
     "password": "hash-diego"
   }
   ```
   ✅ **Resultado Esperado**: Token de acceso + rol SALES

2. **GET /api/inventory/**
   - ✅ **Resultado**: Lista de productos (solo lectura)

3. **POST /api/quotes/**
   - ✅ **Resultado**: Cotización creada

4. **POST /api/sales-orders/**
   - ❌ **Resultado**: 403 Forbidden (Solo MANAGER puede crear órdenes)

5. **GET /api/invoices/**
   - ✅ **Resultado**: Solo sus propias facturas

6. **GET /api/metrics/summary**
   - ❌ **Resultado**: 403 Forbidden (Métricas solo para MANAGER+)

7. **POST /api/inventory/**
   - ❌ **Resultado**: 403 Forbidden (No puede crear productos)

### **Escenario 4: Sin Autenticación**

1. **GET /api/inventory/** (sin token)
   - ❌ **Resultado**: 401 Unauthorized

2. **POST /api/quotes/** (sin token)
   - ❌ **Resultado**: 401 Unauthorized

---

## 📝 Usuarios de Prueba

Después de la implementación, tendrás estos usuarios disponibles:

| Username | Password | Rol | Descripción |
|----------|----------|-----|-------------|
| `ana` | `hash-ana` | ADMIN | Acceso total al sistema |
| `bruno` | `hash-bruno` | MANAGER | Gerente de ventas |
| `carla` | `hash-carla` | MANAGER | Gerente de operaciones |
| `diego` | `hash-diego` | SALES | Vendedor región norte |
| `elena` | `hash-elena` | SALES | Vendedora región sur |
| `felipe` | `hash-felipe` | SALES | Vendedor región oeste |
| `gloria` | `hash-gloria` | SALES | Vendedora región centro |
| `hugo` | `hash-hugo` | SALES | Vendedor región costa |

---

## 🔧 Decoradores Disponibles

```python
# Requiere autenticación
@jwt_required()

# Requiere rol específico
@require_role('ADMIN')
@require_role(['ADMIN', 'MANAGER'])

# Requiere permiso específico
@require_permission('inventory:write')
@require_permission(['sales:read', 'sales:create_quote'])

# Requiere ser el dueño del recurso o tener permiso admin
@require_owner_or_permission('sales:read')
```

---

## 📊 Códigos de Respuesta HTTP

| Código | Significado | Cuándo se usa |
|--------|-------------|---------------|
| 200 | OK | Operación exitosa |
| 201 | Created | Recurso creado exitosamente |
| 401 | Unauthorized | Token inválido o ausente |
| 403 | Forbidden | Usuario autenticado pero sin permisos |
| 404 | Not Found | Recurso no encontrado |
| 422 | Unprocessable Entity | Datos inválidos |

---

## 🎯 Siguiente Pasos

1. ⏳ Implementar servicios de autenticación
2. ⏳ Crear decoradores de autorización
3. ⏳ Proteger todos los endpoints existentes
4. ⏳ Poblar permisos en BD
5. ⏳ Hashear passwords de usuarios
6. ⏳ Actualizar Swagger con autenticación
7. ⏳ Realizar pruebas completas

---

**Estado**: 🚧 En implementación
**Última actualización**: Octubre 2025
