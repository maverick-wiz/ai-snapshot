"""Initial schema + app_config seed. AISNP-25 · Owner: ATLAS"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import DateTime as TIMESTAMPTZ
import uuid

revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('username', sa.String(64), unique=True, nullable=False),
        sa.Column('display_name', sa.String(128), nullable=True),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', TIMESTAMPTZ, server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', TIMESTAMPTZ, server_default=sa.text('now()'), nullable=False),
    )
    op.create_table('user_preferences',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('default_country', sa.CHAR(2), default='US', nullable=False),
        sa.Column('watchlist_tickers', JSONB, nullable=False),
        sa.Column('refresh_interval_secs', sa.SmallInteger, default=5, nullable=False),
        sa.Column('news_limit', sa.SmallInteger, default=20, nullable=False),
        sa.Column('theme', sa.String(16), default='dark', nullable=False),
        sa.Column('updated_at', TIMESTAMPTZ, server_default=sa.text('now()'), nullable=False),
    )
    op.create_table('user_sessions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_token', sa.String(128), unique=True, nullable=False),
        sa.Column('created_at', TIMESTAMPTZ, server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', TIMESTAMPTZ, nullable=False),
        sa.Column('last_seen_at', TIMESTAMPTZ, server_default=sa.text('now()'), nullable=False),
        sa.Column('user_agent', sa.Text, nullable=True),
    )
    op.create_table('app_config',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('config_key', sa.String(128), unique=True, nullable=False),
        sa.Column('config_value', sa.Text, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_public', sa.Boolean, default=False, nullable=False),
        sa.Column('updated_at', TIMESTAMPTZ, server_default=sa.text('now()'), nullable=False),
    )
    # Seed app_config
    op.execute("""
        INSERT INTO app_config (config_key, config_value, description, is_public) VALUES
        ('default_tickers', '["NVDA","AMD","TSM","ASML","MSFT","AVGO"]', 'Default stock watchlist', true),
        ('news_query', 'artificial intelligence OR semiconductor OR AI chip OR NVDA OR ASML OR machine learning', 'Google News RSS query', true),
        ('stock_refresh_interval_secs', '5', 'Default stock panel poll interval (seconds)', true),
        ('max_news_limit', '100', 'Maximum articles per news request', true),
        ('session_ttl_days', '30', 'Session token expiry duration in days', false)
    """)


def downgrade() -> None:
    op.drop_table('app_config')
    op.drop_table('user_sessions')
    op.drop_table('user_preferences')
    op.drop_table('users')
