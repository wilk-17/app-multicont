# 📋 MULTICONT - Guía de Inicio Rápido

**Versión**: 1.0.0 | **Fecha**: 19 de Octubre de 2025 | **Estado**: ✅ Producción

---

## 🎯 ¿Qué es Multicont?

Sistema integral de gestión empresarial con **Clean Architecture** que implementa:
- Gestión de organizaciones, sucursales y empleados
- Control de inventario con trazabilidad
- Flujo completo de ventas (Cotizaciones → Órdenes → Facturas)
- Sistema RBAC con JWT (4 roles: ADMIN, MANAGER, SALES, VIEWER)
- Dashboard con métricas y KPIs de negocio

**Tecnologías**: Flask + PostgreSQL + SQLAlchemy + JWT + RBAC + Marshmallow + pytest

---

## 📚 Documentación por Audiencia

### 🎓 Soy Evaluador Académico

**Necesito**: Ver evidencia de cumplimiento de requisitos

**Documentos clave**:
1. **[AUDITORIA_REQUISITOS.md](docs/academic/AUDITORIA_REQUISITOS.md)** - ✅ Cumplimiento 97% (9/9 componentes)
2. **[METODOLOGIA_RAD.md](docs/academic/METODOLOGIA_RAD.md)** - Evidencia de Req + Plan + Ejec + Testing
3. **[PLANTEAMIENTO_PROYECTO.docx](docs/PLANTEAMIENTO_PROYECTO.docx)** - Documento académico APA 7
4. **[ALCANCE_DEL_PROYECTO.md](docs/academic/ALCANCE_DEL_PROYECTO.md)** - Alcance y roadmap
5. **Tests RBAC** - Ejecutar: `python tests/integration/test_rbac_simple.py` → 90/90 (100%)

**Ver índice completo**: [docs/INDEX.md](docs/INDEX.md) → Sección "Documentación Académica"

---

### 👨‍💻 Soy Desarrollador

**Necesito**: Instalar, ejecutar y entender la arquitectura

**Pasos rápidos**:
```bash
# 1. Clonar e instalar
git clone https://github.com/wilk-17/app-multicont.git
cd app-multicont
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Configurar BD (editar .env)
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/multicont

# 3. Migrar y poblar
flask db upgrade
python scripts/setup/populate_rbac_data.py

# 4. Ejecutar
python run.py
# → http://127.0.0.1:5000/api/docs/
```

**Documentos clave**:
- **[README.md](README.md)** - Guía completa de instalación y uso
- **[AUTHENTICATION_GUIDE.md](docs/technical/guides/AUTHENTICATION_GUIDE.md)** - JWT y RBAC
- **[TESTING_GUIDE.md](docs/technical/guides/TESTING_GUIDE.md)** - Ejecutar tests
- **[EJEMPLOS_USO_API.md](docs/technical/api/EJEMPLOS_USO_API.md)** - Ejemplos con curl

**Ver índice completo**: [docs/INDEX.md](docs/INDEX.md) → Sección "Documentación Técnica"

---

### 🏢 Soy Product Owner / Stakeholder

**Necesito**: Entender el negocio, wireframes y alcance

**Documentos clave**:
- **[ALCANCE_DEL_PROYECTO.md](docs/academic/ALCANCE_DEL_PROYECTO.md)** - Features y roadmap
- **[REGLAS_DE_NEGOCIO.md](docs/business/REGLAS_DE_NEGOCIO.md)** - 7 reglas implementadas
- **[WIREFRAMES.md](docs/business/wireframes/WIREFRAMES.md)** - Visualización de interfaces
- **[DIAGRAMAS.md](docs/architecture/diagrams/DIAGRAMAS.md)** - Diagramas UML del sistema

**Demo en vivo**: 
```bash
python run.py
# Abrir: http://127.0.0.1:5000/api/docs/
```

**Ver índice completo**: [docs/INDEX.md](docs/INDEX.md) → Sección "Documentación de Negocio"

---

## 🗂️ Estructura del Proyecto

