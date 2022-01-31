"""add last 2 columns to posts table

Revision ID: 25757d7fa9ca
Revises: 8d64407d679d
Create Date: 2022-01-31 13:11:08.659686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25757d7fa9ca'
down_revision = '8d64407d679d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
