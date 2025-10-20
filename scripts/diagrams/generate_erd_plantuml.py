#!/usr/bin/env python3
"""
Script para generar diagrama ERD (Entity-Relationship Diagram) en PlantUML
desde los modelos SQLAlchemy del proyecto Multicont.

Uso:
    python scripts/diagrams/generate_erd_plantuml.py

Output:
    - docs/diagrams/ERD_database.puml (código PlantUML)
    
Para generar PNG:
    java -jar plantuml.jar docs/diagrams/ERD_database.puml
    O usar: https://www.plantuml.com/plantuml/uml/
"""

import sys
import os

# Añadir el path del proyecto para poder importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from sqlalchemy import inspect

def get_all_models():
    """Obtiene todos los modelos SQLAlchemy registrados."""
    app = create_app()
    with app.app_context():
        models = []
        for mapper in db.Model.registry.mappers:
            model_class = mapper.class_
            models.append(model_class)
        return models

def generate_plantuml_erd():
    """Genera código PlantUML para ERD desde modelos SQLAlchemy."""
    
    models = get_all_models()
    
    lines = [
        '@startuml ERD_Multicont',
        '!define Table(name,desc) class name as "desc" << (T,#FFAAAA) >>',
        '!define primary_key(x) <b>x</b>',
        'hide methods',
        'hide stereotypes',
        'skinparam classAttributeIconSize 0',
        ''
    ]
    
    # Generar clases (tablas)
    for model in models:
        table_name = model.__tablename__
        lines.append(f'class {model.__name__} {{')
        
        # Obtener columnas
        inspector = inspect(model)
        for column in inspector.columns:
            col_name = column.name
            col_type = str(column.type)
            
            # Marcar primary keys
            if column.primary_key:
                lines.append(f'  + {col_name} : {col_type} <<PK>>')
            elif column.foreign_keys:
                lines.append(f'  # {col_name} : {col_type} <<FK>>')
            else:
                lines.append(f'  {col_name} : {col_type}')
        
        lines.append('}')
        lines.append('')
    
    # Generar relaciones (FK)
    for model in models:
        inspector = inspect(model)
        for column in inspector.columns:
            if column.foreign_keys:
                for fk in column.foreign_keys:
                    # Obtener tabla y columna referenciada
                    target_table = fk.column.table.name
                    
                    # Buscar modelo de destino
                    target_model = None
                    for m in models:
                        if m.__tablename__ == target_table:
                            target_model = m.__name__
                            break
                    
                    if target_model:
                        lines.append(f'{model.__name__} --> {target_model}')
    
    lines.append('')
    lines.append('@enduml')
    
    return '\n'.join(lines)

def main():
    """Función principal."""
    print("🔍 Generando diagrama ERD desde modelos SQLAlchemy...")
    
    try:
        plantuml_code = generate_plantuml_erd()
        
        output_path = 'docs/diagrams/ERD_database.puml'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)
        
        print(f"✅ Diagrama ERD generado exitosamente en: {output_path}")
        print("\n📝 Para generar PNG, ejecuta uno de estos comandos:")
        print(f"   1. java -jar plantuml.jar {output_path}")
        print(f"   2. Sube el código a https://www.plantuml.com/plantuml/uml/")
        print(f"   3. Usa VSCode PlantUML extension (Alt+D para preview)")
        
    except Exception as e:
        print(f"❌ Error al generar ERD: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
