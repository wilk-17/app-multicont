# DIAGRAMAS TÉCNICOS - Sistema Multicont

**Fecha**: 19 de Octubre, 2025  
**Autores**: Wilker & Daniel  
**Herramienta**: PlantUML

---

## Descripción General

Este documento describe todos los diagramas técnicos del proyecto Multicont. Los diagramas están generados con PlantUML y pueden regenerarse automáticamente con los scripts provistos.

**Ubicación**: `docs/diagrams/`

---

## Lista de Diagramas

1. **ERD_database.puml** - Diagrama Entidad-Relación (generado automáticamente)
2. **ARCHITECTURE_layers.puml** - Arquitectura Clean (3 capas)
3. **CLASS_diagram.puml** - Diagrama de clases UML (BaseHandler + handlers)
4. **USE_CASES.puml** - Casos de uso (actores y casos)
5. **SEQ_auth.puml** - Secuencia de autenticación JWT
6. **SEQ_invoice.puml** - Secuencia de creación de factura

---

## Cómo Generar Diagramas

### Opción 1: PlantUML Local (Java)

```powershell
# Descargar PlantUML
# https://plantuml.com/download

# Generar todos los diagramas
java -jar plantuml.jar docs\diagrams\*.puml

# Generar uno específico
java -jar plantuml.jar docs\diagrams\ERD_database.puml
```

### Opción 2: VSCode Extension

1. Instalar extensión: "PlantUML" (jebbs.plantuml)
2. Abrir archivo `.puml`
3. `Alt + D` para preview
4. Click derecho → "Export Current Diagram" → PNG

### Opción 3: Online

Subir código a: https://www.plantuml.com/plantuml/uml/

---

## 1. Diagrama ERD (Entity-Relationship Diagram)

**Archivo**: `docs/diagrams/ERD_database.puml`  
**Generado**: ✅ Automáticamente con script

### Descripción

Diagrama de base de datos mostrando las **22 entidades** del sistema con sus relaciones (Foreign Keys).

### Entidades Principales

1. **User** - Usuarios del sistema
2. **Role** - Roles (Admin, Manager, Sales)
3. **Permission** - Permisos granulares
4. **Organization** - Organizaciones (clientes)
5. **Branch** - Sucursales de organizaciones
6. **Employee** - Empleados de sucursales
7. **Person** - Datos personales (asociado a Employee)
8. **InventoryItem** - Items de inventario
9. **ItemCategory** - Categorías de productos
10. **Brand** - Marcas de productos
11. **Quote** - Cotizaciones
12. **QuoteItem** - Items de cotización (relación Quote-InventoryItem)
13. **QuotationLine** - Líneas de cotización
14. **SalesOrder** - Órdenes de venta
15. **SalesOrderItem** - Items de órdenes
16. **Invoice** - Facturas
17. **InvoiceItem** - Items de facturas
18. **SalesGoal** - Metas de ventas
19. **City** - Ciudades
20. **State** - Estados/Departamentos
21. **UserRole** - Relación N:M User-Role
22. **Assignment** - Asignaciones (empleados-items)

### Relaciones Clave

- `Organization` 1:N `Branch`
- `Branch` 1:N `Employee`
- `User` N:M `Role` (mediante `UserRole`)
- `Quote` 1:N `QuotationLine`
- `SalesOrder` 1:N `SalesOrderItem`
- `Invoice` 1:N `InvoiceItem`
- `InventoryItem` N:1 `ItemCategory`
- `InventoryItem` N:1 `Brand`

### Cómo Regenerar

```powershell
# Ejecutar script automático
python scripts\diagrams\generate_erd_plantuml.py

# Output: docs/diagrams/ERD_database.puml

# Generar PNG
java -jar plantuml.jar docs\diagrams\ERD_database.puml
```

**Estado**: ✅ Script listo para ejecutar

---

## 2. Diagrama de Arquitectura (Clean Architecture)

**Archivo**: `docs/diagrams/ARCHITECTURE_layers.puml`  
**Generado**: ✅ Manualmente (plantilla lista)

### Descripción

Muestra las 3 capas de Clean Architecture implementadas en el proyecto:

1. **API Layer (Presentation)**
   - Flask Blueprints
   - 24 APIs REST
   - Request validation
   - Response formatting
   - Swagger docs

2. **Use Cases Layer (Application)**
   - BaseHandler (DRY pattern)
   - 22 Handlers específicos
   - Business logic
   - Transactions
   - Authorization

3. **Entities Layer (Domain)**
   - 21 SQLAlchemy Models
   - Domain logic
   - Database relationships
   - PostgreSQL

### Flujo de Request

```
Client → API Blueprint → Handler → Entity → Database
         ↓                ↓          ↓
    Validation      Business     Domain
                    Logic        Logic
```

