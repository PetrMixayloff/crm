"""small fix File

Revision ID: f2a3e45ef829
Revises: 53874a3375f5
Create Date: 2020-11-03 21:27:48.605608

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f2a3e45ef829'
down_revision = '53874a3375f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('raw_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'file', 'raw', ['raw_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'file', type_='foreignkey')
    op.drop_column('file', 'raw_id')
    # ### end Alembic commands ###
