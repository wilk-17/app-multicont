"""
Script de Testing Automatizado - RBAC Implementation
Prueba todos los endpoints críticos con los 3 roles: SALES, MANAGER, ADMIN
"""

import requests
import json
from typing import Dict, List, Tuple
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:5000/api"
HEADERS = {"Content-Type": "application/json"}

# Usuarios de prueba
USERS = {
    'SALES': {'username': 'diego', 'password': 'diego123'},
    'MANAGER': {'username': 'bruno', 'password': 'bruno123'},
    'ADMIN': {'username': 'ana', 'password': 'ana123'}
}

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Imprime un encabezado formateado"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_section(text: str):
    """Imprime una sección"""
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'-'*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'-'*80}{Colors.END}")

def print_test_result(endpoint: str, method: str, expected: str, actual: int, passed: bool):
    """Imprime el resultado de un test"""
    status_icon = f"{Colors.GREEN}OK" if passed else f"{Colors.RED}FAIL"
    status_text = f"{Colors.GREEN}PASS" if passed else f"{Colors.RED}FAIL"
    
    print(f"{status_icon} {method:6} {endpoint:40} | Expected: {expected:15} | Got: {actual:3} | {status_text}{Colors.END}")

def login(role: str) -> Dict:
    """Login y obtiene el token para un rol específico"""
    user = USERS[role]
    response = requests.post(
        f"{BASE_URL}/auth/login",
        headers=HEADERS,
        json=user
    )
    
    if response.status_code == 200:
        response_data = response.json()
        print(f"DEBUG - Response for {role}: {response_data}")  # Debug
        # La respuesta está envuelta en 'data' por success_response
        data = response_data.get('data', response_data)  # Fallback a response_data si no hay 'data'
        return {
            'token': data.get('access_token'),
            'user': data.get('user')
        }
    else:
        raise Exception(f"Login failed for {role} - Status: {response.status_code} - Response: {response.text}")

def get_auth_headers(token: str) -> Dict:
    """Retorna headers con autenticación"""
    return {
        **HEADERS,
        "Authorization": f"Bearer {token}"
    }

def test_endpoint(method: str, endpoint: str, token: str, expected_status: int, 
                  data: Dict = None) -> Tuple[int, bool]:
    """
    Prueba un endpoint y retorna (status_code, passed)
    """
    url = f"{BASE_URL}{endpoint}"
    headers = get_auth_headers(token)
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return -1, False
        
        actual_status = response.status_code
        # Para endpoints que esperan 403 o 401, aceptamos cualquiera de los dos
        if expected_status in [403, 401]:
            passed = actual_status in [403, 401]
        else:
            passed = actual_status == expected_status
        
        return actual_status, passed
    except Exception as e:
        print(f"{Colors.RED}ERROR: {e}{Colors.END}")
        return -1, False

