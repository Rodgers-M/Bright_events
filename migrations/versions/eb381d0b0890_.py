"""empty message

Revision ID: eb381d0b0890
Revises: df3c7efbf0c5
Create Date: 2017-12-29 17:00:43.034787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb381d0b0890'
down_revision = 'df3c7efbf0c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'created_by')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('created_by', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
