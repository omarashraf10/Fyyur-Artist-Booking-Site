"""empty message

Revision ID: 8b2587272e01
Revises: 8875260e7f11
Create Date: 2021-09-13 10:06:29.689255

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8b2587272e01'
down_revision = '8875260e7f11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'Genres')
    op.add_column('venues', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    op.drop_column('venues', 'Genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venues', sa.Column('Genres', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.drop_column('venues', 'genres')
    op.add_column('artists', sa.Column('Genres', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
