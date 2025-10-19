# Sistema de Autenticación JWT - multiCont

## 📋 Resumen

Sistema completo de autenticación basado en **JWT (JSON Web Tokens)** con hash de contraseñas usando **bcrypt**.

### ✅ Características Implementadas

- ✅ **Login/Logout** con JWT
- ✅ **Hash de contraseñas** con bcrypt (salt único por contraseña)
- ✅ **Access Token** (24 horas de validez)
- ✅ **Refresh Token** (30 días de validez)
- ✅ **Decoradores de autorización** (@require_role, @require_permission)
- ✅ **Manejo de roles** (ADMIN, MANAGER, SALES)
- ✅ **Manejo de permisos** (READ_REPORTS, WRITE_QUOTES, etc.)
- ✅ **Endpoints protegidos** con JWT

---

## 🔐 Endpoints de Autenticación

### 1. POST `/api/auth/login`
**Login y obtención de tokens**

**Request:**
```json
{
  "username": "ana",
  "password": "ana123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Bienvenido, ana!",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "1",
    "username": "ana",
    "role": "SALES",
    "role_id": "3"
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Usuario o contraseña incorrectos"
}
```

---

### 2. POST `/api/auth/refresh`
**Renovar access token usando refresh token**

**Headers:**
```
Authorization: Bearer {refresh_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 3. GET `/api/auth/me`
**Obtener información del usuario autenticado**

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "user": {
    "id": "1",
    "username": "ana",
    "role_id": "3",
    "role": "SALES",
    "permissions": ["READ_REPORTS", "WRITE_QUOTES"]
  }
}
```

---

### 4. GET `/api/auth/validate`
**Validar si el token es válido**

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "valid": true,
  "user_id": "1",
  "role": "SALES",
  "permissions": ["READ_REPORTS", "WRITE_QUOTES"]
}
```

---

### 5. POST `/api/auth/logout`
**Cerrar sesión (cliente elimina token)**

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Sesión cerrada exitosamente"
}
```

---

## 🛡️ Protección de Endpoints

### Opción 1: Solo requiere estar autenticado
```python
from flask_jwt_extended import jwt_required

@app.route('/protected')
@jwt_required()
def protected_route():
    return {'message': 'Acceso permitido'}
```

### Opción 2: Requiere rol específico
```python
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_role

@app.route('/admin-only')
@jwt_required()
@require_role('ADMIN')
def admin_route():
    return {'message': 'Solo admins'}

@app.route('/admin-or-manager')
@jwt_required()
@require_role('ADMIN', 'MANAGER')
def manager_route():
    return {'message': 'Admins o Managers'}
```

### Opción 3: Requiere permisos específicos
```python
from flask_jwt_extended import jwt_required
from app.utils.decorators import require_permission

@app.route('/write-quotes')
@jwt_required()
@require_permission('WRITE_QUOTES')
def write_quote():
    return {'message': 'Permiso para escribir cotizaciones'}
```

### Opción 4: Obtener usuario actual
```python
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.entities.user import User

@app.route('/my-profile')
@jwt_required()
def my_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user.to_dict()
```

---

## 🔑 Sistema de Roles y Permisos

### Roles Disponibles

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **ADMIN** | Administrador | ADMIN_ALL, READ_REPORTS, WRITE_QUOTES, APPROVE_ORDERS |
| **MANAGER** | Gerente | READ_REPORTS, WRITE_QUOTES, APPROVE_ORDERS |
| **SALES** | Vendedor | READ_REPORTS, WRITE_QUOTES |

### Permisos Disponibles

- `ADMIN_ALL` - Acceso total al sistema
- `READ_REPORTS` - Leer reportes y analytics
- `WRITE_QUOTES` - Crear y editar cotizaciones
- `APPROVE_ORDERS` - Aprobar órdenes de venta

---

## 🔧 Configuración

### Archivo: `app/utils/security.py`

```python
# Configuración de JWT
JWT_SECRET_KEY = "tu-clave-secreta-muy-segura-cambiar-en-produccion"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # 24 horas
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 30 días
```

⚠️ **IMPORTANTE**: En producción, mover `JWT_SECRET_KEY` a variables de entorno (archivo `.env`)

```bash
# .env
JWT_SECRET_KEY=clave-super-secreta-generada-aleatoriamente
```

---

## 📦 Instalación

### 1. Instalar dependencias
```bash
pip install flask-jwt-extended passlib[bcrypt]
```

### 2. Hashear contraseñas existentes
```bash
python hash_existing_passwords.py
```

Opciones:
1. Hashear contraseñas existentes
2. Crear usuario de prueba (test/test123)
3. Verificar sistema de hash
4. Hacer todo

### 3. Reiniciar el servidor
```bash
python run.py
```

---

## 🧪 Testing

### Opción 1: Script automatizado
```bash
python test_auth_system.py
```

Ejecuta 8 pruebas completas:
1. Login
2. Get current user
3. Validate token
4. Refresh token
5. Protected endpoint
6. Sin token (debe fallar)
7. Credenciales incorrectas (debe fallar)
8. Logout