### Principios Aplicados

- **Separation of Concerns**: Cada capa tiene responsabilidades claras
- **Dependency Inversion**: Dependencies apuntan hacia el dominio
- **Single Responsibility**: Handlers con una responsabilidad
- **DRY**: BaseHandler elimina duplicación

**Estado**: ✅ Plantilla lista

---

## 3. Diagrama de Clases UML

**Archivo**: `docs/diagrams/CLASS_diagram.puml`  
**Generado**: ✅ Manualmente (plantilla lista)

### Descripción

Diagrama UML mostrando el patrón de herencia de handlers y relación con entities.

### Clases Principales

**BaseHandler** (abstract):
- `create(**kwargs)`
- `get(id: int)`
- `list_all(page, per_page, filters)`
- `update(id, **kwargs)`
- `delete(id)`
- `count(filters)`
- `search(query, fields)`
- `bulk_create(items)`
- `export_to_csv()`

**Handlers Específicos** (heredan de BaseHandler):
- UserHandler
- OrganizationHandler
- BranchHandler
- EmployeeHandler
- InventoryItemHandler
- QuoteHandler
- SalesOrderHandler
- InvoiceHandler

### Relaciones

- `UserHandler` → `User` (manages)
- `OrganizationHandler` → `Organization` (manages)
- Todos heredan de `BaseHandler`

### Métodos Específicos

Cada handler añade métodos de negocio:
- `UserHandler.get_by_email()`
- `InventoryItemHandler.add_stock()`
- `QuoteHandler.convert_to_sales_order()`

**Estado**: ✅ Plantilla lista

---

## 4. Diagrama de Casos de Uso

**Archivo**: `docs/diagrams/USE_CASES.puml`  
**Generado**: ✅ Manualmente (plantilla lista)

### Descripción

Diagrama UML de casos de uso mostrando actores y funcionalidades del sistema.

### Actores

1. **Administrador**
   - Acceso completo al sistema
   - Gestiona usuarios, roles, permisos
   - Configura organizaciones

2. **Manager**
   - Gestiona operaciones del negocio
   - Aprueba cotizaciones
   - Ve reportes y analytics
   - Gestiona inventario

3. **Vendedor (Sales)**
   - Crea cotizaciones
   - Crea órdenes de venta
   - Consulta inventario
   - Ve su dashboard

4. **Sistema Externo** (futuro)
   - Integraciones con APIs externas

### Casos de Uso (30+)

**Autenticación** (UC-001 a UC-004):
- UC-001: Login con JWT
- UC-002: Refresh Token
- UC-003: Gestionar Roles
- UC-004: Gestionar Permisos

**Gestión Organizacional** (UC-005 a UC-008):
- UC-005: CRUD Organizaciones
- UC-006: CRUD Sucursales
- UC-007: CRUD Empleados
- UC-008: Asignar Empleado a Sucursal

**Inventario** (UC-012 a UC-016):
- UC-012: CRUD Inventario
- UC-013: Gestionar Categorías
- UC-014: Gestionar Marcas
- UC-015: Ajustar Stock
- UC-016: Alertas Stock Bajo

**Ciclo de Ventas** (UC-017 a UC-023):
- UC-017: Crear Cotización
- UC-018: Aprobar/Rechazar Cotización
- UC-019: Convertir Cotización a Orden
- UC-020: Crear Orden de Venta
- UC-021: Confirmar Orden
- UC-022: Generar Factura
- UC-023: Marcar Factura como Pagada

**Analytics** (UC-024 a UC-030):
- UC-024: Ver Dashboard KPIs
- UC-025: Analytics de Ventas
- UC-026: Reportes por Empleado
- UC-027: Reportes por Sucursal
- UC-028: Reportes por Marca
- UC-029: Metas vs Actual
- UC-030: Top Performers

**Estado**: ✅ Plantilla lista

---

## 5. Diagrama de Secuencia: Autenticación JWT

**Archivo**: `docs/diagrams/SEQ_auth.puml`  
**Generado**: ✅ Manualmente (plantilla lista)

### Descripción

Flujo detallado del proceso de autenticación con JWT.

### Actores y Componentes

- Usuario
- Browser/Client
- Flask API (`/api/auth/login`)
- AuthService
- User Model
- PostgreSQL

### Flujo (11 pasos)

1. Usuario ingresa credenciales (username, password)
2. Client → API: `POST /api/auth/login`
3. API → AuthService: `validate_credentials()`
4. AuthService → UserModel: `query.filter_by(username)`
5. UserModel → DB: `SELECT * FROM user`
6. DB → UserModel: user_record
7. UserModel → AuthService: User object
8. AuthService: `bcrypt.check_password_hash()`
9. **Si válido**:
   - AuthService: `generate_access_token(user)`
   - AuthService: `generate_refresh_token(user)`
   - API → Client: `200 OK {access_token, refresh_token}`
