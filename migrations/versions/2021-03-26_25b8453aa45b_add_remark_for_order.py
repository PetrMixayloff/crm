"""add remark for order

Revision ID: 25b8453aa45b
Revises: 91a68f86769b
Create Date: 2021-03-26 15:53:41.418111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25b8453aa45b'
down_revision = '91a68f86769b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('remark', sa.String(length=255), nullable=True, comment='Примечание к заказу'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'remark')
    # ### end Alembic commands ###
