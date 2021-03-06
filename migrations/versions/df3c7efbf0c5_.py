"""empty message

Revision ID: df3c7efbf0c5
Revises: 984aedbf035b
Create Date: 2017-12-29 16:34:20.015398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df3c7efbf0c5'
down_revision = '984aedbf035b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'events', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_column('events', 'user_id')
    # ### end Alembic commands ###
