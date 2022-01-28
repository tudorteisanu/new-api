"""empty message

Revision ID: b3c855ddc341
Revises: cfe217343c25
Create Date: 2022-01-27 22:36:29.437715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c855ddc341'
down_revision = 'cfe217343c25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_auth_tokens', sa.Column('token', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_auth_tokens', 'token')
    # ### end Alembic commands ###