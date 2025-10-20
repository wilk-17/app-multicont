# 📋 REGLAS DE NEGOCIO - Sistema Multicont

**Versión**: 1.0  
**Fecha**: 20 de Enero de 2025  
**Última actualización**: 20 de Enero de 2025

---

## 📑 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Trazabilidad de Empleados](#1-trazabilidad-de-empleados)
3. [Sistema de Metas de Ventas](#2-sistema-de-metas-de-ventas)
4. [Facturación por Empleado](#3-facturación-por-empleado)
5. [Facturación por Sucursal](#4-facturación-por-sucursal)
6. [Facturación por Marca](#5-facturación-por-marca)
7. [Cotizaciones por Marca](#6-cotizaciones-por-marca)
8. [Indicadores de Rendimiento](#7-indicadores-de-rendimiento)
9. [Casos de Uso Comunes](#casos-de-uso-comunes)

---

## Introducción

Este documento describe las **reglas de negocio** implementadas en el sistema Multicont, mapeando cada requisito funcional a su implementación técnica (entidades, handlers, APIs).

### Propósito

El sistema permite:
- **Trazabilidad completa** de empleados y asignaciones de items
- **Seguimiento de metas** mensuales, trimestrales y anuales
- **Análisis de facturación** por empleado, sucursal y marca
- **Estadísticas de cotizaciones** para identificar tendencias
- **Indicadores de rendimiento** (top performers, porcentajes de cumplimiento)

---

## 1. Trazabilidad de Empleados

### 📌 Regla de Negocio

> **RN-001**: El sistema debe permitir rastrear el historial completo de asignaciones de items de inventario a empleados, incluyendo estado actual (activo, devuelto, perdido) y condición del item al momento de devolución.

### Implementación Técnica

#### Entity: `Assignment`
**Archivo**: `app/entities/assignment.py`

```python
class Assignment(db.Model):
    __tablename__ = "assignment"
    
    # Identificadores
    id = db.Column(db.BigInteger, primary_key=True)
    employee_id = db.Column(db.BigInteger, ForeignKey("employee.id"))
    item_id = db.Column(db.BigInteger, ForeignKey("inventory_item.id"))
    
    # Tracking temporal
    assigned_date = db.Column(db.Date, default=date.today)
    return_date = db.Column(db.Date, nullable=True)
    
    # Estado de trazabilidad
    status = db.Column(db.String(20), default='active')  # active, returned, lost
    condition = db.Column(db.String(50), nullable=True)  # good, damaged, missing
    notes = db.Column(db.Text, nullable=True)
    
    # Auditoría
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, onupdate=datetime.utcnow)
```

#### Handler: `AssignmentHandler`
**Archivo**: `app/use_cases/assignment_handler.py`

**Métodos clave**:
- `get_employee_history(employee_id)` → Historial completo agrupado por status
- `mark_returned(assignment_id, condition, notes)` → Marca item como devuelto
- `mark_lost(assignment_id, notes)` → Marca item como perdido
- `get_by_employee(employee_id, status)` → Filtrar asignaciones por status

#### API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/asignaciones/employee/<id>/history` | Historial completo del empleado |
| PUT | `/api/asignaciones/<id>/return` | Marcar como devuelto (good/damaged) |
| PUT | `/api/asignaciones/<id>/lost` | Marcar como perdido |
| GET | `/api/asignaciones/?status=active` | Filtrar por status |

#### Ejemplo de Uso

```bash
# Obtener historial completo de empleado ID=5
GET /api/asignaciones/employee/5/history

Response:
{
  "success": true,
  "data": {
    "employee_id": 5,
    "summary": {
      "total_assignments": 12,
      "active_count": 5,
      "returned_count": 6,
      "lost_count": 1
    },
    "active": [...],
    "returned": [...],
    "lost": [...]
  }
}

# Marcar asignación como devuelta en buen estado
PUT /api/asignaciones/3/return
{
  "condition": "good",
  "notes": "Item devuelto en perfecto estado"
}
```

---

## 2. Sistema de Metas de Ventas

### 📌 Regla de Negocio

> **RN-002**: El sistema debe permitir asignar metas de ventas mensuales, trimestrales y anuales a empleados individuales o a sucursales completas, y comparar el desempeño real contra la meta establecida.

### Implementación Técnica

#### Entity: `SalesGoal`
**Archivo**: `app/entities/sales_goal.py`

```python
class SalesGoal(db.Model):
    __tablename__ = "sales_goal"
    
    id = db.Column(db.BigInteger, primary_key=True)
    
    # Alcance de la meta (mutuamente exclusivo)
    employee_id = db.Column(db.BigInteger, ForeignKey("employee.id"), nullable=True)
    branch_id = db.Column(db.BigInteger, ForeignKey("branch.id"), nullable=True)
    
    # Tipo de período
    period_type = db.Column(db.String(20))  # 'monthly', 'quarterly', 'yearly'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    # Meta y seguimiento
    target_amount = db.Column(db.Numeric(12, 2), nullable=False)
    
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, onupdate=datetime.utcnow)
```

#### Handler: `SalesGoalHandler`
**Archivo**: `app/use_cases/sales_goal_handler.py`

**Métodos CRUD**:
- `create(employee_id, branch_id, period_type, start_date, end_date, target_amount)`
- `get_by_employee(employee_id)`
- `get_by_branch(branch_id)`
- `get_current(reference_date)` → Metas vigentes en una fecha

#### API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/sales_goals/` | Listar todas las metas (filtros: period_type, employee_id, branch_id) |
| GET | `/api/sales_goals/<id>` | Obtener meta por ID |
| GET | `/api/sales_goals/employee/<id>` | Metas de un empleado |
| GET | `/api/sales_goals/branch/<id>` | Metas de una sucursal |
| POST | `/api/sales_goals/` | Crear nueva meta |
| PUT | `/api/sales_goals/<id>` | Actualizar meta |
| DELETE | `/api/sales_goals/<id>` | Eliminar meta |

### Analytics: Metas vs Actual

**Endpoint**: `/api/analytics/goals/vs_actual`

```python
# Lógica de cálculo
actual_sales = db.session.query(func.sum(Invoice.total)).filter(
    Invoice.employee_id == goal.employee_id,
    Invoice.date >= goal.start_date,
    Invoice.date <= goal.end_date
).scalar() or 0

achievement_percentage = (actual_sales / target_amount) * 100

# Determinar status
if achievement_percentage >= 100:
    status = 'exceeded'  # ✅ Superó la meta
elif achievement_percentage >= 80:
    status = 'on_track'  # 🟢 En camino
elif achievement_percentage >= 50:
    status = 'at_risk'   # 🟡 En riesgo
else:
    status = 'failed'    # 🔴 No cumplió
```

#### Ejemplo de Uso

```bash
# Comparar metas mensuales vs facturación real
GET /api/analytics/goals/vs_actual?period_type=monthly&start_date=2025-01-01&end_date=2025-01-31

Response:
{
  "success": true,
  "data": [
    {
      "goal_id": "1",
      "employee_id": "4",
      "employee_name": "Diego Luna",
      "period_type": "monthly",
      "start_date": "2025-01-01",
      "end_date": "2025-01-31",
      "target_amount": 15000000.0,
      "actual_sales": 18300000.0,
      "achievement_percentage": 122.0,
      "status": "exceeded"
    }
  ]
}
```

---

## 3. Facturación por Empleado

### 📌 Regla de Negocio

> **RN-003**: El sistema debe calcular el total facturado por cada empleado (vendedor) en un período de tiempo dado, incluyendo el número de facturas generadas.

### Implementación Técnica

#### SQL Query (Lógica interna)

```sql
SELECT 
    i.employee_id,
    CONCAT(p.first_name, ' ', p.last_name) AS employee_name,
    e.branch_id,
    b.name AS branch_name,
    COUNT(i.id) AS invoice_count,
    SUM(i.total) AS total_invoiced
FROM invoice i
JOIN employee e ON i.employee_id = e.id
JOIN person p ON e.person_id = p.id
LEFT JOIN branch b ON e.branch_id = b.id
WHERE i.date BETWEEN :start_date AND :end_date
GROUP BY i.employee_id
ORDER BY total_invoiced DESC;
```

#### API Endpoint

**Endpoint**: `/api/analytics/invoicing/by_employee`

**Parámetros**:
- `start_date` (required): Fecha inicio (formato: YYYY-MM-DD)
- `end_date` (required): Fecha fin
- `employee_id` (optional): Filtrar por empleado específico

#### Ejemplo de Uso

```bash
GET /api/analytics/invoicing/by_employee?start_date=2025-04-01&end_date=2025-09-30

Response:
{
  "success": true,
  "data": [
    {
      "employee_id": "10",
      "employee_name": "Jorge Nieto",
      "branch_id": "5",
      "branch_name": "Sucursal 5",
      "invoice_count": 4,
      "total_invoiced": 39350000.0
    },
    {
      "employee_id": "4",
      "employee_name": "Diego Luna",
      "branch_id": "2",
      "branch_name": "Sucursal 2",
      "invoice_count": 3,
      "total_invoiced": 30200000.0
    }
  ]
}
```

---

## 4. Facturación por Sucursal

### 📌 Regla de Negocio

> **RN-004**: El sistema debe consolidar la facturación total por sucursal, sumando las ventas de todos los empleados asignados a cada sucursal en un período dado.

### Implementación Técnica

#### SQL Query (Lógica interna)

```sql
SELECT 
    e.branch_id,
    b.name AS branch_name,
    b.city,
    COUNT(DISTINCT i.employee_id) AS employee_count,
    COUNT(i.id) AS invoice_count,
    SUM(i.total) AS total_sales
FROM invoice i
JOIN employee e ON i.employee_id = e.id
LEFT JOIN branch b ON e.branch_id = b.id
WHERE i.date BETWEEN :start_date AND :end_date
GROUP BY e.branch_id
ORDER BY total_sales DESC;
```

#### API Endpoint

**Endpoint**: `/api/analytics/invoicing/by_branch`

**Parámetros**:
- `start_date` (required)
- `end_date` (required)
- `branch_id` (optional): Filtrar por sucursal específica

#### Ejemplo de Uso

```bash
GET /api/analytics/invoicing/by_branch?start_date=2025-04-01&end_date=2025-09-30

Response:
{
  "success": true,
  "data": [
    {
      "branch_id": "5",
      "branch_name": "Sucursal 5",
      "city": "Barranquilla",
      "employee_count": 3,
      "invoice_count": 8,
      "total_sales": 72500000.0
    }
  ]
}
```

---

## 5. Facturación por Marca

### 📌 Regla de Negocio

> **RN-005**: El sistema debe analizar las ventas por marca de producto, calculando el total facturado, cantidad vendida y número de facturas que incluyen productos de cada marca.

### Implementación Técnica

#### SQL Query (Lógica interna)

```sql
SELECT 
    inv_item.brand_id,
    b.name AS brand_name,
    COUNT(DISTINCT inv_i.invoice_id) AS invoice_count,
    SUM(inv_i.quantity * inv_i.price) AS total_invoiced,
    SUM(inv_i.quantity) AS total_quantity
FROM invoice i
JOIN invoice_item inv_i ON i.id = inv_i.invoice_id
JOIN inventory_item inv_item ON inv_i.item_id = inv_item.id
JOIN brand b ON inv_item.brand_id = b.id
WHERE i.date BETWEEN :start_date AND :end_date
  AND inv_item.brand_id IS NOT NULL
GROUP BY inv_item.brand_id
ORDER BY total_invoiced DESC;
```

#### API Endpoint

**Endpoint**: `/api/analytics/invoicing/by_brand`

**Parámetros**:
- `start_date` (required)
- `end_date` (required)
- `brand_id` (optional): Filtrar por marca específica

#### Ejemplo de Uso

```bash
GET /api/analytics/invoicing/by_brand?start_date=2025-04-01&end_date=2025-09-30

Response:
{
  "success": true,
  "data": [
    {
      "brand_id": "1",
      "brand_name": "Omron",
      "invoice_count": 8,
      "total_invoiced": 45000000.0,
      "total_quantity": 120
    },
    {
      "brand_id": "3",
      "brand_name": "Gefran",
      "invoice_count": 5,
      "total_invoiced": 32000000.0,
      "total_quantity": 45
    }
  ]
}
```

---

## 6. Cotizaciones por Marca

### 📌 Regla de Negocio

> **RN-006**: El sistema debe rastrear el número de cotizaciones generadas para productos de cada marca, permitiendo identificar marcas de mayor interés comercial.

### Implementación Técnica

#### SQL Query (Lógica interna)

```sql
SELECT 
    inv_item.brand_id,
    b.name AS brand_name,
    COUNT(DISTINCT q_item.quote_id) AS quote_count,
    SUM(q_item.quantity) AS total_quantity
FROM quote q
JOIN quote_item q_item ON q.id = q_item.quote_id
JOIN inventory_item inv_item ON q_item.item_id = inv_item.id
JOIN brand b ON inv_item.brand_id = b.id
WHERE q.date BETWEEN :start_date AND :end_date
  AND inv_item.brand_id IS NOT NULL
GROUP BY inv_item.brand_id
ORDER BY quote_count DESC;
```

#### API Endpoint

**Endpoint**: `/api/analytics/quotes/by_brand`

**Parámetros**:
- `start_date` (required)
- `end_date` (required)
- `brand_id` (optional)

#### Ejemplo de Uso

```bash
GET /api/analytics/quotes/by_brand?start_date=2025-04-01&end_date=2025-09-30

Response:
{
  "success": true,
  "data": [
    {
      "brand_id": "1",
      "brand_name": "Omron",
      "quote_count": 52,
      "total_quantity": 210
    },
    {
      "brand_id": "2",
      "brand_name": "ING Multicontrol",
      "quote_count": 38,
      "total_quantity": 145
    }
  ]
}
```

---

## 7. Indicadores de Rendimiento

### 📌 Regla de Negocio

> **RN-007**: El sistema debe generar rankings de vendedores (top performers) ordenados por volumen de facturación, permitiendo identificar a los mejores vendedores del período.

### Implementación Técnica

#### API Endpoint

**Endpoint**: `/api/analytics/top_performers`

**Parámetros**:
- `start_date` (required)
- `end_date` (required)
- `limit` (optional, default=10): Top N vendedores

#### SQL Query (Lógica interna)

```sql
SELECT 
    i.employee_id,
    CONCAT(p.first_name, ' ', p.last_name) AS employee_name,
    e.branch_id,
    b.name AS branch_name,
    COUNT(i.id) AS invoice_count,
    SUM(i.total) AS total_sales
FROM invoice i
JOIN employee e ON i.employee_id = e.id
JOIN person p ON e.person_id = p.id
LEFT JOIN branch b ON e.branch_id = b.id
WHERE i.date BETWEEN :start_date AND :end_date
GROUP BY i.employee_id
ORDER BY total_sales DESC
LIMIT :limit;
```

#### Ejemplo de Uso

```bash
GET /api/analytics/top_performers?start_date=2025-04-01&end_date=2025-09-30&limit=5

Response:
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "employee_id": "10",
      "employee_name": "Jorge Nieto",
      "branch_name": "Sucursal 5",
      "invoice_count": 4,
      "total_sales": 39350000.0
    },
    {
      "rank": 2,
      "employee_id": "4",
      "employee_name": "Diego Luna",
      "branch_name": "Sucursal 2",
      "invoice_count": 3,
      "total_sales": 30200000.0
    }
  ]
}
```

---

## Casos de Uso Comunes

### Caso 1: Análisis Mensual de Sucursal

**Objetivo**: Evaluar desempeño completo de una sucursal en un mes

```bash
# 1. Facturación total de la sucursal
GET /api/analytics/invoicing/by_branch?start_date=2025-10-01&end_date=2025-10-31&branch_id=3

# 2. Metas de la sucursal
GET /api/sales_goals/branch/3

# 3. Top performers de la sucursal
GET /api/analytics/top_performers?start_date=2025-10-01&end_date=2025-10-31
# Filtrar manualmente por branch_id=3
```

### Caso 2: Auditoría de Asignaciones de Empleado

**Objetivo**: Verificar estado de todos los items asignados a un empleado

```bash
# Historial completo con estadísticas
GET /api/asignaciones/employee/5/history

Response incluye:
- Total de asignaciones: 12
- Activos: 5 items
- Devueltos: 6 items (con condición: good/damaged)
- Perdidos: 1 item
```

### Caso 3: Comparación Metas vs Ventas Trimestrales

**Objetivo**: Evaluar cumplimiento de metas Q2 2025

```bash
GET /api/analytics/goals/vs_actual?period_type=quarterly&start_date=2025-04-01&end_date=2025-06-30

# Resultado muestra achievement_percentage y status para cada meta
```

---

## Resumen de Endpoints Principales

| Categoría | Endpoint | Método | Descripción |
|-----------|----------|--------|-------------|
| **Trazabilidad** | `/api/asignaciones/employee/<id>/history` | GET | Historial de asignaciones |
| **Trazabilidad** | `/api/asignaciones/<id>/return` | PUT | Marcar como devuelto |
| **Trazabilidad** | `/api/asignaciones/<id>/lost` | PUT | Marcar como perdido |
| **Metas** | `/api/sales_goals/` | GET | Listar metas (CRUD) |
| **Metas** | `/api/analytics/goals/vs_actual` | GET | Metas vs facturación real |
| **Facturación** | `/api/analytics/invoicing/by_employee` | GET | Total por empleado |
| **Facturación** | `/api/analytics/invoicing/by_branch` | GET | Total por sucursal |
| **Facturación** | `/api/analytics/invoicing/by_brand` | GET | Total por marca |
| **Cotizaciones** | `/api/analytics/quotes/by_brand` | GET | Cotizaciones por marca |
| **Rankings** | `/api/analytics/top_performers` | GET | Top vendedores |

---

## Notas de Implementación

### Consideraciones de Performance

1. **Cache**: Los endpoints de analytics usan cache de 10 minutos (`@cache.cached(timeout=600)`)
2. **Índices**: Las columnas `employee_id`, `branch_id`, `brand_id` tienen índices para búsquedas rápidas
3. **Paginación**: Todos los listados soportan paginación (`?page=1&per_page=10`)

### Validaciones de Negocio

1. **Metas**: No se pueden crear dos metas del mismo tipo (monthly/quarterly/yearly) para el mismo empleado en períodos superpuestos
2. **Asignaciones**: Un item marcado como 'lost' no puede cambiarse a 'returned'
3. **Fechas**: `end_date` debe ser mayor que `start_date` en metas y consultas de analytics

---

**Documento generado por**: AI Coding Agent  
**Basado en**: Implementación existente + Requerimientos del usuario  
**Próximas actualizaciones**: Indicadores de tendencia (RN-008)
