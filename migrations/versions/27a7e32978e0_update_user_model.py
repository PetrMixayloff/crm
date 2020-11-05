"""update user model

Revision ID: 27a7e32978e0
Revises: b63b759dd8e9
Create Date: 2020-10-26 15:36:12.792712

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '27a7e32978e0'
down_revision = 'b63b759dd8e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.alter_column('file', 'product_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.create_unique_constraint('_product_user_uc', 'file', ['product_id', 'user_id'])
    op.create_foreign_key(None, 'file', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('description', sa.String(length=255), nullable=True, comment='Данные'))
    op.add_column('user', sa.Column('phone', sa.String(length=255), nullable=False, comment='Номер телефона'))
    op.drop_column('user', 'login')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('login', sa.VARCHAR(length=255), autoincrement=False, nullable=False, comment='Логин'))
    op.drop_column('user', 'phone')
    op.drop_column('user', 'description')
    op.drop_constraint(None, 'file', type_='foreignkey')
    op.drop_constraint('_product_user_uc', 'file', type_='unique')
    op.alter_column('file', 'product_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('file', 'user_id')
    # ### end Alembic commands ###