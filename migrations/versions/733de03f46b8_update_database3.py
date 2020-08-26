"""update database3

Revision ID: 733de03f46b8
Revises: de03bfd82a47
Create Date: 2020-08-26 15:32:55.331714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '733de03f46b8'
down_revision = 'de03bfd82a47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_blacklisttoken_id', table_name='blacklisttoken')
    op.drop_index('ix_file_id', table_name='file')
    op.drop_index('ix_product_id', table_name='product')
    op.drop_index('ix_productcategory_id', table_name='productcategory')
    op.drop_index('ix_shop_id', table_name='shop')
    op.drop_index('ix_user_id', table_name='user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_user_id', 'user', ['id'], unique=True)
    op.create_index('ix_shop_id', 'shop', ['id'], unique=True)
    op.create_index('ix_productcategory_id', 'productcategory', ['id'], unique=True)
    op.create_index('ix_product_id', 'product', ['id'], unique=True)
    op.create_index('ix_file_id', 'file', ['id'], unique=True)
    op.create_index('ix_blacklisttoken_id', 'blacklisttoken', ['id'], unique=True)
    # ### end Alembic commands ###
