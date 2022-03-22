"""message

Revision ID: ac1e5904bc03
Revises: dc97764ab03c
Create Date: 2022-03-21 20:31:19.655566

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ac1e5904bc03'
down_revision = 'dc97764ab03c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authority',
    sa.Column('auth_id', mysql.BIGINT(display_width=20), nullable=False),
    sa.Column('tenant_id', sa.String(length=256), nullable=False),
    sa.Column('auth_name', sa.String(length=256), nullable=False),
    sa.Column('use_monitor', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('use_address', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_address', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('dl_address', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_address', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('scope_address', mysql.INTEGER(display_width=11), server_default=sa.text('0'), nullable=True),
    sa.Column('use_responding', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_responding', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('dl_responding', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_responding', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('scope_responding', mysql.INTEGER(display_width=11), server_default=sa.text('0'), nullable=True),
    sa.Column('use_message', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_message', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('dl_message', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_message', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('scope_message', mysql.INTEGER(display_width=11), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_dashboard', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_dashboard', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('scope_dashboard', mysql.INTEGER(display_width=11), server_default=sa.text('0'), nullable=True),
    sa.Column('use_report', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_report', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('dl_report', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_report', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('scope_report', mysql.INTEGER(display_width=11), server_default=sa.text('0'), nullable=True),
    sa.Column('use_user', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_user', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('dl_user', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_user', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('scope_user', mysql.INTEGER(display_width=11), server_default=sa.text('0'), nullable=True),
    sa.Column('use_group', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_group', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('dl_group', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_group', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('scope_group', mysql.INTEGER(display_width=11), server_default=sa.text('0'), nullable=True),
    sa.Column('use_auth', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_auth', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('dl_auth', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_auth', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('use_flow', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_flow', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_flow', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('use_seat', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_seat', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_seat', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('scope_seat', mysql.INTEGER(display_width=11), server_default=sa.text('0'), nullable=True),
    sa.Column('use_chat', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('scope_chat', mysql.INTEGER(display_width=11), server_default=sa.text('0'), nullable=True),
    sa.Column('use_speech', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_speech', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_speech', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('use_trigger', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_trigger', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('del_trigger', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('use_config', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('edit_config', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('use_log', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('dl_log', mysql.TINYINT(display_width=1), server_default=sa.text('0'), nullable=True),
    sa.Column('insert_date', sa.DateTime(), server_default=sa.text('current_timestamp()'), nullable=False),
    sa.Column('update_date', sa.DateTime(), server_default=sa.text('current_timestamp()'), nullable=False),
    sa.PrimaryKeyConstraint('auth_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('authority')
    # ### end Alembic commands ###
