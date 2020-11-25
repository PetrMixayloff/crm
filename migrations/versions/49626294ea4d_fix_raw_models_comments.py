"""fix raw models comments

Revision ID: 49626294ea4d
Revises: 6c112ceccdbb
Create Date: 2020-11-13 15:23:53.044522

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '49626294ea4d'
down_revision = '6c112ceccdbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('raw', 'description',
               existing_type=sa.VARCHAR(length=255),
               comment='Описание',
               existing_nullable=True)
    op.alter_column('raw', 'green_signal',
               existing_type=sa.INTEGER(),
               comment='Зеленая метка',
               existing_nullable=True)
    op.alter_column('raw', 'image',
               existing_type=sa.VARCHAR(length=255),
               comment='Изображение',
               existing_nullable=True)
    op.alter_column('raw', 'name',
               existing_type=sa.VARCHAR(length=255),
               comment='Название',
               existing_nullable=False)
    op.alter_column('raw', 'per_pack',
               existing_type=sa.INTEGER(),
               comment='В упаковке',
               existing_nullable=True)
    op.alter_column('raw', 'price',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               comment='Суммарная стоимость остатка',
               existing_nullable=True)
    op.alter_column('raw', 'quantity',
               existing_type=sa.INTEGER(),
               comment='Общий остаток',
               existing_nullable=True)
    op.alter_column('raw', 'red_signal',
               existing_type=sa.INTEGER(),
               comment='Красная метка',
               existing_nullable=True)
    op.alter_column('raw', 'unit',
               existing_type=sa.VARCHAR(length=255),
               comment='Ед. измерения',
               existing_nullable=True)
    op.alter_column('raw', 'yellow_signal',
               existing_type=sa.INTEGER(),
               comment='Желтая метка',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('raw', 'yellow_signal',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Желтая метка',
               existing_nullable=True)
    op.alter_column('raw', 'unit',
               existing_type=sa.VARCHAR(length=255),
               comment=None,
               existing_comment='Ед. измерения',
               existing_nullable=True)
    op.alter_column('raw', 'red_signal',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Красная метка',
               existing_nullable=True)
    op.alter_column('raw', 'quantity',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Общий остаток',
               existing_nullable=True)
    op.alter_column('raw', 'price',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               comment=None,
               existing_comment='Суммарная стоимость остатка',
               existing_nullable=True)
    op.alter_column('raw', 'per_pack',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='В упаковке',
               existing_nullable=True)
    op.alter_column('raw', 'name',
               existing_type=sa.VARCHAR(length=255),
               comment=None,
               existing_comment='Название',
               existing_nullable=False)
    op.alter_column('raw', 'image',
               existing_type=sa.VARCHAR(length=255),
               comment=None,
               existing_comment='Изображение',
               existing_nullable=True)
    op.alter_column('raw', 'green_signal',
               existing_type=sa.INTEGER(),
               comment=None,
               existing_comment='Зеленая метка',
               existing_nullable=True)
    op.alter_column('raw', 'description',
               existing_type=sa.VARCHAR(length=255),
               comment=None,
               existing_comment='Описание',
               existing_nullable=True)
    # ### end Alembic commands ###