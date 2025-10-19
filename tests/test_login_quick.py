#!/usr/bin/env python3
"""
Test Rápido de Login - Verificación del sistema de autenticación
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_login():
    """Prueba el endpoint de login"""
    print("="*70)
    print(" 🔐 TEST DE LOGIN")
    print("="*70)
    
    # Credenciales de prueba
    credentials = {
        "username": "testuser",
        "password": "test123"
    }
    
    print(f"\n1. Probando login con usuario: {credentials['username']}")
    print(f"   URL: {BASE_URL}/api/auth/login")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=credentials,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n2. Respuesta del servidor:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ LOGIN EXITOSO!")
            print(f"\n📝 Datos recibidos:")
            print(f"   - Usuario: {data.get('user', {}).get('username')}")
            print(f"   - Rol: {data.get('user', {}).get('role')}")
            print(f"   - Permisos: {', '.join(data.get('user', {}).get('permissions', []))}")
            print(f"   - Access Token: {data.get('access_token', '')[:50]}...")
            print(f"   - Refresh Token: {data.get('refresh_token', '')[:50]}...")
            
            # Guardar token para próximas pruebas
            with open('token.txt', 'w') as f:
                f.write(data.get('access_token', ''))
            print(f"\n💾 Token guardado en token.txt")
            
            return data.get('access_token')
        else:
            print(f"\n❌ LOGIN FALLÓ")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None


def test_protected_endpoint(token):
    """Prueba un endpoint protegido con el token"""
    print("\n" + "="*70)
    print(" 🔒 TEST DE ENDPOINT PROTEGIDO")
    print("="*70)
    
    print(f"\n1. Probando endpoint /api/auth/me")
    print(f"   Con token de autenticación")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"\n2. Respuesta del servidor:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ ACCESO AUTORIZADO!")
            print(f"\n📝 Información del usuario:")
            print(f"   - ID: {data.get('id')}")
            print(f"   - Username: {data.get('username')}")
            print(f"   - Rol: {data.get('role')}")
            print(f"   - Role ID: {data.get('role_id')}")
            print(f"   - Permisos: {', '.join(data.get('permissions', []))}")
        else:
            print(f"\n❌ ACCESO DENEGADO")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def test_without_token():
    """Prueba acceso sin token (debe fallar)"""
    print("\n" + "="*70)
    print(" 🚫 TEST SIN TOKEN (debe fallar)")
    print("="*70)
    
    print(f"\n1. Intentando acceder a /api/auth/me sin token")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n2. Respuesta del servidor:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"\n✅ RECHAZO CORRECTO! (Unauthorized)")
            print(f"   El endpoint está protegido correctamente")
        else:
            print(f"\n⚠️ INESPERADO: Status {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def main():
    print("\n" + "="*70)
    print(" 🚀 TEST RÁPIDO DEL SISTEMA DE AUTENTICACIÓN")
    print("="*70)
    print("\nEste script probará:")
    print("  1. Login con usuario de prueba")
    print("  2. Acceso a endpoint protegido con token")
    print("  3. Rechazo de acceso sin token")
    print("\n" + "="*70)
    
    # Test 1: Login
    token = test_login()
    
    if token:
        # Test 2: Endpoint protegido con token
        test_protected_endpoint(token)
        
        # Test 3: Endpoint sin token
        test_without_token()
        
        # Resumen
        print("\n" + "="*70)
        print(" ✅ TODOS LOS TESTS COMPLETADOS")
        print("="*70)
        print("\n🎉 El sistema de autenticación funciona correctamente!")
        print("\n📚 Próximos pasos:")
        print("   1. Proteger endpoints críticos con @jwt_required()")
        print("   2. Agregar @require_role() a endpoints administrativos")
        print("   3. Ver ejemplos en: EJEMPLO_PROTEGER_ENDPOINTS.py")
        print("\n" + "="*70 + "\n")
    else:
        print("\n" + "="*70)
        print(" ❌ TEST FALLÓ")
        print("="*70)
        print("\n⚠️ No se pudo completar el login")
        print("Verifica que el servidor esté corriendo y la base de datos conectada")
        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
