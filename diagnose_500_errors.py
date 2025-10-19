"""
Script de diagnóstico - Ver errores 500 específicos
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

# Login como ADMIN
print("Login como ADMIN...")
response = requests.post(
    f"{BASE_URL}/auth/login",
    headers={"Content-Type": "application/json"},
    json={"username": "ana", "password": "ana123"}
)

if response.status_code != 200:
    print(f"Error en login: {response.status_code}")
    print(response.text)
    exit(1)

token = response.json()['data']['access_token']
print(f"Token obtenido: {token[:50]}...")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Probar endpoints que dan 500
endpoints_to_test = [
    "/inventory_items/",
    "/sales_orders/",
    "/invoices/",
    "/users/",
    "/permisos/",
    "/organizaciones/",
    "/sucursales/",
    "/empleados/"
]

print("\n" + "="*80)
print("PROBANDO ENDPOINTS QUE DAN 500")
print("="*80 + "\n")

for endpoint in endpoints_to_test:
    print(f"Testing: GET {endpoint}")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 500:
            print(f"  ERROR 500!")
            print(f"  Response: {response.text[:500]}")
        elif response.status_code == 200:
            data = response.json()
            print(f"  OK - Success: {data.get('success', 'N/A')}")
        else:
            print(f"  Response: {response.text[:200]}")
    except Exception as e:
        print(f"  EXCEPTION: {e}")
    print()
