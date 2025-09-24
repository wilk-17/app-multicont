"""Inserta datos de prueba en tabla user

Revision ID: 26d14f6f6172
Revises: 78a49736b3ac
Create Date: 2025-09-19 20:55:52.992571

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# Identificadores de revisión
revision = '26d14f6f6172'
down_revision = '78a49736b3ac'
branch_labels = None
depends_on = None

def upgrade():
    # Tabla virtual para insertar roles
    role_table = table(
        'role',
        column('id', sa.BigInteger()),
        column('name', sa.String())
    )

    op.bulk_insert(role_table, [
        {'id': 1, 'name': 'Admin'},
        {'id': 2, 'name': 'User'}
    ])

    # Tabla virtual para insertar usuarios
    user_table = table(
        'user',
        column('id', sa.BigInteger()),
        column('username', sa.String()),
        column('password', sa.String()),
        column('role_id', sa.BigInteger())
    )

    op.bulk_insert(user_table, [
        {'id': 1, 'username': 'admin', 'password': 'admin123', 'role_id': 1},
        {'id': 2, 'username': 'testuser', 'password': 'testpass', 'role_id': 2}
    ])

def downgrade():
    op.execute("DELETE FROM user WHERE username IN ('admin', 'testuser')")
    op.execute("DELETE FROM role WHERE name IN ('Admin', 'User')")
