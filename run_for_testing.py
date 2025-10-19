"""
Script para ejecutar el servidor Flask sin debug mode para testing
"""
print("Iniciando servidor Flask para testing...")
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Sin debug mode para evitar reloads automáticos
    app.run(debug=False, host='127.0.0.1', port=5000)
