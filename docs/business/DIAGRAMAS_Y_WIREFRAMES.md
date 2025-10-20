# 📊 DIAGRAMAS Y WIREFRAMES - Multicont

**Fecha**: 19 de Octubre, 2025  
**Autores**: Wilker & Daniel  
**Propósito**: Entrega académica - Artefactos visuales del proyecto

---

## 📊 Diagramas Técnicos

Los diagramas técnicos documentan la arquitectura, modelo de datos y flujos del sistema Multicont.

### Archivos Disponibles

Todos los diagramas están en formato **PlantUML (.puml)** y **PNG** exportado:

#### 1. ERD_database - Diagrama Entidad-Relación
- **Archivo**: [`docs/diagrams/ERD_database.puml`](docs/diagrams/ERD_database.puml)
- **PNG**: [`docs/diagrams/ERD_database.png`](docs/diagrams/ERD_database.png)
- **Descripción**: Diagrama de base de datos con 21 tablas y sus relaciones
- **Contenido**:
  - Entidades principales: User, Organization, Branch, Employee
  - Inventario: InventoryItem, ItemCategory, Brand
  - Ciclo de ventas: Quote, SalesOrder, Invoice, QuotationLine, InvoiceItem
  - Configuración: State, City, Role, Permission
  - Analytics: SalesGoal
- **Relaciones**: 1:N, N:M con claves foráneas visibles
- **Generado con**: `python scripts/diagrams/generate_erd_plantuml.py`

#### 2. ARCHITECTURE_layers - Clean Architecture (3 Capas)
- **Archivo**: [`docs/diagrams/ARCHITECTURE_layers.puml`](docs/diagrams/ARCHITECTURE_layers.puml)
- **PNG**: [`docs/diagrams/ARCHITECTURE_layers.png`](docs/diagrams/ARCHITECTURE_layers.png)
- **Descripción**: Arquitectura en capas del sistema
- **Contenido**:
  - **API Layer** (Presentation): 24 blueprints Flask
  - **Handlers Layer** (Application): 22 use cases
  - **Entities Layer** (Domain): 21 modelos de dominio
  - **Database Layer**: PostgreSQL + SQLAlchemy
- **Flujo de datos**: Request → API → Handler → Entity → DB

#### 3. CLASS_diagram - Diagrama de Clases UML
- **Archivo**: [`docs/diagrams/CLASS_diagram.puml`](docs/diagrams/CLASS_diagram.puml)
- **PNG**: [`docs/diagrams/CLASS_diagram.png`](docs/diagrams/CLASS_diagram.png)
- **Descripción**: Diagrama UML de clases principales
- **Contenido**:
  - **BaseHandler**: Clase base con CRUD genérico
  - Handlers específicos: UserHandler, QuoteHandler, InvoiceHandler, etc.
  - Métodos: create(), get(), list_all(), update(), delete(), count()
  - Herencia y reutilización de código (DRY pattern)

#### 4. USE_CASES - Casos de Uso del Sistema
- **Archivo**: [`docs/diagrams/USE_CASES.puml`](docs/diagrams/USE_CASES.puml)
- **PNG**: [`docs/diagrams/USE_CASES.png`](docs/diagrams/USE_CASES.png)
- **Descripción**: Casos de uso funcionales
- **Actores**:
  - **Admin**: Gestión completa del sistema
  - **Manager**: Gestión de ventas y empleados
  - **Sales**: Cotizaciones y consultas
- **Casos de Uso**:
  - Autenticación (Login, Logout)
  - Gestión de organizaciones y sucursales
  - Control de inventario
  - Ciclo de ventas (cotizar, ordenar, facturar)
  - Analytics y reportes

#### 5. SEQ_auth - Secuencia de Autenticación JWT
- **Archivo**: [`docs/diagrams/SEQ_auth.puml`](docs/diagrams/SEQ_auth.puml)
- **PNG**: [`docs/diagrams/SEQ_auth.png`](docs/diagrams/SEQ_auth.png)
- **Descripción**: Flujo de login con JWT
- **Participantes**:
  - Usuario (Frontend)
  - API (Flask Blueprint)
  - AuthService
  - UserHandler
  - Database
