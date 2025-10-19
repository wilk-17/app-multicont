"""
Script para refactorizar sales_analytics_api.py reemplazando jsonify con helpers
"""
import re

def fix_sales_analytics():
    file_path = 'app/api/sales_analytics_api.py'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazos específicos
    replacements = [
        # Errores de validación
        (
            r"return jsonify\(\{'success': False, 'error': 'start_date and end_date are required'\}\), 400",
            "return error_response('start_date and end_date are required', 400)"
        ),
        (
            r"return jsonify\(\{'success': False, 'error': 'period_type must be monthly, quarterly, or yearly'\}\), 400",
            "return error_response('period_type must be monthly, quarterly, or yearly', 400)"
        ),
        # Success responses simples
        (
            r"return jsonify\(\{'success': True, 'data': data\}\), 200",
            "return success_response(data, 'Datos obtenidos exitosamente', 200)"
        ),
        # Error responses
        (
            r"return jsonify\(\{'success': False, 'error': str\(e\)\}\), 500",
            "return error_response(str(e), 500)"
        ),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Caso especial: sales_summary con estructura compleja
    # Buscar el return jsonify con múltiples líneas
    summary_pattern = r"return jsonify\(\{\s+'success': True,\s+'data': \{[^}]+\}[^}]+\}\), 200"
    
    # Para el caso de sales_summary, lo dejamos manual después
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ sales_analytics_api.py refactorizado exitosamente")
    print(f"📝 Archivo actualizado: {file_path}")

if __name__ == '__main__':
    fix_sales_analytics()
