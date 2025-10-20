# 🧪 TESTING MANUAL EN SWAGGER - GUÍA COMPLETA ACTUALIZADA

## 🚨 PROBLEMA RESUELTO: Error 500 al crear inventory_item

**Causa del error:** El schema estaba aceptando `branch_id` que no existe en el modelo.  
**Solución aplicada:** Removido `branch_id` del schema de validación.

---

## 📋 PASO A PASO COMPLETO

### 🔧 PASO 1: Verificar que el servidor esté corriendo

```bash
python run.py
```

**Salida esperada:**
```
 * Running on http://127.0.0.1:5000
 * Debugger is active!
```

---

### 🌐 PASO 2: Acceder a Swagger UI

**URL:** http://127.0.0.1:5000/api/docs/

Deberías ver la interfaz de Swagger con todos los endpoints.

---

### 🔐 PASO 3: AUTENTICACIÓN - Login con usuario ADMIN

#### 3.1. Buscar endpoint de login
- Sección: **"Auth"**
- Endpoint: `POST /api/auth/login`
- Click en **"Try it out"**

#### 3.2. Usar credenciales de ADMIN
```json
{
  "username": "ana",
  "password": "ana123"
}
```

#### 3.3. Click en "Execute"

#### 3.4. Copiar el access_token de la respuesta

**Respuesta exitosa:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",  ← COPIAR ESTO
    "refresh_token": "...",
    "user": {
      "id": "9",
      "username": "ana",
      "role": "ADMIN"
    }
  },
  "message": "Login exitoso"
}
```

**⚠️ IMPORTANTE:** Solo copia el valor de `access_token`, sin las comillas.

---

### 🔑 PASO 4: AUTORIZAR EN SWAGGER

#### 4.1. Click en el botón verde "Authorize" (arriba a la derecha)

#### 4.2. En el campo "Value", pegar:
```
Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**⚠️ CRÍTICO:** 
- Debes incluir la palabra `Bearer` seguida de **UN ESPACIO**
- Luego el token completo
- Formato: `Bearer {tu_token_aquí}`

#### 4.3. Click en "Authorize" y cerrar el modal

**Verificación:** El candado debe aparecer cerrado 🔒

---

### ✅ PASO 5: PROBAR GET (debe funcionar)

#### 5.1. Buscar endpoint GET de inventory_items
- Sección: **"Inventory Items"**
- Endpoint: `GET /api/inventory_items/`

#### 5.2. Click en "Try it out"

#### 5.3. (Opcional) Configurar parámetros:
- `page`: 1
- `per_page`: 10
- `status`: active

#### 5.4. Click en "Execute"

