"""add standard_id to product raw relation

Revision ID: 293f46696f0e
Revises: 7174ff09169d
Create Date: 2020-12-21 17:11:13.138543

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '293f46696f0e'
down_revision = '7174ff09169d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('productrawrelation', sa.Column('standard_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'productrawrelation', 'rawusagestandards', ['standard_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'productrawrelation', type_='foreignkey')
    op.drop_column('productrawrelation', 'standard_id')
    # ### end Alembic commands ###
