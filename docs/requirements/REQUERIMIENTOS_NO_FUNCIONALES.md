# REQUERIMIENTOS NO FUNCIONALES (RNF) - Sistema Multicont

**Fecha**: 19 de Octubre, 2025  
**Autores**: Wilker & Daniel  
**Versión**: 1.0.0

---

## Descripción General

Este documento lista todos los requerimientos no funcionales del sistema Multicont. Los RNF definen atributos de calidad del sistema: seguridad, rendimiento, escalabilidad, mantenibilidad, etc.

**Categorías**:
- Seguridad
- Rendimiento
- Escalabilidad
- Usabilidad
- Mantenibilidad
- Portabilidad
- Confiabilidad

---

## RNF-001: Seguridad - Autenticación JWT

**Código**: RNF-001  
**Categoría**: Seguridad  
**Descripción**: El sistema debe implementar autenticación segura con JSON Web Tokens.

**Criterios de Aceptación**:
- Tokens firmados con algoritmo HS256
- Secret key de 256 bits mínimo
- Access token: 15 minutos de expiración
- Refresh token: 30 días de expiración
- Tokens almacenados en HTTP-only cookies o headers

**Métricas**:
- ✅ Algoritmo: HS256
- ✅ Secret key: 256 bits (generado con `secrets.token_hex(32)`)
- ✅ Expiración configurada correctamente

**Estado**: ✅ COMPLETADO  
**Evidencia**: `app/services/auth_service.py` (183 líneas) ✅

---

## RNF-002: Seguridad - Password Hashing

**Código**: RNF-002  
**Categoría**: Seguridad  
**Descripción**: Las contraseñas deben almacenarse hasheadas con bcrypt.

**Criterios de Aceptación**:
- Usar bcrypt con mínimo 12 rounds
- Nunca almacenar passwords en texto plano
- Validación segura con `check_password_hash()`

**Métricas**:
- ✅ bcrypt rounds: 12
- ✅ 0 passwords en texto plano en BD

**Estado**: ✅ COMPLETADO  
**Evidencia**: 
- `bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))`
- Script: `scripts/database/hash_user_passwords.py` ✅

---

## RNF-003: Seguridad - RBAC (Control de Acceso)

**Código**: RNF-003  
**Categoría**: Seguridad  
**Descripción**: Implementar control de acceso basado en roles (RBAC).

**Criterios de Aceptación**:
- Mínimo 3 roles: Admin, Manager, Sales
- Permisos granulares por endpoint
- Validación en cada request protegido
- Decoradores: `@role_required`, `@permission_required`
- Denegar por defecto (whitelist approach)

**Métricas**:
- ✅ 3 roles implementados
- ✅ Permisos granulares: `users.create`, `users.update`, etc.
- ✅ 100% endpoints críticos protegidos
- ✅ 100% tests RBAC pasando

**Estado**: ✅ COMPLETADO  
**Evidencia**: 
- `app/services/authorization_service.py` (261 líneas)
- `tests/unit/test_rbac.py` (315 líneas con 100% coverage)

---

## RNF-004: Seguridad - Validación de Entrada

**Código**: RNF-004  
**Categoría**: Seguridad  
**Descripción**: Validar todas las entradas de usuario para prevenir inyecciones.

**Criterios de Aceptación**:
- Usar Marshmallow schemas en todos los POST/PUT
- Validar tipos de datos
- Sanitizar inputs
- Prevenir SQL injection (usar ORM)
- Prevenir XSS (escape HTML en outputs)

**Métricas**:
- ✅ 23 schemas Marshmallow implementados
- ✅ 100% endpoints POST/PUT validados
- ✅ ORM SQLAlchemy (previene SQL injection)
- ✅ 48 tests de validación pasando

**Estado**: ✅ COMPLETADO  
**Evidencia**: 
- `app/schemas/` (6 módulos, 23 schemas)
- `tests/integration/test_marshmallow_validation.py` ✅

---

## RNF-005: Rendimiento - Tiempo de Respuesta

**Código**: RNF-005  
**Categoría**: Rendimiento  
**Descripción**: Los endpoints deben responder en < 200ms (promedio).