```
app-multicont/
├── README.md                    # 📖 Guía completa del proyecto
├── INDEX_INICIO.md             # 📋 Este archivo (inicio rápido)
├── RESUMEN_VISUAL.md           # 🎉 Resumen visual de reorganización
├── REORGANIZACION_COMPLETADA.md # 📝 Detalle de reorganización
│
├── app/                         # 💻 Código fuente (Clean Architecture)
│   ├── entities/                # Capa 1 - Modelos de dominio (23)
│   ├── use_cases/               # Capa 2 - Lógica de negocio (20 handlers)
│   ├── api/                     # Capa 3 - Endpoints REST (20 APIs)
│   ├── schemas/                 # Validación Marshmallow
│   └── config.py                # Configuración
│
├── tests/                       # 🧪 Tests automatizados
│   ├── integration/             # test_rbac_simple.py (90 tests)
│   └── unit/                    # test_assignment_tracking.py (7 tests)
│
├── migrations/                  # 🗄️ Migraciones Alembic (23 tablas)
│
├── scripts/                     # 🛠️ Scripts auxiliares
│   ├── setup/                   # Instalación y configuración
│   ├── maintenance/             # Mantenimiento de BD
│   └── testing/                 # Scripts de testing
│
└── docs/                        # 📚 Documentación completa
    ├── INDEX.md                 # Índice completo de documentación
    ├── academic/                # Docs académicos (RAD, Alcance, Requisitos)
    ├── business/                # Reglas de negocio, Wireframes
    ├── architecture/            # Diagramas UML, Fases
    ├── technical/               # Guías técnicas, API docs
    ├── summaries/               # Resúmenes ejecutivos
    └── archive/                 # Documentación legacy
```

---

## 🚀 Acciones Rápidas

### Ver Swagger UI (Documentación Interactiva)
```bash
python run.py
# Abrir: http://127.0.0.1:5000/api/docs/
```

### Ejecutar Tests RBAC (Validar Funcionalidad)
```bash
python tests/integration/test_rbac_simple.py
# Esperado: 90/90 tests passed (100.0%)
```

### Ver Cumplimiento de Requisitos
```bash
cat docs/academic/AUDITORIA_REQUISITOS.md
# Cumplimiento: 97% (9/9 componentes)
```

### Ver Todas las Métricas del Sistema
```bash
# Con servidor corriendo:
curl http://127.0.0.1:5000/api/metrics/summary
```

---

## 📊 Estado del Proyecto

| Componente              | Estado | Evidencia                          |
|-------------------------|--------|------------------------------------|
| **Requisitos**          | ✅ 97%  | 9/9 componentes implementados     |
| **Tests RBAC**          | ✅ 100% | 90/90 tests passing               |
| **Arquitectura**        | ✅ 100% | Clean Architecture (3 capas)      |
| **Documentación**       | ✅ 100% | 50+ docs organizados              |
| **Base de Datos**       | ✅ 100% | 23 tablas migradas                |
| **Endpoints**           | ✅ 100% | 20 APIs RESTful + Swagger         |

---

## 📞 Soporte y Contacto

**¿Tienes dudas?**

- **Documentación completa**: [docs/INDEX.md](docs/INDEX.md)
- **README principal**: [README.md](README.md)
- **Guías técnicas**: `docs/technical/guides/`
- **Ejemplos de API**: [docs/technical/api/EJEMPLOS_USO_API.md](docs/technical/api/EJEMPLOS_USO_API.md)

**Equipo de Desarrollo**:
- Wilker - Backend Developer & Database Architect
- Daniel - Backend Developer & Testing Engineer

**Repositorio**: https://github.com/wilk-17/app-multicont

---

## 🎓 Para Entregar Académicamente

**Documentos principales**:
1. ✅ [AUDITORIA_REQUISITOS.md](docs/academic/AUDITORIA_REQUISITOS.md) - Cumplimiento 97%
2. ✅ [METODOLOGIA_RAD.md](docs/academic/METODOLOGIA_RAD.md) - Evidencia RAD
3. ✅ [PLANTEAMIENTO_PROYECTO.docx](docs/PLANTEAMIENTO_PROYECTO.docx) - APA 7
4. ✅ **Código fuente** en `app/` (Clean Architecture)
5. ✅ **Tests** ejecutables: `python tests/integration/test_rbac_simple.py`
6. ✅ **Swagger UI** en vivo: http://127.0.0.1:5000/api/docs/

**Evidencia de Testing**:
```bash
# Ejecutar y capturar resultado
python tests/integration/test_rbac_simple.py > resultado_tests.txt

# Resultado esperado en resultado_tests.txt:
# TOTAL - 90/90 tests passed (100.0%)
# EXCELENTE! Todos los tests pasaron!
```

---

**Última actualización**: 19 de Octubre de 2025  
**Versión**: 1.0.0  
**Estado**: ✅ PRODUCCIÓN
