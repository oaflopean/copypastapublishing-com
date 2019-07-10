"""empty message

Revision ID: 957aec17dbfd
Revises: 63a6b0893255
Create Date: 2019-07-09 22:22:18.574574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '957aec17dbfd'
down_revision = '63a6b0893255'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('reddit_url', sa.String(), nullable=True))
    op.create_foreign_key(None, 'books', 'redditpost', ['reddit_url'], ['reddit_url'])
    op.create_foreign_key(None, 'books', 'redditpost', ['uri'], ['uri'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'reddit_url')
    # ### end Alembic commands ###
