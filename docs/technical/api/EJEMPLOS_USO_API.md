# 📘 EJEMPLOS DE USO - API ANALYTICS

Ejemplos prácticos de cómo usar los endpoints de analytics del sistema multiCont.

## 🚀 Base URL

```
http://127.0.0.1:5000/api
```

---

## 🎯 METAS vs ACTUAL (Endpoint Principal)

### Obtener todas las metas mensuales con comparación

**Request:**
```http
GET /api/analytics/goals/vs_actual?period_type=monthly&start_date=2025-04-01&end_date=2025-09-30
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "goal_id": "1",
      "employee_id": "4",
      "employee_name": "Diego Luna",
      "period_type": "monthly",
      "start_date": "2025-04-01",
      "end_date": "2025-04-30",
      "target_amount": 15000000.0,
      "actual_sales": 18300000.0,
      "achievement_percentage": 122.0,
      "status": "exceeded"
    },
    {
      "goal_id": "6",
      "employee_id": "10",
      "employee_name": "Jorge Nieto",
      "period_type": "monthly",
      "start_date": "2025-06-01",
      "end_date": "2025-06-30",
      "target_amount": 20000000.0,
      "actual_sales": 22450000.0,
      "achievement_percentage": 112.2,
      "status": "exceeded"
    },
    {
      "goal_id": "8",
      "employee_id": "10",
      "employee_name": "Jorge Nieto",
      "period_type": "monthly",
      "start_date": "2025-07-01",
      "end_date": "2025-07-31",
      "target_amount": 18000000.0,
      "actual_sales": 16900000.0,
      "achievement_percentage": 93.9,
      "status": "on_track"
    }
  ]
}
```

### Filtrar solo metas trimestrales

**Request:**
```http
GET /api/analytics/goals/vs_actual?period_type=quarterly&start_date=2025-04-01&end_date=2025-09-30
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "goal_id": "16",
      "branch_id": "1",
      "branch_name": "Sucursal 1 - Bogotá",
      "period_type": "quarterly",
      "start_date": "2025-04-01",
      "end_date": "2025-06-30",
      "target_amount": 60000000.0,
      "actual_sales": 8600000.0,
      "achievement_percentage": 14.3,
      "status": "failed"
    }
  ]
}
```

---

## 💰 FACTURACIÓN POR EMPLEADO

### Obtener facturación de todos los empleados en un período

**Request:**
```http
GET /api/analytics/invoicing/by_employee?start_date=2025-04-01&end_date=2025-09-30
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "employee_id": "10",
      "employee_name": "Jorge Nieto",
      "branch_id": "5",
      "invoice_count": 2,
      "total_sales": 39350000.0
    },
    {
      "employee_id": "1",
      "employee_name": "Ana García",
      "branch_id": "1",
      "invoice_count": 2,
      "total_sales": 30200000.0
    },
    {
      "employee_id": "7",
      "employee_name": "Gloria Vega",
      "branch_id": "2",
      "invoice_count": 1,
      "total_sales": 19300000.0
    }
  ]
}
```

### Filtrar solo un mes específico

**Request:**
```http
GET /api/analytics/invoicing/by_employee?start_date=2025-06-01&end_date=2025-06-30
```

---

## 🏢 FACTURACIÓN POR SUCURSAL

**Request:**
```http
GET /api/analytics/invoicing/by_branch?start_date=2025-04-01&end_date=2025-09-30
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "branch_id": "5",
      "branch_name": "Sucursal 5",
      "city": "Barranquilla",
      "employee_count": 3,
      "invoice_count": 2,
      "total_sales": 39350000.0
    },
    {
      "branch_id": "1",
      "branch_name": "Sucursal 1",
      "city": "Bogotá",
      "employee_count": 3,
      "invoice_count": 3,
      "total_sales": 39350000.0
    }
  ]
}
```

---

## 📊 RESUMEN DE VENTAS

**Request:**
```http
GET /api/analytics/sales/summary?start_date=2025-04-01&end_date=2025-09-30
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_invoiced": 140040000.0,
    "total_quoted": 175250000.0,
    "invoice_count": 10,
    "quote_count": 12,
    "avg_invoice": 14004000.0,
    "avg_quote": 14604166.67,
    "conversion_rate": 80.0,
    "period": {
      "start_date": "2025-04-01",
      "end_date": "2025-09-30"
    }
  }
}
```

---

