# GUÍA RÁPIDA: Crear Wireframes para Entrega Académica

**Fecha**: 19 de Octubre, 2025  
**Autor**: Wilker  
**Objetivo**: Generar 8 wireframes PNG para demostrar UI/UX del sistema Multicont  
**Tiempo estimado**: 3-5 horas

---

## Opción 1: Excalidraw (RECOMENDADO - Más Rápido)

### Por qué Excalidraw:
- ✅ Totalmente gratis
- ✅ No requiere registro
- ✅ Estilo sketch profesional
- ✅ Exporta PNG de alta calidad
- ✅ Muy rápido para wireframes básicos

### Paso a paso:

1. **Abrir Excalidraw:**
   - URL: https://excalidraw.com

2. **Crear wireframe WF-001: Login**
   
   **Elementos a dibujar:**
   ```
   [============================]
   |                            |
   |      LOGO MULTICONT        |
   |  Bienvenido a Multicont    |
   |                            |
   |  [📧] Usuario/Email        |
   |  [🔒] Contraseña           |
   |                            |
   |  □ Recordar sesión         |
   |                            |
   |  [INICIAR SESIÓN] (azul)   |
   |                            |
   |  ¿Olvidaste tu contraseña? |
   |                            |
   |  v1.0.0 - Multicont 2025   |
   [============================]
   ```

   **Instrucciones:**
   - Usar rectangles para inputs
   - Usar texto para labels
   - Botón con fondo azul (rectangle + texto blanco)
   - Iconos simples (📧, 🔒) o símbolos
   - Exportar: Menu → Export → PNG → Save as `WF-001_login.png`

3. **Crear wireframe WF-002: Dashboard**

   **Elementos a dibujar:**
   ```
   [==================================================================]
   | HEADER: Logo | Usuario: Ana López 👤 | 🔔(3) | [Logout]        |
   |------------------------------------------------------------------|
   | SIDEBAR  |  CONTENT AREA                                        |
   | 🏠 Dashboard | Inicio > Dashboard                               |
   | 🏢 Orgs      |                                                  |
   | 👥 Empleados | [Card]        [Card]        [Card]      [Card]   |
   | 📦 Inventory | Ventas Mes    Órdenes Pend. Stock Bajo  Empleados|
   | 💰 Ventas    | $15,000,000   8              5          45       |
   | 📊 Analytics |                                                  |
   |              | [GRÁFICO DE LÍNEAS: Ventas últimos 6 meses]     |
   |              |                                                  |
   |              | [GRÁFICO BARRAS: Top 5 productos vendidos]      |
   |              |                                                  |
   |              | ÚLTIMAS COTIZACIONES:                            |
   |              | ID | Cliente   | Total      | Estado  | Acciones |
   |              | 1  | ABC Corp  | $500,000   | Abierta | [Ver]   |
   |              | 2  | XYZ Ltd   | $300,000   | Cerrada | [Ver]   |
   |------------------------------------------------------------------|
   | Footer: © 2025 Multicont | v1.0.0                              |
   [==================================================================]
   ```

   **Tips:**
   - Usar líneas para dividir secciones
   - Cards = rectangles con sombra
   - Gráficos = rectangles con línea ondulada adentro
   - Tabla = grid simple
   - Exportar como `WF-002_dashboard.png`

4. **Crear wireframe WF-003: Organizations List**

   **Elementos a dibujar:**
   ```
   [==================================================================]
   | HEADER + SIDEBAR (igual al dashboard)                           |
   |------------------------------------------------------------------|
   | SIDEBAR  |  Inicio > Organizaciones                              |
   |          |                                                        |
   |          |  Gestión de Organizaciones                            |
   |          |                                                        |
   |          |  [🔍 Buscar por nombre, NIT...]  [+ Nueva Org] (azul)|
   |          |  Filtro: [Estado: Todos ▼]                            |
   |          |                                                        |
   |          |  ┌─────────────────────────────────────────────┐      |
   |          |  | ID | Nombre    | NIT    | Tel    | Estado |Acc|  |
   |          |  |────|───────────|────────|────────|────────|───|  |
   |          |  | 1  | ABC Corp  | 123... | 300... |[Activo]|✏️🗑️||
   |          |  | 2  | XYZ Ltd   | 456... | 310... |[Activo]|✏️🗑️||
   |          |  | 3  | DEF SA    | 789... | 320... |[Inact.]|✏️🗑️||
   |          |  └─────────────────────────────────────────────┘      |
   |          |                                                        |
   |          |  Mostrando 1-10 de 45 | [◀] 1 [2] [3] [▶]             |
   [==================================================================]
   ```

   **Tips:**
   - Badge "Activo" = rectangle verde
   - Badge "Inactivo" = rectangle gris
   - Iconos de acción: ✏️ (editar), 🗑️ (eliminar)
   - Exportar como `WF-003_organizations_list.png`