**Resultado esperado:** `200 OK`

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "1",
        "name": "PLC Siemens S7-1200",
        "price": "2500000.00",
        "quantity": 15,
        "category_id": "1",
        "brand_id": "1"
      }
    ],
    "total": 50,
    "page": 1,
    "per_page": 10,
    "total_pages": 5
  }
}
```

---

### 🆕 PASO 6: CREAR NUEVO ITEM (POST) - SOLUCIÓN AL ERROR 500

#### 6.1. Buscar endpoint POST
- Endpoint: `POST /api/inventory_items/`
- Click en **"Try it out"**

#### 6.2. Usar este JSON CORRECTO (sin branch_id):

```json
{
  "name": "PLC Omron CP1E",
  "description": "PLC compacto con 20 I/O",
  "price": "1250000.00",
  "quantity": 5,
  "category_id": 1,
  "brand_id": 1
}
```

**⚠️ NOTAS IMPORTANTES:**

1. **`price` debe ser STRING** (entre comillas): `"1250000.00"`
2. **NO incluir `branch_id`** (fue removido del schema)
3. **`category_id` es obligatorio** y debe existir en la base de datos
4. **`brand_id` es opcional** pero si lo usas, debe existir
5. **`quantity` debe ser número entero** (sin comillas)

#### 6.3. Click en "Execute"

**Resultado esperado:** `201 Created`

```json
{
  "success": true,
  "data": {
    "id": "61",
    "name": "PLC Omron CP1E",
    "description": "PLC compacto con 20 I/O",
    "price": "1250000.00",
    "quantity": 5,
    "category_id": "1",
    "brand_id": "1",
    "status": "active",
    "is_low_stock": true
  },
  "message": "Item de inventario creado exitosamente"
}
```

---

## 🧪 CASOS DE PRUEBA POR ROL

### 🔵 ROL: SALES (diego, elena, felipe, gloria, hugo)

**Login:**
```json
{"username": "diego", "password": "diego123"}
```

**Pruebas:**

| Endpoint | Método | Resultado Esperado |
|----------|--------|-------------------|
| `/api/inventory_items/` | GET | ✅ 200 OK |
| `/api/inventory_items/1` | GET | ✅ 200 OK |
| `/api/inventory_items/` | POST | ❌ 403 Forbidden |
| `/api/inventory_items/1` | PUT | ❌ 403 Forbidden |
| `/api/inventory_items/1` | DELETE | ❌ 403 Forbidden |
| `/api/sales_orders/` | GET | ❌ 403 Forbidden |
| `/api/invoices/` | GET | ❌ 403 Forbidden |

---

### 🟡 ROL: MANAGER (bruno, carla)

**Login:**
```json
{"username": "bruno", "password": "bruno123"}
```

**Pruebas:**

| Endpoint | Método | Resultado Esperado |
|----------|--------|-------------------|
| `/api/inventory_items/` | GET | ✅ 200 OK |
| `/api/inventory_items/` | POST | ✅ 201 Created |
| `/api/inventory_items/1` | PUT | ✅ 200 OK |
| `/api/inventory_items/1` | DELETE | ❌ 403 Forbidden |
| `/api/sales_orders/` | GET | ✅ 200 OK |
| `/api/invoices/` | GET | ✅ 200 OK |
| `/api/sales_orders/1` | DELETE | ❌ 403 Forbidden |
| `/api/users/1` | PUT | ❌ 403 Forbidden |

**POST que debe funcionar:**
```json
{
  "name": "Sensor Proximidad IFM",
  "price": "450000.00",
  "quantity": 20,
  "category_id": 1
}
```

---

### 🔴 ROL: ADMIN (ana)

**Login:**
```json
{"username": "ana", "password": "ana123"}
```

**Pruebas:**

| Endpoint | Método | Resultado Esperado |
|----------|--------|-------------------|
| `/api/inventory_items/` | POST | ✅ 201 Created |
| `/api/inventory_items/1` | PUT | ✅ 200 OK |
| `/api/inventory_items/999` | DELETE | ✅ 404 Not Found* |
| `/api/users/2` | PUT | ✅ 200 OK |
| `/api/permisos/2` | PUT | ✅ 200 OK |
| `/api/organizaciones/999` | DELETE | ✅ 404 Not Found* |

*404 es correcto porque el ID 999 no existe, pero el permiso está OK (no es 403)

---

## 🔄 CAMBIAR DE USUARIO

Para probar con un rol diferente:

1. **Click en "Authorize"** (arriba derecha)
2. **Click en "Logout"**
3. **Cerrar el modal**
4. **Repetir PASO 3:** Login con nuevo usuario
5. **Repetir PASO 4:** Autorizar con nuevo token
6. **Repetir pruebas**

---

## 📊 CÓDIGOS DE RESPUESTA HTTP

| Código | Significado | Cuándo Ocurre |
|--------|-------------|---------------|
| **200** | OK | GET/PUT exitoso |
| **201** | Created | POST exitoso, recurso creado |
| **204** | No Content | DELETE exitoso |
| **400** | Bad Request | Datos inválidos (schema validation) |
| **401** | Unauthorized | Token inválido/expirado |
| **403** | Forbidden | Usuario sin permisos suficientes |
| **404** | Not Found | Recurso no existe |
| **500** | Server Error | Error interno (revisar logs) |

---

## 🐛 TROUBLESHOOTING

### Error: "401 Unauthorized" en todos los endpoints
**Causas posibles:**
- Token no copiado completo
- Falta la palabra "Bearer" antes del token
- Token expirado (dura 24h)

**Solución:**
1. Logout en Swagger
2. Login de nuevo
3. Copiar token COMPLETO
4. Autorizar con formato: `Bearer {token}`

---

### Error: "403 Forbidden" inesperado
**Causas posibles:**
- Usuario no tiene el rol correcto
- Endpoint requiere permisos específicos

**Solución:**
1. Verificar tabla de permisos arriba
2. Usar usuario con rol adecuado (ADMIN para pruebas completas)

---

### Error: "400 Bad Request" en POST
**Causas posibles:**
- Campo `price` como número en vez de string
- Campo `category_id` inválido o no existe
- Campos requeridos faltantes

**Solución - JSON correcto:**
```json
{
  "name": "Producto Test",
  "price": "99999.00",  ← STRING, no número
  "quantity": 10,       ← NÚMERO sin comillas
  "category_id": 1      ← Debe existir en DB
}
```

---

### Error: "500 Internal Server Error" (RESUELTO)
**Causa original:** Schema aceptaba `branch_id` que no existe en modelo

**Solución aplicada:** 
- ✅ Removido `branch_id` de `InventoryItemCreateSchema`
- ✅ Removido `branch_id` de `InventoryItemUpdateSchema`
- ✅ Removido `branch_id` de `InventoryItemResponseSchema`

**Ahora el POST debe funcionar correctamente.**

---

## ✅ CHECKLIST DE VERIFICACIÓN

### Para ADMIN (ana):
- [ ] Login exitoso (200)
- [ ] GET /inventory_items/ → 200 ✅
- [ ] GET /inventory_items/1 → 200 ✅
- [ ] POST /inventory_items/ → 201 ✅ (con JSON correcto)
- [ ] PUT /inventory_items/1 → 200 ✅
- [ ] GET /sales_orders/ → 200 ✅
- [ ] GET /invoices/ → 200 ✅
- [ ] DELETE /inventory_items/999 → 404 ✅ (no es 500)

### Para MANAGER (bruno):
- [ ] Login exitoso (200)
- [ ] GET /inventory_items/ → 200 ✅
- [ ] POST /inventory_items/ → 201 ✅
- [ ] DELETE /inventory_items/1 → 403 ❌ (bloqueado correctamente)

### Para SALES (diego):
- [ ] Login exitoso (200)
- [ ] GET /inventory_items/ → 200 ✅
- [ ] POST /inventory_items/ → 403 ❌ (bloqueado correctamente)
- [ ] GET /sales_orders/ → 403 ❌ (bloqueado correctamente)

---

## 📝 EJEMPLOS DE JSON VÁLIDOS

### Crear Item de Inventario
```json
{
  "name": "Variador de Frecuencia ABB",
  "description": "Variador 5HP 220V",
  "price": "3500000.00",
  "quantity": 8,
  "category_id": 1,
  "brand_id": 2
}
```

### Actualizar Item (PUT)
```json
{
  "name": "Variador ABB ACS355 (Actualizado)",
  "price": "3600000.00",
  "quantity": 10
}
```

### Crear Cotización
```json
{
  "client_name": "Industrias XYZ",
  "organization_id": 1,
  "employee_id": 1,
  "status": "pending"
}
```

---

## 🎯 RESUMEN FINAL

**Problema resuelto:** ✅ Error 500 al crear inventory_items (branch_id removido)

**Formato correcto para POST:**
```json
{
  "name": "string (min 3, max 200)",
  "description": "string opcional (max 500)",
  "price": "STRING decimal (ej: '1250000.00')",
  "quantity": número_entero,
  "category_id": número_entero (obligatorio),
  "brand_id": número_entero (opcional)
}
```

**Usuarios disponibles:**
- 🔴 ADMIN: ana/ana123
- 🟡 MANAGER: bruno/bruno123, carla/carla123
- 🔵 SALES: diego/diego123, elena/elena123, felipe/felipe123

**Servidor:** http://127.0.0.1:5000  
**Swagger:** http://127.0.0.1:5000/api/docs/

---

**Última actualización:** 2025-10-19  
**Estado:** ✅ Schema corregido, POST funcionando correctamente
