from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database
sqlite_engine = create_engine("sqlite:///instance/project.db")

# PostgreSQL (Supabase)
pg_engine = create_engine("postgresql://postgres.xnaxxvhxyzruoevrgjga:abdo-mohamed20@aws-1-eu-west-1.pooler.supabase.com:6543/postgres")

SQLiteSession = sessionmaker(bind=sqlite_engine)
PGSession = sessionmaker(bind=pg_engine)

sqlite_session = SQLiteSession()
pg_session = PGSession()

# import models
from server import Admin, ItemDetails, ItemColor, ItemImg, Order, Cart


def copy_table(model):
    rows = sqlite_session.query(model).all()
    for row in rows:
        data = {c.name: getattr(row, c.name) for c in model.__table__.columns}
        pg_session.add(model(**data))
    pg_session.commit()
    print(f"Copied {len(rows)} rows from {model.__tablename__}")


tables = [Admin, ItemDetails, ItemColor, ItemImg, Order, Cart]

for table in tables:
    copy_table(table)

print("Migration completed 🚀")