**Criterios de Aceptación**:
- GET simples: < 100ms
- GET con joins: < 200ms
- POST/PUT/DELETE: < 300ms
- Queries complejas: < 500ms

**Métricas actuales**:
- ⏳ No medido sistemáticamente
- ⏳ Requiere benchmarking con Apache Bench o Locust

**Estado**: ⏳ EN PROGRESO  
**Acción requerida**: Implementar logging de tiempo de respuesta, crear script de benchmarking

---

## RNF-006: Rendimiento - Paginación

**Código**: RNF-006  
**Categoría**: Rendimiento  
**Descripción**: Todos los endpoints de listado deben paginar resultados.

**Criterios de Aceptación**:
- Default: 10 items por página
- Máximo: 100 items por página
- Metadata en response: `total`, `page`, `per_page`, `total_pages`

**Métricas**:
- ✅ 100% endpoints GET paginados
- ✅ Default: 10 items
- ✅ Implementado en `BaseHandler.list_all()`

**Estado**: ✅ COMPLETADO

---

## RNF-007: Rendimiento - Índices de Base de Datos

**Código**: RNF-007  
**Categoría**: Rendimiento  
**Descripción**: Crear índices en columnas de búsqueda frecuente.

**Criterios de Aceptación**:
- Índices en todas las FK
- Índices en campos de búsqueda (email, username, NIT)
- Índices compuestos para queries frecuentes

**Métricas actuales**:
- ⏳ FK indexadas por defecto (SQLAlchemy)
- ⚠️ Falta agregar `index=True` en campos de búsqueda

**Estado**: ⏳ EN PROGRESO  
**Acción requerida**: Revisar modelos y agregar `index=True` donde corresponda

---

## RNF-008: Escalabilidad - Concurrencia

**Código**: RNF-008  
**Categoría**: Escalabilidad  
**Descripción**: El sistema debe soportar mínimo 1000 usuarios concurrentes.

**Criterios de Aceptación**:
- 1000 requests/segundo sin degradación
- Connection pooling en DB
- Stateless API (sin sesiones en servidor)

**Métricas actuales**:
- ⏳ No testeado con carga
- ✅ API stateless (JWT)
- ⚠️ Connection pooling: usar configuración por defecto de SQLAlchemy

**Estado**: ⏳ EN PROGRESO  
**Acción requerida**: Test de carga con Locust o JMeter

---

## RNF-009: Escalabilidad - Horizontal Scaling

**Código**: RNF-009  
**Categoría**: Escalabilidad  
**Descripción**: La aplicación debe poder escalar horizontalmente.

**Criterios de Aceptación**:
- Sin estado en servidor (stateless)
- Soportar múltiples instancias detrás de load balancer
- Session storage externo (Redis) si se necesita cache

**Métricas**:
- ✅ API stateless (JWT en headers)
- ⏳ No probado con múltiples instancias
- ❌ Redis no implementado aún

**Estado**: ⏳ EN PROGRESO

---

## RNF-010: Usabilidad - Documentación API

**Código**: RNF-010  
**Categoría**: Usabilidad  
**Descripción**: La API debe estar completamente documentada con Swagger UI.

**Criterios de Aceptación**:
- Swagger UI accesible en `/api/docs/`
- Todos los endpoints documentados
- Ejemplos de request/response
- Try-it-out funcional

**Métricas**:
- ✅ Swagger UI en `/api/docs/`
- ✅ 24 APIs documentadas
- ✅ Ejemplos incluidos
- ✅ Try-it-out funcional con JWT

**Estado**: ✅ COMPLETADO  
**Evidencia**: Flasgger configurado en `app/__init__.py` ✅

---

## RNF-011: Usabilidad - Mensajes de Error

**Código**: RNF-011  
**Categoría**: Usabilidad  
**Descripción**: Los mensajes de error deben ser claros y útiles.

**Criterios de Aceptación**:
- Códigos HTTP correctos (400, 401, 403, 404, 500)
- Mensajes descriptivos (no técnicos para usuario final)
- JSON estructurado: `{"success": false, "error": "mensaje"}`
- Detalles de validación en caso de error 400

