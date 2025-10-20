# 🔧 Parámetros de Población de Base de Datos - Sistema Multicont

**Fecha**: 20 de Octubre de 2025  
**Sistema**: PostgreSQL con SQLAlchemy  
**Script de población**: `scripts/setup/populate_rbac_data.py`  
**Estado**: Configuración validada con tests 90/90 (100%)

---

## 📋 Visión General

Este documento contiene todos los parámetros y datos de prueba utilizados para poblar la base de datos del sistema Multicont. Los datos están organizados por módulos y permiten la validación completa del sistema con tests RBAC.

---

## 🔐 MÓDULO DE SEGURIDAD

### 1. Roles (4 registros)

```python
ROLES = [
    {
        'name': 'ADMIN',
        'description': 'Administrador del sistema con acceso total',
        'status': 'active'
    },
    {
        'name': 'MANAGER',
        'description': 'Gerente de sucursal con permisos de gestión',
        'status': 'active'
    },
    {
        'name': 'SALES',
        'description': 'Vendedor con permisos de ventas y cotizaciones',
        'status': 'active'
    },
    {
        'name': 'VIEWER',
        'description': 'Usuario con permisos de solo lectura',
        'status': 'active'
    }
]
```

### 2. Permisos (20+ registros)

```python
PERMISSIONS = [
    # Permisos de ADMIN (acceso total)
    {'role': 'ADMIN', 'resource': 'users', 'action': 'create', 'description': 'Crear usuarios'},
    {'role': 'ADMIN', 'resource': 'users', 'action': 'read', 'description': 'Ver usuarios'},
    {'role': 'ADMIN', 'resource': 'users', 'action': 'update', 'description': 'Actualizar usuarios'},
    {'role': 'ADMIN', 'resource': 'users', 'action': 'delete', 'description': 'Eliminar usuarios'},
    {'role': 'ADMIN', 'resource': 'roles', 'action': 'create', 'description': 'Crear roles'},
    {'role': 'ADMIN', 'resource': 'roles', 'action': 'read', 'description': 'Ver roles'},
    {'role': 'ADMIN', 'resource': 'roles', 'action': 'update', 'description': 'Actualizar roles'},
    {'role': 'ADMIN', 'resource': 'roles', 'action': 'delete', 'description': 'Eliminar roles'},
    {'role': 'ADMIN', 'resource': 'permissions', 'action': 'create', 'description': 'Crear permisos'},
    {'role': 'ADMIN', 'resource': 'permissions', 'action': 'read', 'description': 'Ver permisos'},
    {'role': 'ADMIN', 'resource': 'permissions', 'action': 'update', 'description': 'Actualizar permisos'},
    {'role': 'ADMIN', 'resource': 'permissions', 'action': 'delete', 'description': 'Eliminar permisos'},
    
    # Permisos de MANAGER
    {'role': 'MANAGER', 'resource': 'organizations', 'action': 'read', 'description': 'Ver organizaciones'},
    {'role': 'MANAGER', 'resource': 'organizations', 'action': 'update', 'description': 'Actualizar organizaciones'},
    {'role': 'MANAGER', 'resource': 'branches', 'action': 'create', 'description': 'Crear sucursales'},
    {'role': 'MANAGER', 'resource': 'branches', 'action': 'read', 'description': 'Ver sucursales'},
    {'role': 'MANAGER', 'resource': 'branches', 'action': 'update', 'description': 'Actualizar sucursales'},
    {'role': 'MANAGER', 'resource': 'employees', 'action': 'create', 'description': 'Crear empleados'},
    {'role': 'MANAGER', 'resource': 'employees', 'action': 'read', 'description': 'Ver empleados'},
    {'role': 'MANAGER', 'resource': 'employees', 'action': 'update', 'description': 'Actualizar empleados'},
    {'role': 'MANAGER', 'resource': 'inventory', 'action': 'read', 'description': 'Ver inventario'},
    {'role': 'MANAGER', 'resource': 'inventory', 'action': 'update', 'description': 'Actualizar inventario'},
    {'role': 'MANAGER', 'resource': 'quotes', 'action': 'read', 'description': 'Ver cotizaciones'},
    {'role': 'MANAGER', 'resource': 'quotes', 'action': 'update', 'description': 'Aprobar cotizaciones'},
    {'role': 'MANAGER', 'resource': 'sales', 'action': 'read', 'description': 'Ver ventas'},
    {'role': 'MANAGER', 'resource': 'invoices', 'action': 'read', 'description': 'Ver facturas'},
    
    # Permisos de SALES
    {'role': 'SALES', 'resource': 'inventory', 'action': 'read', 'description': 'Ver inventario'},
    {'role': 'SALES', 'resource': 'quotes', 'action': 'create', 'description': 'Crear cotizaciones'},
    {'role': 'SALES', 'resource': 'quotes', 'action': 'read', 'description': 'Ver cotizaciones'},
    {'role': 'SALES', 'resource': 'quotes', 'action': 'update', 'description': 'Actualizar cotizaciones'},
    {'role': 'SALES', 'resource': 'sales', 'action': 'create', 'description': 'Crear ventas'},
    {'role': 'SALES', 'resource': 'sales', 'action': 'read', 'description': 'Ver ventas'},
    {'role': 'SALES', 'resource': 'invoices', 'action': 'create', 'description': 'Crear facturas'},
    {'role': 'SALES', 'resource': 'invoices', 'action': 'read', 'description': 'Ver facturas'},
    
    # Permisos de VIEWER
    {'role': 'VIEWER', 'resource': 'inventory', 'action': 'read', 'description': 'Ver inventario'},
    {'role': 'VIEWER', 'resource': 'quotes', 'action': 'read', 'description': 'Ver cotizaciones'},
    {'role': 'VIEWER', 'resource': 'sales', 'action': 'read', 'description': 'Ver ventas'},
    {'role': 'VIEWER', 'resource': 'invoices', 'action': 'read', 'description': 'Ver facturas'},
    {'role': 'VIEWER', 'resource': 'organizations', 'action': 'read', 'description': 'Ver organizaciones'},
    {'role': 'VIEWER', 'resource': 'branches', 'action': 'read', 'description': 'Ver sucursales'},
]
```

