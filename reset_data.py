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

cursor.execute("DELETE FROM expenses;")
cursor.execute("DELETE FROM vendors;")
cursor.execute("DELETE FROM categories;")

# Reset identity counters back to 1
cursor.execute("DBCC CHECKIDENT ('categories', RESEED, 0);")
cursor.execute("DBCC CHECKIDENT ('vendors', RESEED, 0);")
cursor.execute("DBCC CHECKIDENT ('expenses', RESEED, 0);")

conn.commit()
print("[OK] All tables cleared and reset!")

cursor.close()
conn.close()