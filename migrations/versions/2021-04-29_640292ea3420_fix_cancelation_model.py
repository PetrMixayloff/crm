"""fix cancelation model

Revision ID: 640292ea3420
Revises: 9abf286a1b50
Create Date: 2021-04-29 16:43:30.808478

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '640292ea3420'
down_revision = '9abf286a1b50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cancellationrecord', sa.Column('raw_id', postgresql.UUID(as_uuid=True), nullable=False, comment='Id сырья в остатках'))
    op.drop_constraint('cancellationrecord_rawremainsdetail_id_fkey', 'cancellationrecord', type_='foreignkey')
    op.create_foreign_key(None, 'cancellationrecord', 'raw', ['raw_id'], ['id'])
    op.drop_column('cancellationrecord', 'rawremainsdetail_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cancellationrecord', sa.Column('rawremainsdetail_id', postgresql.UUID(), autoincrement=False, nullable=False, comment='Id сырья в остатках'))
    op.drop_constraint(None, 'cancellationrecord', type_='foreignkey')
    op.create_foreign_key('cancellationrecord_rawremainsdetail_id_fkey', 'cancellationrecord', 'rawremainsdetail', ['rawremainsdetail_id'], ['id'])
    op.drop_column('cancellationrecord', 'raw_id')
    # ### end Alembic commands ###