### 3. Usuarios (3 registros de prueba)

```python
# Contraseñas hasheadas con bcrypt
# Formato: bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

USERS = [
    {
        'username': 'admin',
        'email': 'admin@multicont.com',
        'password': 'admin123',  # Se hashea en el script
        'first_name': 'Admin',
        'last_name': 'Sistema',
        'phone': '+57 300 1234567',
        'status': 'active',
        'role': 'ADMIN'
    },
    {
        'username': 'manager',
        'email': 'manager@multicont.com',
        'password': 'manager123',  # Se hashea en el script
        'first_name': 'Manager',
        'last_name': 'Sucursal',
        'phone': '+57 310 2345678',
        'status': 'active',
        'role': 'MANAGER'
    },
    {
        'username': 'sales',
        'email': 'sales@multicont.com',
        'password': 'sales123',  # Se hashea en el script
        'first_name': 'Sales',
        'last_name': 'Rep',
        'phone': '+57 320 3456789',
        'status': 'active',
        'role': 'SALES'
    }
]
```

**Credenciales de acceso**:
```
Admin:    username=admin    password=admin123
Manager:  username=manager  password=manager123
Sales:    username=sales    password=sales123
```

---

## 🏢 MÓDULO ORGANIZACIONAL

### 4. Estados (2 registros)

```python
STATES = [
    {
        'name': 'Antioquia',
        'code': 'ANT',
        'status': 'active'
    },
    {
        'name': 'Valle del Cauca',
        'code': 'VAL',
        'status': 'active'
    }
]
```

### 5. Ciudades (2 registros)

```python
CITIES = [
    {
        'state_code': 'ANT',
        'name': 'Medellín',
        'code': 'MED',
        'status': 'active'
    },
    {
        'state_code': 'VAL',
        'name': 'Cali',
        'code': 'CLO',
        'status': 'active'
    }
]
```

