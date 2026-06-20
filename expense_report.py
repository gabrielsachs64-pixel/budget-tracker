import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

conn_str = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server=tcp:{server},1433;"
    f"Database={database};"
    f"Uid={username};"
    f"Pwd={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

conn = pyodbc.connect(conn_str)

# Query 1: Full expense detail with category and vendor names (JOIN across all 3 tables)
query_detail = """
SELECT 
    e.expense_date,
    c.category_name,
    v.vendor_name,
    e.description,
    e.amount
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
JOIN vendors v ON e.vendor_id = v.vendor_id
ORDER BY e.expense_date;
"""

df_detail = pd.read_sql(query_detail, conn)
print("=== Full Expense Detail ===")
print(df_detail.to_string(index=False))

# Query 2: Total spend by category
query_by_category = """
SELECT 
    c.category_name,
    SUM(e.amount) AS total_spent,
    COUNT(e.expense_id) AS num_transactions
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_spent DESC;
"""

df_category = pd.read_sql(query_by_category, conn)
print("\n=== Spend by Category ===")
print(df_category.to_string(index=False))

# Export both to Excel
with pd.ExcelWriter("expense_report.xlsx", engine="openpyxl") as writer:
    df_detail.to_excel(writer, index=False, sheet_name="Detail")
    df_category.to_excel(writer, index=False, sheet_name="By Category")

print("\n[OK] Report exported to expense_report.xlsx")

conn.close()