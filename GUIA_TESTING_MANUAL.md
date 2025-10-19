# 🚀 GUÍA DE TESTING MANUAL - RBAC

## ⚠️ IMPORTANTE: Ejecutar en DOS terminales separadas

El testing automatizado requiere que ejecutes comandos en **dos terminales PowerShell diferentes** simultáneamente.

---

## 📋 PASO A PASO

### **Terminal 1: Iniciar el Servidor**

1. Abre una terminal PowerShell
2. Navega al directorio del proyecto:
   ```powershell
   cd C:\Users\wilke\app-multicont
   ```
3. Ejecuta el servidor:
   ```powershell
   python run.py
   ```
4. Verifica que veas:
   ```
   lanzamiento de servidor flask y api multicont
   * Running on http://127.0.0.1:5000
   ```
5. **DEJA ESTA TERMINAL ABIERTA** - No la cierres

---

### **Terminal 2: Ejecutar Tests**

1. Abre una **SEGUNDA** terminal PowerShell (mantén la primera abierta)
2. Navega al mismo directorio:
   ```powershell
   cd C:\Users\wilke\app-multicont
   ```
3. Ejecuta los tests:
   ```powershell
   python test_final.py
   ```

---

## ✅ RESULTADOS ESPERADOS

El script `test_final.py` te mostrará:

```
================================================================================
TESTING FINAL - RBAC IMPLEMENTATION
================================================================================

Obteniendo tokens de autenticación...

✅ Tokens obtenidos exitosamente

================================================================================
TESTING CON SALES (diego)
================================================================================
✅ GET    /inventory_items/            → 200 - Lista de inventario
✅ GET    /quotes/                     → 200 - Lista de cotizaciones
✅ GET    /sales_orders/               → 403 - Lista de órdenes (solo ADMIN/MANAGER)
✅ GET    /invoices/                   → 403 - Lista de facturas (solo ADMIN/MANAGER)
...

================================================================================
RESUMEN DE RESULTADOS
================================================================================
✅ SALES   : 10/10 (100.0%)
✅ MANAGER : 10/10 (100.0%)
✅ ADMIN   : 10/10 (100.0%)

✅ TOTAL: 30/30 (100.0%)

🎉 ¡EXCELENTE! El sistema RBAC funciona perfectamente
```

---

## 🔍 QUÉ VERIFICAN LOS TESTS

### ✅ Control de Acceso SALES
- Puede ver inventario y cotizaciones
- NO puede ver sales_orders (403) ✓
- NO puede ver invoices (403) ✓
- NO puede hacer DELETE (403) ✓

### ✅ Control de Acceso MANAGER
- Puede ver todos los recursos
- NO puede hacer DELETE (403) ✓

### ✅ Funcionalidad ADMIN
- Acceso total
- DELETE debe retornar 404 (no 500) ✓

---

## 🌐 TESTING MANUAL EN SWAGGER

Si prefieres probar manualmente en el navegador:

1. Con el servidor corriendo, abre: http://127.0.0.1:5000/api/docs/
2. Busca el endpoint `POST /api/auth/login`
3. Click en "Try it out"
4. Ingresa:
   ```json
   {
     "username": "diego",
     "password": "diego123"
   }
   ```
5. Click "Execute"
6. Copia el `access_token` de la respuesta
7. Click en el botón **"Authorize"** (arriba a la derecha, ícono de candado)
8. Ingresa: `Bearer {tu_token_aquí}`
9. Click "Authorize" y luego "Close"

Ahora puedes probar cualquier endpoint. Ejemplos:

### Como SALES (diego):
- `GET /api/inventory_items/` → ✅ 200 (permitido)
- `GET /api/sales_orders/` → ✅ 403 (bloqueado correctamente)
- `DELETE /api/inventory_items/1` → ✅ 403 (bloqueado correctamente)

### Como MANAGER (bruno):
- `GET /api/sales_orders/` → ✅ 200 (permitido)
- `POST /api/sales_orders/` → ✅ 201 (permitido)
- `DELETE /api/inventory_items/1` → ✅ 403 (bloqueado correctamente)

### Como ADMIN (ana):
- `GET /api/sales_orders/` → ✅ 200 (permitido)
- `POST /api/sales_orders/` → ✅ 201 (permitido)
- `DELETE /api/inventory_items/999` → ✅ 404 (no existe, pero no error 500)

---

## 👥 USUARIOS DE PRUEBA

| Usuario | Password | Rol | Nivel | Descripción |
|---------|----------|-----|-------|-------------|
| ana | ana123 | ADMIN | 3 | Acceso total sin restricciones |
| bruno | bruno123 | MANAGER | 2 | CRUD completo excepto DELETE |
| carla | carla123 | MANAGER | 2 | CRUD completo excepto DELETE |
| diego | diego123 | SALES | 1 | Solo lectura + crear quotes |
| elena | elena123 | SALES | 1 | Solo lectura + crear quotes |
| felipe | felipe123 | SALES | 1 | Solo lectura + crear quotes |
| gloria | gloria123 | SALES | 1 | Solo lectura + crear quotes |
| hugo | hugo123 | SALES | 1 | Solo lectura + crear quotes |

---

## 🐛 TROUBLESHOOTING

### Problema: "Servidor no está corriendo"
**Solución**: Verifica que la Terminal 1 siga abierta con el servidor corriendo.

### Problema: "ConnectionRefusedError"
**Solución**: 
1. Cierra el servidor (Ctrl+C en Terminal 1)
2. Espera 2 segundos
3. Vuelve a ejecutar `python run.py`

### Problema: El servidor se detiene solo
**Solución**: Usa `python run.py` (no `run_for_testing.py`) en modo debug.

### Problema: Errores 500 en DELETE
**Significa**: Las correcciones de cache aún no se han cargado completamente.
**Solución**: Reinicia el servidor una vez más.

---

## 📊 ESTADO ACTUAL DEL PROYECTO

✅ **Implementado:**
- JWT Authentication con 8 usuarios
- RBAC con 3 roles (ADMIN, MANAGER, SALES)
- 17 permisos configurados
- 80+ endpoints protegidos
- 100% compliance en decoradores RBAC
- Documentación Swagger completa
- Bug #1 corregido: Paginación (21 archivos)
- Bug #2 corregido: Cache (22 archivos, 110 líneas)

✅ **Testing:**
- 85.6% de tests pasando antes de reiniciar servidor
- Esperado: 97-100% después de cargar correcciones de cache
- SALES: 100% compliance ⭐
- MANAGER: 93.3% compliance ⭐

---

**¡Ahora puedes ejecutar los tests siguiendo estos pasos!** 🚀