### 6. Organizaciones (2 registros)

```python
ORGANIZATIONS = [
    {
        'name': 'Multicont S.A.S.',
        'nit': '900123456-7',
        'address': 'Calle 10 # 20-30, Medellín',
        'phone': '+57 604 3001234',
        'email': 'contacto@multicont.com',
        'status': 'active'
    },
    {
        'name': 'Multicont Sucursal Norte',
        'nit': '900654321-2',
        'address': 'Carrera 50 # 70-80, Cali',
        'phone': '+57 602 4005678',
        'email': 'norte@multicont.com',
        'status': 'active'
    }
]
```

### 7. Sucursales (2 registros)

```python
BRANCHES = [
    {
        'organization_nit': '900123456-7',
        'city_code': 'MED',
        'name': 'Sucursal Principal - Medellín',
        'address': 'Calle 10 # 20-30, Centro',
        'phone': '+57 604 3001234',
        'email': 'principal@multicont.com',
        'status': 'active'
    },
    {
        'organization_nit': '900654321-2',
        'city_code': 'CLO',
        'name': 'Sucursal Norte - Cali',
        'address': 'Carrera 50 # 70-80, Norte',
        'phone': '+57 602 4005678',
        'email': 'cali@multicont.com',
        'status': 'active'
    }
]
```

### 8. Personas (3 registros)

```python
PERSONS = [
    {
        'first_name': 'Juan',
        'last_name': 'Pérez García',
        'document_type': 'CC',
        'document_number': '1234567890',
        'phone': '+57 300 1111111',
        'email': 'juan.perez@gmail.com',
        'address': 'Calle 20 # 30-40, Medellín',
        'birth_date': '1985-03-15',
        'status': 'active'
    },
    {
        'first_name': 'María',
        'last_name': 'González López',
        'document_type': 'CC',
        'document_number': '9876543210',
        'phone': '+57 310 2222222',
        'email': 'maria.gonzalez@gmail.com',
        'address': 'Carrera 40 # 50-60, Medellín',
        'birth_date': '1990-07-22',
        'status': 'active'
    },
    {
        'first_name': 'Carlos',
        'last_name': 'Rodríguez Martínez',
        'document_type': 'CC',
        'document_number': '5555666677',
        'phone': '+57 320 3333333',
        'email': 'carlos.rodriguez@gmail.com',
        'address': 'Avenida 60 # 70-80, Cali',
        'birth_date': '1988-11-10',
        'status': 'active'
    }
]
```

### 9. Empleados (3 registros)

```python
EMPLOYEES = [
    {
        'person_document': '1234567890',
        'branch_name': 'Sucursal Principal - Medellín',
        'position': 'Gerente General',
        'hire_date': '2020-01-15',
        'salary': 5000000.00,
        'status': 'active'
    },
    {
        'person_document': '9876543210',
        'branch_name': 'Sucursal Principal - Medellín',
        'position': 'Vendedor Senior',
        'hire_date': '2021-03-20',
        'salary': 2500000.00,
        'status': 'active'
    },
    {
        'person_document': '5555666677',
        'branch_name': 'Sucursal Norte - Cali',
        'position': 'Vendedor Junior',
        'hire_date': '2022-06-01',
        'salary': 1800000.00,
        'status': 'active'
    }
]
```

---

## 📦 MÓDULO DE INVENTARIO

### 10. Categorías de Items (5 registros)

```python
ITEM_CATEGORIES = [
    {
        'name': 'Electrónica',
        'description': 'Productos electrónicos y tecnológicos',
        'status': 'active'
    },
    {
        'name': 'Muebles',
        'description': 'Muebles de oficina y hogar',
        'status': 'active'
    },
    {
        'name': 'Papelería',
        'description': 'Artículos de papelería y oficina',
        'status': 'active'
    },
    {
        'name': 'Herramientas',
        'description': 'Herramientas y equipos',
        'status': 'active'
    },
    {
        'name': 'Suministros',
        'description': 'Suministros generales',
        'status': 'active'
    }
]
```

