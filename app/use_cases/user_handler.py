"""
User Handler - Use Case Layer
Gestiona la lógica de aplicación para operaciones con usuarios.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.user import User


class UserHandler:
    """Handler para gestionar operaciones con usuarios."""
    
    def create_user(self, username: str, password: str, role_id: int, status: str = 'active') -> User:
        """
        Crea un nuevo usuario.
        
        Args:
            username: Nombre de usuario único.
            password: Contraseña (debe estar hasheada antes de llamar).
            role_id: ID del rol asociado.
            status: Estado inicial del usuario.
        
        Returns:
            User: El usuario creado.
        
        Raises:
            ValueError: Si el username ya existe o los datos son inválidos.
        """
        # Validar que no exista el username
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValueError(f"El usuario con username '{username}' ya existe")
        
        # Validar role_id
        if not role_id or role_id <= 0:
            raise ValueError("El role_id es requerido y debe ser mayor a 0")
        
        try:
            user = User(
                username=username,
                password=password,
                role_id=role_id,
                status=status
            )
            db.session.add(user)
            db.session.commit()
            return user
        
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear usuario: {str(e)}")
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            user_id: ID del usuario.
        
        Returns:
            User o None si no existe.
        """
        return User.query.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Busca un usuario por su nombre de usuario.
        
        Args:
            username: Nombre de usuario a buscar.
        
        Returns:
            User o None si no existe.
        """
        return User.query.filter_by(username=username).first()
    
    def list_users(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> Dict[str, Any]:
        """
        Lista usuarios con paginación.
        
        Args:
            page: Número de página (default: 1).
            per_page: Usuarios por página (default: 10).
            status: Filtrar por status (opcional).
        
        Returns:
            dict: {
                'users': [User],
                'total': int,
                'page': int,
                'per_page': int,
                'total_pages': int
            }
        """
        query = User.query
        
        # Filtrar por status si se especifica
        if status:
            query = query.filter_by(status=status)
        
        # Ordenar por fecha de creación (más recientes primero)
        if hasattr(User, 'creation_date'):
            query = query.order_by(User.creation_date.desc())
        else:
            query = query.order_by(User.id.desc())
        
        # Paginar
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'users': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def list_active_users(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista solo los usuarios activos con paginación.
        
        Args:
            page: Número de página.
            per_page: Usuarios por página.
        
        Returns:
            dict: Resultado paginado de usuarios activos.
        """
        return self.list_users(page=page, per_page=per_page, status='active')
    
    def update_password(self, user_id: int, new_password: str) -> User:
        """
        Actualiza la contraseña de un usuario.
        
        Args:
            user_id: ID del usuario.
            new_password: Nueva contraseña (ya hasheada).
        
        Returns:
            User: El usuario actualizado.
        
        Raises:
            ValueError: Si el usuario no existe.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"El usuario con ID '{user_id}' no existe")
        
        try:
            user.update_password(new_password)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar contraseña: {str(e)}")
    
    def activate_user(self, user_id: int) -> User:
        """
        Activa un usuario.
        
        Args:
            user_id: ID del usuario.
        
        Returns:
            User: El usuario activado.
        
        Raises:
            ValueError: Si el usuario no existe.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"El usuario con ID '{user_id}' no existe")
        
        try:
            user.activate()
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al activar usuario: {str(e)}")
    
    def inactivate_user(self, user_id: int) -> User:
        """
        Inactiva un usuario.
        
        Args:
            user_id: ID del usuario.
        
        Returns:
            User: El usuario inactivado.
        
        Raises:
            ValueError: Si el usuario no existe.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"El usuario con ID '{user_id}' no existe")
        
        try:
            user.inactivate()
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al inactivar usuario: {str(e)}")
    
    def suspend_user(self, user_id: int) -> User:
        """
        Suspende un usuario.
        
        Args:
            user_id: ID del usuario.
        
        Returns:
            User: El usuario suspendido.
        
        Raises:
            ValueError: Si el usuario no existe.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"El usuario con ID '{user_id}' no existe")
        
        try:
            user.suspend()
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al suspender usuario: {str(e)}")
    
    def delete_user(self, user_id: int) -> bool:
        """
        Elimina un usuario de forma permanente.
        
        Args:
            user_id: ID del usuario a eliminar.
        
        Returns:
            bool: True si se eliminó, False si no existía.
        """
        user = User.query.get(user_id)
        if not user:
            return False
        
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al eliminar usuario: {str(e)}")
    
    def count_users(self, status: Optional[str] = None) -> int:
        """
        Cuenta el total de usuarios, opcionalmente filtrado por status.
        
        Args:
            status: Estado a filtrar (opcional).
        
        Returns:
            int: Cantidad de usuarios.
        """
        query = User.query
        if status:
            query = query.filter_by(status=status)
        return query.count()
    
    def get_user_statistics(self) -> Dict[str, int]:
        """
        Obtiene estadísticas de usuarios por estado.
        
        Returns:
            dict: {'active': int, 'inactive': int, 'suspended': int, 'total': int}
        """
        return {
            'active': self.count_users('active'),
            'inactive': self.count_users('inactive'),
            'suspended': self.count_users('suspended'),
            'total': self.count_users()
        }
