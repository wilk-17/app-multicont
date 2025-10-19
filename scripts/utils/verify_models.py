#!/usr/bin/env python3
"""
Script de Verificación de Modelos
Analiza todos los modelos (entities) para determinar:
- Nombres de columnas
- Parámetros del constructor __init__
- Campos requeridos vs opcionales
- Relaciones entre modelos
"""

import os
import re
import ast

def extract_model_info(filepath):
    """Extrae información completa del modelo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parsear con AST
    try:
        tree = ast.parse(content)
    except:
        return None
    
    model_info = {
        'class_name': None,
        'tablename': None,
        'columns': [],
        'init_params': [],
        'init_required': [],
        'init_optional': [],
        'relationships': []
    }
    
    for node in ast.walk(tree):
        # Encontrar la clase del modelo
        if isinstance(node, ast.ClassDef):
            model_info['class_name'] = node.name
            
            # Buscar __tablename__
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and target.id == '__tablename__':
                            if isinstance(item.value, ast.Constant):
                                model_info['tablename'] = item.value.value
            
            # Buscar __init__
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                    # Extraer parámetros
                    for arg in item.args.args[1:]:  # Skip 'self'
                        param_name = arg.arg
                        model_info['init_params'].append(param_name)
                        
                        # Verificar si tiene default (es opcional)
                        defaults_offset = len(item.args.args) - len(item.args.defaults) - 1
                        arg_index = item.args.args.index(arg) - 1
                        
                        if arg_index >= defaults_offset and len(item.args.defaults) > (arg_index - defaults_offset):
                            model_info['init_optional'].append(param_name)
                        else:
                            model_info['init_required'].append(param_name)
    
    # Extraer columnas usando regex (más confiable para esto)
    column_pattern = r'(\w+)\s*=\s*db\.Column\((.*?)\)'
    for match in re.finditer(column_pattern, content, re.MULTILINE):
        col_name = match.group(1)
        col_def = match.group(2)
        
        col_info = {
            'name': col_name,
            'type': None,
            'nullable': 'nullable=False' not in col_def,
            'primary_key': 'primary_key=True' in col_def,
            'foreign_key': 'ForeignKey' in col_def,
            'unique': 'unique=True' in col_def
        }
        
        # Extraer tipo
        if 'db.BigInteger' in col_def:
            col_info['type'] = 'BigInteger'
        elif 'db.Integer' in col_def:
            col_info['type'] = 'Integer'
        elif 'db.String' in col_def:
            size_match = re.search(r'db\.String\((\d+)\)', col_def)
            col_info['type'] = f"String({size_match.group(1)})" if size_match else 'String'
        elif 'db.Numeric' in col_def:
            col_info['type'] = 'Numeric'
        elif 'db.Date' in col_def:
            col_info['type'] = 'Date'
        elif 'db.DateTime' in col_def:
            col_info['type'] = 'DateTime'
        elif 'db.Boolean' in col_def:
            col_info['type'] = 'Boolean'
        elif 'db.Text' in col_def:
            col_info['type'] = 'Text'
        
        model_info['columns'].append(col_info)
    
    # Extraer relaciones
    relationship_pattern = r'(\w+)\s*=\s*db\.relationship\([\'"](\w+)[\'"]'
    for match in re.finditer(relationship_pattern, content):
        rel_name = match.group(1)
        rel_model = match.group(2)
        model_info['relationships'].append({
            'name': rel_name,
            'model': rel_model
        })
    
    return model_info


def scan_all_models():
    """Escanea todos los modelos en app/entities/"""
    entities_dir = 'app/entities'
    models = {}
    
    for filename in os.listdir(entities_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            filepath = os.path.join(entities_dir, filename)
            model_info = extract_model_info(filepath)
            
            if model_info and model_info['class_name']:
                models[model_info['class_name']] = model_info
    
    return models


def print_model_report(models):
    """Imprime reporte detallado de todos los modelos"""
    print("="*100)
    print(" 📊 REPORTE COMPLETO DE MODELOS DE BASE DE DATOS")
    print("="*100)
    print()
    
    for model_name in sorted(models.keys()):
        model = models[model_name]
        
        print(f"📦 {model_name}")
        print(f"   Tabla: {model['tablename']}")
        print()
        
        # Constructor
        print(f"   🔧 Constructor __init__:")
        if model['init_required']:
            print(f"      Requeridos: {', '.join(model['init_required'])}")
        if model['init_optional']:
            print(f"      Opcionales: {', '.join(model['init_optional'])}")
        if not model['init_params']:
            print(f"      ⚠️  Sin constructor personalizado")
        print()
        
        # Columnas
        print(f"   📋 Columnas ({len(model['columns'])}):")
        for col in model['columns']:
            flags = []
            if col['primary_key']:
                flags.append('PK')
            if not col['nullable']:
                flags.append('NOT NULL')
            if col['unique']:
                flags.append('UNIQUE')
            if col['foreign_key']:
                flags.append('FK')
            
            flags_str = f" [{', '.join(flags)}]" if flags else ""
            print(f"      • {col['name']}: {col['type']}{flags_str}")
        print()
        
        # Relaciones
        if model['relationships']:
            print(f"   🔗 Relaciones:")
            for rel in model['relationships']:
                print(f"      • {rel['name']} → {rel['model']}")
            print()
        
        print("-"*100)
        print()


def generate_population_template(models):
    """Genera template de código para población basado en los modelos"""
    print("="*100)
    print(" 📝 TEMPLATE DE CÓDIGO PARA POBLACIÓN")
    print("="*100)
    print()
    
    for model_name in sorted(models.keys()):
        model = models[model_name]
        
        if not model['init_params']:
            continue
        
        print(f"# {model_name}")
        print(f"{model_name.lower()} = {model_name}(")
        
        for i, param in enumerate(model['init_required']):
            comma = "," if i < len(model['init_required']) - 1 or model['init_optional'] else ""
            print(f"    {param}=...{comma}  # REQUERIDO")
        
        for i, param in enumerate(model['init_optional']):
            comma = "," if i < len(model['init_optional']) - 1 else ""
            print(f"    {param}=...{comma}  # Opcional")
        
        print(f")")
        print()


def check_inconsistencies(models):
    """Detecta inconsistencias entre columnas y constructor"""
    print("="*100)
    print(" ⚠️  VERIFICACIÓN DE CONSISTENCIA")
    print("="*100)
    print()
    
    issues_found = False
    
    for model_name in sorted(models.keys()):
        model = models[model_name]
        issues = []
        
        # Verificar columnas NOT NULL que no están en constructor
        for col in model['columns']:
            if not col['nullable'] and not col['primary_key'] and col['name'] not in model['init_params']:
                issues.append(f"Columna '{col['name']}' es NOT NULL pero no está en __init__")
        
        # Verificar parámetros del constructor que no son columnas
        col_names = [col['name'] for col in model['columns']]
        for param in model['init_params']:
            if param not in col_names and param != 'id':
                issues.append(f"Parámetro '{param}' en __init__ no corresponde a ninguna columna")
        
        if issues:
            issues_found = True
            print(f"❌ {model_name}:")
            for issue in issues:
                print(f"   • {issue}")
            print()
    
    if not issues_found:
        print("✅ No se encontraron inconsistencias")
        print()


def main():
    """Ejecuta análisis completo"""
    print()
    print("🔍 Escaneando modelos...")
    print()
    
    models = scan_all_models()
    
    print(f"✓ {len(models)} modelos encontrados")
    print()
    
    # Reporte detallado
    print_model_report(models)
    
    # Verificación de consistencia
    check_inconsistencies(models)
    
    # Template de población
    generate_population_template(models)
    
    print("="*100)
    print(" ✅ ANÁLISIS COMPLETADO")
    print("="*100)
    print()
    print("📝 Usa esta información para crear el script de población correcto")
    print()


if __name__ == "__main__":
    main()
