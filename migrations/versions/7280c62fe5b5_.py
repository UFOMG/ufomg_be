"""empty message

Revision ID: 7280c62fe5b5
Revises: 41059c651ae3
Create Date: 2021-02-22 17:46:10.584711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7280c62fe5b5'
down_revision = '41059c651ae3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reports',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('lat', sa.Float(precision=13), nullable=True),
    sa.Column('long', sa.Float(precision=13), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('event_type', sa.String(length=100), nullable=False),
    sa.Column('image', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('report_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['report_id'], ['reports.id'], ),
    sa.PrimaryKeyConstraint('id', 'text')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('reports')
    # ### end Alembic commands ###
