"""
Generador de Wireframes para Multicont
Genera wireframes PNG usando Pillow para entrega académica
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuración
WIDTH = 1280
HEIGHT = 720
BG_COLOR = (255, 255, 255)
PRIMARY_COLOR = (59, 130, 246)  # Azul
SUCCESS_COLOR = (16, 185, 129)   # Verde
DANGER_COLOR = (239, 68, 68)     # Rojo
TEXT_COLOR = (31, 41, 55)        # Gris oscuro
BORDER_COLOR = (229, 231, 235)   # Gris claro
OUTPUT_DIR = "docs/wireframes"

def create_base_wireframe():
    """Crea una imagen base con fondo blanco"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_rectangle(draw, x, y, width, height, fill=None, outline=None, width_line=2):
    """Dibuja un rectángulo"""
    draw.rectangle([x, y, x + width, y + height], fill=fill, outline=outline, width=width_line)

def draw_text(draw, text, x, y, size=20, color=TEXT_COLOR, bold=False):
    """Dibuja texto"""
    try:
        # Intentar cargar fuente del sistema
        if os.name == 'nt':  # Windows
            font_path = "C:\\Windows\\Fonts\\arial.ttf"
            if bold:
                font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        else:
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        
        font = ImageFont.truetype(font_path, size)
    except:
        font = ImageFont.load_default()
    
    draw.text((x, y), text, fill=color, font=font)