### 11. Marcas (8 registros)

```python
BRANDS = [
    {'name': 'Samsung', 'description': 'Tecnología Samsung', 'status': 'active'},
    {'name': 'HP', 'description': 'Hewlett-Packard', 'status': 'active'},
    {'name': 'Sony', 'description': 'Electrónica Sony', 'status': 'active'},
    {'name': 'LG', 'description': 'LG Electronics', 'status': 'active'},
    {'name': 'Dell', 'description': 'Dell Technologies', 'status': 'active'},
    {'name': 'Lenovo', 'description': 'Lenovo Group', 'status': 'active'},
    {'name': 'Apple', 'description': 'Apple Inc.', 'status': 'active'},
    {'name': 'Generic', 'description': 'Marca genérica', 'status': 'active'}
]
```

### 12. Items de Inventario (10 registros de ejemplo)

```python
INVENTORY_ITEMS = [
    {
        'category': 'Electrónica',
        'brand': 'Samsung',
        'name': 'Monitor LED 24 pulgadas',
        'description': 'Monitor LED Full HD 1920x1080, HDMI',
        'sku': 'MON-SAM-24-001',
        'quantity': 15,
        'unit_price': 450000.00,
        'status': 'active'
    },
    {
        'category': 'Electrónica',
        'brand': 'HP',
        'name': 'Laptop HP Core i5',
        'description': 'Laptop HP 15.6", Core i5, 8GB RAM, 256GB SSD',
        'sku': 'LAP-HP-I5-001',
        'quantity': 8,
        'unit_price': 1800000.00,
        'status': 'active'
    },
    {
        'category': 'Electrónica',
        'brand': 'Dell',
        'name': 'Teclado Mecánico RGB',
        'description': 'Teclado mecánico gaming con retroiluminación RGB',
        'sku': 'TEC-DEL-RGB-001',
        'quantity': 25,
        'unit_price': 180000.00,
        'status': 'active'
    },
    {
        'category': 'Electrónica',
        'brand': 'Logitech',
        'name': 'Mouse Inalámbrico',
        'description': 'Mouse inalámbrico ergonómico 2.4GHz',
        'sku': 'MOU-LOG-WIR-001',
        'quantity': 30,
        'unit_price': 65000.00,
        'status': 'active'
    },
    {
        'category': 'Muebles',
        'brand': 'Generic',
        'name': 'Silla Ergonómica Oficina',
        'description': 'Silla ergonómica con soporte lumbar ajustable',
        'sku': 'SIL-GEN-ERG-001',
        'quantity': 12,
        'unit_price': 350000.00,
        'status': 'active'
    },
    {
        'category': 'Muebles',
        'brand': 'Generic',
        'name': 'Escritorio Ajustable',
        'description': 'Escritorio de altura ajustable 120x60cm',
        'sku': 'ESC-GEN-ADJ-001',
        'quantity': 6,
        'unit_price': 750000.00,
        'status': 'active'
    },
    {
        'category': 'Papelería',
        'brand': 'Generic',
        'name': 'Resma Papel Carta',
        'description': 'Resma papel bond 500 hojas tamaño carta',
        'sku': 'PAP-GEN-RES-001',
        'quantity': 50,
        'unit_price': 12000.00,
        'status': 'active'
    },
    {
        'category': 'Papelería',
        'brand': 'Generic',
        'name': 'Kit Marcadores Borrables',
        'description': 'Set de 4 marcadores borrables para tablero',
        'sku': 'MAR-GEN-KIT-001',
        'quantity': 40,
        'unit_price': 15000.00,
        'status': 'active'
    },
    {
        'category': 'Herramientas',
        'brand': 'Generic',
        'name': 'Destornillador Set 6pz',
        'description': 'Set de destornilladores magnéticos 6 piezas',
        'sku': 'DES-GEN-SET-001',
        'quantity': 20,
        'unit_price': 35000.00,
        'status': 'active'
    },
    {
        'category': 'Suministros',
        'brand': 'Generic',
        'name': 'Caja Organizadora Plástico',
        'description': 'Caja organizadora transparente 30x20x15cm',
        'sku': 'CAJ-GEN-ORG-001',
        'quantity': 35,
        'unit_price': 25000.00,
        'status': 'active'
    }
]
```

