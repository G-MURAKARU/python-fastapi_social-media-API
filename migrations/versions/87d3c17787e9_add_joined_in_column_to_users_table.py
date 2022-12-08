"""add joined_in column to users table

Revision ID: 87d3c17787e9
Revises: fa64bc7b4dab
Create Date: 2022-12-06 14:31:28.064104

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '87d3c17787e9'
down_revision = 'fa64bc7b4dab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('joined_in', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'joined_in')
    # ### end Alembic commands ###
