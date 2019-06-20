"""file_url column

Revision ID: 9e0836c6849b
Revises: d4d903fd0968
Create Date: 2019-06-21 00:25:56.472757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e0836c6849b'
down_revision = 'd4d903fd0968'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('file_url', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'file_url')
    # ### end Alembic commands ###