def run_tests():
    """Ejecuta todos los tests"""
    print_header("TESTING RBAC - MULTICONT API")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    
    # Login para cada rol
    print_section("AUTENTICACION")
    tokens = {}
    for role in ['SALES', 'MANAGER', 'ADMIN']:
        try:
            auth_data = login(role)
            tokens[role] = auth_data['token']
            user_info = auth_data['user']
            print(f"{Colors.GREEN}OK {role:8} - Login exitoso como {user_info['username']} (Role: {user_info['role']}){Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}FAIL {role:8} - Login fallido: {e}{Colors.END}")
            return
    
    # Definir tests por endpoint
    # Formato: (endpoint, method, SALES_expected, MANAGER_expected, ADMIN_expected, data_for_post_put)
    tests = [
        # INVENTORY ITEMS
        ("/inventory-items/", "GET", 200, 200, 200, None),
        ("/inventory-items/1", "GET", 200, 200, 200, None),
        ("/inventory-items/", "POST", 403, 201, 201, {
            "name": "Test Item",
            "sku": "TEST-SKU-001",
            "quantity": 10,
            "unit_price": 100.00,
            "category_id": 1
        }),
        ("/inventory-items/1", "PUT", 403, 200, 200, {
            "name": "Updated Item",
            "quantity": 20
        }),
        ("/inventory-items/999", "DELETE", 403, 403, 404, None),  # 999 no existe, pero ADMIN debería poder intentar
        
        # QUOTES
        ("/quotes/", "GET", 200, 200, 200, None),
        ("/quotes/1", "GET", 200, 200, 200, None),
        ("/quotes/", "POST", 201, 201, 201, {
            "customer_name": "Test Customer",
            "customer_email": "test@example.com",
            "total": 1000.00,
            "status": "pending"
        }),
        ("/quotes/1", "PUT", 403, 200, 200, {
            "status": "approved"
        }),
        ("/quotes/999", "DELETE", 403, 403, 404, None),
        
        # SALES ORDERS (ADMIN y MANAGER ONLY)
        ("/sales-orders/", "GET", 403, 200, 200, None),
        ("/sales-orders/1", "GET", 403, 200, 200, None),
        ("/sales-orders/", "POST", 403, 201, 201, {
            "quote_id": 1,
            "customer_name": "Test Customer",
            "total": 1500.00,
            "status": "pending"
        }),
        ("/sales-orders/1", "PUT", 403, 200, 200, {
            "status": "processing"
        }),
        ("/sales-orders/999", "DELETE", 403, 403, 404, None),
        
        # INVOICES (ADMIN y MANAGER ONLY)
        ("/invoices/", "GET", 403, 200, 200, None),
        ("/invoices/1", "GET", 403, 200, 200, None),
        ("/invoices/", "POST", 403, 201, 201, {
            "sales_order_id": 1,
            "invoice_number": "INV-TEST-001",
            "total": 1500.00,
            "status": "pending"
        }),
        ("/invoices/1", "PUT", 403, 200, 200, {
            "status": "paid"
        }),
        ("/invoices/999", "DELETE", 403, 403, 404, None),
        
        # USERS
        ("/users/", "GET", 200, 200, 200, None),
        ("/users/1", "GET", 200, 200, 200, None),
        ("/users/", "POST", 403, 201, 201, {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com",
            "role_id": 3
        }),
        ("/users/999", "DELETE", 403, 403, 404, None),
        
        # PERMISSIONS (SOLO ADMIN)
        ("/permissions/", "GET", 200, 200, 200, None),
        ("/permissions/1", "GET", 200, 200, 200, None),
        ("/permissions/", "POST", 403, 403, 201, {
            "name": "test:permission",
            "description": "Test permission"
        }),
        ("/permissions/1", "PUT", 403, 403, 200, {
            "description": "Updated description"
        }),
        ("/permissions/999", "DELETE", 403, 403, 404, None),
        
        # ORGANIZATIONS
        ("/organizations/", "GET", 200, 200, 200, None),
        ("/organizations/1", "GET", 200, 200, 200, None),
        ("/organizations/", "POST", 403, 201, 201, {
            "name": "Test Organization",
            "status": "active"
        }),
        ("/organizations/999", "DELETE", 403, 403, 404, None),
        
        # BRANCHES
        ("/branches/", "GET", 200, 200, 200, None),
        ("/branches/1", "GET", 200, 200, 200, None),
        ("/branches/", "POST", 403, 201, 201, {
            "name": "Test Branch",
            "organization_id": 1,
            "status": "active"
        }),
        
        # EMPLOYEES
        ("/employees/", "GET", 200, 200, 200, None),
        ("/employees/1", "GET", 200, 200, 200, None),
    ]
    
    # Ejecutar tests por rol
    results = {
        'SALES': {'passed': 0, 'failed': 0},
        'MANAGER': {'passed': 0, 'failed': 0},
        'ADMIN': {'passed': 0, 'failed': 0}
    }
    
    for role, expected_index in [('SALES', 2), ('MANAGER', 3), ('ADMIN', 4)]:
        print_section(f"TESTING ROLE: {role} ({USERS[role]['username']})")
        token = tokens[role]
        
        for test in tests:
            endpoint, method, sales_exp, manager_exp, admin_exp, data = test
            expected_statuses = [sales_exp, manager_exp, admin_exp]
            expected = expected_statuses[expected_index - 2]
            
            actual, passed = test_endpoint(method, endpoint, token, expected, data)
            
            # Formatear expected como texto
            expected_text = f"{expected}"
            if expected in [403, 401]:
                expected_text = f"{expected} (Forbidden)"
            elif expected == 200:
                expected_text = f"{expected} (OK)"
            elif expected == 201:
                expected_text = f"{expected} (Created)"
            elif expected == 404:
                expected_text = f"{expected} (Not Found)"
            
            print_test_result(endpoint, method, expected_text, actual, passed)
            
            if passed:
                results[role]['passed'] += 1
            else:
                results[role]['failed'] += 1
    
    # Resumen final
    print_header("RESUMEN DE RESULTADOS")
    
    total_tests = len(tests)
    total_passed = 0
    total_failed = 0
    
    for role in ['SALES', 'MANAGER', 'ADMIN']:
        passed = results[role]['passed']
        failed = results[role]['failed']
        total = passed + failed
        percentage = (passed / total * 100) if total > 0 else 0
        
        total_passed += passed
        total_failed += failed
        
        status_color = Colors.GREEN if percentage == 100 else Colors.YELLOW if percentage >= 80 else Colors.RED
        
        print(f"{status_color}{role:8} - {passed:2}/{total:2} tests passed ({percentage:6.2f}%){Colors.END}")
    
    print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
    total_percentage = (total_passed / (total_passed + total_failed) * 100) if (total_passed + total_failed) > 0 else 0
    overall_color = Colors.GREEN if total_percentage == 100 else Colors.YELLOW if total_percentage >= 80 else Colors.RED
    
    print(f"{overall_color}{Colors.BOLD}TOTAL: {total_passed}/{total_passed + total_failed} tests passed ({total_percentage:.2f}%){Colors.END}")
    
    if total_percentage == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}EXCELENTE! TODOS LOS TESTS PASARON! RBAC implementado correctamente.{Colors.END}")
    elif total_percentage >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}ADVERTENCIA: La mayoria de tests pasaron, pero hay algunos fallos.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}ERROR: Hay problemas significativos con la implementacion RBAC.{Colors.END}")
    
    print(f"{Colors.BOLD}{'='*80}{Colors.END}\n")

if __name__ == "__main__":
    try:
        run_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrumpido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error fatal: {e}{Colors.END}")
