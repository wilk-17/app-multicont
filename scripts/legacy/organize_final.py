"""
ORGANIZACIÓN FINAL DEL PROYECTO - MOVIMIENTO DE ARCHIVOS
=========================================================
Mueve archivos sueltos a carpetas apropiadas sin afectar el código
"""

import os
import shutil
from pathlib import Path

# Archivos a mover/eliminar
ACTIONS = {
    'MOVER_A_DOCS_ARCHIVE': [
        'README_OLD_backup.md',
        'REORGANIZACION_COMPLETADA.md',
        'RESUMEN_VISUAL.md'
    ],
    'MOVER_A_SCRIPTS_LEGACY': [
        'cleanup_legacy.py'
    ],
    'MANTENER_EN_RAIZ': [
        '.coverage',
        '.env',
        '.env.example',
        '.gitignore',
        'INDEX_INICIO.md',
        'pytest.ini',
        'README.md',
        'requirements.txt',
        'run.py'
    ]
}

def move_files():
    """Mueve archivos a sus ubicaciones apropiadas"""
    moved = []
    errors = []
    
    # Crear carpetas si no existen
    Path('docs/archive').mkdir(parents=True, exist_ok=True)
    Path('scripts/legacy').mkdir(parents=True, exist_ok=True)
    
    # Mover documentos a docs/archive/
    for file in ACTIONS['MOVER_A_DOCS_ARCHIVE']:
        if os.path.exists(file):
            try:
                dest = f'docs/archive/{file}'
                shutil.move(file, dest)
                moved.append(f"📄 {file} → docs/archive/")
            except Exception as e:
                errors.append(f"❌ Error moviendo {file}: {str(e)}")
    
    # Mover scripts a scripts/legacy/
    for file in ACTIONS['MOVER_A_SCRIPTS_LEGACY']:
        if os.path.exists(file):
            try:
                dest = f'scripts/legacy/{file}'
                shutil.move(file, dest)
                moved.append(f"📄 {file} → scripts/legacy/")
            except Exception as e:
                errors.append(f"❌ Error moviendo {file}: {str(e)}")
    
    return moved, errors

print("="*80)
print("📁 ORGANIZACIÓN FINAL DE ARCHIVOS".center(80))
print("="*80)

moved, errors = move_files()

print(f"\n✅ Archivos movidos: {len(moved)}")
for item in moved:
    print(f"   {item}")

if errors:
    print(f"\n❌ Errores: {len(errors)}")
    for error in errors:
        print(f"   {error}")

print(f"\n📊 Estado final de la raíz:")
root_files = [f for f in os.listdir('.') if os.path.isfile(f) and not f.startswith('.')]
print(f"   Archivos visibles en raíz: {len(root_files)}")
for f in sorted(root_files):
    print(f"   ✓ {f}")

print("\n" + "="*80)
print(f"✅ ORGANIZACIÓN COMPLETADA")
print("="*80)
