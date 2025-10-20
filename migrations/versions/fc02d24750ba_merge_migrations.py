"""Merge migrations

Revision ID: fc02d24750ba
Revises: add_assignment_tracking, f8f134a08970
Create Date: 2025-10-19 23:09:04.968070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc02d24750ba'
down_revision = ('add_assignment_tracking', 'f8f134a08970')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
