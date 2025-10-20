# WIREFRAMES - Sistema Multicont

**Fecha de creación**: 19 de Octubre, 2025  
**Autores**: Wilker & Daniel  
**Herramienta**: Figma / Draw.io / Balsamiq

---

## Descripción General

Este documento describe los wireframes/mockups de las pantallas principales del sistema Multicont. Los wireframes están diseñados para cumplir con los requerimientos del corte académico y mostrar la interfaz de usuario del sistema de gestión empresarial.

**Objetivo**: Proveer una guía visual de la interfaz de usuario (UI/UX) del sistema antes de implementar el frontend.

## ⚠️ Nota Importante: Modelos Simplificados

Los wireframes fueron diseñados pensando en un modelo de negocio completo (basado en SQL reference con todos los campos posibles). Sin embargo, el **modelo actual de la aplicación es SIMPLIFICADO** por decisión de arquitectura (Clean Architecture con entidades puras).

**Ejemplo de diferencia**:
- **Wireframe WF-004** muestra: Nombre, NIT, Teléfono, Email, Dirección para Organization
- **Modelo actual `Organization`** tiene solo: `id`, `name`, `status`, `creation_date`, `update_date`

Esto es **INTENCIONAL** para mantener el sistema simple y funcional. Los wireframes sirven como **guía de diseño futuro** si se decide extender el modelo con más campos. Para la implementación actual, solo se utilizan los campos que existen en los modelos de `app/entities/`.

---

## Convenciones de Diseño

### Layout General
- **Header**: Logo + nombre de usuario + notificaciones + logout
- **Sidebar**: Menú de navegación con iconos y etiquetas
- **Content Area**: Área principal con breadcrumbs + título + contenido
- **Footer**: Copyright + versión del sistema

### Componentes Estándar
- **Tablas**: Con paginación, búsqueda, filtros y acciones (editar/eliminar)
- **Formularios**: Con validación visual (required fields, tipos de dato)
- **Botones**: Primario (azul), Secundario (gris), Peligro (rojo)
- **Cards**: Para métricas y KPIs
- **Modales**: Para confirmaciones y formularios rápidos

### Paleta de Colores (sugerida)
- **Primary**: #3B82F6 (azul)
- **Success**: #10B981 (verde)
- **Warning**: #F59E0B (amarillo)
- **Danger**: #EF4444 (rojo)
- **Gray**: #6B7280 (neutro)

---

## Pantallas Principales

### 1. Login (WF-001)

**Archivo**: `docs/wireframes/WF-001_login.png`

**Descripción**:
Pantalla de autenticación con JWT. Permite al usuario ingresar sus credenciales y acceder al sistema.

**Elementos**:
- Logo del sistema (centrado)
- Título: "Bienvenido a Multicont"
- Input: Username/Email (con icono de usuario)
- Input: Password (con icono de candado, tipo password)
- Checkbox: "Recordar sesión"
- Botón primario: "Iniciar Sesión"
- Link: "¿Olvidaste tu contraseña?"
- Footer con versión del sistema

**Validaciones**:
- Username requerido
- Password requerido (mínimo 6 caracteres)
- Mostrar mensaje de error si credenciales inválidas

**Flujo**:
1. Usuario ingresa credenciales
2. Click en "Iniciar Sesión"
3. Sistema valida con backend (POST /api/auth/login)
4. Si válido: redirecciona a Dashboard
5. Si inválido: muestra error

**Estado actual**: ✅ COMPLETADO - Archivo `WF-001_login.png` y `WF-001_login.html`

---

### 2. Dashboard Principal (WF-002)

**Archivo**: `docs/wireframes/WF-002_dashboard.png`

**Descripción**:
Panel principal con KPIs, gráficos y resumen de actividad reciente.

