from database import get_sqlite_engine
import pandas as pd


engine = get_sqlite_engine()

query = """
SELECT
    COUNT(*) AS total_orders
FROM fact_orders
"""

df = pd.read_sql(query, engine)

print(df)