"""empty message

Revision ID: 726e9fbfb91e
Revises: 734314ad5b82
Create Date: 2022-03-13 20:33:05.252437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '726e9fbfb91e'
down_revision = '734314ad5b82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('alias', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('alias')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role')
    # ### end Alembic commands ###
