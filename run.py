print("Daniel añadió el comentario: Daniel abrió el proyecto")
from app import create_app

app = create_app()   

if __name__ == "__main__":
    app.run(debug=True)