5. **Crear wireframe WF-004: Organization Form**

   **Elementos (Modal o página completa):**
   ```
   [=============== Nueva Organización ================]
   |                                                   |
   |  Nombre de la Organización *                      |
   |  [____________________________________]            |
   |                                                   |
   |  NIT *                                            |
   |  [____________________________________]            |
   |                                                   |
   |  Teléfono                                         |
   |  [____________________________________]            |
   |                                                   |
   |  Email                                            |
   |  [____________________________________]            |
   |                                                   |
   |  Dirección                                        |
   |  [____________________________________]            |
   |  [____________________________________]            |
   |                                                   |
   |  Estado                                           |
   |  [Activo ▼]                                       |
   |                                                   |
   |  [Cancelar (gris)]    [Guardar (azul)]            |
   |                                                   |
   [===================================================]
   ```

   **Tips:**
   - Asterisco (*) para campos requeridos
   - Inputs = rectangles con línea gruesa
   - Dropdown = rectangle con flecha ▼
   - Exportar como `WF-004_organization_form.png`

6. **Crear wireframe WF-005: Employees List**

   Similar a Organizations List pero con estas columnas:
   ```
   | ID | Nombre Completo | Email | Sucursal | Cargo | Estado | Acciones |
   ```

   - Badge de cargo: [ADMIN] (azul), [EMPLOYEE] (verde), [MANAGER] (naranja)
   - Exportar como `WF-005_employees_list.png`

7. **Crear wireframe WF-006: Inventory List**

   Similar a Organizations List pero:
   ```
   | SKU | Nombre | Categoría | Marca | Cantidad | Precio | Acciones |
   ```

   - **IMPORTANTE**: Fila con fondo ROJO claro si Cantidad < 10
   - Ejemplo: Fila con cantidad "3" → fondo rojo + texto "⚠️ Stock Bajo"
   - Exportar como `WF-006_inventory_list.png`

8. **Crear wireframe WF-007: Create Quote**

   **Formulario complejo con 3 secciones:**
   ```
   [==================================================================]
   | HEADER + SIDEBAR                                                 |
   |------------------------------------------------------------------|
   |  Inicio > Cotizaciones > Nueva                                   |
   |                                                                  |
   |  ─── Información General ─────────────────────────               |
   |  Cliente *        [Seleccionar cliente... ▼]                     |
   |  Fecha cotización [📅 19/10/2025]                                |
   |  Fecha vencimiento [📅 26/10/2025]                               |
   |  Vendedor         [Ana López (autocompletado)]                   |
   |                                                                  |
   |  ─── Productos ───────────────────────────────────               |
   |  ┌────────────────────────────────────────────────────────┐     |
   |  | Producto ▼ | Cantidad | Precio Unit. | Subtotal | [🗑️] |     |
   |  |────────────|──────────|──────────────|──────────|─────|     |
   |  | Item A     | 10       | $50,000      | $500,000 | 🗑️   |     |
   |  | Item B     | 5        | $30,000      | $150,000 | 🗑️   |     |
   |  └────────────────────────────────────────────────────────┘     |
   |  [+ Agregar Producto]                                            |
   |                                                                  |
   |  ─── Totales ─────────────────────────────────────               |
   |  Subtotal:          $650,000                                     |
   |  IVA (19%):         $123,500                                     |
   |  TOTAL:             $773,500  ← DESTACADO (grande, negrita)     |
   |                                                                  |
   |  [Cancelar]  [Guardar Borrador (gris)]  [Crear Cotización (azul)]|
   [==================================================================]
   ```

   **Tips:**
   - Tabla editable = inputs dentro de celdas
   - Totales en negrita y destacados
   - Botón primario (azul) más grande
   - Exportar como `WF-007_create_quote.png`