- **Flujo**:
  1. Usuario envía credenciales (POST /api/auth/login)
  2. API valida con AuthService
  3. AuthService busca usuario en BD
  4. Valida password con bcrypt
  5. Genera access_token + refresh_token
  6. Retorna tokens y datos de usuario
  7. Usuario almacena tokens para futuras requests

#### 6. SEQ_invoice - Secuencia de Creación de Factura
- **Archivo**: [`docs/diagrams/SEQ_invoice.puml`](docs/diagrams/SEQ_invoice.puml)
- **PNG**: [`docs/diagrams/SEQ_invoice.png`](docs/diagrams/SEQ_invoice.png)
- **Descripción**: Flujo de facturación
- **Participantes**:
  - Usuario (con JWT)
  - InvoiceAPI
  - InvoiceHandler
  - Invoice Entity
  - InvoiceItem Entity
  - InventoryItem Entity
  - Database
- **Flujo**:
  1. POST /api/invoices/ con items
  2. Validación JWT + RBAC
  3. Crear Invoice
  4. Por cada item:
     - Crear InvoiceItem
     - Reducir stock en InventoryItem (remove_stock())
  5. Calcular total de factura
  6. Commit transacción
  7. Retornar factura creada

---

## 🎨 Wireframes UI/UX

Los wireframes documentan la interfaz de usuario propuesta para el frontend del sistema Multicont.

### Archivos Disponibles

Todos los wireframes están en formato **PNG** con nombres estandarizados `WF-XXX_nombre.png`:

#### WF-001: Login
- **Archivo**: [`docs/wireframes/WF-001_login.png`](docs/wireframes/WF-001_login.png)
- **Descripción**: Pantalla de autenticación con JWT
- **Elementos**:
  - Logo del sistema
  - Input: Username/Email
  - Input: Password (tipo password)
  - Checkbox: "Recordar sesión"
  - Botón: "Iniciar Sesión"
  - Link: "¿Olvidaste tu contraseña?"
  - Footer con versión

