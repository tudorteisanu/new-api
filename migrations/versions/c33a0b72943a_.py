"""empty message

Revision ID: c33a0b72943a
Revises: c3c252c9918f
Create Date: 2022-04-30 17:08:11.813558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c33a0b72943a'
down_revision = 'c3c252c9918f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teacher_course', sa.Column('dates', sa.DateTime(), nullable=True))
    op.add_column('teacher_details', sa.Column('credits', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('teacher_details', 'credits')
    op.drop_column('teacher_course', 'dates')
    # ### end Alembic commands ###
