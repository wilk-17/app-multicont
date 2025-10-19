"""
Script para diagnosticar errores 500 en DELETE
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

token = response.json()['data']['access_token']
print(f"Token obtenido: {token[:50]}...")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Probar DELETE en ID=1 (probablemente existe y tiene relaciones)
# Luego probar en ID alto (probablemente no existe)
endpoints_to_test = [
    ("/inventory_items/999", "DELETE"),
    ("/quotes/999", "DELETE"),
    ("/sales_orders/999", "DELETE"),
    ("/invoices/999", "DELETE"),
    ("/users/999", "DELETE"),
    ("/permisos/999", "DELETE"),
    ("/organizaciones/999", "DELETE"),
    ("/sucursales/999", "DELETE"),
]

print("\n" + "="*80)
print("PROBANDO DELETE EN IDs QUE NO EXISTEN (999)")
print("="*80 + "\n")

for endpoint, method in endpoints_to_test:
    print(f"Testing: {method} {endpoint}")
    try:
        response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 500:
            print(f"  ERROR 500!")
            try:
                error_data = response.json()
                print(f"  Error: {error_data.get('error', 'Unknown')}")
            except:
                print(f"  Response text: {response.text[:300]}")
        elif response.status_code == 404:
            print(f"  OK - 404 Not Found (esperado)")
        elif response.status_code == 200:
            print(f"  OK - 200 Deleted")
        else:
            print(f"  Response: {response.text[:200]}")
    except Exception as e:
        print(f"  EXCEPTION: {e}")
    print()

# Ahora probar PUT sin datos
print("\n" + "="*80)
print("PROBANDO PUT SIN DATOS VÁLIDOS")
print("="*80 + "\n")

put_tests = [
    ("/inventory_items/1", "PUT"),
    ("/quotes/1", "PUT"),
    ("/permisos/1", "PUT"),
]

for endpoint, method in put_tests:
    print(f"Testing: {method} {endpoint}")
    try:
        response = requests.put(f"{BASE_URL}{endpoint}", headers=headers, json={})
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 500:
            print(f"  ERROR 500!")
            try:
                error_data = response.json()
                print(f"  Error: {error_data.get('error', 'Unknown')}")
            except:
                print(f"  Response text: {response.text[:300]}")
        elif response.status_code == 400:
            print(f"  OK - 400 Bad Request (esperado sin datos válidos)")
        elif response.status_code == 200:
            print(f"  OK - 200 Updated")
        else:
            print(f"  Response: {response.text[:200]}")
    except Exception as e:
        print(f"  EXCEPTION: {e}")
    print()
