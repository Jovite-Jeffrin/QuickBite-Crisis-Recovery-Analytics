from database import load_table

df = load_table("fact_orders")

print(df.shape)
print(df.head())