def generate_wf001_login():
    """WF-001: Pantalla de Login"""
    img, draw = create_base_wireframe()
    
    # Fondo degradado simulado con rectángulos
    for i in range(0, HEIGHT, 10):
        color_intensity = int(200 - (i / HEIGHT) * 50)
        draw.rectangle([0, i, WIDTH, i + 10], fill=(color_intensity, color_intensity, 255))
    
    # Container central
    box_x, box_y = 390, 160
    box_width, box_height = 500, 400
    draw_rectangle(draw, box_x, box_y, box_width, box_height, 
                   fill=(255, 255, 255), outline=None)
    
    # Logo (círculo)
    logo_x, logo_y = WIDTH // 2, 200
    draw.ellipse([logo_x - 40, logo_y - 40, logo_x + 40, logo_y + 40], 
                 fill=PRIMARY_COLOR)
    draw_text(draw, "M", logo_x - 18, logo_y - 25, size=50, color=(255, 255, 255))
    
    # Título
    draw_text(draw, "Bienvenido a Multicont", 440, 280, size=28, bold=True)
    draw_text(draw, "Sistema de Gestión Empresarial", 465, 315, size=14, color=(107, 114, 128))
    
    # Input Usuario
    draw_text(draw, "Usuario o Email", box_x + 40, 360, size=14)
    draw_rectangle(draw, box_x + 40, 385, box_width - 80, 45, 
                   fill=(249, 250, 251), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "👤", box_x + 55, 395, size=20)
    draw_text(draw, "Ingresa tu usuario o email", box_x + 90, 395, size=14, color=(156, 163, 175))
    
    # Input Password
    draw_text(draw, "Contraseña", box_x + 40, 450, size=14)
    draw_rectangle(draw, box_x + 40, 475, box_width - 80, 45, 
                   fill=(249, 250, 251), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "🔒", box_x + 55, 485, size=20)
    draw_text(draw, "••••••••••••", box_x + 90, 485, size=14, color=(156, 163, 175))
    
    # Checkbox
    draw_rectangle(draw, box_x + 40, 540, 18, 18, outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Recordar sesión", box_x + 68, 538, size=14, color=(107, 114, 128))
    
    # Botón Login
    draw_rectangle(draw, box_x + 40, 580, box_width - 80, 50, fill=PRIMARY_COLOR)
    draw_text(draw, "Iniciar Sesión", box_x + 190, 595, size=16, color=(255, 255, 255), bold=True)
    
    # Link olvidaste contraseña
    draw_text(draw, "¿Olvidaste tu contraseña?", box_x + 160, 650, size=14, color=PRIMARY_COLOR)
    
    # Footer
    draw_text(draw, "© 2025 Multicont | v1.0.0", box_x + 170, 700, size=12, color=(156, 163, 175))
    
    # Guardar
    img.save(os.path.join(OUTPUT_DIR, "WF-001_login.png"))
    print("✅ WF-001_login.png generado")

def generate_wf002_dashboard():
    """WF-002: Dashboard Principal"""
    img, draw = create_base_wireframe()
    
    # Header
    draw_rectangle(draw, 0, 0, WIDTH, 60, fill=(31, 41, 55))
    draw_text(draw, "🏢 Multicont", 20, 18, size=24, color=(255, 255, 255), bold=True)
    draw_text(draw, "👤 Ana López (ADMIN)", WIDTH - 250, 22, size=14, color=(255, 255, 255))
    draw_text(draw, "🔔 (3)  Salir", WIDTH - 120, 22, size=14, color=(255, 255, 255))
    
    # Sidebar
    draw_rectangle(draw, 0, 60, 220, HEIGHT - 60, fill=(249, 250, 251))
    menu_items = [
        ("🏠 Dashboard", 80, True),
        ("🏢 Organizaciones", 130, False),
        ("👥 Empleados", 180, False),
        ("📦 Inventario", 230, False),
        ("💰 Ventas", 280, False),
        ("📊 Analytics", 330, False),
    ]
    for item, y, active in menu_items:
        bg = PRIMARY_COLOR if active else (249, 250, 251)
        text_color = (255, 255, 255) if active else TEXT_COLOR
        if active:
            draw_rectangle(draw, 10, y, 200, 40, fill=bg)
        draw_text(draw, item, 25, y + 10, size=14, color=text_color)
    
    # Breadcrumb
    draw_text(draw, "Inicio > Dashboard", 240, 80, size=14, color=(107, 114, 128))
    
    # KPI Cards
    cards = [
        ("Ventas Mes", "$15,000,000", 240),
        ("Órdenes Pend.", "8", 520),
        ("Stock Bajo", "5", 800),
        ("Empleados", "45", 1080),
    ]
    for title, value, x in cards:
        draw_rectangle(draw, x, 120, 240, 100, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
        draw_text(draw, title, x + 15, 135, size=14, color=(107, 114, 128))
        draw_text(draw, value, x + 15, 160, size=28, color=TEXT_COLOR, bold=True)
    
    # Gráfico de líneas
    draw_rectangle(draw, 240, 240, 810, 200, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Ventas últimos 6 meses", 260, 255, size=16, bold=True)
    # Línea simulada
    points = [(280, 380), (380, 340), (480, 360), (580, 310), (680, 350), (780, 300)]
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=PRIMARY_COLOR, width=3)
    
    # Gráfico de barras
    draw_rectangle(draw, 1070, 240, 270, 200, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Top 5 Productos", 1090, 255, size=16, bold=True)
    bar_heights = [80, 60, 90, 50, 70]
    for i, h in enumerate(bar_heights):
        x = 1100 + (i * 50)
        draw_rectangle(draw, x, 420 - h, 35, h, fill=SUCCESS_COLOR)
    
    # Tabla de cotizaciones
    draw_rectangle(draw, 240, 460, 1100, 220, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Últimas Cotizaciones", 260, 475, size=16, bold=True)
    
    # Header tabla
    headers = [("ID", 260), ("Cliente", 340), ("Total", 600), ("Estado", 800), ("Acciones", 1000)]
    for header, x in headers:
        draw_text(draw, header, x, 510, size=14, bold=True)
    
    # Línea separadora
    draw.line([(240, 535), (1340, 535)], fill=BORDER_COLOR, width=2)
    
    # Filas
    rows = [
        ("1", "ABC Corp", "$500,000", "Abierta", 545),
        ("2", "XYZ Ltd", "$300,000", "Cerrada", 585),
        ("3", "DEF SA", "$250,000", "Abierta", 625),
    ]
    for id, client, total, status, y in rows:
        draw_text(draw, id, 260, y, size=14)
        draw_text(draw, client, 340, y, size=14)
        draw_text(draw, total, 600, y, size=14)
        # Badge de estado
        badge_color = SUCCESS_COLOR if status == "Abierta" else (156, 163, 175)
        draw_rectangle(draw, 800, y, 80, 25, fill=badge_color)
        draw_text(draw, status, 810, y + 4, size=12, color=(255, 255, 255))
        draw_text(draw, "[Ver]", 1000, y, size=14, color=PRIMARY_COLOR)
    
    # Footer
    draw_rectangle(draw, 0, HEIGHT - 30, WIDTH, 30, fill=(249, 250, 251))
    draw_text(draw, "© 2025 Multicont | v1.0.0", 20, HEIGHT - 22, size=12, color=(107, 114, 128))
    
    img.save(os.path.join(OUTPUT_DIR, "WF-002_dashboard.png"))
    print("✅ WF-002_dashboard.png generado")

def generate_wf003_organizations_list():
    """WF-003: Lista de Organizaciones"""
    img, draw = create_base_wireframe()
    
    # Header y Sidebar (reutilizar estructura del dashboard)
    # Header
    draw_rectangle(draw, 0, 0, WIDTH, 60, fill=(31, 41, 55))
    draw_text(draw, "🏢 Multicont", 20, 18, size=24, color=(255, 255, 255), bold=True)
    draw_text(draw, "👤 Ana López", WIDTH - 200, 22, size=14, color=(255, 255, 255))
    
    # Sidebar
    draw_rectangle(draw, 0, 60, 220, HEIGHT - 60, fill=(249, 250, 251))
    draw_text(draw, "🏠 Dashboard", 25, 90, size=14)
    draw_rectangle(draw, 10, 130, 200, 40, fill=PRIMARY_COLOR)
    draw_text(draw, "🏢 Organizaciones", 25, 140, size=14, color=(255, 255, 255))
    
    # Content
    draw_text(draw, "Inicio > Organizaciones", 240, 80, size=14, color=(107, 114, 128))
    draw_text(draw, "Gestión de Organizaciones", 240, 110, size=24, bold=True)
    
    # Barra de búsqueda y botón
    draw_rectangle(draw, 240, 160, 600, 45, fill=(249, 250, 251), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "🔍 Buscar por nombre, NIT...", 260, 172, size=14, color=(156, 163, 175))
    
    draw_rectangle(draw, 860, 160, 200, 45, fill=PRIMARY_COLOR)
    draw_text(draw, "+ Nueva Organización", 885, 172, size=14, color=(255, 255, 255), bold=True)
    
    # Filtro
    draw_text(draw, "Estado:", 1080, 172, size=14)
    draw_rectangle(draw, 1140, 160, 120, 45, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Todos ▼", 1160, 172, size=14)
    
    # Tabla
    draw_rectangle(draw, 240, 230, 1020, 420, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    
    # Header tabla
    headers = [("ID", 260), ("Nombre", 340), ("NIT", 580), ("Teléfono", 760), ("Estado", 940), ("Acc", 1120)]
    for header, x in headers:
        draw_text(draw, header, x, 245, size=14, bold=True)
    
    draw.line([(240, 275), (1260, 275)], fill=BORDER_COLOR, width=2)
    
    # Filas
    rows = [
        ("1", "ABC Corp", "900123456-7", "300-1234567", "Activo", 290),
        ("2", "XYZ Ltd", "900234567-8", "310-2345678", "Activo", 330),
        ("3", "DEF SA", "900345678-9", "320-3456789", "Inactivo", 370),
        ("4", "GHI SAS", "900456789-0", "330-4567890", "Activo", 410),
        ("5", "JKL Corp", "900567890-1", "340-5678901", "Activo", 450),
    ]
    
    for id, name, nit, phone, status, y in rows:
        draw_text(draw, id, 260, y, size=14)
        draw_text(draw, name, 340, y, size=14)
        draw_text(draw, nit, 580, y, size=14)
        draw_text(draw, phone, 760, y, size=14)
        
        # Badge estado
        badge_color = SUCCESS_COLOR if status == "Activo" else (156, 163, 175)
        draw_rectangle(draw, 940, y, 70, 25, fill=badge_color)
        draw_text(draw, status, 950, y + 4, size=12, color=(255, 255, 255))
        
        # Acciones
        draw_text(draw, "✏️ 🗑️", 1120, y, size=14)
    
    # Paginación
    draw_text(draw, "Mostrando 1-10 de 45", 240, 670, size=14, color=(107, 114, 128))
    draw_text(draw, "◀ 1 [2] [3] ▶", 1100, 670, size=14, color=PRIMARY_COLOR)
    
    img.save(os.path.join(OUTPUT_DIR, "WF-003_organizations_list.png"))
    print("✅ WF-003_organizations_list.png generado")

def generate_wf004_organization_form():
    """WF-004: Formulario de Organización"""
    img, draw = create_base_wireframe()
    
    # Fondo semi-transparente (simulado con gris claro)
    draw_rectangle(draw, 0, 0, WIDTH, HEIGHT, fill=(0, 0, 0, 50))
    
    # Modal
    modal_x, modal_y = 240, 80
    modal_width, modal_height = 800, 560
    draw_rectangle(draw, modal_x, modal_y, modal_width, modal_height, 
                   fill=(255, 255, 255), outline=None)
    
    # Header del modal
    draw_text(draw, "Nueva Organización", modal_x + 30, modal_y + 25, size=24, bold=True)
    draw_text(draw, "✕", modal_x + modal_width - 50, modal_y + 25, size=24, color=(156, 163, 175))
    
    draw.line([(modal_x, modal_y + 70), (modal_x + modal_width, modal_y + 70)], 
             fill=BORDER_COLOR, width=2)
    
    # Formulario
    form_x = modal_x + 40
    
    # Campo Nombre
    y = modal_y + 100
    draw_text(draw, "Nombre de la Organización *", form_x, y, size=14, bold=True)
    draw_rectangle(draw, form_x, y + 25, modal_width - 80, 45, 
                   fill=(249, 250, 251), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Ej: ABC Corporation S.A.S.", form_x + 15, y + 38, size=14, color=(156, 163, 175))
    
    # Campo NIT
    y += 90
    draw_text(draw, "NIT *", form_x, y, size=14, bold=True)
    draw_rectangle(draw, form_x, y + 25, modal_width - 80, 45, 
                   fill=(249, 250, 251), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Ej: 900123456-7", form_x + 15, y + 38, size=14, color=(156, 163, 175))
    
    # Campo Teléfono
    y += 90
    draw_text(draw, "Teléfono", form_x, y, size=14, bold=True)
    draw_rectangle(draw, form_x, y + 25, modal_width - 80, 45, 
                   fill=(249, 250, 251), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Ej: +57 300 123 4567", form_x + 15, y + 38, size=14, color=(156, 163, 175))
    
    # Campo Email
    y += 90
    draw_text(draw, "Email", form_x, y, size=14, bold=True)
    draw_rectangle(draw, form_x, y + 25, modal_width - 80, 45, 
                   fill=(249, 250, 251), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Ej: contacto@empresa.com", form_x + 15, y + 38, size=14, color=(156, 163, 175))
    
    # Campo Estado (Select)
    y += 90
    draw_text(draw, "Estado", form_x, y, size=14, bold=True)
    draw_rectangle(draw, form_x, y + 25, 200, 45, 
                   fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Activo ▼", form_x + 15, y + 38, size=14)
    
    # Nota de campos requeridos
    draw_text(draw, "* Campos requeridos", form_x, y + 85, size=12, color=DANGER_COLOR)
    
    # Botones
    draw_rectangle(draw, modal_x + modal_width - 320, modal_y + modal_height - 70, 
                   140, 45, fill=(229, 231, 235))
    draw_text(draw, "Cancelar", modal_x + modal_width - 275, modal_y + modal_height - 57, 
             size=16, color=TEXT_COLOR)
    
    draw_rectangle(draw, modal_x + modal_width - 160, modal_y + modal_height - 70, 
                   140, 45, fill=PRIMARY_COLOR)
    draw_text(draw, "Guardar", modal_x + modal_width - 120, modal_y + modal_height - 57, 
             size=16, color=(255, 255, 255), bold=True)
    
    img.save(os.path.join(OUTPUT_DIR, "WF-004_organization_form.png"))
    print("✅ WF-004_organization_form.png generado")

def generate_wf005_employees_list():
    """WF-005: Lista de Empleados"""
    img, draw = create_base_wireframe()
    
    # Header
    draw_rectangle(draw, 0, 0, WIDTH, 60, fill=(31, 41, 55))
    draw_text(draw, "🏢 Multicont", 20, 18, size=24, color=(255, 255, 255), bold=True)
    
    # Sidebar
    draw_rectangle(draw, 0, 60, 220, HEIGHT - 60, fill=(249, 250, 251))
    draw_rectangle(draw, 10, 170, 200, 40, fill=PRIMARY_COLOR)
    draw_text(draw, "👥 Empleados", 25, 180, size=14, color=(255, 255, 255))
    
    # Content
    draw_text(draw, "Inicio > Empleados", 240, 80, size=14, color=(107, 114, 128))
    draw_text(draw, "Gestión de Empleados", 240, 110, size=24, bold=True)
    
    # Búsqueda y botón
    draw_rectangle(draw, 240, 160, 500, 45, fill=(249, 250, 251), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "🔍 Buscar empleado...", 260, 172, size=14, color=(156, 163, 175))
    
    draw_rectangle(draw, 760, 160, 190, 45, fill=PRIMARY_COLOR)
    draw_text(draw, "+ Nuevo Empleado", 790, 172, size=14, color=(255, 255, 255), bold=True)
    
    # Tabla
    draw_rectangle(draw, 240, 230, 1020, 420, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    
    # Headers
    headers = [("ID", 260), ("Nombre", 320), ("Email", 550), ("Sucursal", 750), ("Cargo", 930), ("Acc", 1120)]
    for header, x in headers:
        draw_text(draw, header, x, 245, size=14, bold=True)
    
    draw.line([(240, 275), (1260, 275)], fill=BORDER_COLOR, width=2)
    
    # Filas con badges de roles
    rows = [
        ("1", "Ana López", "ana@email.com", "Bogotá", "ADMIN", (59, 130, 246), 290),
        ("2", "Carlos Ruiz", "carlos@email.com", "Medellín", "MANAGER", (249, 115, 22), 330),
        ("3", "María Gómez", "maria@email.com", "Cali", "SALES", (16, 185, 129), 370),
        ("4", "Pedro Torres", "pedro@email.com", "Bogotá", "SALES", (16, 185, 129), 410),
        ("5", "Laura Díaz", "laura@email.com", "Medellín", "MANAGER", (249, 115, 22), 450),
    ]
    
    for id, name, email, branch, role, role_color, y in rows:
        draw_text(draw, id, 260, y, size=14)
        draw_text(draw, name, 320, y, size=14)
        draw_text(draw, email, 550, y, size=14)
        draw_text(draw, branch, 750, y, size=14)
        
        # Badge de rol
        draw_rectangle(draw, 930, y, 90, 25, fill=role_color)
        draw_text(draw, role, 940, y + 4, size=12, color=(255, 255, 255))
        
        draw_text(draw, "✏️ 🗑️", 1120, y, size=14)
    
    img.save(os.path.join(OUTPUT_DIR, "WF-005_employees_list.png"))
    print("✅ WF-005_employees_list.png generado")

def generate_wf006_inventory_list():
    """WF-006: Lista de Inventario con alertas de stock bajo"""
    img, draw = create_base_wireframe()
    
    # Header
    draw_rectangle(draw, 0, 0, WIDTH, 60, fill=(31, 41, 55))
    draw_text(draw, "🏢 Multicont", 20, 18, size=24, color=(255, 255, 255), bold=True)
    
    # Sidebar
    draw_rectangle(draw, 0, 60, 220, HEIGHT - 60, fill=(249, 250, 251))
    draw_rectangle(draw, 10, 220, 200, 40, fill=PRIMARY_COLOR)
    draw_text(draw, "📦 Inventario", 25, 230, size=14, color=(255, 255, 255))
    
    # Content
    draw_text(draw, "Inicio > Inventario", 240, 80, size=14, color=(107, 114, 128))
    draw_text(draw, "Control de Inventario", 240, 110, size=24, bold=True)
    
    # Búsqueda
    draw_rectangle(draw, 240, 160, 400, 45, fill=(249, 250, 251), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "🔍 Buscar producto...", 260, 172, size=14, color=(156, 163, 175))
    
    draw_rectangle(draw, 660, 160, 160, 45, fill=PRIMARY_COLOR)
    draw_text(draw, "+ Nuevo Item", 695, 172, size=14, color=(255, 255, 255), bold=True)
    
    # Filtros
    draw_text(draw, "Categoría:", 840, 172, size=14)
    draw_rectangle(draw, 920, 160, 120, 45, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Todas ▼", 940, 172, size=14)
    
    draw_text(draw, "Stock:", 1060, 172, size=14)
    draw_rectangle(draw, 1120, 160, 100, 45, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Todos ▼", 1140, 172, size=14)
    
    # Tabla
    draw_rectangle(draw, 240, 230, 1020, 420, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    
    # Headers
    headers = [("SKU", 260), ("Nombre", 360), ("Categoría", 600), ("Marca", 780), ("Cant.", 920), ("Precio", 1030), ("Acc", 1170)]
    for header, x in headers:
        draw_text(draw, header, x, 245, size=14, bold=True)
    
    draw.line([(240, 275), (1260, 275)], fill=BORDER_COLOR, width=2)
    
    # Filas (algunas con stock bajo)
    rows = [
        ("SKU001", "Sensor Temp.", "Sensores", "Omron", "45", "$50,000", False, 290),
        ("SKU002", "Relay 24V", "Eléctricos", "Siemens", "3", "$30,000", True, 330),
        ("SKU003", "Cable UTP", "Cables", "Furukawa", "120", "$15,000", False, 370),
        ("SKU004", "PLC S7-1200", "Control", "Siemens", "8", "$850,000", True, 410),
        ("SKU005", "Switch 8P", "Networking", "Cisco", "25", "$120,000", False, 450),
    ]
    
    for sku, name, cat, brand, qty, price, low_stock, y in rows:
        # Fila con fondo rojo si stock bajo
        if low_stock:
            draw_rectangle(draw, 240, y - 5, 1020, 35, fill=(254, 226, 226))
        
        draw_text(draw, sku, 260, y, size=14)
        draw_text(draw, name, 360, y, size=14)
        draw_text(draw, cat, 600, y, size=14)
        draw_text(draw, brand, 780, y, size=14)
        
        # Cantidad con alerta si es baja
        qty_color = DANGER_COLOR if low_stock else TEXT_COLOR
        qty_text = f"⚠️ {qty}" if low_stock else qty
        draw_text(draw, qty_text, 920, y, size=14, color=qty_color, bold=low_stock)
        
        draw_text(draw, price, 1030, y, size=14)
        draw_text(draw, "✏️ 🗑️", 1170, y, size=14)
    
    # Leyenda
    draw_rectangle(draw, 240, 660, 20, 20, fill=(254, 226, 226))
    draw_text(draw, "Stock Bajo (< 10 unidades)", 270, 663, size=12, color=DANGER_COLOR)
    
    img.save(os.path.join(OUTPUT_DIR, "WF-006_inventory_list.png"))
    print("✅ WF-006_inventory_list.png generado")

def generate_wf007_create_quote():
    """WF-007: Crear Cotización (formulario complejo)"""
    img, draw = create_base_wireframe()
    
    # Header
    draw_rectangle(draw, 0, 0, WIDTH, 60, fill=(31, 41, 55))
    draw_text(draw, "🏢 Multicont", 20, 18, size=24, color=(255, 255, 255), bold=True)
    
    # Sidebar
    draw_rectangle(draw, 0, 60, 220, HEIGHT - 60, fill=(249, 250, 251))
    
    # Content
    draw_text(draw, "Inicio > Cotizaciones > Nueva", 240, 80, size=14, color=(107, 114, 128))
    draw_text(draw, "Nueva Cotización", 240, 110, size=24, bold=True)
    
    # Sección 1: Información General
    y = 160
    draw_text(draw, "── Información General ──", 240, y, size=16, bold=True)
    
    y += 40
    # Cliente
    draw_text(draw, "Cliente *", 240, y, size=14)
    draw_rectangle(draw, 240, y + 25, 450, 40, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Seleccionar cliente... ▼", 260, y + 35, size=14, color=(156, 163, 175))
    
    # Fechas
    draw_text(draw, "Fecha Cotización", 720, y, size=14)
    draw_rectangle(draw, 720, y + 25, 220, 40, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "📅 19/10/2025", 740, y + 35, size=14)
    
    draw_text(draw, "Fecha Vencimiento", 970, y, size=14)
    draw_rectangle(draw, 970, y + 25, 220, 40, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "📅 26/10/2025", 990, y + 35, size=14)
    
    # Sección 2: Productos
    y += 120
    draw_text(draw, "── Productos ──", 240, y, size=16, bold=True)
    
    y += 40
    # Tabla de productos
    draw_rectangle(draw, 240, y, 950, 180, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    
    # Headers tabla
    headers = [("Producto", 260), ("Cantidad", 520), ("Precio Unit.", 650), ("Subtotal", 810), ("", 950)]
    for header, x in headers:
        draw_text(draw, header, x, y + 10, size=14, bold=True)
    
    draw.line([(240, y + 40), (1190, y + 40)], fill=BORDER_COLOR, width=2)
    
    # Fila 1
    draw_rectangle(draw, 260, y + 50, 240, 35, fill=(249, 250, 251), outline=BORDER_COLOR)
    draw_text(draw, "Item A ▼", 270, y + 60, size=14)
    draw_text(draw, "10", 540, y + 60, size=14)
    draw_text(draw, "$50,000", 670, y + 60, size=14)
    draw_text(draw, "$500,000", 830, y + 60, size=14, bold=True)
    draw_text(draw, "🗑️", 980, y + 60, size=14, color=DANGER_COLOR)
    
    # Fila 2
    draw_rectangle(draw, 260, y + 95, 240, 35, fill=(249, 250, 251), outline=BORDER_COLOR)
    draw_text(draw, "Item B ▼", 270, y + 105, size=14)
    draw_text(draw, "5", 540, y + 105, size=14)
    draw_text(draw, "$30,000", 670, y + 105, size=14)
    draw_text(draw, "$150,000", 830, y + 105, size=14, bold=True)
    draw_text(draw, "🗑️", 980, y + 105, size=14, color=DANGER_COLOR)
    
    # Botón agregar
    y += 190
    draw_rectangle(draw, 240, y, 180, 35, fill=(229, 231, 235))
    draw_text(draw, "+ Agregar Producto", 255, y + 10, size=14, color=PRIMARY_COLOR)
    
    # Sección 3: Totales
    y += 60
    draw_text(draw, "── Totales ──", 240, y, size=16, bold=True)
    
    y += 40
    # Box de totales (alineado a la derecha)
    totals_x = 920
    draw_text(draw, "Subtotal:", totals_x, y, size=14)
    draw_text(draw, "$650,000", totals_x + 160, y, size=14)
    
    draw_text(draw, "IVA (19%):", totals_x, y + 30, size=14)
    draw_text(draw, "$123,500", totals_x + 160, y + 30, size=14)
    
    draw.line([(totals_x, y + 60), (totals_x + 270, y + 60)], fill=BORDER_COLOR, width=2)
    
    draw_text(draw, "TOTAL:", totals_x, y + 70, size=18, bold=True)
    draw_text(draw, "$773,500", totals_x + 140, y + 70, size=24, color=PRIMARY_COLOR, bold=True)
    
    # Botones de acción
    draw_rectangle(draw, 240, HEIGHT - 90, 140, 45, fill=(229, 231, 235))
    draw_text(draw, "Cancelar", 280, HEIGHT - 75, size=14)
    
    draw_rectangle(draw, 400, HEIGHT - 90, 180, 45, fill=(156, 163, 175))
    draw_text(draw, "Guardar Borrador", 420, HEIGHT - 75, size=14, color=(255, 255, 255))
    
    draw_rectangle(draw, 600, HEIGHT - 90, 200, 45, fill=PRIMARY_COLOR)
    draw_text(draw, "Crear Cotización", 630, HEIGHT - 75, size=14, color=(255, 255, 255), bold=True)
    
    img.save(os.path.join(OUTPUT_DIR, "WF-007_create_quote.png"))
    print("✅ WF-007_create_quote.png generado")

def generate_wf008_analytics_dashboard():
    """WF-008: Analytics Dashboard"""
    img, draw = create_base_wireframe()
    
    # Header
    draw_rectangle(draw, 0, 0, WIDTH, 60, fill=(31, 41, 55))
    draw_text(draw, "🏢 Multicont", 20, 18, size=24, color=(255, 255, 255), bold=True)
    
    # Sidebar
    draw_rectangle(draw, 0, 60, 220, HEIGHT - 60, fill=(249, 250, 251))
    draw_rectangle(draw, 10, 320, 200, 40, fill=PRIMARY_COLOR)
    draw_text(draw, "📊 Analytics", 25, 330, size=14, color=(255, 255, 255))
    
    # Content
    draw_text(draw, "Inicio > Analytics", 240, 80, size=14, color=(107, 114, 128))
    
    # Filtros globales
    draw_text(draw, "Período:", 240, 115, size=14)
    draw_rectangle(draw, 310, 110, 120, 35, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Mes ▼", 330, 120, size=14)
    
    draw_text(draw, "Sucursal:", 450, 115, size=14)
    draw_rectangle(draw, 530, 110, 140, 35, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Todas ▼", 550, 120, size=14)
    
    draw_text(draw, "Empleado:", 690, 115, size=14)
    draw_rectangle(draw, 780, 110, 140, 35, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Todos ▼", 800, 120, size=14)
    
    # 6 KPI Cards
    y = 165
    kpis = [
        ("Ventas Totales", "$45M", 240),
        ("Metas Cumplidas", "87%", 450),
        ("Promedio Venta", "$350K", 660),
        ("Órdenes", "124", 870),
        ("Facturación Pend.", "$2.5M", 1080),
    ]
    for title, value, x in kpis:
        draw_rectangle(draw, x, y, 190, 75, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
        draw_text(draw, title, x + 10, y + 10, size=12, color=(107, 114, 128))
        draw_text(draw, value, x + 10, y + 35, size=22, color=PRIMARY_COLOR, bold=True)
    
    # Gráfico de líneas: Ventas vs Metas
    y = 260
    draw_rectangle(draw, 240, y, 600, 200, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Ventas vs Metas (6 meses)", 260, y + 15, size=16, bold=True)
    
    # Líneas simuladas
    points_ventas = [(280, y + 180), (360, y + 140), (440, y + 160), (520, y + 110), (600, y + 130), (680, y + 90)]
    points_metas = [(280, y + 150), (360, y + 150), (440, y + 150), (520, y + 150), (600, y + 150), (680, y + 150)]
    
    for i in range(len(points_ventas) - 1):
        draw.line([points_ventas[i], points_ventas[i + 1]], fill=PRIMARY_COLOR, width=3)
        draw.line([points_metas[i], points_metas[i + 1]], fill=(249, 115, 22), width=3)
    
    # Leyenda
    draw_rectangle(draw, 760, y + 20, 15, 15, fill=PRIMARY_COLOR)
    draw_text(draw, "Ventas", 780, y + 18, size=12)
    draw_rectangle(draw, 760, y + 40, 15, 15, fill=(249, 115, 22))
    draw_text(draw, "Metas", 780, y + 38, size=12)
    
    # Gráfico de barras: Ventas por Sucursal
    draw_rectangle(draw, 860, y, 380, 200, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Ventas por Sucursal", 880, y + 15, size=16, bold=True)
    
    bars = [(900, 120), (970, 90), (1040, 140), (1110, 75), (1180, 100)]
    for x, h in bars:
        draw_rectangle(draw, x, y + 180 - h, 50, h, fill=SUCCESS_COLOR)
    
    # Tabla Top 10 Performers
    y = 480
    draw_rectangle(draw, 240, y, 1000, 200, fill=(255, 255, 255), outline=BORDER_COLOR, width_line=2)
    draw_text(draw, "Top 10 Performers", 260, y + 15, size=16, bold=True)
    
    # Headers
    headers = [("#", 260), ("Nombre", 320), ("Ventas", 550), ("Meta", 720), ("% Cumpl.", 880), ("Estado", 1050)]
    for header, x in headers:
        draw_text(draw, header, x, y + 45, size=14, bold=True)
    
    draw.line([(240, y + 70), (1240, y + 70)], fill=BORDER_COLOR, width=2)
    
    # Top 3
    performers = [
        ("1", "🥇 Ana López", "$5,000,000", "$4M", "125%", SUCCESS_COLOR, y + 80),
        ("2", "🥈 Carlos Ruiz", "$4,500,000", "$4M", "112%", SUCCESS_COLOR, y + 110),
        ("3", "🥉 María Gómez", "$4,000,000", "$4M", "100%", SUCCESS_COLOR, y + 140),
    ]
    
    for rank, name, sales, goal, perc, color, row_y in performers:
        draw_text(draw, rank, 260, row_y, size=14, bold=True)
        draw_text(draw, name, 320, row_y, size=14)
        draw_text(draw, sales, 550, row_y, size=14)
        draw_text(draw, goal, 720, row_y, size=14)
        draw_text(draw, perc, 900, row_y, size=14, color=color, bold=True)
        draw_rectangle(draw, 1050, row_y, 80, 22, fill=color)
        draw_text(draw, "Superó", 1060, row_y + 3, size=11, color=(255, 255, 255))
    
    img.save(os.path.join(OUTPUT_DIR, "WF-008_analytics_dashboard.png"))
    print("✅ WF-008_analytics_dashboard.png generado")

def main():
    """Generar todos los wireframes"""
    print("🎨 Generando wireframes para Multicont...")
    print("📂 Directorio de salida: docs/wireframes/")
    print()
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    generate_wf001_login()
    generate_wf002_dashboard()
    generate_wf003_organizations_list()
    generate_wf004_organization_form()
    generate_wf005_employees_list()
    generate_wf006_inventory_list()
    generate_wf007_create_quote()
    generate_wf008_analytics_dashboard()
    
    print()
    print("🎉 ¡Todos los wireframes generados exitosamente!")
    print("📊 Total: 8 wireframes PNG (1280x720px)")
    print()
    print("Archivos generados:")
    for i in range(1, 9):
        filename = f"WF-{i:03d}_*.png"
        print(f"  ✅ {filename}")

if __name__ == "__main__":
    main()
