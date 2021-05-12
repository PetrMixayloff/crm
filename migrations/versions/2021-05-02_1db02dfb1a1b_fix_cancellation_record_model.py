"""fix cancellation record model

Revision ID: 1db02dfb1a1b
Revises: 2f80abea8bff
Create Date: 2021-05-02 01:04:41.761301

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1db02dfb1a1b'
down_revision = '2f80abea8bff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cancellation_record', sa.Column('price', sa.Float(), nullable=True, comment='Цена за ед.'))
    op.add_column('cancellation_record', sa.Column('raw_remains_details_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key(None, 'cancellation_record', 'raw_remains_detail', ['raw_remains_details_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cancellation_record', type_='foreignkey')
    op.drop_column('cancellation_record', 'raw_remains_details_id')
    op.drop_column('cancellation_record', 'price')
    # ### end Alembic commands ###