**Métricas**:
- ✅ Códigos HTTP correctos
- ✅ JSON estructurado en responses
- ✅ Exception handling personalizado (133 líneas)

**Estado**: ✅ COMPLETADO  
**Evidencia**: `app/exceptions.py` ✅

---

## RNF-012: Mantenibilidad - Clean Architecture

**Código**: RNF-012  
**Categoría**: Mantenibilidad  
**Descripción**: El código debe seguir Clean Architecture (3 capas).

**Criterios de Aceptación**:
- Separación clara: Entities → Use Cases → API
- Dependencias apuntan hacia dentro (domain no depende de API)
- Business logic en handlers, no en API
- Models sin lógica de aplicación

**Métricas**:
- ✅ 3 capas implementadas correctamente
- ✅ 21 entities en `app/entities/`
- ✅ 22 handlers en `app/use_cases/`
- ✅ 24 APIs en `app/api/`

**Estado**: ✅ COMPLETADO  
**Evidencia**: Estructura de carpetas ✅

---

## RNF-013: Mantenibilidad - Patrón DRY

**Código**: RNF-013  
**Categoría**: Mantenibilidad  
**Descripción**: Evitar duplicación de código con BaseHandler.

**Criterios de Aceptación**:
- BaseHandler con métodos CRUD comunes
- Herencia en todos los handlers
- Métodos reutilizables: `create()`, `get()`, `list_all()`, `update()`, `delete()`

**Métricas**:
- ✅ BaseHandler: 341 líneas
- ✅ 22 handlers heredan de BaseHandler
- ✅ Reducción de código duplicado: ~70%

**Estado**: ✅ COMPLETADO  
**Evidencia**: `app/use_cases/base_handler.py` (Fase 5 - Wilker) ✅

---

## RNF-014: Mantenibilidad - Versionado de Código

**Código**: RNF-014  
**Categoría**: Mantenibilidad  
**Descripción**: Usar Git con commits descriptivos.

**Criterios de Aceptación**:
- Commits con mensajes semánticos (feat, fix, docs, refactor)
- Branching strategy (main, develop, feature branches)
- Pull requests con code review

**Métricas**:
- ✅ 200+ commits
- ✅ Mensajes descriptivos
- ✅ GitHub como repositorio remoto

**Estado**: ✅ COMPLETADO  
**Evidencia**: Historial de Git ✅

---

## RNF-015: Testabilidad - Cobertura de Tests

**Código**: RNF-015  
**Categoría**: Testabilidad  
**Descripción**: Mínimo 70% de cobertura de código con tests.

**Criterios de Aceptación**:
- pytest configurado
- Tests unitarios para lógica de negocio
- Tests de integración para endpoints
- Coverage report disponible

**Métricas actuales**:
- ✅ pytest + pytest-cov configurado
- ✅ 111 tests implementados
- ⚠️ Coverage: 37.69% (objetivo: 70%)
- ✅ Coverage report HTML disponible

**Estado**: ⏳ EN PROGRESO  
**Acción requerida**: Aumentar cobertura a 70% (falta 32.31%)  
**Evidencia**: `tests/unit/` y `tests/integration/` ✅

---

## RNF-016: Portabilidad - Docker Support

**Código**: RNF-016  
**Categoría**: Portabilidad  
**Descripción**: La aplicación debe ejecutarse en contenedores Docker.

**Criterios de Aceptación**:
- Dockerfile para la app
- docker-compose.yml con app + PostgreSQL
- Variables de entorno configurables
- Imagen < 500MB

**Métricas**:
- ❌ Dockerfile no existe
- ❌ docker-compose.yml no existe

**Estado**: ❌ PENDIENTE  
**Acción requerida**: Crear Dockerfile y docker-compose.yml

---

## RNF-017: Confiabilidad - Disponibilidad

**Código**: RNF-017  
**Categoría**: Confiabilidad  
**Descripción**: El sistema debe tener 99.9% de disponibilidad (uptime).

