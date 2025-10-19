print("lanzamiento de servidor flask y api multicont")
from app import create_app

app = create_app()   

if __name__ == "__main__":
    app.run(debug=True)
