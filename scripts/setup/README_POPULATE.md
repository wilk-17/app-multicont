# Instrucciones para poblar la base de datos

Este documento explica cómo ejecutar los scripts de población de datos para el proyecto Multicont.

Requisitos previos
- Entorno virtual de Python activado (recomendado).
- Base de datos PostgreSQL configurada y accesible según `.env` (ver `DATABASE_URL`).
- Migraciones aplicadas: `flask db upgrade`.

Resumen de scripts
- `scripts/setup/populate_rbac_data.py` — Script validado (RBAC, usuarios, roles, datos básicos). Está probado con los tests RBAC.
- `scripts/setup/populate_mechatronics_complete.py` — Seeder completo para el dominio mecatrónica:
  - Crea 6 marcas mecatrónicas (OMRON, ING Multicontrol, Gefran, Weidmüller, Rice Lake, Optec).
  - Asegura >15 organizaciones (incluye `ING Multicontrol`).
  - Crea 5 sucursales para `ING Multicontrol` en: Bogotá, Medellín, Cali, Ibagué y Cartagena.
  - Crea mínimo 14 empleados distribuidos en esas 5 sucursales.
  - Inserta inventario representativo y transacciones en Q1–Q3 (cotizaciones, órdenes, facturas).

Recomendación de orden de ejecución
1. Activar entorno virtual y posicionarse en la raíz del repo.
   PowerShell (Windows):
   ```powershell
   .\.venv\Scripts\Activate.ps1  # si usas .venv
   # o
   .venv\Scripts\activate        # según tu entorno
   ```

2. Instalar dependencias (si no están instaladas):
   ```powershell
   pip install -r requirements.txt
   ```

3. Aplicar migraciones (asegúrate de tener `DATABASE_URL` configurada en `.env`):
   ```powershell
   flask db upgrade
   ```

4. Ejecutar el seeder RBAC (opcional — crea roles/usuarios básicos):
   ```powershell
   python scripts\setup\populate_rbac_data.py
   ```

5. Ejecutar el seeder mecatrónica (recomendado después de RBAC). El script es idempotente y soporta `--reset` para un borrado "best-effort":
   ```powershell
   # Población normal
   python scripts\setup\populate_mechatronics_complete.py

   # Forzar reset (elimina datos sembrados por este seeder y vuelve a poblar)
   python scripts\setup\populate_mechatronics_complete.py --reset
   ```

Notas y precauciones
- El flag `--reset` realiza un borrado conservador y "best-effort" sobre tablas relacionadas con los datos sembrados por este script; no es un wipe total de la base de datos.
- Si la base de datos contiene datos de producción, NO ejecutar `--reset` sin respaldo.
- El script usa claves únicas y `get_or_create` por nombres/códigos para evitar duplicados; aun así, revisa los logs en caso de conflictos.
- Si aparecen errores de firmas de modelos (por ejemplo `ItemCategory` con distinto constructor), revisar y ajustar el seeder: `scripts/setup/populate_mechatronics_complete.py` contiene fallbacks para esas firmas.

Verificación rápida
- Ejecuta los tests RBAC para confirmar que los roles/usuarios fueron creados correctamente:
  ```powershell
  python tests\integration\test_rbac_simple.py
  ```

- Verifica conteos mínimos esperados (ejemplo desde Flask shell):
  ```python
  from app import create_app, db
  from app.entities import Organization, Branch, Employee, Brand
  app = create_app(); ctx = app.app_context(); ctx.push()
  print('Orgs:', Organization.query.count())
  print('Branches (ING Multicontrol):', Branch.query.join(Organization).filter(Organization.current_name=='ING Multicontrol').count())
  print('Employees (seed):', Employee.query.filter(Employee.id != None).count())
  print('Brands (mechatronics):', Brand.query.filter(Brand.name.in_(['OMRON','ING Multicontrol','Gefran','Weidmüller','Rice Lake','Optec'])).count())
  ctx.pop()
  ```

Commit asociado
- Archivos añadidos en este cambio: `scripts/setup/populate_mechatronics_complete.py` (seeder) y `scripts/setup/README_POPULATE.md` (instrucciones).
  Mensaje de commit propuesto: "feat(seed): add mechatronics seeder + README with run instructions for Wilker"

Contacto / responsable
- Autor del seeder: GitHub Copilot (generado automáticamente) — por favor Wilker, revisa los nombres de entidades y realiza una ejecución en un entorno de desarrollo antes de usar en staging/producción.

Última actualización: 2025-10-21
