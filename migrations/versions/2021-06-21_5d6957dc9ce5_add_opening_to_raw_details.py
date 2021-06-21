"""add opening to raw details

Revision ID: 5d6957dc9ce5
Revises: 3532488aa022
Create Date: 2021-06-21 11:51:32.713407

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5d6957dc9ce5'
down_revision = '3532488aa022'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('raw_remains_detail', sa.Column('opening_id', postgresql.UUID(as_uuid=True), nullable=True, comment='Id документа разборки'))
    op.alter_column('raw_remains_detail', 'inventory_id',
               existing_type=postgresql.UUID(),
               comment='Id документа инвентаризации',
               existing_comment='Id инвентаризации',
               existing_nullable=True)
    op.create_foreign_key(None, 'raw_remains_detail', 'opening', ['opening_id'], ['id'])
    op.drop_column('raw_remains_detail', 'invoice')
    op.alter_column('raw_remains_log', 'action',
               existing_type=sa.VARCHAR(length=255),
               comment='Событие: приход, списание, инвентаризация, продажа, разборка',
               existing_comment='Событие: приход, списание, инвентаризация, продажа',
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('raw_remains_log', 'action',
               existing_type=sa.VARCHAR(length=255),
               comment='Событие: приход, списание, инвентаризация, продажа',
               existing_comment='Событие: приход, списание, инвентаризация, продажа, разборка',
               existing_nullable=False)
    op.add_column('raw_remains_detail', sa.Column('invoice', sa.BOOLEAN(), autoincrement=False, nullable=False, comment='True: приходная накладная, False: инвентаризация'))
    op.drop_constraint(None, 'raw_remains_detail', type_='foreignkey')
    op.alter_column('raw_remains_detail', 'inventory_id',
               existing_type=postgresql.UUID(),
               comment='Id инвентаризации',
               existing_comment='Id документа инвентаризации',
               existing_nullable=True)
    op.drop_column('raw_remains_detail', 'opening_id')
    # ### end Alembic commands ###