### Opción 2: Swagger UI
1. Ir a http://127.0.0.1:5000/api/docs/
2. Probar endpoint `/api/auth/login`
3. Copiar el `access_token` de la respuesta
4. Hacer clic en el botón **Authorize** (arriba a la derecha)
5. Ingresar: `Bearer {tu_access_token}`
6. Ahora puedes probar todos los endpoints protegidos

### Opción 3: cURL
```bash
# Login
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"ana","password":"ana123"}'

# Usar token en otro endpoint
curl -X GET http://127.0.0.1:5000/api/auth/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Opción 4: Postman
1. Importar colección (crear archivo `multiCont_Auth.postman_collection.json`)
2. Login → Guardar token en variable de entorno
3. Usar `{{access_token}}` en otros requests

---

## 🔐 Hash de Contraseñas

### ¿Cómo funciona?

El sistema usa **bcrypt** con las siguientes características:

1. **Salt único**: Cada contraseña tiene un salt diferente (incluido en el hash)
2. **Costo computacional**: 12 rondas (balance entre seguridad y performance)
3. **Longitud del hash**: ~60 caracteres
4. **Formato**: `$2b$12$salt...hash...`

### Ejemplo
```python
from app.utils.security import hash_password, verify_password

# Hashear contraseña
password = "mi_password_123"
hashed = hash_password(password)
# $2b$12$abc123def456...

# Verificar contraseña
is_valid = verify_password("mi_password_123", hashed)  # True
is_invalid = verify_password("password_incorrecta", hashed)  # False
```

### Ventajas de bcrypt
- ✅ Salt automático (no necesitas gestionarlo)
- ✅ Resistente a ataques de fuerza bruta (lento intencionalmente)
- ✅ Adaptativo (puedes aumentar el costo en el futuro)
- ✅ Estándar de la industria

---

## 🚀 Flujo de Autenticación Completo

### Frontend (Cliente)

```javascript
// 1. Login
const loginResponse = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'ana', password: 'ana123' })
});

const { access_token, refresh_token, user } = await loginResponse.json();

// 2. Guardar tokens en localStorage
localStorage.setItem('access_token', access_token);
localStorage.setItem('refresh_token', refresh_token);
localStorage.setItem('user', JSON.stringify(user));

// 3. Hacer requests autenticados
const response = await fetch('http://localhost:5000/api/users/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});

// 4. Si el token expira (401), renovar automáticamente
if (response.status === 401) {
  const refreshResponse = await fetch('http://localhost:5000/api/auth/refresh', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('refresh_token')}`
    }
  });
  
  const { access_token: newToken } = await refreshResponse.json();
  localStorage.setItem('access_token', newToken);
  
  // Reintentar request original con nuevo token
  // ...
}

// 5. Logout
await fetch('http://localhost:5000/api/auth/logout', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
});

localStorage.removeItem('access_token');
localStorage.removeItem('refresh_token');
localStorage.removeItem('user');
```

---

## 📝 TODO / Mejoras Futuras

### Seguridad
- [ ] Implementar blacklist de tokens (para logout real)
- [ ] Rate limiting en endpoint de login (prevenir ataques de fuerza bruta)
- [ ] Logs de intentos de login fallidos
- [ ] 2FA (autenticación de dos factores)
- [ ] Expiración de refresh tokens después de inactividad

### Gestión de Usuarios
- [ ] Recuperación de contraseña (email con token)
- [ ] Cambio de contraseña (requiere contraseña actual)
- [ ] Política de contraseñas (longitud mínima, caracteres especiales)
- [ ] Bloqueo de cuenta después de X intentos fallidos

### Permisos
- [ ] Sistema de permisos granular (read/write/delete por recurso)
- [ ] Permisos personalizados por usuario (además de los del rol)
- [ ] Auditoría de acciones (quién hizo qué y cuándo)

---

## 🐛 Troubleshooting

### Error: "Import 'flask_jwt_extended' could not be resolved"
**Solución**: Reinstalar dependencia
```bash
pip install flask-jwt-extended
```

### Error: "Invalid token" o "Token has expired"
**Causas posibles**:
1. Token realmente expirado → Usar refresh token
2. Clave secreta cambió → Regenerar tokens (hacer login de nuevo)
3. Token malformado → Verificar formato `Bearer {token}`

### Error: "Usuario o contraseña incorrectos" (pero están correctos)
**Causa**: Contraseñas no están hasheadas en la BD
**Solución**:
```bash
python hash_existing_passwords.py
```

### Contraseñas hasheadas pero login falla
**Verificar** que las contraseñas se hashearon correctamente:
```bash
python hash_existing_passwords.py
# Opción 3: Verificar sistema de hash
```

---

## 📚 Referencias

- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [Passlib Documentation](https://passlib.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Decodificador de tokens JWT
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

**Última actualización**: 2025-10-18  
**Autor**: multiCont Development Team