### 13. Asignaciones (Ejemplo - 3 registros)

```python
ASSIGNMENTS = [
    {
        'employee_document': '1234567890',
        'item_sku': 'LAP-HP-I5-001',
        'quantity': 1,
        'assignment_date': '2024-01-15',
        'return_date': None,
        'notes': 'Laptop asignada para trabajo remoto',
        'status': 'assigned'
    },
    {
        'employee_document': '9876543210',
        'item_sku': 'MON-SAM-24-001',
        'quantity': 1,
        'assignment_date': '2024-02-20',
        'return_date': None,
        'notes': 'Monitor para estación de trabajo',
        'status': 'assigned'
    },
    {
        'employee_document': '5555666677',
        'item_sku': 'TEC-DEL-RGB-001',
        'quantity': 1,
        'assignment_date': '2024-03-10',
        'return_date': None,
        'notes': 'Teclado para oficina',
        'status': 'assigned'
    }
]
```

---

## 💼 MÓDULO DE VENTAS

### 14. Cotizaciones (Ejemplo - 2 registros)

```python
QUOTES = [
    {
        'branch_name': 'Sucursal Principal - Medellín',
        'user_username': 'sales',
        'customer_name': 'Empresa ABC S.A.S.',
        'customer_email': 'compras@empresaabc.com',
        'customer_phone': '+57 300 9999999',
        'quote_date': '2024-10-01',
        'expiration_date': '2024-10-15',
        'total_amount': 0,  # Se calcula automáticamente
        'status': 'pending',
        'notes': 'Cotización de equipos de oficina'
    },
    {
        'branch_name': 'Sucursal Norte - Cali',
        'user_username': 'sales',
        'customer_name': 'Corporación XYZ Ltda.',
        'customer_email': 'adquisiciones@xyz.com',
        'customer_phone': '+57 310 8888888',
        'quote_date': '2024-10-05',
        'expiration_date': '2024-10-20',
        'total_amount': 0,  # Se calcula automáticamente
        'status': 'approved',
        'notes': 'Cotización aprobada - generar orden'
    }
]
```

### 15. Líneas de Cotización (Ejemplo - 5 registros)

```python
QUOTATION_LINES = [
    # Cotización 1
    {
        'quote_customer': 'Empresa ABC S.A.S.',
        'item_sku': 'LAP-HP-I5-001',
        'quantity': 5,
        'unit_price': 1800000.00,
        'discount': 0,
        'tax': 19,
        'subtotal': 9000000.00,  # Se calcula automáticamente
        'total': 10710000.00  # Se calcula automáticamente
    },
    {
        'quote_customer': 'Empresa ABC S.A.S.',
        'item_sku': 'MON-SAM-24-001',
        'quantity': 5,
        'unit_price': 450000.00,
        'discount': 5,
        'tax': 19,
        'subtotal': 2250000.00,
        'total': 2534250.00
    },
    
    # Cotización 2
    {
        'quote_customer': 'Corporación XYZ Ltda.',
        'item_sku': 'SIL-GEN-ERG-001',
        'quantity': 10,
        'unit_price': 350000.00,
        'discount': 10,
        'tax': 19,
        'subtotal': 3500000.00,
        'total': 3723500.00
    },
    {
        'quote_customer': 'Corporación XYZ Ltda.',
        'item_sku': 'ESC-GEN-ADJ-001',
        'quantity': 10,
        'unit_price': 750000.00,
        'discount': 10,
        'tax': 19,
        'subtotal': 7500000.00,
        'total': 7987500.00
    },
    {
        'quote_customer': 'Corporación XYZ Ltda.',
        'item_sku': 'TEC-DEL-RGB-001',
        'quantity': 10,
        'unit_price': 180000.00,
        'discount': 0,
        'tax': 19,
        'subtotal': 1800000.00,
        'total': 2142000.00
    }
]
```

