"""
User Handler - Use Case Layer
Gestiona la lógica de aplicación para operaciones con usuarios.
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.exc import IntegrityError
from app import db
from app.entities.user import User


class UserHandler:
    """Handler para gestionar operaciones con usuarios."""
    
    def create_user(self, username: str, password: str, role_id: int) -> User:
        """
        Crea un nuevo usuario.
        
        Args:
            username: Nombre de usuario único.
            password: Contraseña (debe estar hasheada antes de llamar).
            role_id: ID del rol asociado.
        
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
                role_id=role_id
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
    
    def list_users(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista usuarios con paginación.
        
        Args:
            page: Número de página (default: 1).
            per_page: Usuarios por página (default: 10).
        
        Returns:
            dict: {
                'users': [User],
                'total': int,
                'page': int,
                'per_page': int,
                'total_pages': int
            }
        """
        query = User.query.order_by(User.id.desc())
        
        # Paginar
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'users': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
    
    def update_user(self, user_id: int, **kwargs) -> User:
        """
        Actualiza los datos de un usuario.
        
        Args:
            user_id: ID del usuario.
            **kwargs: Campos a actualizar (username, password, role_id).
        
        Returns:
            User: El usuario actualizado.
        
        Raises:
            ValueError: Si el usuario no existe.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"El usuario con ID '{user_id}' no existe")
        
        try:
            # Validar username único si se está actualizando
            if 'username' in kwargs and kwargs['username'] != user.username:
                existing = User.query.filter_by(username=kwargs['username']).first()
                if existing:
                    raise ValueError(f"El username '{kwargs['username']}' ya está en uso")
            
            # Actualizar campos permitidos
            for key, value in kwargs.items():
                if hasattr(user, key) and key != 'id':
                    setattr(user, key, value)
            
            db.session.commit()
            return user
        except ValueError:
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar usuario: {str(e)}")
    
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
    
    def count_users(self) -> int:
        """
        Cuenta el total de usuarios.
        
        Returns:
            int: Cantidad de usuarios.
        """
        return User.query.count()
    
    def get_users_by_role(self, role_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista usuarios filtrados por rol.
        
        Args:
            role_id: ID del rol a filtrar.
            page: Número de página.
            per_page: Usuarios por página.
        
        Returns:
            dict: Resultado paginado de usuarios del rol especificado.
        """
        query = User.query.filter_by(role_id=role_id).order_by(User.id.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'users': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
