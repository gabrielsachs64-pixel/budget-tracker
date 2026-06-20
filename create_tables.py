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

cursor.execute("IF OBJECT_ID('expenses', 'U') IS NOT NULL DROP TABLE expenses;")
cursor.execute("IF OBJECT_ID('vendors', 'U') IS NOT NULL DROP TABLE vendors;")
cursor.execute("IF OBJECT_ID('categories', 'U') IS NOT NULL DROP TABLE categories;")

cursor.execute("""
CREATE TABLE categories (
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    category_name NVARCHAR(50) NOT NULL UNIQUE
);
""")

cursor.execute("""
CREATE TABLE vendors (
    vendor_id INT IDENTITY(1,1) PRIMARY KEY,
    vendor_name NVARCHAR(100) NOT NULL UNIQUE
);
""")

cursor.execute("""
CREATE TABLE expenses (
    expense_id INT IDENTITY(1,1) PRIMARY KEY,
    expense_date DATE NOT NULL,
    category_id INT NOT NULL,
    vendor_id INT NOT NULL,
    description NVARCHAR(200),
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);
""")

conn.commit()
print("[OK] All tables created successfully!")

cursor.close()
conn.close()