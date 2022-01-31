"""add content column to posts table

Revision ID: ef259be645b6
Revises: cbd04ded89d2
Create Date: 2022-01-28 17:28:30.858602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef259be645b6'
down_revision = 'cbd04ded89d2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