## 🏆 TOP PERFORMERS

### Top 10 vendedores

**Request:**
```http
GET /api/analytics/top_performers?start_date=2025-04-01&end_date=2025-09-30&limit=10
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "employee_id": "10",
      "employee_name": "Jorge Nieto",
      "branch_id": "5",
      "total_sales": 39350000.0,
      "invoice_count": 2,
      "avg_invoice": 19675000.0
    },
    {
      "rank": 2,
      "employee_id": "1",
      "employee_name": "Ana García",
      "branch_id": "1",
      "total_sales": 30200000.0,
      "invoice_count": 2,
      "avg_invoice": 15100000.0
    },
    {
      "rank": 3,
      "employee_id": "7",
      "employee_name": "Gloria Vega",
      "branch_id": "2",
      "total_sales": 19300000.0,
      "invoice_count": 1,
      "avg_invoice": 19300000.0
    }
  ]
}
```

### Top 3 vendedores

**Request:**
```http
GET /api/analytics/top_performers?limit=3&start_date=2025-07-01&end_date=2025-09-30
```

---

## 🏷️ FACTURACIÓN POR MARCA

**Request:**
```http
GET /api/analytics/invoicing/by_brand?start_date=2025-04-01&end_date=2025-09-30
```

**Response (si hay invoice_items poblados):**
```json
{
  "success": true,
  "data": [
    {
      "brand_id": "1",
      "brand_name": "Omron",
      "invoice_count": 8,
      "total_sales": 45000000.0,
      "item_count": 120
    },
    {
      "brand_id": "3",
      "brand_name": "Gefran",
      "invoice_count": 5,
      "total_sales": 32000000.0,
      "item_count": 45
    }
  ]
}
```

**Response (sin invoice_items):**
```json
{
  "success": true,
  "data": [],
  "message": "No invoice items found for the specified period"
}
```

---

## 📝 COTIZACIONES POR MARCA

**Request:**
```http
GET /api/analytics/quotes/by_brand?start_date=2025-04-01&end_date=2025-09-30
```

---

## 🎯 GESTIÓN DE METAS

### Listar todas las metas

**Request:**
```http
GET /api/sales_goals/?page=1&per_page=20
```

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "1",
        "employee_id": "1",
        "branch_id": null,
        "period_type": "monthly",
        "start_date": "2025-04-01",
        "end_date": "2025-04-30",
        "target_amount": 12000000.0,
        "created_by_user_id": "1",
        "creation_date": "2025-10-18T10:30:00"
      }
    ],
    "total": 18,
    "page": 1,
    "per_page": 20,
    "total_pages": 1
  }
}
```

### Crear meta mensual para empleado

**Request:**
```http
POST /api/sales_goals/
Content-Type: application/json

{
  "employee_id": 3,
  "period_type": "monthly",
  "start_date": "2025-10-01",
  "end_date": "2025-10-31",
  "target_amount": 25000000,
  "created_by_user_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "19",
    "employee_id": "3",
    "period_type": "monthly",
    "start_date": "2025-10-01",
    "end_date": "2025-10-31",
    "target_amount": 25000000.0
  },
  "message": "Sales goal created successfully"
}
```

### Crear meta trimestral para sucursal

**Request:**
```http
POST /api/sales_goals/
Content-Type: application/json

{
  "branch_id": 2,
  "period_type": "quarterly",
  "start_date": "2025-10-01",
  "end_date": "2025-12-31",
  "target_amount": 100000000,
  "created_by_user_id": 1
}
```

### Obtener metas actuales (vigentes hoy)

**Request:**
```http
GET /api/sales_goals/current
```

### Obtener metas de un empleado específico

**Request:**
```http
GET /api/sales_goals/by_employee/1
```

### Obtener metas de una sucursal específica

**Request:**
```http
GET /api/sales_goals/by_branch/3
```

---

## 🏷️ GESTIÓN DE MARCAS

### Listar todas las marcas

**Request:**
```http
GET /api/brands/?page=1&per_page=10
```

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "1",
        "name": "Omron",
        "description": "Fabricante japonés de automatización industrial",
        "creation_date": "2025-10-18T10:00:00"
      },
      {
        "id": "2",
        "name": "ING Multicontrol",
        "description": "Soluciones de control industrial",
        "creation_date": "2025-10-18T10:00:00"
      }
    ],
    "total": 6,
    "page": 1,
    "per_page": 10,
    "total_pages": 1
  }
}
```

