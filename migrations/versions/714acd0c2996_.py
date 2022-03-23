"""empty message

Revision ID: 714acd0c2996
Revises: df358c479881
Create Date: 2022-03-23 22:57:56.251269

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '714acd0c2996'
down_revision = 'df358c479881'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher_course')
    op.drop_table('course')
    op.drop_table('teacher')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('teacher_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='teacher_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='teacher_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('course',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('course_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('credits', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('start_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('end_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='course_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('teacher_course',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('course_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], name='teacher_course_course_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], name='teacher_course_teacher_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='teacher_course_pkey')
    )
    # ### end Alembic commands ###
