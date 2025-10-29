# 🎨 WIREFRAMES - Sistema Multicont

**Proyecto**: Sistema de Gestión Empresarial Multicont  
**Fecha de creación**: 28 de Octubre de 2025  
**Autores**: Wilker & Daniel  
**Curso**: Desarrollo de Aplicaciones Web  
**Corte**: Tercero

---

## 📋 Tabla de Contenidos

1. [Branding y Paleta de Colores](#branding-y-paleta-de-colores)
2. [Árbol de Navegación](#árbol-de-navegación)
3. [Público Objetivo](#público-objetivo)
4. [Wireframes de la Aplicación](#wireframes-de-la-aplicación)
5. [Disposición de Controles](#disposición-de-controles)

---

## 🎨 Branding y Paleta de Colores

### Logo y Identidad Corporativa

**Nombre**: MULTICONT  
**Slogan**: "Control Total, Gestión Eficiente"  
**Concepto**: Sistema profesional de gestión empresarial con enfoque en multi-organización

### Logo Design

```
╔══════════════════════════════════════╗
║                                      ║
║     ███╗   ███╗ ██████╗             ║
║     ████╗ ████║██╔════╝             ║
║     ██╔████╔██║██║                  ║
║     ██║╚██╔╝██║██║                  ║
║     ██║ ╚═╝ ██║╚██████╗             ║
║     ╚═╝     ╚═╝ ╚═════╝             ║
║                                      ║
║     M U L T I C O N T                ║
║   Control Total, Gestión Eficiente   ║
╚══════════════════════════════════════╝
```

### Paleta de Colores Corporativa

#### Colores Principales

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| 🔵 **Azul Corporativo** | `#1E40AF` | `rgb(30, 64, 175)` | Primario, Headers, Botones principales |
| ⚫ **Gris Oscuro** | `#1F2937` | `rgb(31, 41, 55)` | Texto principal, Sidebar |
| ⚪ **Blanco Puro** | `#FFFFFF` | `rgb(255, 255, 255)` | Fondos, Cards |
| 🔷 **Azul Claro** | `#3B82F6` | `rgb(59, 130, 246)` | Hover, Links |

#### Colores de Acción

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| 🟢 **Verde Éxito** | `#10B981` | `rgb(16, 185, 129)` | Confirmaciones, Status activo |
| 🟡 **Amarillo Alerta** | `#F59E0B` | `rgb(245, 158, 11)` | Advertencias, Pending |
| 🔴 **Rojo Peligro** | `#EF4444` | `rgb(239, 68, 68)` | Eliminar, Errores |
| ⚪ **Gris Neutro** | `#6B7280` | `rgb(107, 114, 128)` | Texto secundario, Disabled |

#### Colores de Roles (RBAC)

| Rol | Color Badge | Hex |
|-----|-------------|-----|
| ADMIN | 🔴 Rojo | `#DC2626` |
| MANAGER | 🟡 Amarillo | `#F59E0B` |
| SALES | 🟢 Verde | `#059669` |
| VIEWER | ⚪ Gris | `#6B7280` |

### Tipografía

- **Headings (H1-H3)**: Inter Bold, 24-32px
- **Botones**: Inter SemiBold, 14-16px
- **Texto Principal**: Inter Regular, 14px
- **Texto Secundario**: Inter Regular, 12px

---

## 🗺️ Árbol de Navegación

### Estructura de Navegación Completa

```
MULTICONT (Sistema)
│
├── 🏠 INICIO (Dashboard)
│   ├── Panel de KPIs
│   ├── Gráficos de Ventas
│   ├── Alertas de Stock Bajo
│   └── Actividad Reciente
│
├── 🔐 AUTENTICACIÓN (Público)
│   ├── Login
│   ├── Recuperar Contraseña
│   └── Cambiar Contraseña
│
├── 👥 USUARIOS (ADMIN only)
│   ├── Lista de Usuarios
│   ├── Crear Usuario
│   ├── Editar Usuario
│   ├── Asignar Roles
│   └── Estadísticas de Usuarios
│
├── 🏢 GESTIÓN ORGANIZACIONAL
│   ├── Organizaciones (ADMIN, MANAGER)
│   │   ├── Lista de Organizaciones
│   │   ├── Crear Organización
│   │   ├── Editar Organización
│   │   └── Detalles de Organización
│   │
│   ├── Sucursales (ADMIN, MANAGER)
│   │   ├── Lista de Sucursales
│   │   ├── Crear Sucursal
│   │   ├── Editar Sucursal
│   │   └── Asignar Empleados
│   │
│   └── Empleados (ADMIN, MANAGER, SALES-read)
│       ├── Lista de Empleados
│       ├── Crear Empleado
│       ├── Editar Empleado
│       ├── Historial de Asignaciones
│       └── Metas de Empleado
│
├── 📦 INVENTARIO (Todos los roles)
│   ├── Items de Inventario
│   │   ├── Lista de Items (Todos)
│   │   ├── Crear Item (ADMIN, MANAGER)
│   │   ├── Editar Item (ADMIN, MANAGER)
│   │   ├── Alertas de Stock Bajo
│   │   └── Agregar Stock (ADMIN, MANAGER)
│   │
│   ├── Categorías (ADMIN, MANAGER)
│   │   ├── Lista de Categorías
│   │   ├── Crear Categoría
│   │   └── Editar Categoría
│   │
│   ├── Marcas (ADMIN, MANAGER)
│   │   ├── Lista de Marcas
│   │   ├── Crear Marca
│   │   └── Editar Marca
│   │
│   └── Asignaciones (ADMIN, MANAGER)
│       ├── Lista de Asignaciones
│       ├── Asignar Item a Empleado
│       ├── Marcar como Devuelto
│       ├── Marcar como Perdido
│       └── Historial por Empleado
│
├── 💰 VENTAS
│   ├── Cotizaciones (ADMIN, MANAGER, SALES)
│   │   ├── Lista de Cotizaciones (Todos)
│   │   ├── Crear Cotización (Todos)
│   │   ├── Editar Cotización (Todos)
│   │   ├── Agregar Líneas (Todos)
│   │   ├── Aprobar Cotización (ADMIN, MANAGER)
│   │   └── Convertir a Orden (ADMIN, MANAGER)
│   │
│   ├── Órdenes de Venta (ADMIN, MANAGER)
│   │   ├── Lista de Órdenes
│   │   ├── Crear Orden
│   │   ├── Editar Orden
│   │   ├── Convertir a Factura
│   │   └── Cancelar Orden
│   │
│   ├── Facturas (ADMIN, MANAGER)
│   │   ├── Lista de Facturas
│   │   ├── Crear Factura
│   │   ├── Ver Detalles de Factura
│   │   ├── Anular Factura
│   │   └── Descargar PDF
│   │
│   └── Metas de Ventas (ADMIN, MANAGER)
│       ├── Lista de Metas
│       ├── Crear Meta (Mensual/Trimestral/Anual)
│       ├── Asignar a Empleado/Sucursal
│       └── Seguimiento de Cumplimiento
│
├── 📊 ANALYTICS Y REPORTES (ADMIN, MANAGER)
│   ├── Dashboard de Ventas
│   │   ├── Gráficos de Ventas Mensuales
│   │   ├── Comparación vs Metas
│   │   ├── Tendencias
│   │   └── Proyecciones
│   │
│   ├── Facturación
│   │   ├── Por Empleado
│   │   ├── Por Sucursal
│   │   ├── Por Marca
│   │   └── Por Período
│   │
│   ├── Cotizaciones
│   │   ├── Por Marca
│   │   ├── Tasa de Conversión
│   │   └── Análisis de Tendencias
│   │
│   ├── Indicadores de Rendimiento
│   │   ├── Top Performers
│   │   ├── Cumplimiento de Metas
│   │   ├── Ranking de Sucursales
│   │   └── Productos Más Vendidos
│   │
│   └── Exportar Reportes
│       ├── Excel
│       ├── PDF
│       └── CSV
│
├── 🎯 METAS Y OBJETIVOS (ADMIN, MANAGER)
│   ├── Dashboard de Metas
│   ├── Crear Meta Nueva
│   ├── Asignar Meta
│   ├── Seguimiento en Tiempo Real
│   └── Metas vs Actual
│
├── 🔧 ADMINISTRACIÓN (ADMIN only)
│   ├── Roles y Permisos
│   │   ├── Lista de Roles
│   │   ├── Crear Rol
│   │   ├── Asignar Permisos
│   │   └── Ver Usuarios por Rol
│   │
│   ├── Permisos
│   │   ├── Lista de Permisos
│   │   ├── Crear Permiso
│   │   └── Matriz de Permisos
│   │
│   └── Configuración del Sistema
│       ├── Variables de Entorno
│       ├── Logs del Sistema
│       └── Respaldo de Base de Datos
│
└── 👤 PERFIL DE USUARIO (Todos)
    ├── Ver Perfil
    ├── Editar Información Personal
    ├── Cambiar Contraseña
    ├── Mis Cotizaciones (SALES)
    ├── Mis Metas (SALES)
    └── Cerrar Sesión
```

### Leyenda de Accesos

- **🟢 Verde (Todos)**: Acceso sin restricción
- **🟡 Amarillo (ADMIN + MANAGER)**: Acceso limitado a administradores y managers
- **🔴 Rojo (ADMIN only)**: Acceso exclusivo de administrador

---

## 👥 Público Objetivo

### Entidad a la que está dirigida la aplicación

**Nombre de la entidad**: Empresas Medianas y Grandes con Múltiples Sucursales  
**Sector**: Comercio, distribución, servicios industriales  
**Tamaño**: 20-500 empleados  
**Características**:
- Múltiples puntos de venta o sucursales
- Necesidad de control centralizado de inventario
- Flujo de ventas con cotizaciones, órdenes y facturación
- Equipos de ventas distribuidos geográficamente

### Cantidad de usuarios totales

**Estimación por empresa**:
- **Pequeña implementación**: 10-20 usuarios (1 organización, 2-3 sucursales)
- **Implementación mediana**: 50-100 usuarios (1-2 organizaciones, 5-10 sucursales)
- **Implementación grande**: 200-500 usuarios (3-5 organizaciones, 15-30 sucursales)

**Total en sistema multi-tenant**: Hasta 10,000 usuarios concurrentes (escalable con PostgreSQL + cache)

### Distribución de roles típica (por 100 usuarios)

| Rol | Cantidad | Porcentaje | Descripción |
|-----|----------|------------|-------------|
| **ADMIN** | 2-3 | 2-3% | Administradores del sistema, IT |
| **MANAGER** | 10-15 | 10-15% | Gerentes de sucursal, supervisores |
| **SALES** | 60-70 | 60-70% | Vendedores, asesores comerciales |
| **VIEWER** | 15-20 | 15-20% | Contadores, auditores, analistas |

---

## 🎯 Características de los Usuarios

### 1. Conocimiento en Tecnología

#### Nivel Técnico por Rol

| Rol | Nivel Técnico | Descripción |
|-----|---------------|-------------|
| **ADMIN** | Alto (8-10/10) | Usuarios con conocimientos técnicos, familiarizados con sistemas empresariales, capacitación en TI |
| **MANAGER** | Medio-Alto (6-8/10) | Usuarios con experiencia en software de gestión, capacidad de aprender rápido |
| **SALES** | Básico-Medio (3-6/10) | Usuarios cotidianos, necesitan interfaz intuitiva, pueden requerir capacitación |
| **VIEWER** | Medio (5-7/10) | Usuarios analíticos, familiarizados con reportes y métricas |

#### Curva de Aprendizaje Esperada

- **Semana 1**: Login, navegación básica, crear cotización simple
- **Semana 2**: Gestión completa de cotizaciones, uso de filtros y búsqueda
- **Semana 3-4**: Reportes, analytics, metas (roles MANAGER/ADMIN)
- **Mes 2+**: Uso avanzado, optimización de workflows

### 2. Dispositivos de Acceso

#### Dispositivos Primarios

| Dispositivo | Porcentaje de Uso | Prioridad de Diseño |
|-------------|-------------------|---------------------|
| **Desktop** (Windows 10/11) | 70% | Alta ⭐⭐⭐ |
| **Laptop** (1366x768 - 1920x1080) | 20% | Alta ⭐⭐⭐ |
| **Tablet** (iPad, Android 10") | 8% | Media ⭐⭐ |
| **Móvil** (iOS, Android) | 2% | Baja ⭐ |

#### Navegadores Soportados

- **Chrome** 90+ (Recomendado) - 60%
- **Edge** 90+ - 25%
- **Firefox** 85+ - 10%
- **Safari** 14+ (macOS/iOS) - 5%

**Nota**: IE11 NO soportado (deprecado)

### 3. Modo Responsivo

#### Breakpoints de Diseño

```css
/* Mobile First Approach */
@media (min-width: 640px)  { /* sm - Móvil grande */ }
@media (min-width: 768px)  { /* md - Tablet */ }
@media (min-width: 1024px) { /* lg - Laptop */ }
@media (min-width: 1280px) { /* xl - Desktop */ }
@media (min-width: 1536px) { /* 2xl - Desktop grande */ }
```

#### Estrategia Responsiva por Pantalla

| Pantalla | Desktop (>1024px) | Tablet (768-1023px) | Móvil (<768px) |
|----------|-------------------|---------------------|----------------|
| **Dashboard** | 4 columnas de KPIs | 2 columnas | 1 columna |
| **Tablas** | Todas las columnas | Ocultar columnas secundarias | Cards verticales |
| **Formularios** | 2 columnas | 1-2 columnas | 1 columna |
| **Sidebar** | Siempre visible | Colapsable | Menú hamburguesa |
| **Gráficos** | Grande (800px) | Mediano (600px) | Compacto (100% width) |

### 4. Conexión a Internet

#### Velocidad de Conexión Esperada

- **Óptima**: 10+ Mbps (Oficinas principales) - 60%
- **Buena**: 3-10 Mbps (Sucursales remotas) - 30%
- **Básica**: 1-3 Mbps (Conexiones móviles) - 10%

#### Optimizaciones para Conexión Lenta

- ✅ Paginación en todas las listas (máximo 50 items por página)
- ✅ Compresión de imágenes (WebP)
- ✅ Lazy loading de gráficos
- ✅ Cache de datos estáticos (10 minutos)
- ✅ API responses comprimidas (gzip)

---

## ♿ Características de Accesibilidad

### Cumplimiento de Estándares

**Nivel objetivo**: **WCAG 2.1 Nivel AA**

### 1. Contraste de Colores

Todos los textos cumplen con ratio mínimo de contraste:

| Elemento | Contraste | Cumplimiento |
|----------|-----------|--------------|
| Texto normal (#1F2937 sobre #FFFFFF) | 16.1:1 | ✅ AAA |
| Texto grande (#6B7280 sobre #FFFFFF) | 4.6:1 | ✅ AA |
| Botones primarios (#FFFFFF sobre #1E40AF) | 8.6:1 | ✅ AAA |
| Enlaces (#3B82F6 sobre #FFFFFF) | 4.9:1 | ✅ AA |

### 2. Navegación por Teclado

- ✅ **Tab**: Navegar entre campos/botones
- ✅ **Shift + Tab**: Navegar hacia atrás
- ✅ **Enter**: Activar botón/link
- ✅ **Escape**: Cerrar modales
- ✅ **Flechas**: Navegar en selects/dropdowns
- ✅ **Ctrl + /**: Abrir búsqueda rápida

### 3. Etiquetas ARIA

Todos los componentes incluyen:

```html
<!-- Ejemplo de botón accesible -->
<button 
  aria-label="Crear nueva cotización"
  aria-describedby="tooltip-create-quote"
  role="button"
  tabindex="0">
  + Nueva Cotización
</button>

<!-- Ejemplo de tabla accesible -->
<table role="table" aria-label="Lista de organizaciones">
  <thead role="rowgroup">
    <tr role="row">
      <th role="columnheader" aria-sort="ascending">Nombre</th>
    </tr>
  </thead>
</table>
```

### 4. Soporte para Lectores de Pantalla

- ✅ **NVDA** (Windows) - Compatible
- ✅ **JAWS** (Windows) - Compatible
- ✅ **VoiceOver** (macOS/iOS) - Compatible
- ✅ **TalkBack** (Android) - Compatible

#### Mensajes de Estado

```html
<div role="status" aria-live="polite" aria-atomic="true">
  Cotización creada exitosamente. ID: 12345
</div>

<div role="alert" aria-live="assertive">
  Error: No se pudo guardar la cotización. Intente nuevamente.
</div>
```

### 5. Tamaño de Fuentes y Zoom

- ✅ Fuente base: 14px (mínimo recomendado: 16px)
- ✅ Soporte de zoom hasta 200% sin pérdida de funcionalidad
- ✅ Tamaño mínimo de botones: 44x44px (recomendación WCAG)

### 6. Indicadores Visuales

- ✅ **Focus visible**: Borde azul en elementos enfocados
- ✅ **Hover states**: Cambio de color al pasar mouse
- ✅ **Loading states**: Spinners con texto alternativo
- ✅ **Error states**: Mensajes en rojo con iconos
- ✅ **Success states**: Mensajes en verde con iconos

### 7. Formularios Accesibles

```html
<label for="organization-name">
  Nombre de la Organización *
  <span class="sr-only">(Campo requerido)</span>
</label>
<input 
  id="organization-name"
  name="name"
  type="text"
  required
  aria-required="true"
  aria-invalid="false"
  aria-describedby="name-error name-help">
<span id="name-help" class="help-text">
  Mínimo 3 caracteres, máximo 200
</span>
<span id="name-error" role="alert" class="error-message" hidden>
  El nombre es requerido
</span>
```

### 8. Alternativas de Color

**Problema**: Usuarios daltónicos no distinguen colores

**Solución**:
- ✅ Uso de iconos además de colores (✓, ✗, ⚠)
- ✅ Patrones de relleno en gráficos
- ✅ Texto descriptivo en badges (`Estado: Activo`)
- ✅ Bordes adicionales para distinguir estados

---

## 📱 Wireframes de la Aplicación

### Disposición General de Controles

Todos los wireframes siguen esta estructura:

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER (Fixed)                                               │
│ ┌─────┐  MULTICONT      [Buscar...]  [👤][🔔][⚙️][Salir] │
│ └─────┘                                                      │
├──────┬──────────────────────────────────────────────────────┤
│      │ BREADCRUMB                                           │
│      │ Inicio > Organizaciones > Lista                      │
│  S   ├──────────────────────────────────────────────────────┤
│  I   │                                                      │
│  D   │ CONTENT AREA                                         │
│  E   │                                                      │
│  B   │  ┌─────────────────────────────────────────────┐   │
│  A   │  │                                             │   │
│  R   │  │  Contenido principal (Cards, Tablas, etc)   │   │
│      │  │                                             │   │
│  (   │  └─────────────────────────────────────────────┘   │
│  C   │                                                      │
│  o   │                                                      │
│  l   │  PAGINATION                                          │
│  l   │  ← 1 2 3 ... 10 →                                   │
│  a   │                                                      │
│  p   │                                                      │
│  s   │                                                      │
│  e   │                                                      │
│  )   │                                                      │
│      │                                                      │
├──────┴──────────────────────────────────────────────────────┤
│ FOOTER (Fixed)                                               │
│ © 2025 Multicont | v3.0.0 | Desarrollado por Wilker & Daniel│
└─────────────────────────────────────────────────────────────┘
```

### Componentes Estándar

#### Header (Todos los wireframes)

```
┌────────────────────────────────────────────────────────────────┐
│ [Logo MC]  MULTICONT        [🔍 Buscar...]  [👤 Ana][🔔 3][⚙️] │
└────────────────────────────────────────────────────────────────┘
```

Elementos:
- Logo clickeable (regresa a Dashboard)
- Nombre del sistema
- Búsqueda global (Ctrl + /)
- Avatar con nombre de usuario + rol badge
- Notificaciones con contador
- Configuración rápida
- Botón de logout

#### Sidebar (Navegación Principal)

```
┌─────────────────────┐
│ [≡] Menú            │
├─────────────────────┤
│ 🏠 Inicio           │
│ 👥 Usuarios         │ ← Solo ADMIN
│ 🏢 Organizaciones   │
│ 🏬 Sucursales       │
│ 👤 Empleados        │
│ 📦 Inventario       │ ▼
│   └ Items           │
│   └ Categorías      │
│   └ Marcas          │
│   └ Asignaciones    │
│ 💰 Ventas           │ ▼
│   └ Cotizaciones    │
│   └ Órdenes         │
│   └ Facturas        │
│   └ Metas           │
│ 📊 Analytics        │ ← ADMIN/MANAGER
│ 🔧 Admin            │ ← Solo ADMIN
└─────────────────────┘
```

### WF-001: Login

**Vista**: Pantalla de inicio de sesión

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│                    ███╗   ███╗ ██████╗                    │
│                    ████╗ ████║██╔════╝                    │
│                    ██╔████╔██║██║                         │
│                    ██║╚██╔╝██║██║                         │
│                    ██║ ╚═╝ ██║╚██████╗                    │
│                    ╚═╝     ╚═╝ ╚═════╝                    │
│                                                            │
│                  M U L T I C O N T                         │
│            Control Total, Gestión Eficiente                │
│                                                            │
│          ┌─────────────────────────────────────┐          │
│          │                                     │          │
│          │  📧 Usuario o Email                 │          │
│          │  ┌─────────────────────────────┐   │          │
│          │  │ ana@multicont.com           │   │          │
│          │  └─────────────────────────────┘   │          │
│          │                                     │          │
│          │  🔒 Contraseña                      │          │
│          │  ┌─────────────────────────────┐   │          │
│          │  │ ••••••••••                  │   │          │
│          │  └─────────────────────────────┘   │          │
│          │                                     │          │
│          │  [ ] Recordar sesión                │          │
│          │                                     │          │
│          │  ┌─────────────────────────────┐   │          │
│          │  │   INICIAR SESIÓN            │   │          │
│          │  └─────────────────────────────┘   │          │
│          │           (Azul #1E40AF)            │          │
│          │                                     │          │
│          │   ¿Olvidaste tu contraseña?         │          │
│          │                                     │          │
│          └─────────────────────────────────────┘          │
│                                                            │
│             © 2025 Multicont | v3.0.0                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Funcionalidades**:
- Login con JWT
- Validación de credenciales
- Remember me (localStorage)
- Recuperación de contraseña
- Responsive (100% en móvil)

---

### WF-002: Dashboard Principal

**Vista**: Panel de control principal (todos los roles)

```
┌────────────────────────────────────────────────────────────────┐
│ [Logo] MULTICONT  [Buscar...]  [Ana-ADMIN][🔔 3][⚙️][Salir]   │
├────┬───────────────────────────────────────────────────────────┤
│ S  │ Inicio > Dashboard                                        │
│ I  ├───────────────────────────────────────────────────────────┤
│ D  │                                                           │
│ E  │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│ B  │ │💰 Ventas│ │📝 Cots. │ │📦 Stock │ │👥 Empls.│         │
│ A  │ │$125.3M  │ │  245    │ │   15    │ │   48    │         │
│ R  │ │+12.5%   │ │  +8%    │ │ ⚠ Bajo  │ │ Activos │         │
│    │ └─────────┘ └─────────┘ └─────────┘ └─────────┘         │
│ 🏠 │                                                           │
│ 👥 │ ┌─────────────────────────────────────────────┐         │
│ 🏢 │ │ 📈 Ventas de los Últimos 6 Meses            │         │
│ 📦 │ │                                             │         │
│ 💰 │ │     ┌────┐                                  │         │
│ 📊 │ │     │    │  ┌────┐                          │         │
│    │ │  ┌──┤    ├──┤    │  ┌────┐                 │         │
│    │ │  │  │    │  │    ├──┤    │  ┌────┐         │         │
│    │ │  │  │    │  │    │  │    ├──┤    │         │         │
│    │ │  May Jun  Jul Ago  Sep  Oct                 │         │
│    │ └─────────────────────────────────────────────┘         │
│    │                                                           │
│    │ ┌──────────────────────┐ ┌─────────────────────┐        │
│    │ │ 📊 Top 5 Productos   │ │ 🔔 Alertas Recientes │        │
│    │ │                      │ │                     │        │
│    │ │ 1. Sensor XYZ        │ │ ⚠ Stock bajo: 15   │        │
│    │ │ 2. PLC ABC           │ │ ✓ Meta cumplida    │        │
│    │ │ 3. Válvula 123       │ │ 📝 5 cotizaciones  │        │
│    │ │ 4. Cable DEF         │ │ 💰 Factura #12345  │        │
│    │ │ 5. Motor GHI         │ │                     │        │
│    │ └──────────────────────┘ └─────────────────────┘        │
│    │                                                           │
├────┴───────────────────────────────────────────────────────────┤
│ © 2025 Multicont | v3.0.0                                     │
└────────────────────────────────────────────────────────────────┘
```

**Elementos**:
- 4 KPI cards con iconos y tendencias
- Gráfico de líneas (ventas mensuales)
- Top 5 productos (tabla simple)
- Alertas y notificaciones en tiempo real
- Responsive: 4→2→1 columnas

---

### WF-003: Lista de Organizaciones

**Vista**: Tabla de organizaciones con CRUD

```
┌────────────────────────────────────────────────────────────────┐
│ [Logo] MULTICONT  [Buscar...]  [Ana-ADMIN][🔔][⚙️][Salir]     │
├────┬───────────────────────────────────────────────────────────┤
│ S  │ Inicio > Organizaciones                                   │
│ I  ├───────────────────────────────────────────────────────────┤
│ D  │                                                           │
│ E  │ Gestión de Organizaciones                                │
│ B  │                                                           │
│ A  │ [🔍 Buscar por nombre...]  [Filtro: ▼]  [+ Nueva Org]   │
│ R  │                                                           │
│    │ ┌───┬──────────────────┬────────┬────────────────────┐  │
│ 🏠 │ │ID │ Nombre           │ Estado │ Acciones           │  │
│ 👥 │ ├───┼──────────────────┼────────┼────────────────────┤  │
│ 🏢 │ │ 1 │ Empresa ABC      │ 🟢Act. │ [✏️ Editar][🗑️]    │  │
│ 📦 │ │ 2 │ Corporación XYZ  │ 🟢Act. │ [✏️ Editar][🗑️]    │  │
│ 💰 │ │ 3 │ Grupo 123        │ ⚫Inac. │ [✏️ Editar][🗑️]    │  │
│ 📊 │ │ 4 │ Distribuidora LM │ 🟢Act. │ [✏️ Editar][🗑️]    │  │
│    │ │ 5 │ Importadora DEF  │ 🟢Act. │ [✏️ Editar][🗑️]    │  │
│    │ └───┴──────────────────┴────────┴────────────────────┘  │
│    │                                                           │
│    │ Mostrando 1-5 de 15 | [◀ 1] [2] [3] [▶]                │
│    │                                                           │
├────┴───────────────────────────────────────────────────────────┤
│ © 2025 Multicont | v3.0.0                                     │
└────────────────────────────────────────────────────────────────┘
```

**Funcionalidades**:
- Búsqueda en tiempo real
- Filtros por status
- Paginación (10, 25, 50, 100 items)
- Acciones: Editar (modal), Eliminar (confirmación)
- Badge de estado con colores

---

### WF-004: Formulario de Organización (Modal)

**Vista**: Modal para crear/editar organización

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ ✖ Nueva Organización                                    │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │                                                        │   │
│  │  Nombre de la Organización *                           │   │
│  │  ┌────────────────────────────────────────────────┐    │   │
│  │  │ Empresa ABC Corp                               │    │   │
│  │  └────────────────────────────────────────────────┘    │   │
│  │  Campo requerido, máximo 200 caracteres                │   │
│  │                                                        │   │
│  │  Estado                                                │   │
│  │  ◉ Activo   ○ Inactivo                                 │   │
│  │                                                        │   │
│  │                                                        │   │
│  │  ┌─────────────────┐  ┌─────────────────┐            │   │
│  │  │    Cancelar     │  │     Guardar     │            │   │
│  │  │   (Gris #6B7)   │  │   (Azul #1E4)   │            │   │
│  │  └─────────────────┘  └─────────────────┘            │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Validaciones**:
- Nombre requerido (client-side + server-side)
- Longitud máxima 200 caracteres
- Estado default: Activo
- Feedback visual de errores

---

### WF-005: Lista de Inventario

**Vista**: Control de stock con alertas

```
┌────────────────────────────────────────────────────────────────┐
│ [Logo] MULTICONT  [Buscar...]  [Carlos-MANAGER][🔔][⚙️]       │
├────┬───────────────────────────────────────────────────────────┤
│ S  │ Inicio > Inventario > Items                               │
│ I  ├───────────────────────────────────────────────────────────┤
│ D  │                                                           │
│ E  │ Gestión de Inventario                                     │
│ B  │                                                           │
│ A  │ [🔍 Buscar...]  [Categoría ▼][Marca ▼]  [+ Nuevo Item]   │
│ R  │                                                           │
│    │ ⚠ 15 items con stock bajo (< 10 unidades)                │
│ 🏠 │                                                           │
│ 👥 │ ┌───┬────────────┬─────────┬───────┬────────┬─────────┐ │
│ 🏢 │ │ID │ Nombre     │Categoría│Cantidad│ Precio │Acciones │ │
│ 📦 │ ├───┼────────────┼─────────┼───────┼────────┼─────────┤ │
│ 💰 │ │ 1 │Sensor XYZ  │Sensores │ ⚠️ 8  │ $1,200 │[✏️][🗑️] │ │
│ 📊 │ │ 2 │PLC ABC     │Control  │  45   │ $3,500 │[✏️][🗑️] │ │
│    │ │ 3 │Válvula 123 │Válvulas │  120  │ $850   │[✏️][🗑️] │ │
│    │ │ 4 │Cable DEF   │Cables   │ ⚠️ 5  │ $45    │[✏️][🗑️] │ │
│    │ │ 5 │Motor GHI   │Motores  │  30   │ $2,200 │[✏️][🗑️] │ │
│    │ └───┴────────────┴─────────┴───────┴────────┴─────────┘ │
│    │                                                           │
│    │ Fondo rojo claro en filas con stock < 10                 │
│    │                                                           │
│    │ [◀ 1] [2] [3] ... [10] [▶]                              │
│    │                                                           │
├────┴───────────────────────────────────────────────────────────┤
│ © 2025 Multicont | v3.0.0                                     │
└────────────────────────────────────────────────────────────────┘
```

**Alertas visuales**:
- Icono ⚠️ en cantidad < 10
- Fondo rojo claro (#FEE2E2) en filas críticas
- Banner de alerta en header
- Badge de estado de stock

---

### WF-006: Crear Cotización

**Vista**: Formulario complejo multi-línea

```
┌────────────────────────────────────────────────────────────────┐
│ [Logo] MULTICONT  [Buscar...]  [Elena-SALES][🔔][⚙️][Salir]   │
├────┬───────────────────────────────────────────────────────────┤
│ S  │ Inicio > Ventas > Cotizaciones > Nueva                    │
│ I  ├───────────────────────────────────────────────────────────┤
│ D  │                                                           │
│ E  │ Nueva Cotización                                          │
│ B  │                                                           │
│ A  │ ┌─────────────────────────────────────────────────────┐  │
│ R  │ │ 📋 Información General                              │  │
│    │ ├─────────────────────────────────────────────────────┤  │
│ 🏠 │ │ Cliente: [Seleccionar cliente... ▼]                 │  │
│ 👥 │ │ Fecha: [2025-10-28]  Vencimiento: [2025-11-27]      │  │
│ 🏢 │ │ Vendedor: Elena Torres (auto-completado)            │  │
│ 📦 │ └─────────────────────────────────────────────────────┘  │
│ 💰 │                                                           │
│ 📊 │ ┌─────────────────────────────────────────────────────┐  │
│    │ │ 📦 Líneas de Productos                              │  │
│    │ ├─────┬────────────┬────┬────────┬──────────┬───────┤  │
│    │ │ # │ Producto    │Cant│ Precio │ Subtotal │ 🗑️     │  │
│    │ ├─────┼────────────┼────┼────────┼──────────┼───────┤  │
│    │ │ 1   │Sensor XYZ  │ 5  │ $1,200 │ $6,000   │ [X]   │  │
│    │ │ 2   │PLC ABC     │ 2  │ $3,500 │ $7,000   │ [X]   │  │
│    │ │ 3   │Cable DEF   │ 10 │ $45    │ $450     │ [X]   │  │
│    │ └─────┴────────────┴────┴────────┴──────────┴───────┘  │
│    │ [+ Agregar Producto]                                     │
│    │                                                           │
│    │ ┌─────────────────────────────────────────────────────┐  │
│    │ │ 💰 Totales                                          │  │
│    │ ├─────────────────────────────────────────────────────┤  │
│    │ │                              Subtotal:  $ 13,450.00 │  │
│    │ │                              IVA (19%): $  2,555.50 │  │
│    │ │                              ─────────────────────── │  │
│    │ │                              TOTAL:     $ 16,005.50 │  │
│    │ └─────────────────────────────────────────────────────┘  │
│    │                                                           │
│    │ [Guardar Borrador]  [Crear Cotización]  [Cancelar]      │
│    │                                                           │
├────┴───────────────────────────────────────────────────────────┤
│ © 2025 Multicont | v3.0.0                                     │
└────────────────────────────────────────────────────────────────┘
```

**Funcionalidades**:
- Autocompletar vendedor con usuario actual
- Tabla editable de líneas
- Cálculo automático de subtotales y total
- Agregar/eliminar líneas dinámicamente
- Validación: Al menos 1 línea requerida

---

### WF-007: Dashboard de Analytics

**Vista**: Métricas y gráficos (ADMIN/MANAGER only)

```
┌────────────────────────────────────────────────────────────────┐
│ [Logo] MULTICONT  [Buscar...]  [Ana-ADMIN][🔔][⚙️][Salir]     │
├────┬───────────────────────────────────────────────────────────┤
│ S  │ Inicio > Analytics                                        │
│ I  ├───────────────────────────────────────────────────────────┤
│ D  │                                                           │
│ E  │ Dashboard de Analytics                                    │
│ B  │                                                           │
│ A  │ [Período: ▼ Mes] [Sucursal: ▼ Todas] [Empleado: ▼ Todos]│
│ R  │                                                           │
│    │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│ 🏠 │ │💰 Ventas│ │🎯 Metas │ │📊 Prom. │ │📝 Órd.  │         │
│ 👥 │ │$125.3M  │ │  92.5%  │ │ $8,350  │ │  1,234  │         │
│ 🏢 │ │+12.5%   │ │  🟢On   │ │  +5.2%  │ │  +8.1%  │         │
│ 📦 │ └─────────┘ └─────────┘ └─────────┘ └─────────┘         │
│ 💰 │                                                           │
│ 📊 │ ┌───────────────────────────────────────────────────┐   │
│    │ │ 📈 Ventas vs Metas (Últimos 6 Meses)             │   │
│    │ │                                                   │   │
│    │ │  Línea azul: Ventas reales                        │   │
│    │ │  Línea punteada: Meta                             │   │
│    │ │                                                   │   │
│    │ │  [Gráfico de líneas interactivo]                  │   │
│    │ └───────────────────────────────────────────────────┘   │
│    │                                                           │
│    │ ┌────────────────────┐ ┌──────────────────────────┐     │
│    │ │ 📊 Por Sucursal    │ │ 🏆 Top 10 Performers     │     │
│    │ │ [Gráfico barras]   │ │                          │     │
│    │ │                    │ │ 1. Jorge Nieto  $39.3M   │     │
│    │ │ Suc1 ████████      │ │ 2. Diego Luna   $30.2M   │     │
│    │ │ Suc2 ██████        │ │ 3. Elena Torres $28.5M   │     │
│    │ │ Suc3 ████          │ │ ... (Top 10)             │     │
│    │ └────────────────────┘ └──────────────────────────┘     │
│    │                                                           │
│    │ [Exportar a Excel] [Exportar a PDF]                     │
│    │                                                           │
├────┴───────────────────────────────────────────────────────────┤
│ © 2025 Multicont | v3.0.0                                     │
└────────────────────────────────────────────────────────────────┘
```

**Gráficos incluidos**:
- Líneas: Ventas vs Metas
- Barras: Ventas por Sucursal
- Pie: Ventas por Marca
- Tabla: Top Performers

---

### WF-008: Gestión de Usuarios (ADMIN only)

**Vista**: CRUD de usuarios con roles

```
┌────────────────────────────────────────────────────────────────┐
│ [Logo] MULTICONT  [Buscar...]  [Ana-ADMIN][🔔][⚙️][Salir]     │
├────┬───────────────────────────────────────────────────────────┤
│ S  │ Inicio > Administración > Usuarios                        │
│ I  ├───────────────────────────────────────────────────────────┤
│ D  │                                                           │
│ E  │ Gestión de Usuarios                                       │
│ B  │                                                           │
│ A  │ [🔍 Buscar...]  [Rol: ▼ Todos]  [Estado: ▼]  [+ Nuevo]  │
│ R  │                                                           │
│    │ ┌───┬────────────┬──────────┬──────────┬──────┬────────┐ │
│ 🏠 │ │ID │ Usuario    │ Email    │ Rol      │Estado│Acciones│ │
│ 👥 │ ├───┼────────────┼──────────┼──────────┼──────┼────────┤ │
│ 🏢 │ │ 1 │ana         │ana@mc.com│🔴 ADMIN  │🟢Act.│[✏️][🗑️]│ │
│ 📦 │ │ 2 │carlos      │car@mc.com│🟡 MANAGER│🟢Act.│[✏️][🗑️]│ │
│ 💰 │ │ 3 │elena       │ele@mc.com│🟢 SALES  │🟢Act.│[✏️][🗑️]│ │
│ 📊 │ │ 4 │david       │dav@mc.com│⚫ VIEWER │⚫Inac.│[✏️][🗑️]│ │
│ 🔧 │ └───┴────────────┴──────────┴──────────┴──────┴────────┘ │
│    │                                                           │
│    │ [◀ 1] [2] [3] [▶]                                        │
│    │                                                           │
├────┴───────────────────────────────────────────────────────────┤
│ © 2025 Multicont | v3.0.0                                     │
└────────────────────────────────────────────────────────────────┘
```

**Funcionalidades**:
- Filtro por rol y estado
- Badges de colores por rol (según paleta RBAC)
- Crear/Editar/Eliminar usuarios
- Asignar roles (dropdown)
- Activar/Desactivar usuarios

---

## 📊 Resumen de Wireframes

### Wireframes Creados

| ID | Nombre | Descripción | Prioridad | Estado |
|----|--------|-------------|-----------|--------|
| WF-001 | Login | Autenticación JWT | Alta ⭐⭐⭐ | ✅ |
| WF-002 | Dashboard | Panel principal | Alta ⭐⭐⭐ | ✅ |
| WF-003 | Lista Organizaciones | CRUD organizaciones | Alta ⭐⭐⭐ | ✅ |
| WF-004 | Formulario Org | Modal crear/editar | Alta ⭐⭐⭐ | ✅ |
| WF-005 | Lista Inventario | Control de stock | Alta ⭐⭐⭐ | ✅ |
| WF-006 | Crear Cotización | Formulario multi-línea | Alta ⭐⭐⭐ | ✅ |
| WF-007 | Analytics Dashboard | Métricas y gráficos | Alta ⭐⭐⭐ | ✅ |
| WF-008 | Gestión Usuarios | CRUD usuarios (ADMIN) | Alta ⭐⭐⭐ | ✅ |

### Cobertura de Funcionalidades

- ✅ Autenticación y Seguridad
- ✅ Dashboard y KPIs
- ✅ Gestión Organizacional
- ✅ Control de Inventario
- ✅ Flujo de Ventas (Cotizaciones)
- ✅ Analytics y Reportes
- ✅ Administración de Usuarios

---

## 📝 Notas de Implementación

### Tecnologías Recomendadas para Frontend

**Framework**: Angular 16+ o React 18+  
**UI Library**: Angular Material o Material-UI  
**Gráficos**: Chart.js, ApexCharts, Recharts  
**Tablas**: AG-Grid, TanStack Table  
**Formularios**: Reactive Forms (Angular), React Hook Form  
**HTTP**: Axios, Fetch API  
**State Management**: NgRx (Angular), Redux Toolkit (React)

### Responsive Design

- **Mobile First**: Diseñar desde 320px hacia arriba
- **Breakpoints**: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
- **Sidebar**: Colapsable en < 1024px
- **Tablas**: Convertir a cards verticales en móvil

---

**Fecha de creación**: 28 de Octubre de 2025  
**Última actualización**: 28 de Octubre de 2025  
**Versión**: 1.0.0  
**Estado**: ✅ COMPLETO - Listo para implementación
