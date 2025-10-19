"""
Script para probar el sistema de autenticación JWT
Requiere que el servidor Flask esté corriendo

Ejecutar: python test_auth_system.py
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"


def print_header(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_response(response):
    """Imprime respuesta formateada"""
    print(f"  Status: {response.status_code}")
    try:
        data = response.json()
        print(f"  Response:\n{json.dumps(data, indent=4, ensure_ascii=False)}")
    except:
        print(f"  Response: {response.text}")


def test_login(username, password):
    """Prueba el endpoint de login"""
    print_header(f"TEST 1: Login con usuario '{username}'")
    
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=payload)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('access_token'), data.get('refresh_token')
        
        return None, None
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None, None


def test_get_current_user(access_token):
    """Prueba el endpoint /me"""
    print_header("TEST 2: Obtener información del usuario actual")
    
    url = f"{BASE_URL}/auth/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print_response(response)
        return response.status_code == 200
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_validate_token(access_token):
    """Prueba el endpoint de validación de token"""
    print_header("TEST 3: Validar token")
    
    url = f"{BASE_URL}/auth/validate"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print_response(response)
        return response.status_code == 200
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_refresh_token(refresh_token):
    """Prueba el endpoint de refresh token"""
    print_header("TEST 4: Renovar access token")
    
    url = f"{BASE_URL}/auth/refresh"
    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    
    try:
        response = requests.post(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('access_token')
        
        return None
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def test_protected_endpoint(access_token):
    """Prueba acceso a un endpoint protegido (por ejemplo, users)"""
    print_header("TEST 5: Acceso a endpoint protegido (/api/users/)")
    
    url = f"{BASE_URL}/users/"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print_response(response)
        return response.status_code == 200
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_without_token():
    """Prueba acceso sin token (debe fallar)"""
    print_header("TEST 6: Acceso sin token (debe fallar)")
    
    url = f"{BASE_URL}/users/"
    
    try:
        response = requests.get(url)
        print_response(response)
        # Esperamos un 401 o similar
        if response.status_code in [401, 403]:
            print("\n  ✅ Correcto: Acceso denegado sin token")
            return True
        else:
            print(f"\n  ⚠️  Inesperado: Status {response.status_code} (esperado 401)")
            return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_invalid_credentials():
    """Prueba login con credenciales incorrectas"""
    print_header("TEST 7: Login con credenciales incorrectas")
    
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": "usuario_inexistente",
        "password": "password_incorrecta"
    }
    
    try:
        response = requests.post(url, json=payload)
        print_response(response)
        
        if response.status_code == 401:
            print("\n  ✅ Correcto: Login rechazado con credenciales incorrectas")
            return True
        else:
            print(f"\n  ⚠️  Inesperado: Status {response.status_code} (esperado 401)")
            return False
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_logout(access_token):
    """Prueba el endpoint de logout"""
    print_header("TEST 8: Logout")
    
    url = f"{BASE_URL}/auth/logout"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.post(url, headers=headers)
        print_response(response)
        return response.status_code == 200
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def run_complete_flow():
    """Ejecuta el flujo completo de pruebas"""
    print("\n" + "=" * 70)
    print(" PRUEBA COMPLETA DEL SISTEMA DE AUTENTICACIÓN JWT")
    print("=" * 70)
    print(f"\n  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Base URL: {BASE_URL}")
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get("http://127.0.0.1:5000/")
        print(f"\n  ✅ Servidor conectado")
    except:
        print(f"\n  ❌ ERROR: No se puede conectar al servidor")
        print(f"     Asegúrate de que el servidor esté corriendo en http://127.0.0.1:5000")
        return
    
    # Usuario para testing (ajustar según tu BD)
    # Opciones: ana/ana123, test/test123, etc.
    username = input("\n  Username [ana]: ").strip() or "ana"
    password = input(f"  Password [ana123]: ").strip() or "ana123"
    
    print("\n  🚀 Iniciando pruebas...\n")
    
    results = {}
    
    # Test 1: Login
    access_token, refresh_token = test_login(username, password)
    results['login'] = access_token is not None
    
    if not access_token:
        print("\n❌ ERROR: No se pudo obtener access token. Deteniendo pruebas.")
        return
    
    # Test 2: Get current user
    results['get_user'] = test_get_current_user(access_token)
    
    # Test 3: Validate token
    results['validate'] = test_validate_token(access_token)
    
    # Test 4: Refresh token
    new_access_token = test_refresh_token(refresh_token)
    results['refresh'] = new_access_token is not None
    
    # Usar el nuevo token si está disponible
    if new_access_token:
        access_token = new_access_token
    
    # Test 5: Protected endpoint
    results['protected'] = test_protected_endpoint(access_token)
    
    # Test 6: Sin token
    results['no_token'] = test_without_token()
    
    # Test 7: Credenciales incorrectas
    results['invalid_creds'] = test_invalid_credentials()
    
    # Test 8: Logout
    results['logout'] = test_logout(access_token)
    
    # Resumen
    print("\n" + "=" * 70)
    print(" RESUMEN DE PRUEBAS")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, passed_test in results.items():
        icon = "✅" if passed_test else "❌"
        print(f"  {icon} {test_name.replace('_', ' ').title()}")
    
    print("\n" + "=" * 70)
    print(f" RESULTADO: {passed}/{total} pruebas exitosas ({passed*100//total}%)")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema de autenticación funciona correctamente.\n")
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron. Revisa los detalles arriba.\n")


def main():
    """Función principal con menú"""
    import sys
    
    print("\n" + "=" * 70)
    print(" TEST DE AUTENTICACIÓN JWT")
    print("=" * 70)
    print("\n⚠️  IMPORTANTE: El servidor debe estar corriendo en http://127.0.0.1:5000")
    print("   Ejecuta: python run.py (en otra terminal)\n")
    
    print("Opciones:")
    print("  1. Ejecutar flujo completo de pruebas")
    print("  2. Solo probar login")
    print("  0. Salir")
    
    try:
        choice = input("\nElige una opción [1-2, 0]: ").strip()
        
        if choice == '1':
            run_complete_flow()
        elif choice == '2':
            username = input("\n  Username: ").strip()
            password = input("  Password: ").strip()
            test_login(username, password)
        elif choice == '0':
            print("\n👋 Saliendo...")
            sys.exit(0)
        else:
            print("\n❌ Opción inválida")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
        sys.exit(1)


if __name__ == "__main__":
    main()