9. **Crear wireframe WF-008: Analytics Dashboard**

   ```
   [==================================================================]
   | HEADER + SIDEBAR                                                 |
   |------------------------------------------------------------------|
   |  Inicio > Analytics                                              |
   |                                                                  |
   |  Periodo: [Mes ▼]  Sucursal: [Todas ▼]  Empleado: [Todos ▼]     |
   |                                                                  |
   |  [Card]     [Card]      [Card]      [Card]      [Card]   [Card] |
   |  Ventas     Metas       Promedio    Órdenes     Facturac Top    |
   |  Totales    Cumplidas   por Venta   Completas   Pendiente Vended|
   |  $45M       87%         $350K       124         $2.5M    Ana L. |
   |                                                                  |
   |  [GRÁFICO DE LÍNEAS: Ventas vs Metas (6 meses)]                  |
   |   │                                                              |
   |   │     /\                                                       |
   |   │    /  \    /\                                                |
   |   │   /    \  /  \                                               |
   |   │  /      \/    \                                              |
   |   └─────────────────────► meses                                 |
   |    E  F  M  A  M  J                                              |
   |                                                                  |
   |  [GRÁFICO BARRAS: Ventas por Sucursal]  [GRÁFICO PIE: por Marca]|
   |                                                                  |
   |  TOP 10 PERFORMERS:                                              |
   |  | # | Nombre      | Ventas    | Meta  | % Cumplimiento |       |
   |  | 1 | Ana López   | $5,000,000| $4M   | 125%          |       |
   |  | 2 | Carlos Ruiz | $4,500,000| $4M   | 112%          |       |
   [==================================================================]
   ```

   **Tips:**
   - 6 cards en fila superior
   - Gráficos = sketches simples (no necesitan ser perfectos)
   - Tabla de performers con ranking (1, 2, 3...)
   - Exportar como `WF-008_analytics_dashboard.png`

---

## Opción 2: Figma (Más Profesional pero Requiere Más Tiempo)

### Si prefieres Figma:

1. **Crear cuenta gratuita:**
   - URL: https://www.figma.com/signup

2. **Usar template de dashboard:**
   - Buscar en Figma Community: "Admin Dashboard Template Free"
   - Duplicar template a tu workspace
   - Customizar con los elementos de Multicont

3. **Exportar:**
   - Seleccionar frame
   - Click derecho → Export → PNG → 2x scale
   - Guardar en `docs/wireframes/`

---

## Checklist de Archivos Wireframe

Al finalizar, deberías tener estos 8 archivos PNG:

- [ ] `docs/wireframes/WF-001_login.png`
- [ ] `docs/wireframes/WF-002_dashboard.png`
- [ ] `docs/wireframes/WF-003_organizations_list.png`
- [ ] `docs/wireframes/WF-004_organization_form.png`
- [ ] `docs/wireframes/WF-005_employees_list.png`
- [ ] `docs/wireframes/WF-006_inventory_list.png`
- [ ] `docs/wireframes/WF-007_create_quote.png`
- [ ] `docs/wireframes/WF-008_analytics_dashboard.png`

---

## Consejos Generales

### Estilo Visual:
- **Colores**: Usar azul para acciones principales, verde para success, rojo para alertas
- **Tipografía**: Sans-serif simple (Arial, Helvetica)
- **Espaciado**: Dejar espacio en blanco, no amontonar elementos
- **Consistencia**: Usar mismo tamaño de botones, inputs, cards en todas las pantallas

### Elementos Comunes:
- **Header**: Siempre incluir logo, nombre usuario, notificaciones, logout
- **Sidebar**: Menú con iconos consistente en todas las pantallas internas
- **Breadcrumb**: Mostrar navegación (Inicio > Sección > Subsección)
- **Footer**: Copyright + versión

### Resolución:
- **Mínimo**: 1280x720 px
- **Recomendado**: 1920x1080 px
- **Formato**: PNG de alta calidad (no comprimir demasiado)

---

## Atajos de Excalidraw

- **Rectangle**: R
- **Text**: T
- **Line**: L
- **Arrow**: A
- **Select**: V
- **Duplicate**: Ctrl+D
- **Group**: Ctrl+G
- **Export**: Top-right menu → Export

---

## Tiempo Estimado por Wireframe

- WF-001 (Login): 15 min
- WF-002 (Dashboard): 45 min (más complejo)
- WF-003 (List): 20 min
- WF-004 (Form): 15 min
- WF-005 (List): 15 min
- WF-006 (List): 20 min
- WF-007 (Quote): 45 min (más complejo)
- WF-008 (Analytics): 45 min (más complejo)

**TOTAL**: 3-4 horas aproximadamente

---

## Próximo Paso

Una vez creados los 8 wireframes PNG:
1. Actualizar `WIREFRAMES.md` con screenshots embebidos
2. Verificar que todos los PNG estén en `docs/wireframes/`
3. Continuar con verificación de requerimientos
4. Commit y push de todos los artefactos

---

## Ejemplos de Wireframes de Referencia

Puedes buscar inspiración en:
- https://wireframe.cc (ejemplos de wireframes)
- Dribbble.com → buscar "admin dashboard wireframe"
- Behance.com → buscar "dashboard UI wireframe"

**Recuerda**: No necesitan ser perfectos, solo deben comunicar la estructura y flujo de la UI.

---

**¡Éxito con los wireframes!** 🎨
