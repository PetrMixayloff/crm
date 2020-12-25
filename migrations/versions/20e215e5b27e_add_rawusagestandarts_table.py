"""add RawUsageStandarts table

Revision ID: 20e215e5b27e
Revises: f925c1b0638e
Create Date: 2020-12-09 09:59:58.625950

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20e215e5b27e'
down_revision = 'f925c1b0638e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rawusagestandards',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('raw_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Сырье'),
    sa.Column('name', sa.String(length=255), nullable=False, comment='Название стандарта'),
    sa.Column('quantity', sa.Float(), nullable=True, comment='Количество сырья на ед. стандарта'),
    sa.ForeignKeyConstraint(['raw_id'], ['raw.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rawusagestandards')
    # ### end Alembic commands ###