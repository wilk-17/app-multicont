"""Add assignment tracking fields

Revision ID: add_assignment_tracking
Revises: 
Create Date: 2025-01-20

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_assignment_tracking'
down_revision = None  # Usuario debe actualizar esto con el último revision ID
branch_labels = None
depends_on = None


def upgrade():
    # Agregar nuevas columnas a assignment
    op.add_column('assignment', sa.Column('status', sa.String(20), nullable=False, server_default='active'))
    op.add_column('assignment', sa.Column('return_date', sa.Date(), nullable=True))
    op.add_column('assignment', sa.Column('condition', sa.String(50), nullable=True))
    op.add_column('assignment', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('assignment', sa.Column('creation_date', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.add_column('assignment', sa.Column('update_date', sa.DateTime(), nullable=False, server_default=sa.func.now()))


def downgrade():
    # Revertir cambios
    op.drop_column('assignment', 'update_date')
    op.drop_column('assignment', 'creation_date')
    op.drop_column('assignment', 'notes')
    op.drop_column('assignment', 'condition')
    op.drop_column('assignment', 'return_date')
    op.drop_column('assignment', 'status')
