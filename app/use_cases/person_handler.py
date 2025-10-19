"""
PersonHandler - Use Case Layer
Gestiona personas (base para empleados, clientes, proveedores).
"""
from typing import Optional, Dict, Any
from app.entities.person import Person
from app.use_cases.base_handler import BaseHandler


class PersonHandler(BaseHandler):
    """Handler para gestionar operaciones con personas."""
    
    def __init__(self):
        super().__init__(Person)
    
    def get_by_document(self, document_type: str, document_number: str) -> Optional[Person]:
        """
        Busca una persona por tipo y número de documento.
        
        Args:
            document_type: Tipo de documento (DNI, Passport, etc)
            document_number: Número de documento
        
        Returns:
            Person si existe, None si no
        """
        return Person.query.filter_by(
            document_type=document_type,
            document_number=document_number
        ).first()
    
    def get_by_email(self, email: str) -> Optional[Person]:
        """
        Busca una persona por email.
        
        Args:
            email: Email de la persona
        
        Returns:
            Person si existe, None si no
        """
        return Person.query.filter_by(email=email).first()
    
    def search_by_name(self, name: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Busca personas por nombre (búsqueda parcial).
        
        Args:
            name: Nombre a buscar
            page: Número de página
            per_page: Items por página
        
        Returns:
            Dict con personas paginadas
        """
        query = Person.query.filter(
            Person.first_name.ilike(f'%{name}%') | 
            Person.last_name.ilike(f'%{name}%')
        )
        query = query.order_by(Person.first_name, Person.last_name)
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total_pages': paginated.pages
        }
