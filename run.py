""" 
Daniel abrió el proyecto
"""
print("Daniel abrió el proyecto para añadir")
from app import create_app

app = create_app()   

if __name__ == "__main__":
    app.run(debug=True)
