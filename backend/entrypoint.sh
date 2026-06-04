#!/bin/sh
# entrypoint.sh — wait for Postgres, run migrations, start uvicorn
# AI-SNAPSHOT · AISNP-48 · Owner: ALPHA

echo "[entrypoint] Starting AI-SNAPSHOT backend..."

DB_URL="${DATABASE_URL:-postgresql+asyncpg://postgres:postgres@localhost:5432/ai_snapshot}"
MAX_WAIT=60
WAITED=0

echo "[entrypoint] Waiting for Postgres to accept connections..."
while [ $WAITED -lt $MAX_WAIT ]; do
    python3 - << 'PYEOF'
import asyncio, os, re, sys
async def check():
    import asyncpg
    url = os.environ.get('DATABASE_URL', '')
    # Parse: postgresql+asyncpg://user:pass@host:port/db
    m = re.match(r'postgresql\+asyncpg://([^:]+):([^@]+)@([^:]+):(\d+)/(.+?)(\?.*)?$', url)
    if not m:
        print(f'Cannot parse DATABASE_URL', file=sys.stderr)
        sys.exit(1)
    user, password, host, port, dbname = m.group(1), m.group(2), m.group(3), int(m.group(4)), m.group(5)
    try:
        conn = await asyncio.wait_for(
            asyncpg.connect(host=host, port=port, user=user, password=password, database=dbname, ssl=False),
            timeout=5
        )
        await conn.close()
        print('[entrypoint] Postgres is ready!')
        sys.exit(0)
    except Exception as e:
        print(f'[entrypoint] DB not ready: {type(e).__name__}', file=sys.stderr)
        sys.exit(1)
asyncio.run(check())
PYEOF
    [ $? -eq 0 ] && break
    sleep 3
    WAITED=$((WAITED + 3))
done

# Run migrations (non-fatal — uvicorn starts regardless)
echo "[entrypoint] Running alembic upgrade head..."
alembic upgrade head 2>&1 || echo "[entrypoint] WARNING: alembic upgrade failed — app will start anyway"

echo "[entrypoint] Starting uvicorn on port 8765..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8765 --workers 1
