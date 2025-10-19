"""
QuoteHandler - Use Case Layer (Refactored with BaseHandler)

Hereda de BaseHandler para eliminar duplicación de código.
Solo contiene métodos específicos del dominio Quote.
"""
from typing import Optional, Dict, Any
from app.entities.quote import Quote
from app.use_cases.base_handler import BaseHandler


class QuoteHandler(BaseHandler):
    """
    Handler para gestionar operaciones con quotes.
    
    Hereda CRUD genérico de BaseHandler:
    - create(**kwargs)
    - get(id)
    - list_all(page, per_page, status)
    - update(id, **kwargs)
    - delete(id)
    - count(status)
    
    Solo agrega métodos específicos del dominio.
    """
    
    def __init__(self):
        """Inicializa con el modelo Quote."""
        super().__init__(Quote)
    
    # Métodos específicos del dominio Quote
    
    def approve(self, id: int) -> Optional[Quote]:
        """
        Aprueba una cotización (cambia status a 'approved').
        
        Args:
            id (int): ID de la quote
        
        Returns:
            Quote: Quote actualizada o None si no existe
        
        Example:
            quote = handler.approve(1)
            if quote:
                print(f"Quote {quote.id} approved")
        """
        return self.update(id, status='approved')
    
    def reject(self, id: int) -> Optional[Quote]:
        """
        Rechaza una cotización (cambia status a 'rejected').
        
        Args:
            id (int): ID de la quote
        
        Returns:
            Quote: Quote actualizada o None si no existe
        """
        return self.update(id, status='rejected')
    
    def get_by_organization(self, organization_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Lista quotes de una organización específica.
        
        Args:
            organization_id (int): ID de la organización
            page (int): Número de página
            per_page (int): Items por página
        
        Returns:
            dict: Resultado paginado con quotes de la organización
        
        Example:
            result = handler.get_by_organization(1, page=1, per_page=20)
            print(f"Found {result['total']} quotes for org 1")
        """
        return self.list_all(page=page, per_page=per_page, organization_id=organization_id)
