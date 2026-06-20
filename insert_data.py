import pyodbc
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
cursor = conn.cursor()

# Insert categories
categories = ["Office Supplies", "Travel", "Software", "Marketing", "Utilities"]
for cat in categories:
    cursor.execute("INSERT INTO categories (category_name) VALUES (?)", cat)

# Insert vendors
vendors = ["Amazon", "Delta Airlines", "Adobe", "Google Ads", "Comcast Business"]
for v in vendors:
    cursor.execute("INSERT INTO vendors (vendor_name) VALUES (?)", v)

conn.commit()
# Insert expenses (linking category_id and vendor_id manually based on insert order: 1-5)
expenses = [
    ("2024-01-10", 1, 1, "Printer paper and ink", 89.50),
    ("2024-01-15", 2, 2, "Flight to client meeting", 412.00),
    ("2024-02-01", 3, 3, "Adobe Creative Cloud subscription", 54.99),
    ("2024-02-10", 4, 4, "Google Ads campaign", 300.00),
    ("2024-02-15", 5, 5, "Internet and phone service", 150.00),
    ("2024-03-01", 1, 1, "Office chair", 220.00),
    ("2024-03-05", 2, 2, "Hotel for conference", 380.00),
    ("2024-03-12", 3, 3, "Software license renewal", 99.00),
]

for exp in expenses:
    cursor.execute("""
        INSERT INTO expenses (expense_date, category_id, vendor_id, description, amount)
        VALUES (?, ?, ?, ?, ?)
    """, exp)

conn.commit()
print("[OK] Sample data inserted successfully!")

cursor.close()
conn.close()