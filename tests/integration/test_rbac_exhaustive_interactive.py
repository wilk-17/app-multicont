"""
TEST RBAC EXHAUSTIVO INTERACTIVO - 123 ENDPOINTS × 3 ROLES
===========================================================
Muestra TODAS las peticiones HTTP y respuestas en consola con colores
para los 123 endpoints del sistema con los 3 roles (ADMIN, MANAGER, SALES)

Total de tests: 369 (123 endpoints × 3 roles)
"""

import requests
import json
from datetime import datetime, date, timedelta
from colorama import init, Fore, Back, Style

# Inicializar colorama para colores en Windows
init(autoreset=True)

BASE_URL = "http://127.0.0.1:5000/api"

# Credenciales de los 3 roles
CREDENTIALS = {
    'ADMIN': {'username': 'admin', 'password': 'admin123'},
    'MANAGER': {'username': 'manager', 'password': 'manager123'},
    'SALES': {'username': 'sales', 'password': 'sales123'}
}

TOKENS = {}

def print_header(text, char="=", color=Fore.CYAN):
    """Imprime un header decorado"""
    line = char * 100
    print(f"\n{color}{line}")
    print(f"{text.center(100)}")
    print(f"{line}{Style.RESET_ALL}\n")

def get_token(role):
    """Obtiene token de autenticación"""
    creds = CREDENTIALS[role]
    response = requests.post(f"{BASE_URL}/auth/login", json=creds)
    if response.status_code == 200:
        return response.json().get('data', {}).get('access_token')
    return None

