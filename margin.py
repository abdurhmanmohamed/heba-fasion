# margin.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# ==========================
# DATABASE CONNECTIONS
# ==========================
sqlite_engine = create_engine("sqlite:///instance/project.db")
pg_engine = create_engine("postgresql://postgres.xnaxxvhxyzruoevrgjga:abdo-mohamed20@aws-1-eu-west-1.pooler.supabase.com:6543/postgres")

SQLiteSession = sessionmaker(bind=sqlite_engine)
PGSession = sessionmaker(bind=pg_engine)

sqlite_session = SQLiteSession()
pg_session = PGSession()

# ==========================
# IMPORT YOUR MODELS
# ==========================
from server import Admin, ItemDetails, ItemColor, ItemImg, Order, Cart

# ==========================
# GENERIC MERGE FUNCTION
# ==========================
def merge_table(model, use_updated_at=False):
    rows = sqlite_session.query(model).all()
    print(f"\n🔄 Merging {model.__tablename__}...")

    for row in rows:
        data = {c.name: getattr(row, c.name) for c in model.__table__.columns}

        existing = pg_session.query(model).filter_by(id=row.id).first()

        if existing:
            # ✅ OPTIONAL SMART UPDATE
            if use_updated_at and hasattr(row, "updated_at") and hasattr(existing, "updated_at"):
                if row.updated_at and existing.updated_at:
                    if row.updated_at <= existing.updated_at:
                        continue  # Skip older data

            # ✅ UPDATE
            for key, value in data.items():
                setattr(existing, key, value)

        else:
            # ✅ INSERT
            pg_session.add(model(**data))

    pg_session.commit()
    print(f"✅ Done {model.__tablename__} ({len(rows)} rows)")


# ==========================
# RESET SEQUENCES (VERY IMPORTANT)
# ==========================
def reset_sequence(table_name):
    try:
        pg_session.execute(text(f"""
            SELECT setval(
                pg_get_serial_sequence('{table_name}', 'id'),
                COALESCE(MAX(id), 1)
            ) FROM {table_name};
        """))
        pg_session.commit()
        print(f"🔧 Sequence fixed for {table_name}")
    except Exception as e:
        print(f"⚠️ Sequence error for {table_name}: {e}")


# ==========================
# RUN MIGRATION (ORDER MATTERS 🔥)
# ==========================
try:
    # 1️⃣ Independent tables first
    merge_table(Admin)
    merge_table(ItemDetails)

    # 2️⃣ Dependent tables (FK relations)
    merge_table(ItemColor)
    merge_table(ItemImg)
    merge_table(Order)
    merge_table(Cart)

    # 3️⃣ Fix sequences
    reset_sequence("admin")
    reset_sequence("item_details")
    reset_sequence("item_color")
    reset_sequence("item_img")
    reset_sequence("order")
    reset_sequence("cart")

    print("\n🚀 MIGRATION COMPLETED SUCCESSFULLY")

except Exception as e:
    pg_session.rollback()
    print("❌ ERROR:", e)