from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models import User

# Define el namespace para Swagger
user_ns = Namespace("users", description="Operaciones sobre usuarios")

# Define el modelo para Swagger
user_model = user_ns.model("User", {
    "id": fields.Integer(readonly=True),
    "username": fields.String(required=True, description="Nombre de usuario"),
    "password": fields.String(required=True, description="Contraseña"),
    "role_id": fields.Integer(required=True, description="ID del rol asociado")
})

# Endpoint para listar y crear usuarios
@user_ns.route("/")
class UserList(Resource):
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """Listar todos los usuarios"""
        return User.query.all()

    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        """Crear un nuevo usuario"""
        data = request.json
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

# Endpoint para operaciones sobre un usuario específico
@user_ns.route("/<int:id>")
class UserDetail(Resource):
    @user_ns.marshal_with(user_model)
    def get(self, id):
        """Obtener un usuario por ID"""
        return User.query.get_or_404(id)

    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model)
    def put(self, id):
        """Actualizar un usuario existente"""
        user = User.query.get_or_404(id)
        data = request.json
        user.username = data["username"]
        user.password = data["password"]
        user.role_id = data["role_id"]
        db.session.commit()
        return user

    def delete(self, id):
        """Eliminar un usuario"""
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Usuario eliminado"}, 204