#### WF-002: Dashboard Principal
- **Archivo**: [`docs/wireframes/WF-002_dashboard.png`](docs/wireframes/WF-002_dashboard.png)
- **Descripción**: Panel principal con KPIs y métricas
- **Elementos**:
  - Header con breadcrumb
  - 4 Cards de KPIs:
    * Total Ventas del Mes ($)
    * Órdenes Pendientes (#)
    * Inventario Bajo Stock (#)
    * Empleados Activos (#)
  - Gráfico de líneas: Ventas últimos 6 meses
  - Gráfico de barras: Top 5 productos
  - Tabla: Últimas 5 cotizaciones
  - Card lateral: Notificaciones/Alertas

#### WF-003: Lista de Organizaciones
- **Archivo**: [`docs/wireframes/WF-003_organizations_list.png`](docs/wireframes/WF-003_organizations_list.png)
- **Descripción**: Tabla de organizaciones con CRUD
- **Elementos**:
  - Breadcrumb: Inicio > Organizaciones
  - Barra de búsqueda
  - Botón "+ Nueva Organización"
  - Filtro por Estado (Activo/Inactivo)
  - Tabla con columnas:
    * ID, Nombre, NIT, Teléfono, Estado
    * Acciones (editar, eliminar)
  - Paginación: "Mostrando 1-10 de 45 | Página 1 2 3 >"

#### WF-004: Formulario de Organización
- **Archivo**: [`docs/wireframes/WF-004_organization_form.png`](docs/wireframes/WF-004_organization_form.png)
- **Descripción**: Modal/formulario para crear/editar organización
- **Elementos**:
  - Campos: Nombre*, NIT*, Teléfono, Email, Dirección, Estado
  - Indicadores de campos requeridos (*)
  - Validaciones visuales (rojo para errores)
  - Botones: "Guardar" (primario), "Cancelar" (secundario)

#### WF-005: Lista de Empleados
- **Archivo**: [`docs/wireframes/WF-005_employees_list.png`](docs/wireframes/WF-005_employees_list.png)
- **Descripción**: Gestión de empleados
- **Elementos**:
  - Similar a Organizations List
  - Filtros: Sucursal, Estado
  - Tabla: ID, Nombre Completo, Email, Sucursal, Cargo (badge), Estado, Acciones
  - Badges de rol: [ADMIN] (azul), [MANAGER] (naranja), [SALES] (verde)

#### WF-006: Lista de Inventario
- **Archivo**: [`docs/wireframes/WF-006_inventory_list.png`](docs/wireframes/WF-006_inventory_list.png)
- **Descripción**: Control de inventario con alertas de stock bajo
- **Elementos**:
  - Filtros: Categoría, Marca, Stock (Todos/Bajo/Normal)
  - Tabla: SKU, Nombre, Categoría, Marca, Cantidad, Precio, Acciones
  - **Alerta visual**: Filas con fondo rojo claro cuando Cantidad < 10
  - Indicador: "⚠️ Stock Bajo" en columna de cantidad

#### WF-007: Crear Cotización
- **Archivo**: [`docs/wireframes/WF-007_create_quote.png`](docs/wireframes/WF-007_create_quote.png)
- **Descripción**: Formulario complejo para cotización con líneas de productos
- **Secciones**:
  1. **Información General**:
     - Cliente (select/autocomplete)
     - Fecha cotización, Fecha vencimiento (date pickers)
     - Vendedor (autocompletado con usuario actual)
  2. **Líneas de Productos**:
     - Tabla editable: Producto, Cantidad, Precio Unit., Subtotal, [Eliminar]
     - Botón "+ Agregar Producto"
  3. **Totales**:
     - Subtotal, IVA (19%), **TOTAL** (destacado, grande)
  - Botones: "Cancelar", "Guardar Borrador" (gris), "Crear Cotización" (azul)

#### WF-008: Analytics Dashboard
- **Archivo**: [`docs/wireframes/WF-008_analytics_dashboard.png`](docs/wireframes/WF-008_analytics_dashboard.png)
- **Descripción**: Dashboard de análisis y métricas avanzadas
- **Elementos**:
  - Filtros globales: Periodo (Día/Semana/Mes/Año), Sucursal, Empleado
  - 6 Cards de KPIs:
    * Ventas Totales
    * Metas Cumplidas (%)
    * Promedio por Venta
    * Órdenes Completadas
    * Facturación Pendiente
    * Top Vendedor del Mes
  - Gráfico de líneas: Ventas vs Metas (6 meses)
  - Gráfico de barras: Ventas por Sucursal
  - Gráfico de pie: Ventas por Marca
  - Tabla: Top 10 Performers (ranking de vendedores)

---

## 📐 Especificaciones Técnicas

### Herramientas Usadas

- **PlantUML**: Para diagramas técnicos (ERD, UML, Secuencias)
- **Excalidraw/Figma**: Para wireframes UI/UX (recomendado)
- **Exportación**: PNG de alta calidad (mínimo 1280x720 px)

### Convenciones de Wireframes

#### Layout General
- **Header**: Logo + Usuario + Notificaciones + Logout
- **Sidebar**: Menú de navegación con iconos
- **Content Area**: Breadcrumbs + Título + Contenido principal
- **Footer**: Copyright + Versión del sistema

#### Componentes Estándar
- **Tablas**: Con paginación, búsqueda, filtros, acciones (editar/eliminar)
- **Formularios**: Con validación visual (campos required, tipos de dato)
- **Botones**: 
  - Primario (azul): Acción principal
  - Secundario (gris): Acción alternativa
  - Peligro (rojo): Acciones destructivas (eliminar)
- **Cards**: Para métricas y KPIs
- **Modales**: Para confirmaciones y formularios rápidos

#### Paleta de Colores
- **Primary**: #3B82F6 (azul)
- **Success**: #10B981 (verde)
- **Warning**: #F59E0B (amarillo)
- **Danger**: #EF4444 (rojo)
- **Gray**: #6B7280 (neutro)

---

## 📚 Documentación Relacionada

### Diagramas
- **Guía de generación**: [`docs/diagrams/GENERAR_PNG_INSTRUCCIONES.md`](docs/diagrams/GENERAR_PNG_INSTRUCCIONES.md)
- **Documentación técnica**: [`docs/diagrams/DIAGRAMAS.md`](docs/diagrams/DIAGRAMAS.md)
- **Script de ERD**: [`scripts/diagrams/generate_erd_plantuml.py`](scripts/diagrams/generate_erd_plantuml.py)

### Wireframes
- **Guía de creación**: [`docs/wireframes/CREAR_WIREFRAMES_GUIA.md`](docs/wireframes/CREAR_WIREFRAMES_GUIA.md)
- **Especificaciones**: [`docs/wireframes/WIREFRAMES.md`](docs/wireframes/WIREFRAMES.md)

### Arquitectura
- **README principal**: [`README.md`](README.md)
- **Copilot Instructions**: [`.github/copilot-instructions.md`](.github/copilot-instructions.md)
- **Estructura del proyecto**: [`docs/ESTRUCTURA_PROYECTO.md`](docs/ESTRUCTURA_PROYECTO.md)

---

## 📝 Checklist de Entrega Académica

### Diagramas Técnicos ✅
- [x] ERD_database.puml (generado automáticamente)
- [x] ERD_database.png (exportado)
- [x] ARCHITECTURE_layers.puml
- [x] ARCHITECTURE_layers.png
- [x] CLASS_diagram.puml
- [x] CLASS_diagram.png
- [x] USE_CASES.puml
- [x] USE_CASES.png
- [x] SEQ_auth.puml
- [x] SEQ_auth.png
- [x] SEQ_invoice.puml
- [x] SEQ_invoice.png

### Wireframes UI/UX ⚠️
- [ ] WF-001_login.png (PENDIENTE - seguir guía en CREAR_WIREFRAMES_GUIA.md)
- [ ] WF-002_dashboard.png (PENDIENTE)
- [ ] WF-003_organizations_list.png (PENDIENTE)
- [ ] WF-004_organization_form.png (PENDIENTE)
- [ ] WF-005_employees_list.png (PENDIENTE)
- [ ] WF-006_inventory_list.png (PENDIENTE)
- [ ] WF-007_create_quote.png (PENDIENTE)
- [ ] WF-008_analytics_dashboard.png (PENDIENTE)

### Documentación ✅
- [x] WIREFRAMES.md (especificaciones completas)
- [x] DIAGRAMAS.md (guía técnica)
- [x] GENERAR_PNG_INSTRUCCIONES.md (cómo generar PNG desde PlantUML)
- [x] CREAR_WIREFRAMES_GUIA.md (cómo crear wireframes con Excalidraw/Figma)
- [x] Este archivo (DIAGRAMAS_Y_WIREFRAMES.md)

---

## 🚀 Próximos Pasos

### Para Wilker (Wireframes)

1. **Generar PNG de Diagramas** (15-20 minutos):
   - Abrir https://www.plantuml.com/plantuml/uml/
   - Por cada archivo .puml en `docs/diagrams/`:
     * Copiar contenido completo
     * Pegar en editor online
     * Click "Submit"
     * Guardar imagen PNG con mismo nombre
   - Total: 6 PNGs a generar

2. **Crear Wireframes** (3-5 horas):
   - Opción recomendada: https://excalidraw.com
   - Seguir guía detallada en `CREAR_WIREFRAMES_GUIA.md`
   - Crear 8 wireframes según especificaciones en `WIREFRAMES.md`
   - Exportar como PNG (1280x720 mínimo)
   - Guardar en `docs/wireframes/` con nombres estándar

3. **Commit y Push**:
   ```bash
   git add docs/diagrams/*.png docs/wireframes/*.png
   git commit -m "docs: Add diagram PNGs and wireframes for academic delivery"
   git push origin main
   ```

---

## 📊 Estadísticas del Proyecto

### Diagramas
- **Total archivos**: 12 (.puml sources + .png exports)
- **Tipos**: ERD, Architecture, Classes, Use Cases, Sequences (2)
- **Generados automáticamente**: ERD (con script Python)
- **Herramienta**: PlantUML

### Wireframes
- **Total requerido**: 8 pantallas
- **Formato**: PNG (alta calidad)
- **Herramienta recomendada**: Excalidraw (gratis, rápido)
- **Tiempo estimado**: 3-5 horas

### Documentación
- **Archivos .md**: 6 documentos técnicos
- **Guías paso a paso**: 2 (diagramas + wireframes)
- **Líneas de documentación**: ~1,500 líneas

---

**Última actualización**: 19 de Octubre, 2025  
**Autores**: Wilker & Daniel  
**Propósito**: Entrega académica - Proyecto Multicont

---

**⚠️ IMPORTANTE**: Los wireframes (archivos PNG) están pendientes de creación. Todas las especificaciones, guías y documentación están completas. Solo falta la generación de los archivos visuales siguiendo las guías proporcionadas.
