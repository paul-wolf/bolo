"""Extend user table

Revision ID: e3dda7be6a95
Revises: 
Create Date: 2021-06-07 11:43:45.144088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e3dda7be6a95"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("auth_user", sa.Column("comment", sa.String(255)))


def downgrade():
    pass
