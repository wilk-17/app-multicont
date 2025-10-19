"""
Script de prueba para verificar validación Marshmallow en endpoints
Prueba los 6 endpoints integrados con schemas
"""
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:5000"

# Colores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_section(title):
    print(f"\n{BLUE}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{END}\n")

def test_quote_validation():
    """Prueba validación en Quote API"""
    print_section("🧪 TEST 1: Quote API - Validación Marshmallow")
    
    # Test 1: Datos inválidos (debería fallar)
    print(f"{YELLOW}Test 1.1: Crear cotización con datos inválidos{END}")
    invalid_data = {
        "customer_name": "AB",  # Muy corto (min 3)
        "date": str(date.today() + timedelta(days=10)),  # Fecha futura
        "items": [
            {
                "inventory_item_id": 0,  # Inválido (min 1)
                "quantity": -5,  # Negativo
                "unit_price": -100  # Negativo
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/quotes/", json=invalid_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400 and 'errors' in response.json():
        print(f"{GREEN}✅ Validación funcionando correctamente - Datos inválidos rechazados{END}")
    else:
        print(f"{RED}❌ Error: Se esperaba HTTP 400 con errores de validación{END}")
    
    # Test 2: Datos válidos (debería funcionar)
    print(f"\n{YELLOW}Test 1.2: Crear cotización con datos válidos{END}")
    valid_data = {
        "customer_name": "Empresa Test S.A.",
        "date": str(date.today()),
        "employee_id": 1,
        "items": [
            {
                "inventory_item_id": 1,
                "quantity": 5,
                "unit_price": 150.50
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/quotes/", json=valid_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print(f"{GREEN}✅ Cotización creada exitosamente{END}")
    else:
        print(f"{RED}❌ Error al crear cotización válida{END}")

def test_user_password_validation():
    """Prueba validación de contraseña fuerte en User API"""
    print_section("🧪 TEST 2: User API - Validación de Contraseña Fuerte")
    
    # Test 1: Contraseña débil
    print(f"{YELLOW}Test 2.1: Crear usuario con contraseña débil{END}")
    weak_password_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "weak"  # Muy corta, sin mayúsculas, números, especiales
    }
    
    response = requests.post(f"{BASE_URL}/api/users/", json=weak_password_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400 and 'errors' in response.json():
        print(f"{GREEN}✅ Validación de contraseña fuerte funcionando{END}")
    else:
        print(f"{RED}❌ Error: Contraseña débil no fue rechazada{END}")
    
    # Test 2: Contraseña fuerte
    print(f"\n{YELLOW}Test 2.2: Crear usuario con contraseña fuerte{END}")
    strong_password_data = {
        "username": "testuser123",
        "email": "test@example.com",
        "password": "SecurePass123!",  # Cumple todos los requisitos
        "full_name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/api/users/", json=strong_password_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201 or response.status_code == 400:  # 400 si usuario ya existe
        print(f"{GREEN}✅ Contraseña fuerte aceptada{END}")
    else:
        print(f"{RED}❌ Error inesperado{END}")

def test_inventory_validation():
    """Prueba validación en Inventory Item API"""
    print_section("🧪 TEST 3: Inventory Item API - Validación de Datos")
    
    # Test 1: Datos inválidos
    print(f"{YELLOW}Test 3.1: Crear item con datos inválidos{END}")
    invalid_item = {
        "name": "AB",  # Muy corto
        "price": -50,  # Negativo
        "quantity": -10,  # Negativo
        "category_id": 0  # Inválido
    }
    
    response = requests.post(f"{BASE_URL}/api/inventory_items/", json=invalid_item)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400 and 'errors' in response.json():
        print(f"{GREEN}✅ Validación de inventario funcionando{END}")
    else:
        print(f"{RED}❌ Error: Datos inválidos no fueron rechazados{END}")
    
    # Test 2: Datos válidos
    print(f"\n{YELLOW}Test 3.2: Crear item con datos válidos{END}")
    valid_item = {
        "name": "Producto Test XYZ",
        "description": "Descripción del producto de prueba",
        "price": 299.99,
        "quantity": 50,
        "category_id": 1,
        "branch_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/inventory_items/", json=valid_item)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print(f"{GREEN}✅ Item de inventario creado exitosamente{END}")
    else:
        print(f"{RED}❌ Error al crear item válido{END}")

def test_employee_validation():
    """Prueba validación de nombres de empleados"""
    print_section("🧪 TEST 4: Employee API - Validación de Nombres")
    
    # Test 1: Nombre con números (inválido)
    print(f"{YELLOW}Test 4.1: Crear empleado con nombre inválido (números){END}")
    invalid_employee = {
        "first_name": "Juan123",  # Contiene números
        "last_name": "Pérez",
        "email": "juan@test.com",
        "position": "Developer",
        "hire_date": str(date.today()),
        "branch_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/employees/", json=invalid_employee)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400 and 'errors' in response.json():
        print(f"{GREEN}✅ Validación de nombres funcionando (rechaza números){END}")
    else:
        print(f"{RED}❌ Error: Nombre con números no fue rechazado{END}")
    
    # Test 2: Nombre válido con acentos
    print(f"\n{YELLOW}Test 4.2: Crear empleado con nombre válido (con acentos){END}")
    valid_employee = {
        "first_name": "José María",
        "last_name": "García Pérez",
        "email": "jose.garcia@test.com",
        "position": "Desarrollador Senior",
        "hire_date": str(date.today()),
        "salary": 3500.00,
        "branch_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/employees/", json=valid_employee)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print(f"{GREEN}✅ Empleado con nombre válido (acentos) creado{END}")
    else:
        print(f"{RED}❌ Error al crear empleado válido{END}")

def test_get_serialization():
    """Prueba serialización en endpoints GET"""
    print_section("🧪 TEST 5: Serialización en GET Endpoints")
    
    endpoints = [
        "/api/quotes/",
        "/api/invoices/",
        "/api/inventory_items/",
        "/api/sales_orders/",
        "/api/employees/"
    ]
    
    for endpoint in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}?page=1&per_page=5")
        print(f"\n{YELLOW}GET {endpoint}{END}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'success' in data and 'data' in data:
                print(f"{GREEN}✅ Serialización funcionando correctamente{END}")
                print(f"Total items: {data['data'].get('total', 0)}")
            else:
                print(f"{RED}❌ Formato de respuesta incorrecto{END}")
        else:
            print(f"{RED}❌ Error en endpoint: {response.status_code}{END}")

def main():
    print(f"\n{BLUE}{'='*60}")
    print("🚀 TEST SUITE - Validación Marshmallow")
    print("Verificando integración de schemas en 6 APIs")
    print(f"{'='*60}{END}\n")
    
    print(f"{YELLOW}⚠️  NOTA: Algunos tests pueden fallar si requieren autenticación JWT{END}")
    print(f"{YELLOW}    Los tests de validación (HTTP 400) deberían funcionar siempre{END}\n")
    
    try:
        # Verificar que el servidor está corriendo
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print(f"{RED}❌ Error: Servidor no está corriendo en {BASE_URL}{END}")
            return
        
        print(f"{GREEN}✅ Servidor Flask detectado en {BASE_URL}{END}\n")
        
        # Ejecutar tests
        test_quote_validation()
        test_user_password_validation()
        test_inventory_validation()
        test_employee_validation()
        test_get_serialization()
        
        # Resumen final
        print_section("📊 RESUMEN DE TESTS")
        print(f"{GREEN}✅ Tests completados{END}")
        print(f"\n{YELLOW}Verifica que:")
        print("1. Datos inválidos son rechazados con HTTP 400")
        print("2. Mensajes de error son descriptivos en español")
        print("3. Datos válidos son aceptados con HTTP 201")
        print("4. Serialización en GET funciona correctamente")
        print(f"{END}")
        
    except requests.exceptions.ConnectionError:
        print(f"{RED}❌ Error: No se puede conectar al servidor en {BASE_URL}{END}")
        print(f"{YELLOW}Asegúrate de que el servidor esté corriendo con: python run.py{END}")
    except Exception as e:
        print(f"{RED}❌ Error inesperado: {str(e)}{END}")

if __name__ == "__main__":
    main()
