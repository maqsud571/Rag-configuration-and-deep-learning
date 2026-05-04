from sqlalchemy import text
from db.database import engine

def load_ddl():
    with open("db/ddl.sql", "r", encoding="utf-8") as f:
        return f.read()

def init_db():
    ddl = load_ddl()

    with engine.connect() as conn:
        conn.execute(text(ddl))
        conn.commit()