"""
Base Handler with Generic CRUD Operations

Elimina duplicación de código en handlers implementando
métodos CRUD genéricos reutilizables.

Uso:
    class QuoteHandler(BaseHandler):
        def __init__(self):
            super().__init__(Quote)
        
        # Métodos personalizados adicionales aquí
"""

from app import db
from sqlalchemy.exc import IntegrityError


class BaseHandler:
    """
    Handler base con operaciones CRUD genéricas.
    
    Todos los handlers específicos deben heredar de esta clase
    para reutilizar funcionalidad común.
    
    Attributes:
        model (db.Model): Modelo SQLAlchemy a manejar
    """
    
    def __init__(self, model):
        """
        Inicializa el handler con un modelo específico.
        
        Args:
            model (db.Model): Clase del modelo SQLAlchemy
        """
        self.model = model
    
    def create(self, **kwargs):
        """
        Crea una nueva entidad en la base de datos.
        
        Args:
            **kwargs: Campos del modelo a crear
        
        Returns:
            model: Instancia creada
        
        Raises:
            IntegrityError: Si hay violación de constraints
            ValueError: Si faltan campos requeridos
        
        Example:
            handler = QuoteHandler()
            quote = handler.create(
                organization_id=1,
                client_name='Test Client',
                status='pending'
            )
        """
        try:
            instance = self.model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise
    
    def get(self, id):
        """
        Obtiene una entidad por ID.
        
        Args:
            id (int): ID de la entidad
        
        Returns:
            model: Instancia encontrada o None
        
        Example:
            quote = handler.get(1)
            if quote:
                print(quote.client_name)
        """
        return self.model.query.get(id)
    
    def list_all(self, page=1, per_page=10, status=None, **filters):
        """
        Lista entidades con paginación y filtros opcionales.
        
        Args:
            page (int): Número de página (default: 1)
            per_page (int): Items por página (default: 10)
            status (str): Filtrar por status (opcional)
            **filters: Filtros adicionales (ej: organization_id=1)
        
        Returns:
            dict: {
                'items': [instances],
                'total': int,
                'page': int,
                'per_page': int,
                'total_pages': int
            }
        
        Example:
            # Sin filtros
            result = handler.list_all(page=1, per_page=10)
            
            # Con status
            result = handler.list_all(page=1, status='active')
            
            # Con filtros custom
            result = handler.list_all(page=1, organization_id=1)
        """
        query = self.model.query
        
        # Aplicar filtro de status si el modelo lo tiene
        if status and hasattr(self.model, 'status'):
            query = query.filter_by(status=status)
        
        # Aplicar filtros adicionales
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter_by(**{key: value})
        
        # Ordenar por fecha de creación descendente (más recientes primero)
        if hasattr(self.model, 'creation_date'):
            query = query.order_by(self.model.creation_date.desc())
        
        # Paginar
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update(self, id, **kwargs):
        """
        Actualiza una entidad existente.
        
        Args:
            id (int): ID de la entidad a actualizar
            **kwargs: Campos a actualizar
        
        Returns:
            model: Instancia actualizada o None si no existe
        
        Example:
            quote = handler.update(1, status='approved')
            if quote:
                print(f"Status updated: {quote.status}")
        """
        instance = self.get(id)
        if not instance:
            return None
        
        try:
            # Actualizar campos
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            # Actualizar update_date si existe
            if hasattr(instance, 'update_date'):
                from datetime import datetime
                instance.update_date = datetime.utcnow()
            
            db.session.commit()
            return instance
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise
    
    def delete(self, id):
        """
        Elimina una entidad por ID.
        
        Args:
            id (int): ID de la entidad a eliminar
        
        Returns:
            bool: True si se eliminó, False si no existe
        
        Example:
            if handler.delete(1):
                print("Deleted successfully")
            else:
                print("Not found")
        """
        instance = self.get(id)
        if not instance:
            return False
        
        try:
            db.session.delete(instance)
            db.session.commit()
            return True
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"No se puede eliminar: tiene registros relacionados")
        except Exception as e:
            db.session.rollback()
            raise
    
    def count(self, status=None, **filters):
        """
        Cuenta entidades con filtros opcionales.
        
        Args:
            status (str): Filtrar por status (opcional)
            **filters: Filtros adicionales
        
        Returns:
            int: Número de registros
        
        Example:
            # Total
            total = handler.count()
            
            # Por status
            active = handler.count(status='active')
            
            # Con filtros custom
            org_items = handler.count(organization_id=1)
        """
        query = self.model.query
        
        if status and hasattr(self.model, 'status'):
            query = query.filter_by(status=status)
        
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter_by(**{key: value})
        
        return query.count()
    
    def exists(self, id):
        """
        Verifica si una entidad existe.
        
        Args:
            id (int): ID a verificar
        
        Returns:
            bool: True si existe, False si no
        
        Example:
            if handler.exists(1):
                print("Record exists")
        """
        return self.get(id) is not None
    
    def get_by_field(self, field_name, field_value):
        """
        Obtiene entidades por un campo específico.
        
        Args:
            field_name (str): Nombre del campo
            field_value: Valor a buscar
        
        Returns:
            list: Lista de instancias encontradas
        
        Example:
            # Buscar por email
            users = handler.get_by_field('email', 'test@example.com')
            
            # Buscar por username
            users = handler.get_by_field('username', 'admin')
        """
        if not hasattr(self.model, field_name):
            raise ValueError(f"El modelo {self.model.__name__} no tiene el campo '{field_name}'")
        
        return self.model.query.filter_by(**{field_name: field_value}).all()
    
    def bulk_create(self, instances_data):
        """
        Crea múltiples instancias en una transacción.
        
        Args:
            instances_data (list): Lista de dicts con datos de instancias
        
        Returns:
            list: Instancias creadas
        
        Raises:
            ValueError: Si falla la transacción
        
        Example:
            quotes_data = [
                {'client_name': 'Client 1', 'status': 'pending'},
                {'client_name': 'Client 2', 'status': 'pending'}
            ]
            quotes = handler.bulk_create(quotes_data)
        """
        try:
            instances = []
            for data in instances_data:
                instance = self.model(**data)
                db.session.add(instance)
                instances.append(instance)
            
            db.session.commit()
            return instances
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error en bulk_create: {str(e)}")
    
    def bulk_delete(self, ids):
        """
        Elimina múltiples entidades por IDs.
        
        Args:
            ids (list): Lista de IDs a eliminar
        
        Returns:
            int: Número de registros eliminados
        
        Example:
            deleted_count = handler.bulk_delete([1, 2, 3])
            print(f"Deleted {deleted_count} records")
        """
        try:
            query = self.model.query.filter(self.model.id.in_(ids))
            count = query.delete(synchronize_session=False)
            db.session.commit()
            return count
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error en bulk_delete: {str(e)}")
