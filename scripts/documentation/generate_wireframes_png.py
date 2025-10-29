"""
Script para generar wireframes en formato PNG para el Sistema Multicont
Fecha: 28 de Octubre de 2025
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Colores de la paleta Multicont
COLORS = {
    'primary_blue': '#1E40AF',
    'dark_gray': '#1F2937',
    'white': '#FFFFFF',
    'light_blue': '#3B82F6',
    'success_green': '#10B981',
    'warning_yellow': '#F59E0B',
    'danger_red': '#EF4444',
    'neutral_gray': '#6B7280',
    'bg_gray': '#F3F4F6',
    'border_gray': '#E5E7EB'
}

def hex_to_rgb(hex_color):
    """Convierte color hexadecimal a RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_wireframe_login():
    """WF-001: Pantalla de Login"""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_gray']))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 48)
        font_normal = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Fondo blanco central
    card_x, card_y = 300, 150
    card_w, card_h = 600, 500
    draw.rectangle([card_x, card_y, card_x + card_w, card_y + card_h], 
                   fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    
    # Logo y título
    draw.text((600, 200), "MULTICONT", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_title, anchor="mm")
    draw.text((600, 250), "Control Total, Gestión Eficiente", 
              fill=hex_to_rgb(COLORS['neutral_gray']), font=font_normal, anchor="mm")
    
    # Campo de usuario
    draw.text((350, 320), "📧 Usuario o Email", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal)
    draw.rectangle([350, 345, 850, 380], 
                   fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((360, 362), "ana@multicont.com", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_normal, anchor="lm")
    
    # Campo de contraseña
    draw.text((350, 410), "🔒 Contraseña", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal)
    draw.rectangle([350, 435, 850, 470], 
                   fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((360, 452), "••••••••••", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_normal, anchor="lm")
    
    # Checkbox recordar
    draw.rectangle([350, 490, 365, 505], 
                   fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((375, 497), "Recordar sesión", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal, anchor="lm")
    
    # Botón de login
    draw.rectangle([350, 530, 850, 575], 
                   fill=hex_to_rgb(COLORS['primary_blue']), 
                   outline=hex_to_rgb(COLORS['primary_blue']), width=2)
    draw.text((600, 552), "INICIAR SESIÓN", fill=hex_to_rgb(COLORS['white']), 
              font=font_normal, anchor="mm")
    
    # Link recuperar contraseña
    draw.text((600, 600), "¿Olvidaste tu contraseña?", 
              fill=hex_to_rgb(COLORS['light_blue']), font=font_small, anchor="mm")
    
    # Footer
    draw.text((600, 750), "© 2025 Multicont | v3.0.0", 
              fill=hex_to_rgb(COLORS['neutral_gray']), font=font_small, anchor="mm")
    
    return img

def create_wireframe_dashboard():
    """WF-002: Dashboard Principal"""
    width, height = 1400, 900
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_gray']))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_normal = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
        font_big = ImageFont.truetype("arial.ttf", 32)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_big = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, width, 60], fill=hex_to_rgb(COLORS['white']))
    draw.text((20, 30), "MULTICONT", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_title, anchor="lm")
    draw.text((width-200, 30), "Ana - ADMIN 🔔 ⚙️", 
              fill=hex_to_rgb(COLORS['dark_gray']), font=font_normal, anchor="rm")
    
    # Sidebar
    sidebar_width = 200
    draw.rectangle([0, 60, sidebar_width, height], fill=hex_to_rgb(COLORS['dark_gray']))
    menu_items = ["🏠 Inicio", "👥 Usuarios", "🏢 Organizaciones", "📦 Inventario", 
                  "💰 Ventas", "📊 Analytics"]
    y_pos = 100
    for item in menu_items:
        draw.text((20, y_pos), item, fill=hex_to_rgb(COLORS['white']), 
                  font=font_normal, anchor="lm")
        y_pos += 40
    
    # Breadcrumb
    draw.text((220, 80), "Inicio > Dashboard", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_small, anchor="lm")
    
    # KPI Cards (4 tarjetas)
    kpis = [
        {"icon": "💰", "title": "Ventas", "value": "$125.3M", "change": "+12.5%"},
        {"icon": "📝", "title": "Cotizaciones", "value": "245", "change": "+8%"},
        {"icon": "📦", "title": "Stock Bajo", "value": "15", "change": "⚠ Alerta"},
        {"icon": "👥", "title": "Empleados", "value": "48", "change": "Activos"}
    ]
    
    x_start = 220
    for i, kpi in enumerate(kpis):
        x = x_start + (i * 280)
        # Card
        draw.rectangle([x, 120, x+260, 220], fill=hex_to_rgb(COLORS['white']), 
                       outline=hex_to_rgb(COLORS['border_gray']), width=2)
        draw.text((x+130, 145), kpi["icon"], fill=hex_to_rgb(COLORS['primary_blue']), 
                  font=font_big, anchor="mm")
        draw.text((x+130, 175), kpi["value"], fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_title, anchor="mm")
        draw.text((x+130, 200), kpi["change"], fill=hex_to_rgb(COLORS['success_green']), 
                  font=font_small, anchor="mm")
    
    # Gráfico de ventas (placeholder)
    draw.rectangle([220, 250, 920, 550], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((570, 270), "📈 Ventas de los Últimos 6 Meses", 
              fill=hex_to_rgb(COLORS['dark_gray']), font=font_title, anchor="mm")
    
    # Simular barras de gráfico
    months = ["May", "Jun", "Jul", "Ago", "Sep", "Oct"]
    heights = [120, 180, 150, 200, 170, 220]
    bar_width = 80
    x_start_graph = 280
    for i, (month, h) in enumerate(zip(months, heights)):
        x = x_start_graph + (i * 100)
        draw.rectangle([x, 500-h, x+bar_width, 500], 
                       fill=hex_to_rgb(COLORS['primary_blue']))
        draw.text((x+40, 520), month, fill=hex_to_rgb(COLORS['neutral_gray']), 
                  font=font_small, anchor="mm")
    
    # Top 5 productos
    draw.rectangle([220, 580, 570, 850], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((395, 600), "📊 Top 5 Productos", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal, anchor="mm")
    products = ["1. Sensor XYZ", "2. PLC ABC", "3. Válvula 123", "4. Cable DEF", "5. Motor GHI"]
    y_pos = 630
    for prod in products:
        draw.text((240, y_pos), prod, fill=hex_to_rgb(COLORS['neutral_gray']), 
                  font=font_small, anchor="lm")
        y_pos += 35
    
    # Alertas recientes
    draw.rectangle([590, 580, 920, 850], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((755, 600), "🔔 Alertas Recientes", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal, anchor="mm")
    alerts = ["⚠ Stock bajo: 15 items", "✓ Meta cumplida", "📝 5 cotizaciones nuevas", "💰 Factura #12345"]
    y_pos = 630
    for alert in alerts:
        draw.text((610, y_pos), alert, fill=hex_to_rgb(COLORS['neutral_gray']), 
                  font=font_small, anchor="lm")
        y_pos += 35
    
    return img

def create_wireframe_organizations_list():
    """WF-003: Lista de Organizaciones"""
    width, height = 1400, 900
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_gray']))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_normal = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header
    draw.rectangle([0, 0, width, 60], fill=hex_to_rgb(COLORS['white']))
    draw.text((20, 30), "MULTICONT", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_title, anchor="lm")
    
    # Sidebar
    draw.rectangle([0, 60, 200, height], fill=hex_to_rgb(COLORS['dark_gray']))
    
    # Breadcrumb
    draw.text((220, 80), "Inicio > Organizaciones", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_small, anchor="lm")
    
    # Título
    draw.text((220, 120), "Gestión de Organizaciones", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="lm")
    
    # Barra de búsqueda y botón
    draw.rectangle([220, 160, 600, 195], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((230, 177), "🔍 Buscar por nombre...", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_normal, anchor="lm")
    
    # Botón nueva organización
    draw.rectangle([1100, 160, 1350, 195], fill=hex_to_rgb(COLORS['primary_blue']))
    draw.text((1225, 177), "+ Nueva Organización", fill=hex_to_rgb(COLORS['white']), 
              font=font_normal, anchor="mm")
    
    # Tabla
    table_x, table_y = 220, 220
    table_width = 1130
    
    # Header de tabla
    draw.rectangle([table_x, table_y, table_x+table_width, table_y+40], 
                   fill=hex_to_rgb(COLORS['dark_gray']))
    headers = [("ID", 50), ("Nombre", 400), ("Estado", 200), ("Acciones", 200)]
    x_offset = table_x + 10
    for header, width_col in headers:
        draw.text((x_offset, table_y+20), header, fill=hex_to_rgb(COLORS['white']), 
                  font=font_normal, anchor="lm")
        x_offset += width_col
    
    # Filas
    orgs = [
        ("1", "Empresa ABC", "🟢 Activo"),
        ("2", "Corporación XYZ", "🟢 Activo"),
        ("3", "Grupo 123", "⚫ Inactivo"),
        ("4", "Distribuidora LM", "🟢 Activo"),
        ("5", "Importadora DEF", "🟢 Activo")
    ]
    
    row_y = table_y + 40
    for i, (id_val, name, status) in enumerate(orgs):
        bg_color = COLORS['white'] if i % 2 == 0 else COLORS['bg_gray']
        draw.rectangle([table_x, row_y, table_x+table_width, row_y+40], 
                       fill=hex_to_rgb(bg_color), 
                       outline=hex_to_rgb(COLORS['border_gray']))
        
        draw.text((table_x+10, row_y+20), id_val, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+70, row_y+20), name, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+480, row_y+20), status, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+700, row_y+20), "✏️ Editar  🗑️ Eliminar", 
                  fill=hex_to_rgb(COLORS['light_blue']), font=font_small, anchor="lm")
        
        row_y += 40
    
    # Paginación
    draw.text((220, row_y+30), "Mostrando 1-5 de 15", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_small, anchor="lm")
    draw.text((1200, row_y+30), "◀ 1 2 3 ▶", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_small, anchor="mm")
    
    return img

def create_wireframe_organization_form():
    """WF-004: Formulario de Organización (Modal)"""
    width, height = 1000, 700
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_gray']))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_normal = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Fondo semi-transparente simulado
    draw.rectangle([0, 0, width, height], fill=hex_to_rgb('#9CA3AF'))
    
    # Modal
    modal_x, modal_y = 150, 100
    modal_w, modal_h = 700, 500
    draw.rectangle([modal_x, modal_y, modal_x+modal_w, modal_y+modal_h], 
                   fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=3)
    
    # Header del modal
    draw.rectangle([modal_x, modal_y, modal_x+modal_w, modal_y+50], 
                   fill=hex_to_rgb(COLORS['primary_blue']))
    draw.text((modal_x+20, modal_y+25), "Nueva Organización", 
              fill=hex_to_rgb(COLORS['white']), font=font_title, anchor="lm")
    draw.text((modal_x+modal_w-30, modal_y+25), "✖", 
              fill=hex_to_rgb(COLORS['white']), font=font_title, anchor="mm")
    
    # Contenido del formulario
    form_y = modal_y + 80
    
    # Campo nombre
    draw.text((modal_x+30, form_y), "Nombre de la Organización *", 
              fill=hex_to_rgb(COLORS['dark_gray']), font=font_normal, anchor="lm")
    draw.rectangle([modal_x+30, form_y+25, modal_x+modal_w-30, form_y+60], 
                   fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((modal_x+40, form_y+42), "Empresa ABC Corp", 
              fill=hex_to_rgb(COLORS['neutral_gray']), font=font_normal, anchor="lm")
    draw.text((modal_x+30, form_y+70), "Campo requerido, máximo 200 caracteres", 
              fill=hex_to_rgb(COLORS['neutral_gray']), font=font_small, anchor="lm")
    
    # Estado
    form_y += 130
    draw.text((modal_x+30, form_y), "Estado", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal, anchor="lm")
    draw.text((modal_x+30, form_y+30), "◉ Activo    ○ Inactivo", 
              fill=hex_to_rgb(COLORS['dark_gray']), font=font_normal, anchor="lm")
    
    # Botones
    btn_y = modal_y + modal_h - 80
    # Cancelar
    draw.rectangle([modal_x+30, btn_y, modal_x+250, btn_y+40], 
                   fill=hex_to_rgb(COLORS['neutral_gray']))
    draw.text((modal_x+140, btn_y+20), "Cancelar", fill=hex_to_rgb(COLORS['white']), 
              font=font_normal, anchor="mm")
    
    # Guardar
    draw.rectangle([modal_x+modal_w-250, btn_y, modal_x+modal_w-30, btn_y+40], 
                   fill=hex_to_rgb(COLORS['primary_blue']))
    draw.text((modal_x+modal_w-140, btn_y+20), "Guardar", 
              fill=hex_to_rgb(COLORS['white']), font=font_normal, anchor="mm")
    
    return img

def create_wireframe_inventory_list():
    """WF-005: Lista de Inventario con Alertas"""
    width, height = 1400, 900
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_gray']))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_normal = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header y Sidebar (similar a otros)
    draw.rectangle([0, 0, width, 60], fill=hex_to_rgb(COLORS['white']))
    draw.text((20, 30), "MULTICONT", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_title, anchor="lm")
    draw.rectangle([0, 60, 200, height], fill=hex_to_rgb(COLORS['dark_gray']))
    
    # Breadcrumb
    draw.text((220, 80), "Inicio > Inventario > Items", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_small, anchor="lm")
    
    # Título
    draw.text((220, 120), "Gestión de Inventario", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="lm")
    
    # Alerta de stock bajo
    draw.rectangle([220, 160, 1350, 200], fill='#FEE2E2', 
                   outline=hex_to_rgb(COLORS['danger_red']), width=2)
    draw.text((230, 180), "⚠ 15 items con stock bajo (< 10 unidades)", 
              fill=hex_to_rgb(COLORS['danger_red']), font=font_normal, anchor="lm")
    
    # Barra de búsqueda
    draw.rectangle([220, 220, 600, 255], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((230, 237), "🔍 Buscar...", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_normal, anchor="lm")
    
    # Botón nuevo item
    draw.rectangle([1180, 220, 1350, 255], fill=hex_to_rgb(COLORS['primary_blue']))
    draw.text((1265, 237), "+ Nuevo Item", fill=hex_to_rgb(COLORS['white']), 
              font=font_normal, anchor="mm")
    
    # Tabla
    table_x, table_y = 220, 280
    table_width = 1130
    
    # Header
    draw.rectangle([table_x, table_y, table_x+table_width, table_y+40], 
                   fill=hex_to_rgb(COLORS['dark_gray']))
    headers = [("ID", 50), ("Nombre", 250), ("Categoría", 200), ("Cantidad", 150), 
               ("Precio", 150), ("Acciones", 150)]
    x_offset = table_x + 10
    for header, width_col in headers:
        draw.text((x_offset, table_y+20), header, fill=hex_to_rgb(COLORS['white']), 
                  font=font_normal, anchor="lm")
        x_offset += width_col
    
    # Filas
    items = [
        ("1", "Sensor XYZ", "Sensores", "⚠️ 8", "$1,200", True),
        ("2", "PLC ABC", "Control", "45", "$3,500", False),
        ("3", "Válvula 123", "Válvulas", "120", "$850", False),
        ("4", "Cable DEF", "Cables", "⚠️ 5", "$45", True),
        ("5", "Motor GHI", "Motores", "30", "$2,200", False)
    ]
    
    row_y = table_y + 40
    for i, (id_val, name, cat, qty, price, low_stock) in enumerate(items):
        bg_color = '#FEE2E2' if low_stock else (COLORS['white'] if i % 2 == 0 else COLORS['bg_gray'])
        draw.rectangle([table_x, row_y, table_x+table_width, row_y+40], 
                       fill=hex_to_rgb(bg_color), 
                       outline=hex_to_rgb(COLORS['border_gray']))
        
        draw.text((table_x+10, row_y+20), id_val, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+70, row_y+20), name, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+330, row_y+20), cat, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+540, row_y+20), qty, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+700, row_y+20), price, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+860, row_y+20), "✏️ 🗑️", fill=hex_to_rgb(COLORS['light_blue']), 
                  font=font_small, anchor="lm")
        
        row_y += 40
    
    return img