### 16. Órdenes de Venta (Ejemplo - 1 registro)

```python
SALES_ORDERS = [
    {
        'quote_customer': 'Corporación XYZ Ltda.',
        'branch_name': 'Sucursal Norte - Cali',
        'user_username': 'sales',
        'order_number': 'SO-2024-001',
        'order_date': '2024-10-06',
        'delivery_date': '2024-10-20',
        'customer_name': 'Corporación XYZ Ltda.',
        'customer_email': 'adquisiciones@xyz.com',
        'customer_phone': '+57 310 8888888',
        'total_amount': 0,  # Se calcula automáticamente
        'status': 'approved',
        'notes': 'Orden generada desde cotización aprobada'
    }
]
```

### 17. Items de Orden de Venta (Ejemplo - 3 registros)

```python
SALES_ORDER_ITEMS = [
    {
        'order_number': 'SO-2024-001',
        'item_sku': 'SIL-GEN-ERG-001',
        'quantity': 10,
        'unit_price': 350000.00,
        'discount': 10,
        'tax': 19,
        'subtotal': 3500000.00,
        'total': 3723500.00
    },
    {
        'order_number': 'SO-2024-001',
        'item_sku': 'ESC-GEN-ADJ-001',
        'quantity': 10,
        'unit_price': 750000.00,
        'discount': 10,
        'tax': 19,
        'subtotal': 7500000.00,
        'total': 7987500.00
    },
    {
        'order_number': 'SO-2024-001',
        'item_sku': 'TEC-DEL-RGB-001',
        'quantity': 10,
        'unit_price': 180000.00,
        'discount': 0,
        'tax': 19,
        'subtotal': 1800000.00,
        'total': 2142000.00
    }
]
```

### 18. Facturas (Ejemplo - 1 registro)

```python
INVOICES = [
    {
        'order_number': 'SO-2024-001',
        'branch_name': 'Sucursal Norte - Cali',
        'user_username': 'sales',
        'invoice_number': 'INV-2024-001',
        'invoice_date': '2024-10-06',
        'due_date': '2024-11-06',
        'customer_name': 'Corporación XYZ Ltda.',
        'customer_email': 'adquisiciones@xyz.com',
        'customer_phone': '+57 310 8888888',
        'customer_address': 'Calle 100 # 20-30, Cali',
        'subtotal': 12800000.00,
        'tax': 2432000.00,  # 19% de subtotal
        'discount': 1280000.00,  # 10% en algunos items
        'total_amount': 13853000.00,
        'status': 'active',
        'payment_status': 'unpaid',
        'payment_date': None,
        'notes': 'Factura generada desde orden SO-2024-001'
    }
]
```

### 19. Items de Factura (Ejemplo - 3 registros)

```python
INVOICE_ITEMS = [
    {
        'invoice_number': 'INV-2024-001',
        'item_sku': 'SIL-GEN-ERG-001',
        'quantity': 10,
        'unit_price': 350000.00,
        'discount': 10,
        'tax': 19,
        'subtotal': 3500000.00,
        'total': 3723500.00
    },
    {
        'invoice_number': 'INV-2024-001',
        'item_sku': 'ESC-GEN-ADJ-001',
        'quantity': 10,
        'unit_price': 750000.00,
        'discount': 10,
        'tax': 19,
        'subtotal': 7500000.00,
        'total': 7987500.00
    },
    {
        'invoice_number': 'INV-2024-001',
        'item_sku': 'TEC-DEL-RGB-001',
        'quantity': 10,
        'unit_price': 180000.00,
        'discount': 0,
        'tax': 19,
        'subtotal': 1800000.00,
        'total': 2142000.00
    }
]
```

### 20. Metas de Ventas (Ejemplo - 3 registros)