**Elementos**:
- Header con breadcrumb: "Inicio > Dashboard"
- 4 Cards de KPIs en fila:
  - Total Ventas del Mes ($)
  - Órdenes Pendientes (#)
  - Inventario Bajo Stock (#)
  - Empleados Activos (#)
- Gráfico de líneas: Ventas de los últimos 6 meses
- Gráfico de barras: Top 5 productos vendidos
- Tabla: Últimas 5 cotizaciones (con estado y acciones)
- Card lateral: Notificaciones/Alertas

**Acciones**:
- Ver detalles de cada KPI (click en card)
- Filtrar gráficos por fecha
- Ir a cotización desde tabla

**Estado actual**: ✅ COMPLETADO - Archivo `WF-002_dashboard.png`

---

### 3. Lista de Organizaciones (WF-003)

**Archivo**: `docs/wireframes/WF-003_organizations_list.png`

**Descripción**:
Pantalla con tabla de organizaciones, búsqueda, filtros y paginación.

**Elementos**:
- Breadcrumb: "Inicio > Organizaciones"
- Título: "Gestión de Organizaciones"
- Barra superior:
  - Input de búsqueda (placeholder: "Buscar por nombre, NIT...")
  - Botón: "+ Nueva Organización"
  - Filtros: Estado (Activo/Inactivo)
- Tabla con columnas:
  - ID
  - Nombre
  - NIT
  - Teléfono
  - Estado (badge: activo=verde, inactivo=gris)
  - Acciones (editar, eliminar)
- Paginación inferior: "Mostrando 1-10 de 45 | Página 1 2 3 >"

**Acciones**:
- Búsqueda en tiempo real
- Click en "+ Nueva Organización" → Modal de creación
- Click en "editar" → Modal de edición
- Click en "eliminar" → Modal de confirmación

**Estado actual**: ✅ COMPLETADO - Archivo `WF-003_organizations_list.png`

---

### 4. Formulario de Organización (WF-004)

**Archivo**: `docs/wireframes/WF-004_organization_form.png`

**Descripción**:
Modal o página de formulario para crear/editar organizaciones.

**Elementos**:
- Título: "Nueva Organización" / "Editar Organización"
- Campos:
  - Nombre* (text, required)
  - NIT* (text, required, único)
  - Teléfono (text, formato: +57 123 456 7890)
  - Email (email)
  - Dirección (textarea)
  - Estado (select: Activo/Inactivo)
- Botones:
  - "Guardar" (primario)
  - "Cancelar" (secundario)

**Validaciones**:
- Nombre: requerido, max 200 caracteres
- NIT: requerido, único, formato válido
- Email: formato email válido
- Indicadores visuales (rojo) para errores

**Estado actual**: ✅ COMPLETADO - Archivo `WF-004_organization_form.png`  
**Nota**: Campos mostrados en wireframe son más completos que modelo actual (solo usa `name` + `status`)

---

### 5. Lista de Empleados (WF-005)

**Archivo**: `docs/wireframes/WF-005_employees_list.png`

**Descripción**:
Similar a lista de organizaciones, pero para empleados.

**Elementos**:
- Breadcrumb: "Inicio > Empleados"
- Barra superior con búsqueda y "+ Nuevo Empleado"
- Filtros: Sucursal, Estado
- Tabla con columnas:
  - ID
  - Nombre Completo
  - Email
  - Sucursal
  - Cargo (role badge)
  - Estado
  - Acciones
- Paginación

**Estado actual**: ✅ COMPLETADO - Archivo `WF-005_employees_list.png`  
**Nota**: Modelo actual solo tiene `Employee` + `Person` + `Branch` (sin email, cargo, estado)

---

### 6. Lista de Inventario (WF-006)

**Archivo**: `docs/wireframes/WF-006_inventory_list.png`

**Descripción**:
Tabla de items de inventario con alertas de stock bajo.

**Elementos**:
- Breadcrumb: "Inicio > Inventario"
- Barra superior con búsqueda y "+ Nuevo Item"
- Filtros: Categoría, Marca, Stock (Todos/Bajo/Normal)
- Tabla con columnas:
  - SKU
  - Nombre
  - Categoría
  - Marca
  - Cantidad (con alerta roja si < 10)
  - Precio
  - Acciones
- Indicador visual: filas con fondo rojo claro para stock bajo
- Paginación

**Estado actual**: ✅ COMPLETADO - Archivo `WF-006_inventory_list.png`  
**Nota**: Modelo actual no tiene campo `code` (SKU), se usa `id` como identificador

---

### 7. Crear Cotización (WF-007)

**Archivo**: `docs/wireframes/WF-007_create_quote.png`

**Descripción**:
Formulario complejo para crear cotización con múltiples líneas de productos.

**Elementos**:
- Breadcrumb: "Inicio > Cotizaciones > Nueva"
- Título: "Nueva Cotización"
- Sección 1: Información General
  - Cliente (select o autocomplete)
  - Fecha de cotización (date picker)
  - Fecha de vencimiento (date picker)
  - Vendedor (select - autocompletar con usuario actual)
- Sección 2: Líneas de Productos
  - Tabla editable:
    - Producto (select/autocomplete)
    - Cantidad (number)
    - Precio unitario (auto-calculado)
    - Subtotal (auto-calculado)
    - Acción: Eliminar línea
  - Botón: "+ Agregar Producto"
- Sección 3: Totales
  - Subtotal: $ calculado
  - IVA (19%): $ calculado
  - Total: $ calculado (destacado)
- Botones:
  - "Guardar Borrador" (secundario)
  - "Crear Cotización" (primario)
  - "Cancelar" (link)

**Estado actual**: ✅ COMPLETADO - Archivo `WF-007_create_quote.png`  
**Nota**: Modelo simplificado - `QuoteItem` solo tiene `item_id` + `quantity` (precio viene de `InventoryItem`)

---

### 8. Dashboard de Analytics (WF-008)

**Archivo**: `docs/wireframes/WF-008_analytics_dashboard.png`

**Descripción**:
Pantalla de análisis con gráficos y métricas de ventas.

**Elementos**:
- Breadcrumb: "Inicio > Analytics"
- Filtros globales: Periodo (Día/Semana/Mes/Año), Sucursal, Empleado
- Fila de KPIs (6 cards):
  - Ventas Totales
  - Metas Cumplidas (%)
  - Promedio por Venta
  - Órdenes Completadas
  - Facturación Pendiente
  - Top Vendedor del Mes
- Gráfico de líneas: Ventas vs Metas (últimos 6 meses)
- Gráfico de barras: Ventas por Sucursal
- Gráfico de pie: Ventas por Marca
- Tabla: Top 10 Performers

**Estado actual**: ✅ COMPLETADO - Archivo `WF-008_analytics_dashboard.png`  
**Nota**: Métricas calculables con datos actuales, endpoints en `sales_analytics_api.py`

---

## Pantallas Adicionales (Opcionales)

### 9. Reportes de Ventas (WF-009)
**Estado**: Opcional - Combinado con Analytics

### 10. Configuración de Usuario (WF-010)
**Estado**: Opcional - Formulario básico de perfil

---

## Instrucciones para Wilker

### Paso 1: Elegir Herramienta
- **Figma** (recomendado): https://www.figma.com - gratis, colaborativo
- **Draw.io**: https://app.diagrams.net - gratis, simple
- **Balsamiq**: Wireframes más formales (de pago)
- **Excalidraw**: https://excalidraw.com - sketch rápido

### Paso 2: Usar Templates
Buscar templates gratuitos de dashboards en Figma Community:
- "Admin Dashboard Template"
- "SaaS Dashboard UI Kit"
- "Bootstrap Dashboard"

### Paso 3: Exportar
- Resolución: 1280x720 o 1920x1080
- Formato: PNG (alta calidad)
- Nombrar archivos: `WF-001_login.png`, `WF-002_dashboard.png`, etc.

### Paso 4: Documentar
Actualizar este archivo con:
- Screenshots de cada wireframe
- Decisiones de diseño
- Flujos de navegación

---

## Checklist de Entrega

- [x] WF-001: Login ✅
- [x] WF-002: Dashboard Principal ✅
- [x] WF-003: Lista de Organizaciones ✅
- [x] WF-004: Formulario de Organización ✅ 
- [x] WF-005: Lista de Empleados ✅
- [x] WF-006: Lista de Inventario ✅
- [x] WF-007: Crear Cotización ✅
- [x] WF-008: Analytics Dashboard ✅
- [x] Todos los PNG exportados en `docs/business/wireframes/` ✅
- [x] Este archivo completado con descripción de cada wireframe ✅
- [x] Nota agregada sobre modelos simplificados ✅
- [ ] Commit y push al repositorio (pendiente del usuario)

---

## Notas Técnicas

**Componentes a usar (si se implementa frontend)**:
- React/Angular: Material-UI, Ant Design, Bootstrap
- Tablas: AG-Grid, React Table, Datatables
- Gráficos: Chart.js, Recharts, ApexCharts
- Formularios: Formik, React Hook Form

**Accesibilidad**:
- Etiquetas ARIA
- Contraste de colores WCAG AA
- Navegación por teclado
- Responsive design (mobile-first)

---

**Última actualización**: 20 de Octubre, 2025  
**Estado**: ✅ TODOS LOS WIREFRAMES COMPLETADOS (8 PNG + 1 HTML)  
**Validación**: Ver `docs/summaries/VALIDACION_WIREFRAMES_20251020.md` para análisis completo
