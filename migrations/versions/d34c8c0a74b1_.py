"""empty message

Revision ID: d34c8c0a74b1
Revises: a2b72a114ce5
Create Date: 2022-05-09 19:40:41.372984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd34c8c0a74b1'
down_revision = 'a2b72a114ce5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category_file',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('category_file_id_fkey', 'category', type_='foreignkey')
    op.drop_column('category', 'file_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('file_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('category_file_id_fkey', 'category', 'file', ['file_id'], ['id'], ondelete='CASCADE')
    op.drop_table('category_file')
    # ### end Alembic commands ###