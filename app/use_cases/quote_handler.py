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
    
    # Override del método create para manejar items anidados
    
    def create(self, **kwargs) -> Quote:
        """
        Crea una nueva cotización con sus líneas de items.
        
        Args:
            **kwargs: Datos de la cotización incluyendo 'items' (lista de líneas)
        
        Returns:
            Quote: Cotización creada
        
        Raises:
            ValueError: Si hay error en los datos
        """
        from app import db
        from app.entities.quotation_line import QuotationLine
        
        try:
            # Extraer items del kwargs si existen
            items_data = kwargs.pop('items', [])
            
            # Crear la cotización sin los items
            quote = Quote(**kwargs)
            db.session.add(quote)
            db.session.flush()  # Para obtener el ID de la quote
            
            # Crear las líneas de items
            total = 0
            for item_data in items_data:
                line = QuotationLine(
                    quote_id=quote.id,
                    item_id=item_data['inventory_item_id'],  # Mapeo de nombre
                    quantity=item_data['quantity'],
                    price=item_data['unit_price'],  # Mapeo de nombre
                    description=item_data.get('description')
                )
                # Calcular total de la línea
                line_total = item_data['quantity'] * float(item_data['unit_price'])
                total += line_total
                
                db.session.add(line)
            
            # Actualizar el total de la cotización
            quote.total = total
            
            db.session.commit()
            return quote
            
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error al crear cotización: {str(e)}")
    
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
