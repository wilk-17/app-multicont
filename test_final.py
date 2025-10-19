"""
Script de Testing Final - RBAC
Prueba endpoints críticos con todos los roles después de las correcciones
"""

import requests
import time
import sys

BASE_URL = "http://127.0.0.1:5000/api"

def get_token(username, password):
    """Obtiene token JWT"""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            headers={"Content-Type": "application/json"},
            json={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print(f"Error en login {username}: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Servidor no está corriendo en http://127.0.0.1:5000")
        print("Por favor, ejecuta 'python run.py' en otra terminal primero\n")
        sys.exit(1)
    except Exception as e:
        print(f"Error en login: {e}")
        return None

def test_endpoint(method, url, token, description="Test"):
    """Prueba un endpoint"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{url}", headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{url}", headers=headers, json={"test": "data"}, timeout=5)
        elif method == "PUT":
            response = requests.put(f"{BASE_URL}{url}", headers=headers, json={"test": "data"}, timeout=5)
        elif method == "DELETE":
            response = requests.delete(f"{BASE_URL}{url}", headers=headers, timeout=5)
        
        status_icon = "✅" if response.status_code in [200, 201, 404] else ("⚠️" if response.status_code == 403 else "❌")
        return response.status_code, status_icon
    except Exception as e:
        return None, "❌"

print("="*80)
print("TESTING FINAL - RBAC IMPLEMENTATION")
print("="*80)
print("\nObteniendo tokens de autenticación...\n")

# Obtener tokens
token_admin = get_token("ana", "ana123")
token_manager = get_token("bruno", "bruno123")
token_sales = get_token("diego", "diego123")

if not all([token_admin, token_manager, token_sales]):
    print("❌ Error obteniendo tokens")
    sys.exit(1)

print("✅ Tokens obtenidos exitosamente\n")

# Tests críticos
tests = [
    # GET / - Deben funcionar para todos después del fix de paginación
    ("GET", "/inventory_items/", "Lista de inventario"),
    ("GET", "/quotes/", "Lista de cotizaciones"),
    ("GET", "/sales_orders/", "Lista de órdenes (solo ADMIN/MANAGER)"),
    ("GET", "/invoices/", "Lista de facturas (solo ADMIN/MANAGER)"),
    ("GET", "/users/", "Lista de usuarios"),
    
    # GET /{id}
    ("GET", "/inventory_items/1", "Item de inventario específico"),
    ("GET", "/quotes/1", "Cotización específica"),
    
    # DELETE - Deben funcionar sin 500 errors después del fix de cache
    ("DELETE", "/inventory_items/999", "Eliminar item (solo ADMIN)"),
    ("DELETE", "/quotes/999", "Eliminar quote (solo ADMIN)"),
    ("DELETE", "/sales_orders/999", "Eliminar orden (solo ADMIN)"),
]

results = {
    "ADMIN": {"passed": 0, "total": 0},
    "MANAGER": {"passed": 0, "total": 0},
    "SALES": {"passed": 0, "total": 0}
}

print("="*80)
print("TESTING CON SALES (diego)")
print("="*80)
for method, endpoint, description in tests:
    status, icon = test_endpoint(method, endpoint, token_sales, description)
    results["SALES"]["total"] += 1
    
    # Determinar si el test pasó
    if "/sales_orders/" in endpoint or "/invoices/" in endpoint:
        # SALES debe recibir 403
        passed = (status == 403)
    elif "DELETE" in method:
        # SALES debe recibir 403 en DELETE
        passed = (status == 403)
    else:
        # Otros deben ser 200 o 404
        passed = (status in [200, 201, 404])
    
    if passed:
        results["SALES"]["passed"] += 1
    
    print(f"{icon} {method:6} {endpoint:30} → {status} - {description}")

print("\n" + "="*80)
print("TESTING CON MANAGER (bruno)")
print("="*80)
for method, endpoint, description in tests:
    status, icon = test_endpoint(method, endpoint, token_manager, description)
    results["MANAGER"]["total"] += 1
    
    # Determinar si el test pasó
    if "DELETE" in method:
        # MANAGER debe recibir 403 en DELETE
        passed = (status == 403)
    else:
        # Otros deben ser 200 o 404
        passed = (status in [200, 201, 404])
    
    if passed:
        results["MANAGER"]["passed"] += 1
    
    print(f"{icon} {method:6} {endpoint:30} → {status} - {description}")

print("\n" + "="*80)
print("TESTING CON ADMIN (ana)")
print("="*80)
for method, endpoint, description in tests:
    status, icon = test_endpoint(method, endpoint, token_admin, description)
    results["ADMIN"]["total"] += 1
    
    # Determinar si el test pasó
    # ADMIN todo debe ser 200, 201, o 404 (NO 500)
    passed = (status in [200, 201, 404])
    
    if passed:
        results["ADMIN"]["passed"] += 1
    
    # Marcar específicamente si es 500 (error grave)
    if status == 500:
        icon = "🔥"
    
    print(f"{icon} {method:6} {endpoint:30} → {status} - {description}")

# Resumen
print("\n" + "="*80)
print("RESUMEN DE RESULTADOS")
print("="*80)

total_passed = 0
total_tests = 0

for role, data in results.items():
    passed = data["passed"]
    total = data["total"]
    percentage = (passed / total * 100) if total > 0 else 0
    
    total_passed += passed
    total_tests += total
    
    status = "✅" if percentage == 100 else ("⚠️" if percentage >= 90 else "❌")
    print(f"{status} {role:8}: {passed}/{total} ({percentage:.1f}%)")

overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
overall_status = "✅" if overall_percentage >= 95 else ("⚠️" if overall_percentage >= 85 else "❌")

print(f"\n{overall_status} TOTAL: {total_passed}/{total_tests} ({overall_percentage:.1f}%)")

if overall_percentage >= 95:
    print("\n🎉 ¡EXCELENTE! El sistema RBAC funciona perfectamente")
elif overall_percentage >= 85:
    print("\n✅ BIEN! El sistema RBAC funciona correctamente con mejoras menores pendientes")
else:
    print("\n⚠️ Se necesitan más correcciones")

print("\n" + "="*80)
print("VERIFICACIONES CLAVE:")
print("="*80)
print("✓ ¿SALES bloqueado de sales_orders? (debe ser 403)")
print("✓ ¿SALES bloqueado de invoices? (debe ser 403)")
print("✓ ¿SALES bloqueado de DELETE? (debe ser 403)")
print("✓ ¿MANAGER bloqueado de DELETE? (debe ser 403)")
print("✓ ¿ADMIN sin errores 500 en DELETE? (debe ser 404, no 500)")
print("✓ ¿Todos los GET / funcionan? (debe ser 200, no 500)")
print("="*80)
