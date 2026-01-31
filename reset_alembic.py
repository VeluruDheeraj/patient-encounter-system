from sqlalchemy import text
from src.database import engine

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
    conn.commit()

print("alembic_version table removed")