### Buscar marca por nombre

**Request:**
```http
GET /api/brands/search?name=Omron
```

### Crear nueva marca

**Request:**
```http
POST /api/brands/
Content-Type: application/json

{
  "name": "Siemens",
  "description": "Automatización y control industrial alemán"
}
```

---

## ⚠️ MANEJO DE ERRORES

### Meta inválida (faltan campos)

**Request:**
```http
POST /api/sales_goals/
Content-Type: application/json

{
  "period_type": "monthly"
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Missing required field: target_amount"
}
```

### Meta con período inválido

**Request:**
```http
POST /api/sales_goals/
Content-Type: application/json

{
  "employee_id": 1,
  "period_type": "invalid",
  "start_date": "2025-10-01",
  "end_date": "2025-10-31",
  "target_amount": 10000000
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Invalid period_type. Must be one of: monthly, quarterly, yearly"
}
```

### Recurso no encontrado

**Request:**
```http
GET /api/sales_goals/99999
```

**Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Sales goal not found"
}
```

---

## 📊 FILTROS COMUNES

### Por Rango de Fechas
```
?start_date=2025-04-01&end_date=2025-09-30
```

### Por Tipo de Período
```
?period_type=monthly
?period_type=quarterly
?period_type=yearly
```

### Por Estado
```
?status=active
?status=inactive
```

### Paginación
```
?page=1&per_page=20
```

### Límite de Resultados
```
?limit=10
```

---

## 🔐 AUTENTICACIÓN (Pendiente)

Actualmente los endpoints **NO requieren autenticación**. En producción se recomienda:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🧪 TESTING CON CURL

### Resumen de ventas
```bash
curl "http://127.0.0.1:5000/api/analytics/sales/summary?start_date=2025-04-01&end_date=2025-09-30"
```

### Metas vs actual
```bash
curl "http://127.0.0.1:5000/api/analytics/goals/vs_actual?period_type=monthly&start_date=2025-04-01&end_date=2025-09-30"
```

### Top performers
```bash
curl "http://127.0.0.1:5000/api/analytics/top_performers?limit=5&start_date=2025-04-01&end_date=2025-09-30"
```

### Crear meta (POST)
```bash
curl -X POST "http://127.0.0.1:5000/api/sales_goals/" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "period_type": "monthly",
    "start_date": "2025-10-01",
    "end_date": "2025-10-31",
    "target_amount": 20000000,
    "created_by_user_id": 1
  }'
```

---

## 📱 TESTING CON POSTMAN

### Importar Colección

1. Crear nueva colección "multiCont Analytics"
2. Agregar variable `base_url` = `http://127.0.0.1:5000/api`
3. Crear requests para cada endpoint
4. Guardar respuestas como ejemplos

### Ejemplo de Request en Postman

**Method**: GET  
**URL**: `{{base_url}}/analytics/goals/vs_actual`  
**Params**:
- `period_type` = `monthly`
- `start_date` = `2025-04-01`
- `end_date` = `2025-09-30`

---

## 🎯 CASOS DE USO COMUNES

### Dashboard Ejecutivo
```javascript
// Obtener KPIs principales
const summary = await fetch('/api/analytics/sales/summary?start_date=2025-04-01&end_date=2025-09-30');
const topPerformers = await fetch('/api/analytics/top_performers?limit=5&start_date=2025-04-01&end_date=2025-09-30');
const goalStatus = await fetch('/api/analytics/goals/vs_actual?period_type=monthly&start_date=2025-04-01&end_date=2025-09-30');
```

### Reporte Mensual de Vendedor
```javascript
const employeeId = 1;
const month = '2025-06';

// Facturación del mes
const sales = await fetch(`/api/analytics/invoicing/by_employee?start_date=${month}-01&end_date=${month}-30`);

// Metas del mes
const goals = await fetch(`/api/sales_goals/by_employee/${employeeId}`);
```

### Análisis de Sucursal
```javascript
const branchId = 3;

// Ventas de la sucursal
const branchSales = await fetch('/api/analytics/invoicing/by_branch?start_date=2025-04-01&end_date=2025-09-30');

// Metas de la sucursal
const branchGoals = await fetch(`/api/sales_goals/by_branch/${branchId}`);
```

---

**Última actualización**: 2025-10-18  
**Versión API**: 1.0  
**Base URL**: http://127.0.0.1:5000/api
