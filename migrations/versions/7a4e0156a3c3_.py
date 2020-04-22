"""empty message

Revision ID: 7a4e0156a3c3
Revises: 
Create Date: 2020-04-20 10:49:37.064918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a4e0156a3c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.String(length=255), nullable=True),
    sa.Column('imgtype', sa.String(length=4), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_my_upload_created_on'), 'my_upload', ['created_on'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_created_on'), 'user', ['created_on'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_created_on'), 'post', ['created_on'], unique=False)
    op.create_table('prediction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('img_id', sa.Integer(), nullable=True),
    sa.Column('output', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['img_id'], ['my_upload.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prediction_created_on'), 'prediction', ['created_on'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_prediction_created_on'), table_name='prediction')
    op.drop_table('prediction')
    op.drop_index(op.f('ix_post_created_on'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_created_on'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_my_upload_created_on'), table_name='my_upload')
    op.drop_table('my_upload')
    # ### end Alembic commands ###