def create_wireframe_create_quote():
    """WF-006: Crear Cotización"""
    width, height = 1400, 1000
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_gray']))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_normal = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header y Sidebar
    draw.rectangle([0, 0, width, 60], fill=hex_to_rgb(COLORS['white']))
    draw.text((20, 30), "MULTICONT", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_title, anchor="lm")
    draw.rectangle([0, 60, 200, height], fill=hex_to_rgb(COLORS['dark_gray']))
    
    # Breadcrumb
    draw.text((220, 80), "Inicio > Ventas > Cotizaciones > Nueva", 
              fill=hex_to_rgb(COLORS['neutral_gray']), font=font_small, anchor="lm")
    
    # Título
    draw.text((220, 120), "Nueva Cotización", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="lm")
    
    # Sección información general
    section_y = 170
    draw.rectangle([220, section_y, 1350, section_y+180], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((240, section_y+20), "📋 Información General", 
              fill=hex_to_rgb(COLORS['dark_gray']), font=font_title, anchor="lm")
    
    # Campos del formulario
    draw.text((240, section_y+60), "Cliente:", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal, anchor="lm")
    draw.rectangle([240, section_y+85, 700, section_y+120], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((250, section_y+102), "Seleccionar cliente... ▼", 
              fill=hex_to_rgb(COLORS['neutral_gray']), font=font_normal, anchor="lm")
    
    draw.text((750, section_y+60), "Fecha:", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal, anchor="lm")
    draw.rectangle([750, section_y+85, 1000, section_y+120], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((760, section_y+102), "2025-10-28", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_normal, anchor="lm")
    
    # Sección líneas de productos
    section_y = 380
    draw.rectangle([220, section_y, 1350, section_y+350], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((240, section_y+20), "📦 Líneas de Productos", 
              fill=hex_to_rgb(COLORS['dark_gray']), font=font_title, anchor="lm")
    
    # Tabla de líneas
    table_y = section_y + 60
    draw.rectangle([240, table_y, 1330, table_y+35], fill=hex_to_rgb(COLORS['dark_gray']))
    headers = ["#", "Producto", "Cant", "Precio", "Subtotal", ""]
    x_positions = [250, 320, 750, 900, 1050, 1250]
    for i, header in enumerate(headers):
        draw.text((x_positions[i], table_y+17), header, fill=hex_to_rgb(COLORS['white']), 
                  font=font_normal, anchor="lm")
    
    # Líneas de productos
    products = [
        ("1", "Sensor XYZ", "5", "$1,200", "$6,000"),
        ("2", "PLC ABC", "2", "$3,500", "$7,000"),
        ("3", "Cable DEF", "10", "$45", "$450")
    ]
    
    row_y = table_y + 35
    for prod in products:
        draw.rectangle([240, row_y, 1330, row_y+35], fill=hex_to_rgb(COLORS['bg_gray']), 
                       outline=hex_to_rgb(COLORS['border_gray']))
        for i, val in enumerate(prod):
            draw.text((x_positions[i], row_y+17), val, fill=hex_to_rgb(COLORS['dark_gray']), 
                      font=font_normal, anchor="lm")
        draw.text((x_positions[5], row_y+17), "🗑️", fill=hex_to_rgb(COLORS['danger_red']), 
                  font=font_normal, anchor="lm")
        row_y += 35
    
    # Botón agregar producto
    draw.text((240, row_y+20), "+ Agregar Producto", fill=hex_to_rgb(COLORS['light_blue']), 
              font=font_normal, anchor="lm")
    
    # Sección totales
    section_y = 760
    draw.rectangle([950, section_y, 1350, section_y+150], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((970, section_y+20), "💰 Totales", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="lm")
    draw.text((1300, section_y+60), "$13,450.00", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal, anchor="rm")
    draw.text((970, section_y+60), "Subtotal:", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_normal, anchor="lm")
    draw.text((1300, section_y+90), "$2,555.50", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_normal, anchor="rm")
    draw.text((970, section_y+90), "IVA (19%):", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_normal, anchor="lm")
    draw.text((1300, section_y+120), "$16,005.50", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="rm")
    draw.text((970, section_y+120), "TOTAL:", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="lm")
    
    # Botones finales
    draw.rectangle([220, 940, 420, 980], fill=hex_to_rgb(COLORS['neutral_gray']))
    draw.text((320, 960), "Cancelar", fill=hex_to_rgb(COLORS['white']), 
              font=font_normal, anchor="mm")
    
    draw.rectangle([1000, 940, 1350, 980], fill=hex_to_rgb(COLORS['primary_blue']))
    draw.text((1175, 960), "Crear Cotización", fill=hex_to_rgb(COLORS['white']), 
              font=font_normal, anchor="mm")
    
    return img

def create_wireframe_analytics():
    """WF-007: Dashboard de Analytics"""
    width, height = 1400, 1000
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_gray']))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_normal = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
        font_big = ImageFont.truetype("arial.ttf", 28)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_big = ImageFont.load_default()
    
    # Header y Sidebar
    draw.rectangle([0, 0, width, 60], fill=hex_to_rgb(COLORS['white']))
    draw.text((20, 30), "MULTICONT", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_title, anchor="lm")
    draw.rectangle([0, 60, 200, height], fill=hex_to_rgb(COLORS['dark_gray']))
    
    # Breadcrumb
    draw.text((220, 80), "Inicio > Analytics", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_small, anchor="lm")
    
    # Título
    draw.text((220, 120), "Dashboard de Analytics", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="lm")
    
    # Filtros
    draw.text((220, 160), "Período: ▼ Mes    Sucursal: ▼ Todas    Empleado: ▼ Todos", 
              fill=hex_to_rgb(COLORS['neutral_gray']), font=font_normal, anchor="lm")
    
    # KPI Cards
    kpis = [
        {"icon": "💰", "title": "Ventas", "value": "$125.3M", "change": "+12.5%"},
        {"icon": "🎯", "title": "Metas", "value": "92.5%", "change": "🟢 On Track"},
        {"icon": "📊", "title": "Promedio", "value": "$8,350", "change": "+5.2%"},
        {"icon": "📝", "title": "Órdenes", "value": "1,234", "change": "+8.1%"}
    ]
    
    x_start = 220
    for i, kpi in enumerate(kpis):
        x = x_start + (i * 280)
        draw.rectangle([x, 200, x+260, 300], fill=hex_to_rgb(COLORS['white']), 
                       outline=hex_to_rgb(COLORS['border_gray']), width=2)
        draw.text((x+130, 225), kpi["icon"], fill=hex_to_rgb(COLORS['primary_blue']), 
                  font=font_big, anchor="mm")
        draw.text((x+130, 260), kpi["value"], fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_title, anchor="mm")
        draw.text((x+130, 285), kpi["change"], fill=hex_to_rgb(COLORS['success_green']), 
                  font=font_small, anchor="mm")
    
    # Gráfico principal
    draw.rectangle([220, 330, 900, 650], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((560, 350), "📈 Ventas vs Metas (Últimos 6 Meses)", 
              fill=hex_to_rgb(COLORS['dark_gray']), font=font_title, anchor="mm")
    
    # Simular líneas de gráfico
    draw.text((240, 400), "Línea azul: Ventas reales", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_small, anchor="lm")
    draw.text((240, 420), "Línea punteada: Meta", fill=hex_to_rgb(COLORS['warning_yellow']), 
              font=font_small, anchor="lm")
    
    # Gráfico de barras por sucursal
    draw.rectangle([930, 330, 1350, 650], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((1140, 350), "📊 Ventas por Sucursal", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="mm")
    
    sucursales = [("Suc 1", 200), ("Suc 2", 150), ("Suc 3", 100)]
    bar_y = 420
    for suc, width_bar in sucursales:
        draw.text((950, bar_y), suc, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.rectangle([1020, bar_y-10, 1020+width_bar, bar_y+15], 
                       fill=hex_to_rgb(COLORS['primary_blue']))
        bar_y += 60
    
    # Top 10 Performers
    draw.rectangle([220, 680, 700, 950], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((460, 700), "🏆 Top 10 Performers", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="mm")
    
    performers = [
        "1. Jorge Nieto    $39.3M",
        "2. Diego Luna     $30.2M",
        "3. Elena Torres   $28.5M",
        "4. Ana García     $25.1M",
        "5. Carlos Ruiz    $22.8M"
    ]
    perf_y = 740
    for perf in performers:
        draw.text((240, perf_y), perf, fill=hex_to_rgb(COLORS['neutral_gray']), 
                  font=font_normal, anchor="lm")
        perf_y += 35
    
    # Botones exportar
    draw.rectangle([950, 900, 1150, 940], fill=hex_to_rgb(COLORS['success_green']))
    draw.text((1050, 920), "Exportar Excel", fill=hex_to_rgb(COLORS['white']), 
              font=font_normal, anchor="mm")
    
    draw.rectangle([1180, 900, 1350, 940], fill=hex_to_rgb(COLORS['danger_red']))
    draw.text((1265, 920), "Exportar PDF", fill=hex_to_rgb(COLORS['white']), 
              font=font_normal, anchor="mm")
    
    return img

def create_wireframe_users():
    """WF-008: Gestión de Usuarios (ADMIN only)"""
    width, height = 1400, 900
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['bg_gray']))
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_normal = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header y Sidebar
    draw.rectangle([0, 0, width, 60], fill=hex_to_rgb(COLORS['white']))
    draw.text((20, 30), "MULTICONT", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_title, anchor="lm")
    draw.rectangle([0, 60, 200, height], fill=hex_to_rgb(COLORS['dark_gray']))
    
    # Breadcrumb
    draw.text((220, 80), "Inicio > Administración > Usuarios", 
              fill=hex_to_rgb(COLORS['neutral_gray']), font=font_small, anchor="lm")
    
    # Título
    draw.text((220, 120), "Gestión de Usuarios", fill=hex_to_rgb(COLORS['dark_gray']), 
              font=font_title, anchor="lm")
    
    # Barra de búsqueda y filtros
    draw.rectangle([220, 160, 600, 195], fill=hex_to_rgb(COLORS['white']), 
                   outline=hex_to_rgb(COLORS['border_gray']), width=2)
    draw.text((230, 177), "🔍 Buscar...", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_normal, anchor="lm")
    
    draw.text((650, 177), "Rol: ▼ Todos    Estado: ▼", 
              fill=hex_to_rgb(COLORS['neutral_gray']), font=font_normal, anchor="lm")
    
    # Botón nuevo usuario
    draw.rectangle([1180, 160, 1350, 195], fill=hex_to_rgb(COLORS['primary_blue']))
    draw.text((1265, 177), "+ Nuevo Usuario", fill=hex_to_rgb(COLORS['white']), 
              font=font_normal, anchor="mm")
    
    # Tabla
    table_x, table_y = 220, 220
    table_width = 1130
    
    # Header
    draw.rectangle([table_x, table_y, table_x+table_width, table_y+40], 
                   fill=hex_to_rgb(COLORS['dark_gray']))
    headers = [("ID", 50), ("Usuario", 200), ("Email", 300), ("Rol", 200), 
               ("Estado", 150), ("Acciones", 150)]
    x_offset = table_x + 10
    for header, width_col in headers:
        draw.text((x_offset, table_y+20), header, fill=hex_to_rgb(COLORS['white']), 
                  font=font_normal, anchor="lm")
        x_offset += width_col
    
    # Filas con roles de colores
    users = [
        ("1", "ana", "ana@mc.com", "🔴 ADMIN", "🟢 Activo"),
        ("2", "carlos", "car@mc.com", "🟡 MANAGER", "🟢 Activo"),
        ("3", "elena", "ele@mc.com", "🟢 SALES", "🟢 Activo"),
        ("4", "david", "dav@mc.com", "⚫ VIEWER", "⚫ Inactivo")
    ]
    
    row_y = table_y + 40
    for i, (id_val, user, email, role, status) in enumerate(users):
        bg_color = COLORS['white'] if i % 2 == 0 else COLORS['bg_gray']
        draw.rectangle([table_x, row_y, table_x+table_width, row_y+40], 
                       fill=hex_to_rgb(bg_color), 
                       outline=hex_to_rgb(COLORS['border_gray']))
        
        draw.text((table_x+10, row_y+20), id_val, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+70, row_y+20), user, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+280, row_y+20), email, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+590, row_y+20), role, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+800, row_y+20), status, fill=hex_to_rgb(COLORS['dark_gray']), 
                  font=font_normal, anchor="lm")
        draw.text((table_x+960, row_y+20), "✏️ 🗑️", fill=hex_to_rgb(COLORS['light_blue']), 
                  font=font_small, anchor="lm")
        
        row_y += 40
    
    # Paginación
    draw.text((220, row_y+30), "Mostrando 1-4 de 48", fill=hex_to_rgb(COLORS['neutral_gray']), 
              font=font_small, anchor="lm")
    draw.text((1200, row_y+30), "◀ 1 2 3 ... 12 ▶", fill=hex_to_rgb(COLORS['primary_blue']), 
              font=font_small, anchor="mm")
    
    return img

def main():
    """Genera todos los wireframes"""
    output_dir = "c:/Users/spiri/MultiContGit/docs/business/wireframes"
    os.makedirs(output_dir, exist_ok=True)
    
    wireframes = [
        ("WF-001_login.png", create_wireframe_login),
        ("WF-002_dashboard.png", create_wireframe_dashboard),
        ("WF-003_organizations_list.png", create_wireframe_organizations_list),
        ("WF-004_organization_form.png", create_wireframe_organization_form),
        ("WF-005_inventory_list.png", create_wireframe_inventory_list),
        ("WF-006_create_quote.png", create_wireframe_create_quote),
        ("WF-007_analytics_dashboard.png", create_wireframe_analytics),
        ("WF-008_users_management.png", create_wireframe_users)
    ]
    
    print("🎨 Generando wireframes PNG para Sistema Multicont...")
    print("=" * 60)
    
    for filename, func in wireframes:
        print(f"  Generando {filename}...", end=" ")
        img = func()
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        print("✅")
    
    print("=" * 60)
    print(f"✅ {len(wireframes)} wireframes generados exitosamente!")
    print(f"📁 Ubicación: {output_dir}")

if __name__ == "__main__":
    main()
