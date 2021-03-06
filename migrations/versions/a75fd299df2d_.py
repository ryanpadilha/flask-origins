"""empty message

Revision ID: a75fd299df2d
Revises: 
Create Date: 2018-02-09 14:01:58.804499

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = 'a75fd299df2d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('xf_auth_api',
    sa.Column('internal', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('client_secret', sa.String(), nullable=False),
    sa.Column('api_key', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('internal'),
    sa.UniqueConstraint('api_key'),
    sa.UniqueConstraint('client_secret')
    )
    op.create_table('xf_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('internal', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('user_name', sa.String(length=100), nullable=True),
    sa.Column('user_email', sa.String(length=200), nullable=True),
    sa.Column('user_password', sa.String(length=200), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.Column('file_url', sa.String(), nullable=True),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('occupation', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sqlite_autoincrement=True
    )
    op.create_index(op.f('ix_xf_user_internal'), 'xf_user', ['internal'], unique=True)
    op.create_index(op.f('ix_xf_user_user_email'), 'xf_user', ['user_email'], unique=True)
    op.create_index(op.f('ix_xf_user_user_name'), 'xf_user', ['user_name'], unique=True)
    op.create_table('xf_login_activities',
    sa.Column('internal', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.String(), nullable=False),
    sa.Column('ip_address', sa.String(), nullable=False),
    sa.Column('ua_header', sa.String(), nullable=False),
    sa.Column('ua_device', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['xf_user.id'], ),
    sa.PrimaryKeyConstraint('internal')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('xf_login_activities')
    op.drop_index(op.f('ix_xf_user_user_name'), table_name='xf_user')
    op.drop_index(op.f('ix_xf_user_user_email'), table_name='xf_user')
    op.drop_index(op.f('ix_xf_user_internal'), table_name='xf_user')
    op.drop_table('xf_user')
    op.drop_table('xf_auth_api')
    # ### end Alembic commands ###
