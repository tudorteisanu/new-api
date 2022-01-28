"""empty message

Revision ID: 8b20488f714c
Revises: 284e40bbb484
Create Date: 2022-01-27 22:23:46.924267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b20488f714c'
down_revision = '284e40bbb484'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_auth_tokens', sa.Column('request_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user_auth_tokens', 'user', ['request_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_auth_tokens', type_='foreignkey')
    op.drop_column('user_auth_tokens', 'request_id')
    # ### end Alembic commands ###