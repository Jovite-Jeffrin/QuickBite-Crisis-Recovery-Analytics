import os
import pandas as pd
from sqlalchemy import create_engine
from config import DB_CONFIG


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

SQLITE_DB = os.path.join(
    BASE_DIR,
    "quickbite.db"
)


# ============================================================
# POSTGRESQL CONNECTION
# ============================================================

def get_engine():

    connection_string = (
        f"postgresql://{DB_CONFIG['user']}:"
        f"{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}:"
        f"{DB_CONFIG['port']}/"
        f"{DB_CONFIG['database']}"
    )

    return create_engine(connection_string)


# ============================================================
# CSV LOADER
# ============================================================

def load_table(table_name):

    file_path = os.path.join(
        DATA_DIR,
        f"{table_name}.csv"
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    return pd.read_csv(file_path)


# ============================================================
# SQLITE ENGINE
# ============================================================

def get_sqlite_engine():

    engine = create_engine(
        f"sqlite:///{SQLITE_DB}"
    )

    tables = [
        "dim_customer",
        "dim_delivery_partner",
        "dim_menu_item",
        "dim_restaurant",
        "fact_delivery_performance",
        "fact_order_items",
        "fact_orders",
        "fact_ratings",
    ]

    for table in tables:

        print(f"Loading {table}...")

        df = load_table(table)

        df.to_sql(
            table,
            engine,
            if_exists="replace",
            index=False
        )

    print("All QuickBite tables loaded into SQLite.")

    return engine