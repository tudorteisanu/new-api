"""empty message

Revision ID: e4e6bd5c1d00
Revises: 4651b08ea212
Create Date: 2022-03-19 19:16:44.658499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4e6bd5c1d00'
down_revision = '4651b08ea212'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('good', sa.Column('description_ro', sa.Text(), nullable=True))
    op.add_column('good', sa.Column('description_en', sa.Text(), nullable=True))
    op.add_column('good', sa.Column('description_ru', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('good', 'description_ru')
    op.drop_column('good', 'description_en')
    op.drop_column('good', 'description_ro')
    # ### end Alembic commands ###