**Criterios de Aceptación**:
- Máximo 43 minutos de downtime por mes
- Health check endpoint
- Monitoreo con logs

**Métricas actuales**:
- ⏳ No medido (proyecto académico)
- ❌ Health check endpoint no implementado

**Estado**: ❌ PENDIENTE  
**Acción requerida**: Crear `/health` endpoint

---

## RNF-018: Confiabilidad - Backup y Recuperación

**Código**: RNF-018  
**Categoría**: Confiabilidad  
**Descripción**: Backup automático de base de datos.

**Criterios de Aceptación**:
- Backup diario de PostgreSQL
- Retención: 30 días
- Procedimiento de restore documentado

**Métricas**:
- ❌ Backups automáticos no configurados
- ⏳ Script manual: `pg_dump` disponible

**Estado**: ❌ PENDIENTE  
**Acción requerida**: Configurar cron job para backups

---

## RNF-019: Confiabilidad - Transacciones ACID

**Código**: RNF-019  
**Categoría**: Confiabilidad  
**Descripción**: Operaciones críticas deben ser transaccionales.

**Criterios de Aceptación**:
- Uso de `db.session.begin()` / `commit()` / `rollback()`
- Operaciones multi-tabla en transacción única
- Rollback automático en caso de error

**Métricas**:
- ✅ SQLAlchemy con transacciones
- ✅ `try/except` con `db.session.rollback()`
- ✅ Operaciones atómicas en handlers

**Estado**: ✅ COMPLETADO

---

## RNF-020: Documentación - README Completo

**Código**: RNF-020  
**Categoría**: Documentación  
**Descripción**: README.md con instrucciones completas.

**Criterios de Aceptación**:
- Descripción del proyecto
- Instalación paso a paso
- Configuración de variables de entorno
- Comandos de desarrollo
- Arquitectura explicada

**Métricas**:
- ✅ README.md: 1650+ líneas
- ✅ Secciones completas
- ✅ Guías de instalación

**Estado**: ✅ COMPLETADO  
**Evidencia**: `README.md` versión 3.0.0 ✅

---

## Resumen de Estados

| Estado | Cantidad | Porcentaje |
|--------|----------|------------|
| ✅ COMPLETADO | 11 | 55% |
| ⏳ EN PROGRESO | 5 | 25% |
| ❌ PENDIENTE | 4 | 20% |
| **TOTAL** | **20** | **100%** |

---

## Categorías

| Categoría | Cantidad |
|-----------|----------|
| Seguridad | 4 ✅ |
| Rendimiento | 3 (1⏳) |
| Escalabilidad | 2 ⏳ |
| Usabilidad | 2 ✅ |
| Mantenibilidad | 3 ✅ |
| Testabilidad | 1 ⏳ |
| Portabilidad | 1 ❌ |
| Confiabilidad | 3 (1✅, 2❌) |
| Documentación | 1 ✅ |

---

## Prioridades para Mejorar

### 🔴 CRÍTICO
1. **RNF-015**: Aumentar coverage de 37.69% a 70%
2. **RNF-016**: Implementar Docker support

### 🟡 IMPORTANTE
3. **RNF-005**: Benchmarking de rendimiento
4. **RNF-007**: Agregar índices en campos de búsqueda
5. **RNF-017**: Implementar health check endpoint

### 🟢 DESEABLE
6. **RNF-008**: Test de carga (1000 usuarios concurrentes)
7. **RNF-018**: Configurar backups automáticos
8. **RNF-009**: Probar escalado horizontal

---

## Métricas Actuales del Sistema

```
Seguridad:              100% ✅
Validación:             100% ✅
RBAC:                   100% ✅
Clean Architecture:     100% ✅
Patrón DRY:             100% ✅
Documentación Swagger:  100% ✅
Test Coverage:          37.69% ⚠️
Rendimiento:            No medido ⏳
Escalabilidad:          No testeada ⏳
Docker:                 0% ❌
Backups:                Manual ⚠️
```

---

**Última actualización**: 19 de Octubre, 2025  
**Responsables**: Wilker (Seguridad, Arquitectura, Testing) & Daniel (Analytics, Organización)
