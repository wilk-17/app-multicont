from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models.user import User
from app.models.role import Role
from app.models.person import Person
from app.models.employee import Employee
from app.models.organization import Organization
from app.models.branch import Branch
from app.models.state import State
from app.models.city import City
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.item_category import ItemCategory
from app.models.inventory_item import InventoryItem
from app.models.assignment import Assignment
from app.models.quote import Quote
from app.models.quotation_line import QuotationLine
from app.models.quote_item import QuoteItem
from app.models.sales_order import SalesOrder
from app.models.sales_order_item import SalesOrderItem
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
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

from app.models import (
    Role, Person, Employee, Organization, Branch, State, City,
    Permission, UserRole, ItemCategory, InventoryItem, Assignment,
    Quote, QuotationLine, QuoteItem, SalesOrder, SalesOrderItem, Invoice, InvoiceItem
)

# ========== ROLES ==========
role_ns = Namespace("role", description="Operaciones sobre roles")
role_model = role_ns.model("Role", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True)
})

@role_ns.route("/")
class RoleList(Resource):
    @role_ns.marshal_list_with(role_model)
    def get(self):
        return Role.query.all()

    @role_ns.expect(role_model)
    @role_ns.marshal_with(role_model, code=201)
    def post(self):
        data = request.json
        obj = Role(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@role_ns.route("/<int:id>")
class RoleDetail(Resource):
    @role_ns.marshal_with(role_model)
    def get(self, id):
        return Role.query.get_or_404(id)

    @role_ns.expect(role_model)
    @role_ns.marshal_with(role_model)
    def put(self, id):
        obj = Role.query.get_or_404(id)
        obj.name = request.json["name"]
        db.session.commit()
        return obj

    def delete(self, id):
        obj = Role.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Rol eliminado"}, 204

# ========== PERSONAS ==========
person_ns = Namespace("person", description="Operaciones sobre personas")
person_model = person_ns.model("Person", {
    "id": fields.Integer(readonly=True),
    "dni": fields.String(),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "address": fields.String(),
    "phone": fields.String(),
    "city_id": fields.Integer()
})

@person_ns.route("/")
class PersonList(Resource):
    @person_ns.marshal_list_with(person_model)
    def get(self):
        return Person.query.all()

    @person_ns.expect(person_model)
    @person_ns.marshal_with(person_model, code=201)
    def post(self):
        data = request.json
        obj = Person(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@person_ns.route("/<int:id>")
class PersonDetail(Resource):
    @person_ns.marshal_with(person_model)
    def get(self, id):
        return Person.query.get_or_404(id)

    @person_ns.expect(person_model)
    @person_ns.marshal_with(person_model)
    def put(self, id):
        obj = Person.query.get_or_404(id)
        for key in ["dni", "first_name", "last_name", "address", "phone", "city_id"]:
            if key in request.json:
                setattr(obj, key, request.json[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = Person.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Persona eliminada"}, 204

# ========== EMPLEADOS ==========
employee_ns = Namespace("employee", description="Operaciones sobre empleados")
employee_model = employee_ns.model("Employee", {
    "id": fields.Integer(readonly=True),
    "person_id": fields.Integer(required=True),
    "branch_id": fields.Integer(required=True)
})

@employee_ns.route("/")
class EmployeeList(Resource):
    @employee_ns.marshal_list_with(employee_model)
    def get(self):
        return Employee.query.all()

    @employee_ns.expect(employee_model)
    @employee_ns.marshal_with(employee_model, code=201)
    def post(self):
        data = request.json
        obj = Employee(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@employee_ns.route("/<int:id>")
class EmployeeDetail(Resource):
    @employee_ns.marshal_with(employee_model)
    def get(self, id):
        return Employee.query.get_or_404(id)

    @employee_ns.expect(employee_model)
    @employee_ns.marshal_with(employee_model)
    def put(self, id):
        obj = Employee.query.get_or_404(id)
        for key in ["person_id", "branch_id"]:
            if key in request.json:
                setattr(obj, key, request.json[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = Employee.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Empleado eliminado"}, 204

# ========== ORGANIZACIONES ==========
organization_ns = Namespace("organization", description="Operaciones sobre organizaciones")
organization_model = organization_ns.model("Organization", {
    "id": fields.Integer(readonly=True),
    "historical_name": fields.String(required=True),
    "current_name": fields.String(required=True)
})

@organization_ns.route("/")
class OrganizationList(Resource):
    @organization_ns.marshal_list_with(organization_model)
    def get(self):
        return Organization.query.all()

    @organization_ns.expect(organization_model)
    @organization_ns.marshal_with(organization_model, code=201)
    def post(self):
        data = request.json
        obj = Organization(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@organization_ns.route("/<int:id>")
class OrganizationDetail(Resource):
    @organization_ns.marshal_with(organization_model)
    def get(self, id):
        return Organization.query.get_or_404(id)

    @organization_ns.expect(organization_model)
    @organization_ns.marshal_with(organization_model)
    def put(self, id):
        obj = Organization.query.get_or_404(id)
        for key in ["historical_name", "current_name"]:
            if key in request.json:
                setattr(obj, key, request.json[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = Organization.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Organización eliminada"}, 204

# ========== SUCURSALES ==========
branch_ns = Namespace("branch", description="Operaciones sobre sucursales")
branch_model = branch_ns.model("Branch", {
    "id": fields.Integer(readonly=True),
    "organization_id": fields.Integer(required=True),
    "city_id": fields.Integer(required=True)
})

@branch_ns.route("/")
class BranchList(Resource):
    @branch_ns.marshal_list_with(branch_model)
    def get(self):
        return Branch.query.all()

    @branch_ns.expect(branch_model)
    @branch_ns.marshal_with(branch_model, code=201)
    def post(self):
        data = request.json
        obj = Branch(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@branch_ns.route("/<int:id>")
class BranchDetail(Resource):
    @branch_ns.marshal_with(branch_model)
    def get(self, id):
        return Branch.query.get_or_404(id)

    @branch_ns.expect(branch_model)
    @branch_ns.marshal_with(branch_model)
    def put(self, id):
        obj = Branch.query.get_or_404(id)
        for key in ["organization_id", "city_id"]:
            if key in request.json:
                setattr(obj, key, request.json[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = Branch.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Sucursal eliminada"}, 204

# ========== ESTADOS ==========
state_ns = Namespace("state", description="Operaciones sobre estados")
state_model = state_ns.model("State", {
    "id": fields.Integer(readonly=True),
    "description": fields.String(required=True),
    "code": fields.String(required=True)
})

@state_ns.route("/")
class StateList(Resource):
    @state_ns.marshal_list_with(state_model)
    def get(self):
        return State.query.all()

    @state_ns.expect(state_model)
    @state_ns.marshal_with(state_model, code=201)
    def post(self):
        data = request.json
        obj = State(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@state_ns.route("/<int:id>")
class StateDetail(Resource):
    @state_ns.marshal_with(state_model)
    def get(self, id):
        return State.query.get_or_404(id)

    @state_ns.expect(state_model)
    @state_ns.marshal_with(state_model)
    def put(self, id):
        obj = State.query.get_or_404(id)
        for key in ["description", "code"]:
            if key in request.json:
                setattr(obj, key, request.json[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = State.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Estado eliminado"}, 204

# ========== CIUDADES ==========
city_ns = Namespace("city", description="Operaciones sobre ciudades")
city_model = city_ns.model("City", {
    "id": fields.Integer(readonly=True),
    "description": fields.String(required=True),
    "code": fields.String(),
    "state_id": fields.Integer(required=True)
})

@city_ns.route("/")
class CityList(Resource):
    @city_ns.marshal_list_with(city_model)
    def get(self):
        return City.query.all()

    @city_ns.expect(city_model)
    @city_ns.marshal_with(city_model, code=201)
    def post(self):
        data = request.json
        obj = City(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@city_ns.route("/<int:id>")
class CityDetail(Resource):
    @city_ns.marshal_with(city_model)
    def get(self, id):
        return City.query.get_or_404(id)

    @city_ns.expect(city_model)
    @city_ns.marshal_with(city_model)
    def put(self, id):
        obj = City.query.get_or_404(id)
        for key in ["description", "code", "state_id"]:
            if key in request.json:
                setattr(obj, key, request.json[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = City.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Ciudad eliminada"}, 204

# ========== PERMISSION ==========
permission_ns = Namespace("permission", description="Operaciones sobre permisos")
permission_model = permission_ns.model("Permission", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True)
})

@permission_ns.route("/")
class PermissionList(Resource):
    @permission_ns.marshal_list_with(permission_model)
    def get(self):
        return Permission.query.all()

    @permission_ns.expect(permission_model)
    @permission_ns.marshal_with(permission_model, code=201)
    def post(self):
        data = request.json
        obj = Permission(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@permission_ns.route("/<int:id>")
class PermissionDetail(Resource):
    @permission_ns.marshal_with(permission_model)
    def get(self, id):
        return Permission.query.get_or_404(id)

    @permission_ns.expect(permission_model)
    @permission_ns.marshal_with(permission_model)
    def put(self, id):
        obj = Permission.query.get_or_404(id)
        obj.name = request.json["name"]
        db.session.commit()
        return obj

    def delete(self, id):
        obj = Permission.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Permiso eliminado"}, 204

# ========== USER ROLE ==========
user_role_ns = Namespace("user_role", description="Operaciones sobre roles de usuario")
user_role_model = user_role_ns.model("UserRole", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer(required=True),
    "role_id": fields.Integer(required=True)
})

@user_role_ns.route("/")
class UserRoleList(Resource):
    @user_role_ns.marshal_list_with(user_role_model)
    def get(self):
        return UserRole.query.all()

    @user_role_ns.expect(user_role_model)
    @user_role_ns.marshal_with(user_role_model, code=201)
    def post(self):
        data = request.json
        obj = UserRole(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@user_role_ns.route("/<int:id>")
class UserRoleDetail(Resource):
    @user_role_ns.marshal_with(user_role_model)
    def get(self, id):
        return UserRole.query.get_or_404(id)

    @user_role_ns.expect(user_role_model)
    @user_role_ns.marshal_with(user_role_model)
    def put(self, id):
        obj = UserRole.query.get_or_404(id)
        data = request.json
        for key in ["user_id", "role_id"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = UserRole.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "UserRole eliminado"}, 204

# ========== ASSIGNMENT ==========
assignment_ns = Namespace("assignment", description="Operaciones sobre asignaciones")
assignment_model = assignment_ns.model("Assignment", {
    "id": fields.Integer(readonly=True),
    "employee_id": fields.Integer(required=True),
    "item_id": fields.Integer(required=True),
    "assigned_date": fields.Date(required=True),
})

@assignment_ns.route("/")
class AssignmentList(Resource):
    @assignment_ns.marshal_list_with(assignment_model)
    def get(self):
        return Assignment.query.all()

    @assignment_ns.expect(assignment_model)
    @assignment_ns.marshal_with(assignment_model, code=201)
    def post(self):
        data = request.json
        obj = Assignment(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@assignment_ns.route("/<int:id>")
class AssignmentDetail(Resource):
    @assignment_ns.marshal_with(assignment_model)
    def get(self, id):
        return Assignment.query.get_or_404(id)

    @assignment_ns.expect(assignment_model)
    @assignment_ns.marshal_with(assignment_model)
    def put(self, id):
        obj = Assignment.query.get_or_404(id)
        data = request.json
        for key in ["employee_id", "item_id", "assigned_date"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = Assignment.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Assignment eliminado"}, 204

# ========== INVENTORY ITEM ==========
inventory_item_ns = Namespace("inventory_item", description="Operaciones sobre items de inventario")
inventory_item_model = inventory_item_ns.model("InventoryItem", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "description": fields.String(),
    "category_id": fields.Integer(),
})

@inventory_item_ns.route("/")
class InventoryItemList(Resource):
    @inventory_item_ns.marshal_list_with(inventory_item_model)
    def get(self):
        return InventoryItem.query.all()

    @inventory_item_ns.expect(inventory_item_model)
    @inventory_item_ns.marshal_with(inventory_item_model, code=201)
    def post(self):
        data = request.json
        obj = InventoryItem(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@inventory_item_ns.route("/<int:id>")
class InventoryItemDetail(Resource):
    @inventory_item_ns.marshal_with(inventory_item_model)
    def get(self, id):
        return InventoryItem.query.get_or_404(id)

    @inventory_item_ns.expect(inventory_item_model)
    @inventory_item_ns.marshal_with(inventory_item_model)
    def put(self, id):
        obj = InventoryItem.query.get_or_404(id)
        data = request.json
        for key in ["name", "description", "category_id"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = InventoryItem.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "InventoryItem eliminado"}, 204

# ========== QUOTE ==========
quote_ns = Namespace("quote", description="Operaciones sobre cotizaciones")
quote_model = quote_ns.model("Quote", {
    "id": fields.Integer(readonly=True),
    "customer_name": fields.String(required=True),
    "date": fields.Date(required=True),
    "total": fields.Float(required=True)
})

@quote_ns.route("/")
class QuoteList(Resource):
    @quote_ns.marshal_list_with(quote_model)
    def get(self):
        return Quote.query.all()

    @quote_ns.expect(quote_model)
    @quote_ns.marshal_with(quote_model, code=201)
    def post(self):
        data = request.json
        obj = Quote(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@quote_ns.route("/<int:id>")
class QuoteDetail(Resource):
    @quote_ns.marshal_with(quote_model)
    def get(self, id):
        return Quote.query.get_or_404(id)

    @quote_ns.expect(quote_model)
    @quote_ns.marshal_with(quote_model)
    def put(self, id):
        obj = Quote.query.get_or_404(id)
        data = request.json
        for key in ["customer_name", "date", "total"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = Quote.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Quote eliminado"}, 204

# ========== QUOTATION LINE ==========
quotation_line_ns = Namespace("quotation_line", description="Operaciones sobre líneas de cotización")
quotation_line_model = quotation_line_ns.model("QuotationLine", {
    "id": fields.Integer(readonly=True),
    "quote_id": fields.Integer(required=True),
    "description": fields.String(required=True),
    "quantity": fields.Integer(required=True),
    "price": fields.Float(required=True),
    "item_id": fields.Integer()
})

@quotation_line_ns.route("/")
class QuotationLineList(Resource):
    @quotation_line_ns.marshal_list_with(quotation_line_model)
    def get(self):
        return QuotationLine.query.all()

    @quotation_line_ns.expect(quotation_line_model)
    @quotation_line_ns.marshal_with(quotation_line_model, code=201)
    def post(self):
        data = request.json
        obj = QuotationLine(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@quotation_line_ns.route("/<int:id>")
class QuotationLineDetail(Resource):
    @quotation_line_ns.marshal_with(quotation_line_model)
    def get(self, id):
        return QuotationLine.query.get_or_404(id)

    @quotation_line_ns.expect(quotation_line_model)
    @quotation_line_ns.marshal_with(quotation_line_model)
    def put(self, id):
        obj = QuotationLine.query.get_or_404(id)
        data = request.json
        # Reemplaza los campos por los que tenga tu modelo QuotationLine
        for key in ["quote_id", "description", "quantity", "price", "item_id"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = QuotationLine.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "QuotationLine eliminado"}, 204

# ========== QUOTE ITEM ==========
quote_item_ns = Namespace("quote_item", description="Operaciones sobre items de cotización")
quote_item_model = quote_item_ns.model("QuoteItem", {
    "id": fields.Integer(readonly=True),
    "quote_id": fields.Integer(required=True),
    "item_id": fields.Integer(required=True),
    "quantity": fields.Integer(required=True)
})

@quote_item_ns.route("/")
class QuoteItemList(Resource):
    @quote_item_ns.marshal_list_with(quote_item_model)
    def get(self):
        return QuoteItem.query.all()

    @quote_item_ns.expect(quote_item_model)
    @quote_item_ns.marshal_with(quote_item_model, code=201)
    def post(self):
        data = request.json
        obj = QuoteItem(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@quote_item_ns.route("/<int:id>")
class QuoteItemDetail(Resource):
    @quote_item_ns.marshal_with(quote_item_model)
    def get(self, id):
        return QuoteItem.query.get_or_404(id)

    @quote_item_ns.expect(quote_item_model)
    @quote_item_ns.marshal_with(quote_item_model)
    def put(self, id):
        obj = QuoteItem.query.get_or_404(id)
        data = request.json
        for key in ["quote_id", "item_id", "quantity"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = QuoteItem.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "QuoteItem eliminado"}, 204

# ========== SALES ORDER ==========
sales_order_ns = Namespace("sales_order", description="Operaciones sobre órdenes de venta")
sales_order_model = sales_order_ns.model("SalesOrder", {
    "id": fields.Integer(readonly=True),
    "quote_id": fields.Integer(required=True),
    "date": fields.Date(required=True),
    "total": fields.Float(required=True)
})

@sales_order_ns.route("/")
class SalesOrderList(Resource):
    @sales_order_ns.marshal_list_with(sales_order_model)
    def get(self):
        return SalesOrder.query.all()

    @sales_order_ns.expect(sales_order_model)
    @sales_order_ns.marshal_with(sales_order_model, code=201)
    def post(self):
        data = request.json
        obj = SalesOrder(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@sales_order_ns.route("/<int:id>")
class SalesOrderDetail(Resource):
    @sales_order_ns.marshal_with(sales_order_model)
    def get(self, id):
        return SalesOrder.query.get_or_404(id)

    @sales_order_ns.expect(sales_order_model)
    @sales_order_ns.marshal_with(sales_order_model)
    def put(self, id):
        obj = SalesOrder.query.get_or_404(id)
        data = request.json
        for key in ["quote_id", "date", "total"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = SalesOrder.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "SalesOrder eliminado"}, 204

# ========== SALES ORDER ITEM ==========
sales_order_item_ns = Namespace("sales_order_item", description="Operaciones sobre items de orden de venta")
sales_order_item_model = sales_order_item_ns.model("SalesOrderItem", {
    "id": fields.Integer(readonly=True),
    "sales_order_id": fields.Integer(required=True),
    "item_id": fields.Integer(required=True),
    "quantity": fields.Integer(required=True)
})

@sales_order_item_ns.route("/")
class SalesOrderItemList(Resource):
    @sales_order_item_ns.marshal_list_with(sales_order_item_model)
    def get(self):
        return SalesOrderItem.query.all()

    @sales_order_item_ns.expect(sales_order_item_model)
    @sales_order_item_ns.marshal_with(sales_order_item_model, code=201)
    def post(self):
        data = request.json
        obj = SalesOrderItem(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@sales_order_item_ns.route("/<int:id>")
class SalesOrderItemDetail(Resource):
    @sales_order_item_ns.marshal_with(sales_order_item_model)
    def get(self, id):
        return SalesOrderItem.query.get_or_404(id)

    @sales_order_item_ns.expect(sales_order_item_model)
    @sales_order_item_ns.marshal_with(sales_order_item_model)
    def put(self, id):
        obj = SalesOrderItem.query.get_or_404(id)
        data = request.json
        for key in ["sales_order_id", "item_id", "quantity"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = SalesOrderItem.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "SalesOrderItem eliminado"}, 204

# ========== INVOICE ==========
invoice_ns = Namespace("invoice", description="Operaciones sobre facturas")
invoice_model = invoice_ns.model("Invoice", {
    "id": fields.Integer(readonly=True),
    "sales_order_id": fields.Integer(required=True),
    "quotation_line_id": fields.Integer(),
    "date": fields.Date(required=True),
    "total": fields.Float(required=True)
})

@invoice_ns.route("/")
class InvoiceList(Resource):
    @invoice_ns.marshal_list_with(invoice_model)
    def get(self):
        return Invoice.query.all()

    @invoice_ns.expect(invoice_model)
    @invoice_ns.marshal_with(invoice_model, code=201)
    def post(self):
        data = request.json
        obj = Invoice(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@invoice_ns.route("/<int:id>")
class InvoiceDetail(Resource):
    @invoice_ns.marshal_with(invoice_model)
    def get(self, id):
        return Invoice.query.get_or_404(id)

    @invoice_ns.expect(invoice_model)
    @invoice_ns.marshal_with(invoice_model)
    def put(self, id):
        obj = Invoice.query.get_or_404(id)
        data = request.json
        for key in ["sales_order_id", "quotation_line_id", "date", "total"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = Invoice.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "Invoice eliminado"}, 204

# ========== INVOICE ITEM ==========
invoice_item_ns = Namespace("invoice_item", description="Operaciones sobre items de factura")
invoice_item_model = invoice_item_ns.model("InvoiceItem", {
    "id": fields.Integer(readonly=True),
    "invoice_id": fields.Integer(required=True),
    "item_id": fields.Integer(required=True),
    "quantity": fields.Integer(required=True),
    "price": fields.Float(required=True)
})

@invoice_item_ns.route("/")
class InvoiceItemList(Resource):
    @invoice_item_ns.marshal_list_with(invoice_item_model)
    def get(self):
        return InvoiceItem.query.all()

    @invoice_item_ns.expect(invoice_item_model)
    @invoice_item_ns.marshal_with(invoice_item_model, code=201)
    def post(self):
        data = request.json
        obj = InvoiceItem(**data)
        db.session.add(obj)
        db.session.commit()
        return obj, 201

@invoice_item_ns.route("/<int:id>")
class InvoiceItemDetail(Resource):
    @invoice_item_ns.marshal_with(invoice_item_model)
    def get(self, id):
        return InvoiceItem.query.get_or_404(id)

    @invoice_item_ns.expect(invoice_item_model)
    @invoice_item_ns.marshal_with(invoice_item_model)
    def put(self, id):
        obj = InvoiceItem.query.get_or_404(id)
        data = request.json
        for key in ["invoice_id", "item_id", "quantity", "price"]:
            if key in data:
                setattr(obj, key, data[key])
        db.session.commit()
        return obj

    def delete(self, id):
        obj = InvoiceItem.query.get_or_404(id)
        db.session.delete(obj)
        db.session.commit()
        return {"message": "InvoiceItem eliminado"}, 204