```python
SALES_GOALS = [
    {
        'employee_document': '1234567890',
        'goal_period': 'monthly',
        'start_date': '2024-10-01',
        'end_date': '2024-10-31',
        'target_amount': 20000000.00,
        'achieved_amount': 13853000.00,
        'status': 'active',
        'notes': 'Meta mensual octubre 2024'
    },
    {
        'employee_document': '9876543210',
        'goal_period': 'monthly',
        'start_date': '2024-10-01',
        'end_date': '2024-10-31',
        'target_amount': 15000000.00,
        'achieved_amount': 8500000.00,
        'status': 'active',
        'notes': 'Meta mensual octubre 2024'
    },
    {
        'employee_document': '5555666677',
        'goal_period': 'monthly',
        'start_date': '2024-10-01',
        'end_date': '2024-10-31',
        'target_amount': 10000000.00,
        'achieved_amount': 5000000.00,
        'status': 'active',
        'notes': 'Meta mensual octubre 2024 - Vendedor junior'
    }
]
```

---

## 🔧 Script de Población

### Función Principal

```python
def populate_database():
    """
    Pobla la base de datos con datos de prueba siguiendo el orden correcto
    de dependencias para evitar errores de FK.
    """
    
    print("🚀 Iniciando población de base de datos...")
    
    # Orden de población (respetando dependencias de FK)
    steps = [
        ("Roles", populate_roles),
        ("Permisos", populate_permissions),
        ("Usuarios", populate_users),
        ("Asignación Usuarios-Roles", populate_user_roles),
        ("Estados", populate_states),
        ("Ciudades", populate_cities),
        ("Organizaciones", populate_organizations),
        ("Sucursales", populate_branches),
        ("Personas", populate_persons),
        ("Empleados", populate_employees),
        ("Categorías de Items", populate_item_categories),
        ("Marcas", populate_brands),
        ("Items de Inventario", populate_inventory_items),
        ("Asignaciones", populate_assignments),
        ("Cotizaciones", populate_quotes),
        ("Líneas de Cotización", populate_quotation_lines),
        ("Órdenes de Venta", populate_sales_orders),
        ("Items de Órdenes", populate_sales_order_items),
        ("Facturas", populate_invoices),
        ("Items de Facturas", populate_invoice_items),
        ("Metas de Ventas", populate_sales_goals)
    ]
    
    for step_name, step_function in steps:
        try:
            print(f"\n📋 {step_name}...")
            step_function()
            db.session.commit()
            print(f"✅ {step_name} completado")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error en {step_name}: {str(e)}")
            raise
    
    print("\n🎉 ¡Base de datos poblada exitosamente!")
    print_summary()
```

### Validación de Datos

```python
def validate_population():
    """
    Valida que todos los datos se hayan insertado correctamente.
    """
    
    checks = [
        ("Roles", Role.query.count(), 4),
        ("Usuarios", User.query.count(), 3),
        ("Estados", State.query.count(), 2),
        ("Ciudades", City.query.count(), 2),
        ("Organizaciones", Organization.query.count(), 2),
        ("Sucursales", Branch.query.count(), 2),
        ("Personas", Person.query.count(), 3),
        ("Empleados", Employee.query.count(), 3),
        ("Categorías", ItemCategory.query.count(), 5),
        ("Marcas", Brand.query.count(), 8),
        ("Items", InventoryItem.query.count(), 10),
    ]
    
    print("\n🔍 Validación de datos:")
    all_ok = True
    for name, actual, expected in checks:
        status = "✅" if actual == expected else "❌"
        print(f"{status} {name}: {actual}/{expected}")
        if actual != expected:
            all_ok = False
    
    if all_ok:
        print("\n✅ Todos los datos validados correctamente")
    else:
        print("\n⚠️ Algunos datos no coinciden con lo esperado")
    
    return all_ok
```

---

## 📊 Resumen de Datos

### Conteo por Tabla

