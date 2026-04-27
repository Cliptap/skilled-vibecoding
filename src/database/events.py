import os
import sys

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import event
from sqlalchemy.orm import Session
from src.database.models import SoftDeleteMixin

@event.listens_for(Session, "do_orm_execute")
def _add_soft_delete_filter(execute_state):
    """
    Intercepta consultas y añade filtro `is_deleted == False` automáticamente.
    Garantiza que la API no devuelva registros eliminados lógicamente.
    """
    if (
        execute_state.is_select 
        and not execute_state.is_column_load 
        and not execute_state.is_relationship_load
    ):
        entity = getattr(execute_state.statement, 'column_descriptions', [{}])[0].get('type')
        if hasattr(entity, 'is_deleted'):
            execute_state.statement = execute_state.statement.filter(
                entity.is_deleted == False
            )
