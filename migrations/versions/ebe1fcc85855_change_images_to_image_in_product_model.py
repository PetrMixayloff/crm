"""change images to image in product model

Revision ID: ebe1fcc85855
Revises: dd9220f74ea1
Create Date: 2020-12-07 17:23:00.921168

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ebe1fcc85855'
down_revision = 'dd9220f74ea1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('image', sa.String(length=255), nullable=True))
    op.drop_column('product', 'images')
    op.drop_column('product', 'url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('url', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('product', sa.Column('images', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.drop_column('product', 'image')
    # ### end Alembic commands ###