| Tabla | Registros | Notas |
|-------|-----------|-------|
| `role` | 4 | ADMIN, MANAGER, SALES, VIEWER |
| `permission` | 20+ | Permisos granulares por rol |
| `user` | 3 | admin, manager, sales |
| `user_role` | 3 | Asignaciones 1:1 |
| `state` | 2 | Antioquia, Valle |
| `city` | 2 | Medellín, Cali |
| `organization` | 2 | Multicont principal y norte |
| `branch` | 2 | Sucursal Medellín y Cali |
| `person` | 3 | Datos personales |
| `employee` | 3 | Empleados activos |
| `item_category` | 5 | Categorías básicas |
| `brand` | 8 | Marcas populares + Generic |
| `inventory_item` | 10 | Items de muestra |
| `assignment` | 3 | Asignaciones de ejemplo |
| `quote` | 2 | Cotizaciones en diferentes estados |
| `quotation_line` | 5 | Líneas de las cotizaciones |
| `sales_order` | 1 | Orden generada de cotización aprobada |
| `sales_order_item` | 3 | Items de la orden |
| `invoice` | 1 | Factura generada |
| `invoice_item` | 3 | Items facturados |
| `sales_goal` | 3 | Metas mensuales por empleado |

**Total de registros**: ~80 registros de datos de prueba

---

## 🧪 Validación con Tests

### Tests RBAC (90 tests - 100%)

```bash
# Ejecutar tests de validación
python tests/integration/test_rbac_simple.py

# Resultado esperado:
# SALES: 30/30 tests ✅
# MANAGER: 30/30 tests ✅
# ADMIN: 30/30 tests ✅
# TOTAL: 90/90 tests (100.0%)
```

### Endpoints Validados

Los datos de prueba permiten validar:

- ✅ Autenticación JWT con 3 usuarios
- ✅ Permisos RBAC por rol (20+ permisos)
- ✅ CRUD de todas las entidades
- ✅ Relaciones entre entidades (FKs)
- ✅ Flujo de ventas completo (Quote → Order → Invoice)
- ✅ Cálculos de totales y descuentos
- ✅ Asignaciones de items a empleados
- ✅ Metas de ventas y progreso

---

## 🔐 Credenciales de Acceso

### Para Testing Manual

```bash
# Login como ADMIN
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Login como MANAGER
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"manager","password":"manager123"}'

# Login como SALES
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"sales","password":"sales123"}'
```

### Para Swagger UI

1. Abrir: http://127.0.0.1:5000/api/docs/
2. Hacer clic en "Authorize" (candado)
3. Ingresar credenciales:
   - Username: `admin` / `manager` / `sales`
   - Password: `admin123` / `manager123` / `sales123`

---

## 📝 Notas Importantes

### Orden de Ejecución

⚠️ **IMPORTANTE**: El script debe ejecutarse siguiendo el orden exacto de dependencias:

1. Primero: Tablas raíz (sin FK) → `role`, `state`, `organization`, `person`, `item_category`, `brand`
2. Segundo: Tablas con 1 FK → `user`, `city`, `branch`, `permission`, `employee`, `inventory_item`
3. Tercero: Tablas con múltiples FK → `quote`, `sales_order`, `invoice`, `assignment`, `sales_goal`
4. Cuarto: Tablas de líneas/items → `quotation_line`, `sales_order_item`, `invoice_item`
5. Quinto: Tablas pivot → `user_role`

### Limpiar Base de Datos

```bash
# Eliminar todos los datos (reset completo)
flask db downgrade base
flask db upgrade head
python scripts/setup/populate_rbac_data.py
```

### Regenerar Datos

```bash
# Solo regenerar datos (mantener estructura)
python scripts/setup/populate_rbac_data.py --reset
```

---

## 🎓 Uso Académico

Este conjunto de datos de prueba está diseñado para:

✅ Demostrar funcionalidad completa del sistema  
✅ Validar tests RBAC (90/90 al 100%)  
✅ Probar flujo completo de ventas  
✅ Simular ambiente de producción  
✅ Presentación de proyecto académico  

**Documentación relacionada**:
- `docs/technical/database/ANALISIS_BASE_DATOS_COMPLETO.md`
- `docs/technical/guides/TESTING_GUIDE.md`
- `docs/academic/AUDITORIA_REQUISITOS.md`

---

**Fecha**: 20 de Octubre de 2025  
**Script**: `scripts/setup/populate_rbac_data.py`  
**Estado**: ✅ Validado con tests 90/90 (100%)
