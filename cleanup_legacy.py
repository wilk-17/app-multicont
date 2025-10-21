"""
SCRIPT DE LIMPIEZA AUTOMÁTICA DE ARCHIVOS LEGACY
=================================================
Elimina archivos obsoletos identificados en el análisis
"""

import os
import shutil
from pathlib import Path

# Archivos/carpetas legacy a eliminar
LEGACY_TO_DELETE = {
    # Scripts de testing obsoletos
    'scripts/testing/test_all_131_endpoints.py',
    'scripts/testing/test_all_endpoints_complete.py',
    'scripts/testing/test_fixed_endpoints.py',
    'scripts/testing/test_rbac_live.py',
    'scripts/testing/test_rbac_with_server.py',
    'scripts/testing/analyze_errors.py',
    'scripts/testing/analyze_manager.py',
    'scripts/testing/debug_manager.py',
    'scripts/testing/diagnose_errors.py',
    'scripts/testing/find_failures.py',
    'scripts/testing/verify_endpoints.py',
    'scripts/testing/verify_database_population.py',
    
    # Resultados de tests
    'scripts/testing/test_results.txt',
    'scripts/testing/test_results_100.txt',
    'scripts/testing/test_results_final.txt',
    'scripts/testing/test_results_final_v2.txt',
    'scripts/testing/test_results_fixed.txt',
    
    # Scripts legacy en raíz
    'analyze_and_cleanup.py',
    'analyze_project_cleanup.py',
    'create_retroactive_goals.py',
    'diagnose_interactive_errors.py',
    'diagnose_interactive_failures.py',
    'fix_admin_user.py',
    'list_users.py',
    'populate_database.py',
    'recreate_users.py',
    'RESUMEN_POBLACION.py',
    'simple_test_debug.py',
    'test_analytics_endpoints.py',
    'test_sales_analytics_data.py',
    'test_simple_debug.py',
    'update_passwords.py',
    'verify_data.py',
    
    # Documentos legacy en raíz (mover a docs/archive/)
    'ALINEACION_COMPLETA_REPORTE.md',
    'ANALISIS_CRUD_Y_RECOMENDACIONES_VISTAS.md',
    'ANALISIS_REQUERIMIENTOS_CORTE.md',
    'IMPLEMENTACION_COMPLETA.md',
    'POBLACION_BASE_DATOS_COMPLETA.md',
    'ROADMAP_IMPLEMENTACION.md',
    'SISTEMA_METAS_VENTAS_COMPLETO.md',
    
    # Archivos temporales
    'all_endpoints.txt',
    'temp_all_endpoints.txt',
    'temp_endpoints.txt',
    'test_inter.txt',
    'test_interactive_output.txt',
    'test_rbac_resultado.txt',
    
    # App legacy
    'app/models',
    'app/routes.py',
    
    # Tests legacy
    'tests/integration/test_rbac_live.py',
    'tests/integration/test_rbac_interactive_console.py',
    
    # Scripts maintenance legacy
    'scripts/maintenance/check_database_issues.py',
    'scripts/maintenance/check_new_issues.py',
    'scripts/maintenance/fix_database_issues.py',
    'scripts/maintenance/fix_database_reorder_and_complete.py',
}

def delete_legacy_files():
    """Elimina archivos y carpetas legacy"""
    deleted = []
    errors = []
    
    for item in sorted(LEGACY_TO_DELETE):
        try:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                    deleted.append(f"📁 {item}")
                else:
                    os.remove(item)
                    deleted.append(f"📄 {item}")
        except Exception as e:
            errors.append(f"❌ Error eliminando {item}: {str(e)}")
    
    return deleted, errors

print("="*80)
print("🗑️  ELIMINANDO ARCHIVOS LEGACY".center(80))
print("="*80)

deleted, errors = delete_legacy_files()

print(f"\n✅ Archivos eliminados: {len(deleted)}")
for item in deleted:
    print(f"   {item}")

if errors:
    print(f"\n❌ Errores: {len(errors)}")
    for error in errors:
        print(f"   {error}")

print("\n" + "="*80)
print(f"✅ LIMPIEZA COMPLETADA: {len(deleted)} items eliminados")
print("="*80)