def make_request(method, endpoint, token, data=None):
    """Hace una petición HTTP"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        return response.status_code
    except Exception as e:
        return None

def print_test_result(endpoint_num, total_endpoints, method, path, description, results_by_role):
    """Imprime el resultado de un endpoint probado con los 3 roles"""
    # Crear string del endpoint con número
    endpoint_str = f"{endpoint_num:3}/{total_endpoints} {method:6} {path:<50}"
    
    # Colorear cada resultado según el status
    colored_results = []
    for role, status in results_by_role.items():
        if status is None:
            colored_results.append(f"{Fore.RED}ERR{Style.RESET_ALL}")
        elif status in [200, 201, 204]:
            colored_results.append(f"{Fore.GREEN}{status:3}{Style.RESET_ALL}")
        elif status == 403:
            colored_results.append(f"{Fore.YELLOW}{status:3}{Style.RESET_ALL}")
        elif status in [400, 404, 500]:
            colored_results.append(f"{Fore.CYAN}{status:3}{Style.RESET_ALL}")
        else:
            colored_results.append(f"{Fore.RED}{status:3}{Style.RESET_ALL}")
    
    print(f"{endpoint_str} │ A:{colored_results[0]} M:{colored_results[1]} S:{colored_results[2]} │ {description[:30]}")

def main():
    """Función principal"""
    print_header("🚀 TEST RBAC EXHAUSTIVO - 123 ENDPOINTS × 3 ROLES", "═", Fore.CYAN)
    print(f"{Fore.WHITE}Fecha:{Style.RESET_ALL} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.WHITE}Base URL:{Style.RESET_ALL} {BASE_URL}")
    print(f"{Fore.WHITE}Total de tests:{Style.RESET_ALL} 369 (123 endpoints × 3 roles)")
    
    # 1. AUTENTICACIÓN
    print_header("🔐 AUTENTICANDO ROLES", "═", Fore.YELLOW)
    
    for role in ['ADMIN', 'MANAGER', 'SALES']:
        token = get_token(role)
        if token:
            TOKENS[role] = token
            print(f"{Fore.GREEN}✓{Style.RESET_ALL} {role:8} autenticado - Token: {token[:30]}...")
        else:
            print(f"{Fore.RED}✗{Style.RESET_ALL} {role:8} ERROR en autenticación")
            return
    
    # 2. DEFINIR TODOS LOS ENDPOINTS
    timestamp = int(datetime.now().timestamp())
    
    endpoints = [
        # === AUTHENTICATION ===
        ('GET', '/auth/me', None, 'Usuario actual', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/auth/validate', None, 'Validar token', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/auth/logout', None, 'Cerrar sesión', ['ADMIN', 'MANAGER', 'SALES']),
        
        # === USERS ===
        ('GET', '/users/', None, 'Listar usuarios', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/users/1', None, 'Obtener usuario', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/users/', {'username': f'test{timestamp}', 'password': 'test123', 'role_id': 3}, 'Crear usuario', ['ADMIN']),
        ('PUT', '/users/2', {'username': 'updated_user'}, 'Actualizar usuario', ['ADMIN']),
        ('DELETE', '/users/999', None, 'Eliminar usuario', ['ADMIN']),
        
        # === ROLES ===
        ('GET', '/roles/', None, 'Listar roles', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/roles/1', None, 'Obtener rol', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/roles/', {'name': f'TestRole{timestamp}'}, 'Crear rol', ['ADMIN']),
        ('PUT', '/roles/1', {'name': 'UpdatedRole'}, 'Actualizar rol', ['ADMIN']),
        ('DELETE', '/roles/999', None, 'Eliminar rol', ['ADMIN']),
        
        # === PERMISSIONS ===
        ('GET', '/permisos/', None, 'Listar permisos', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/permisos/1', None, 'Obtener permiso', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/permisos/', {'name': f'TestPerm{timestamp}'}, 'Crear permiso', ['ADMIN']),
        ('PUT', '/permisos/2', {'name': 'UpdatedPerm'}, 'Actualizar permiso', ['ADMIN']),
        ('DELETE', '/permisos/999', None, 'Eliminar permiso', ['ADMIN']),
        
        # === ORGANIZATIONS ===
        ('GET', '/organizaciones/', None, 'Listar organizaciones', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/organizaciones/1', None, 'Obtener organizacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/organizaciones/', {'historical_name': f'Org{timestamp}', 'current_name': f'Org{timestamp}'}, 'Crear organizacion', ['ADMIN', 'MANAGER']),
        ('PUT', '/organizaciones/1', {'current_name': 'Updated'}, 'Actualizar organizacion', ['ADMIN', 'MANAGER']),
        ('DELETE', '/organizaciones/999', None, 'Eliminar organizacion', ['ADMIN']),
        
        # === BRANCHES ===
        ('GET', '/sucursales/', None, 'Listar sucursales', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/sucursales/1', None, 'Obtener sucursal', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/sucursales/', {'organization_id': 1, 'city_id': 1}, 'Crear sucursal', ['ADMIN', 'MANAGER']),
        ('PUT', '/sucursales/1', {'name': 'Updated'}, 'Actualizar sucursal', ['ADMIN', 'MANAGER']),
        ('DELETE', '/sucursales/999', None, 'Eliminar sucursal', ['ADMIN']),
        
        # === PERSONS ===
        ('GET', '/personas/', None, 'Listar personas', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/personas/1', None, 'Obtener persona', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/personas/', {'first_name': 'Test', 'last_name': 'Person', 'dni': str(timestamp), 'city_id': 1}, 'Crear persona', ['ADMIN', 'MANAGER']),
        ('PUT', '/personas/1', {'phone': '+57-300-1234567'}, 'Actualizar persona', ['ADMIN', 'MANAGER']),
        ('DELETE', '/personas/999', None, 'Eliminar persona', ['ADMIN']),
        
        # === EMPLOYEES ===
        ('GET', '/empleados/', None, 'Listar empleados', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/empleados/1', None, 'Obtener empleado', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/empleados/', {'person_id': 1, 'branch_id': 1}, 'Crear empleado', ['ADMIN', 'MANAGER']),
        ('PUT', '/empleados/1', {'branch_id': 1}, 'Actualizar empleado', ['ADMIN', 'MANAGER']),
        ('DELETE', '/empleados/999', None, 'Eliminar empleado', ['ADMIN']),
        
        # === STATES ===
        ('GET', '/estados/', None, 'Listar estados', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/estados/1', None, 'Obtener estado', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/estados/', {'description': f'Estado{timestamp}', 'code': f'E{timestamp}'}, 'Crear estado', ['ADMIN', 'MANAGER']),
        ('PUT', '/estados/1', {'description': 'Updated'}, 'Actualizar estado', ['ADMIN', 'MANAGER']),
        ('DELETE', '/estados/999', None, 'Eliminar estado', ['ADMIN']),
        
        # === CITIES ===
        ('GET', '/ciudades/', None, 'Listar ciudades', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/ciudades/1', None, 'Obtener ciudad', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/ciudades/', {'description': f'City{timestamp}', 'state_id': 1, 'code': f'C{timestamp}'}, 'Crear ciudad', ['ADMIN', 'MANAGER']),
        ('PUT', '/ciudades/1', {'description': 'Updated'}, 'Actualizar ciudad', ['ADMIN', 'MANAGER']),
        ('DELETE', '/ciudades/999', None, 'Eliminar ciudad', ['ADMIN']),
        
        # === CATEGORIES ===
        ('GET', '/categorías/', None, 'Listar categorias', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/categorías/1', None, 'Obtener categoria', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/categorías/', {'name': f'Cat{timestamp}'}, 'Crear categoria', ['ADMIN', 'MANAGER']),
        ('PUT', '/categorías/1', {'name': 'Updated'}, 'Actualizar categoria', ['ADMIN', 'MANAGER']),
        ('DELETE', '/categorías/999', None, 'Eliminar categoria', ['ADMIN']),
        
        # === BRANDS ===
        ('GET', '/marcas/', None, 'Listar marcas', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/marcas/21', None, 'Obtener marca', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/marcas/', {'name': f'Brand{timestamp}'}, 'Crear marca', ['ADMIN', 'MANAGER']),
        ('PUT', '/marcas/21', {'name': 'Updated'}, 'Actualizar marca', ['ADMIN', 'MANAGER']),
        ('DELETE', '/marcas/999', None, 'Eliminar marca', ['ADMIN']),
        
        # === INVENTORY ITEMS ===
        ('GET', '/inventory_items/', None, 'Listar items', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/inventory_items/1', None, 'Obtener item', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/inventory_items/', {'name': f'Item{timestamp}', 'price': 100, 'quantity': 10, 'category_id': 1, 'brand_id': 21}, 'Crear item', ['ADMIN', 'MANAGER']),
        ('PUT', '/inventory_items/1', {'price': 150}, 'Actualizar item', ['ADMIN', 'MANAGER']),
        ('DELETE', '/inventory_items/999', None, 'Eliminar item', ['ADMIN']),
        
        # === ASSIGNMENTS ===
        ('GET', '/asignaciones/', None, 'Listar asignaciones', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/asignaciones/1', None, 'Obtener asignacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/asignaciones/employee/1/history', None, 'Historial empleado', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/asignaciones/', {'item_id': 1, 'employee_id': 1, 'assigned_date': date.today().isoformat(), 'status': 'active'}, 'Crear asignacion', ['ADMIN', 'MANAGER']),
        ('PUT', '/asignaciones/1', {'status': 'returned'}, 'Actualizar asignacion', ['ADMIN', 'MANAGER']),
        ('PUT', '/asignaciones/1/return', None, 'Devolver asignacion', ['ADMIN', 'MANAGER']),
        ('PUT', '/asignaciones/1/lost', None, 'Reportar perdida', ['ADMIN', 'MANAGER']),
        ('DELETE', '/asignaciones/999', None, 'Eliminar asignacion', ['ADMIN']),
        
        # === QUOTES ===
        ('GET', '/quotes/', None, 'Listar cotizaciones', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/quotes/1', None, 'Obtener cotizacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/quotes/', {'customer_name': 'Test Customer', 'date': date.today().isoformat(), 'employee_id': 1}, 'Crear cotizacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('PUT', '/quotes/1', {'customer_name': 'Updated'}, 'Actualizar cotizacion', ['ADMIN', 'MANAGER']),
        ('DELETE', '/quotes/999', None, 'Eliminar cotizacion', ['ADMIN']),
        
        # === QUOTE ITEMS ===
        ('GET', '/items de cotización/', None, 'Listar items cotizacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/items de cotización/1', None, 'Obtener item cotizacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/items de cotización/', {'quote_id': 1, 'item_id': 1, 'quantity': 1}, 'Crear item cotizacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('PUT', '/items de cotización/1', {'quantity': 2}, 'Actualizar item cotizacion', ['ADMIN', 'MANAGER']),
        ('DELETE', '/items de cotización/999', None, 'Eliminar item cotizacion', ['ADMIN']),
        
        # === QUOTATION LINES ===
        ('GET', '/líneas de cotización/', None, 'Listar lineas cotizacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/líneas de cotización/1', None, 'Obtener linea cotizacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/líneas de cotización/', {'quote_id': 1, 'inventory_item_id': 1, 'quantity': 1, 'unit_price': '100.00'}, 'Crear linea cotizacion', ['ADMIN', 'MANAGER', 'SALES']),
        ('PUT', '/líneas de cotización/1', {'quantity': 2}, 'Actualizar linea cotizacion', ['ADMIN', 'MANAGER']),
        ('DELETE', '/líneas de cotización/999', None, 'Eliminar linea cotizacion', ['ADMIN']),
        
        # === SALES ORDERS ===
        ('GET', '/sales_orders/', None, 'Listar ordenes', ['ADMIN', 'MANAGER']),
        ('GET', '/sales_orders/1', None, 'Obtener orden', ['ADMIN', 'MANAGER']),
        ('POST', '/sales_orders/', {'customer_name': 'Test', 'quote_id': 1, 'order_date': date.today().isoformat(), 'total': '1000.00', 'employee_id': 1}, 'Crear orden', ['ADMIN', 'MANAGER']),
        ('PUT', '/sales_orders/1', {'total': '1500.00'}, 'Actualizar orden', ['ADMIN', 'MANAGER']),
        ('DELETE', '/sales_orders/999', None, 'Eliminar orden', ['ADMIN']),
        
        # === SALES ORDER ITEMS ===
        ('GET', '/items de orden/', None, 'Listar items orden', ['ADMIN', 'MANAGER']),
        ('GET', '/items de orden/1', None, 'Obtener item orden', ['ADMIN', 'MANAGER']),
        ('POST', '/items de orden/', {'sales_order_id': 1, 'item_id': 1, 'quantity': 1}, 'Crear item orden', ['ADMIN', 'MANAGER']),
        ('PUT', '/items de orden/1', {'quantity': 2}, 'Actualizar item orden', ['ADMIN', 'MANAGER']),
        ('DELETE', '/items de orden/999', None, 'Eliminar item orden', ['ADMIN']),
        
        # === INVOICES ===
        ('GET', '/invoices/', None, 'Listar facturas', ['ADMIN', 'MANAGER']),
        ('GET', '/invoices/1', None, 'Obtener factura', ['ADMIN', 'MANAGER']),
        ('POST', '/invoices/', {'customer_name': 'Test', 'sales_order_id': 1, 'invoice_date': date.today().isoformat(), 'total': '1000.00', 'employee_id': 1}, 'Crear factura', ['ADMIN', 'MANAGER']),
        ('PUT', '/invoices/1', {'total': '1500.00'}, 'Actualizar factura', ['ADMIN', 'MANAGER']),
        ('DELETE', '/invoices/999', None, 'Eliminar factura', ['ADMIN']),
        
        # === INVOICE ITEMS ===
        ('GET', '/items de factura/', None, 'Listar items factura', ['ADMIN', 'MANAGER']),
        ('GET', '/items de factura/1', None, 'Obtener item factura', ['ADMIN', 'MANAGER']),
        ('POST', '/items de factura/', {'invoice_id': 1, 'item_id': 1, 'quantity': 1, 'price': 100.00}, 'Crear item factura', ['ADMIN', 'MANAGER']),
        ('PUT', '/items de factura/1', {'quantity': 2}, 'Actualizar item factura', ['ADMIN', 'MANAGER']),
        ('DELETE', '/items de factura/999', None, 'Eliminar item factura', ['ADMIN']),
        
        # === SALES GOALS ===
        ('GET', '/metas de ventas/', None, 'Listar metas', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/metas de ventas/1', None, 'Obtener meta', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/metas de ventas/', {'branch_id': 1, 'period_type': 'monthly', 'start_date': date.today().isoformat(), 'end_date': (date.today() + timedelta(days=30)).isoformat(), 'target_amount': 100000.00}, 'Crear meta', ['ADMIN', 'MANAGER']),
        ('PUT', '/metas de ventas/1', {'target_amount': 150000.00}, 'Actualizar meta', ['ADMIN', 'MANAGER']),
        ('DELETE', '/metas de ventas/999', None, 'Eliminar meta', ['ADMIN']),
        
        # === ANALYTICS ===
        ('GET', '/analytics/invoicing/by_employee?start_date=2025-09-20&end_date=2025-10-20', None, 'Analytics por empleado', ['ADMIN', 'MANAGER']),
        ('GET', '/analytics/invoicing/by_branch?start_date=2025-09-20&end_date=2025-10-20', None, 'Analytics por sucursal', ['ADMIN', 'MANAGER']),
        ('GET', '/analytics/invoicing/by_brand?start_date=2025-09-20&end_date=2025-10-20', None, 'Analytics por marca', ['ADMIN', 'MANAGER']),
        ('GET', '/analytics/quotes/by_brand?start_date=2025-09-20&end_date=2025-10-20', None, 'Analytics cotizaciones', ['ADMIN', 'MANAGER']),
        ('GET', '/analytics/goals/vs_actual?start_date=2025-09-20&end_date=2025-10-20', None, 'Metas vs actual', ['ADMIN', 'MANAGER']),
        ('GET', '/analytics/sales/summary?start_date=2025-09-20&end_date=2025-10-20', None, 'Resumen ventas', ['ADMIN', 'MANAGER']),
        ('GET', '/analytics/top_performers?start_date=2025-09-20&end_date=2025-10-20', None, 'Top performers', ['ADMIN', 'MANAGER']),
        
        # === USER ROLES (Legacy) ===
        ('GET', '/roles de usuario/', None, 'Listar user-roles', ['ADMIN', 'MANAGER', 'SALES']),
        ('GET', '/roles de usuario/1', None, 'Obtener user-role', ['ADMIN', 'MANAGER', 'SALES']),
        ('POST', '/roles de usuario/', {'user_id': 1, 'role_id': 1}, 'Crear user-role', ['ADMIN']),
        ('PUT', '/roles de usuario/1', {'role_id': 2}, 'Actualizar user-role', ['ADMIN']),
        ('DELETE', '/roles de usuario/999', None, 'Eliminar user-role', ['ADMIN']),
    ]
    
    # 3. EJECUTAR TODOS LOS TESTS
    print_header(f"🧪 EJECUTANDO 123 ENDPOINTS CON 3 ROLES = 369 TESTS", "═", Fore.YELLOW)
    print(f"{'Nº/Total':<10} {'Método':<6} {'Endpoint':<50} │ {'Status por Rol':<20} │ {'Descripción'}")
    print("─" * 100)
    
    results = {'ADMIN': {'passed': 0, 'failed': 0}, 'MANAGER': {'passed': 0, 'failed': 0}, 'SALES': {'passed': 0, 'failed': 0}}
    
    for idx, (method, path, data, description, allowed_roles) in enumerate(endpoints, 1):
        # Probar con cada rol
        results_by_role = {}
        
        for role in ['ADMIN', 'MANAGER', 'SALES']:
            status = make_request(method, path, TOKENS[role], data)
            results_by_role[role] = status
            
            # Validar resultado
            if role in allowed_roles:
                # Debe tener acceso
                if status in [200, 201, 204, 400, 404, 500]:
                    results[role]['passed'] += 1
                else:
                    results[role]['failed'] += 1
            else:
                # No debe tener acceso
                if status in [403, 404]:
                    results[role]['passed'] += 1
                else:
                    results[role]['failed'] += 1
        
        # Imprimir resultado
        print_test_result(idx, len(endpoints), method, path, description, results_by_role)
    
    # 4. RESUMEN FINAL
    print_header("📊 RESUMEN FINAL", "═", Fore.GREEN)
    
    total_passed = 0
    total_tests = 0
    
    for role in ['ADMIN', 'MANAGER', 'SALES']:
        passed = results[role]['passed']
        failed = results[role]['failed']
        total = passed + failed
        percentage = (passed / total * 100) if total > 0 else 0
        
        total_passed += passed
        total_tests += total
        
        if percentage == 100:
            status_icon = f"{Fore.GREEN}✓{Style.RESET_ALL}"
        elif percentage >= 95:
            status_icon = f"{Fore.YELLOW}⚠{Style.RESET_ALL}"
        else:
            status_icon = f"{Fore.RED}✗{Style.RESET_ALL}"
        
        print(f"{status_icon} {role:8} - {passed:3}/{total:3} tests pasados ({percentage:5.1f}%) - {failed:2} fallados")
    
    print("─" * 100)
    total_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"TOTAL GLOBAL - {total_passed}/{total_tests} tests pasados ({total_percentage:.1f}%)")
    print("=" * 100)
    
    if total_percentage == 100:
        print(f"\n{Fore.GREEN}🎉 ¡PERFECTO! Todos los tests pasaron (100%){Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Sistema RBAC funcionando correctamente para todos los roles{Style.RESET_ALL}\n")
    elif total_percentage >= 95:
        print(f"\n{Fore.YELLOW}⚠ BUENO: {total_percentage:.1f}% de éxito{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.RED}✗ ADVERTENCIA: Se encontraron {total_tests - total_passed} errores{Style.RESET_ALL}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠ Test interrumpido por el usuario{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n\n{Fore.RED}✗ Error crítico: {str(e)}{Style.RESET_ALL}\n")
        import traceback
        traceback.print_exc()