10. **Si inválido**:
    - API → Client: `401 Unauthorized`

### Detalles Técnicos

- **Hashing**: bcrypt con 12 rounds
- **Access Token**: 15 min expiración
- **Refresh Token**: 30 días expiración
- **Algoritmo**: HS256

**Estado**: ✅ Plantilla lista

---

## 6. Diagrama de Secuencia: Creación de Factura

**Archivo**: `docs/diagrams/SEQ_invoice.puml`  
**Generado**: ✅ Manualmente (plantilla lista)

### Descripción

Flujo completo de creación de factura desde una orden de venta, incluyendo reducción automática de stock.

### Actores y Componentes

- Manager (usuario)
- Client
- Invoice API (`/api/invoices`)
- InvoiceHandler
- SalesOrder Model
- Invoice Model
- InvoiceItem Model
- InventoryItem Model
- PostgreSQL

### Flujo (20+ pasos)

1. Manager solicita crear factura desde orden
2. Client → API: `POST /api/invoices/`
3. API: Validación JWT + RBAC (`@role_required(['Admin', 'Manager'])`)
4. API → Handler: `create_from_sales_order(sales_order_id)`
5. Handler → SOModel: Obtener orden de venta
6. Handler: Validar status == 'confirmed'
7. Handler: Crear Invoice
8. **Loop**: Para cada item en sales_order.items:
   - Crear InvoiceItem
   - Obtener InventoryItem
   - Reducir stock: `inventory_item.remove_stock(quantity)`
   - UPDATE inventory_item SET quantity = quantity - X
9. Handler: `db.session.commit()` (transacción atómica)
10. Handler → API: invoice.to_dict()
11. API → Client: `201 Created`

### Lógica de Negocio

1. Validar orden confirmada
2. Crear Invoice
3. Copiar items de orden
4. **Reducir stock automáticamente** ⚠️
5. Transacción atómica (rollback on error)

### Integridad

- Foreign Keys
- Transactions ACID
- Rollback automático en caso de error

**Estado**: ✅ Plantilla lista

---

## Instrucciones para Wilker

### Paso 1: Generar ERD Automáticamente

```powershell
# Ejecutar script
python scripts\diagrams\generate_erd_plantuml.py

# Verificar output
cat docs\diagrams\ERD_database.puml

# Generar PNG (si tienes PlantUML)
java -jar plantuml.jar docs\diagrams\ERD_database.puml
```

### Paso 2: Generar PNG de Plantillas

**Opción A: PlantUML local**

```powershell
java -jar plantuml.jar docs\diagrams\*.puml
```

**Opción B: VSCode Extension**

1. Instalar: "PlantUML" (jebbs.plantuml)
2. Abrir cada `.puml`
3. `Alt + D` para preview
4. Export PNG

**Opción C: Online**

1. Copiar contenido de cada `.puml`
2. Pegar en: https://www.plantuml.com/plantuml/uml/
3. Descargar PNG

### Paso 3: Verificar Output

Debe tener estos 6 PNG en `docs/diagrams/`:

- [ ] `ERD_database.png`
- [ ] `ARCHITECTURE_layers.png`
- [ ] `CLASS_diagram.png`
- [ ] `USE_CASES.png`
- [ ] `SEQ_auth.png`
- [ ] `SEQ_invoice.png`

### Paso 4: Commit

```powershell
git add docs/diagrams/
git commit -m "docs: add technical diagrams (ERD, architecture, UML, sequences)"
git push origin main
```

---

## Herramientas Alternativas

Si PlantUML no funciona:

1. **Draw.io** (https://app.diagrams.net)
   - Import PlantUML code
   - Editar visualmente
   - Exportar PNG

2. **Mermaid** (Markdown integrado)
   - Alternativa más simple
   - Soportado en GitHub

3. **dbdiagram.io** (solo para ERD)
   - Syntax más simple que PlantUML
   - Específico para bases de datos

---

## Checklist de Entrega

- [ ] Script `generate_erd_plantuml.py` ejecutado
- [ ] ERD generado con 21 entidades
- [ ] Arquitectura Clean (3 capas) exportado
- [ ] Diagrama de clases UML exportado
- [ ] Casos de uso exportado (30+ casos)
- [ ] Secuencia de auth exportado
- [ ] Secuencia de facturación exportado
- [ ] Todos los PNG en `docs/diagrams/`
- [ ] Este archivo completado
- [ ] Commit y push

---

**Última actualización**: 19 de Octubre, 2025  
**Próximo paso**: Ejecutar scripts y generar PNG de todos los diagramas
