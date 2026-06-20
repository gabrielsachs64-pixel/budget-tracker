# Budget Tracker

A business expense tracking system using Python and Azure SQL Database.

## What it does
- Stores expenses in a relational database (categories, vendors, expenses)
- Connects Python to a live Azure SQL Database using pyodbc
- Runs SQL JOIN queries to generate expense reports
- Exports results to a formatted Excel report

## Tech stack
- Python 3.14
- Azure SQL Database
- pyodbc, pandas, openpyxl, python-dotenv

## Database schema
- `categories` — expense categories (Office Supplies, Travel, Software, etc.)
- `vendors` — who payments are made to
- `expenses` — transactions, linked to categories and vendors via foreign keys

## Sample output

| category_name   | total_spent | num_transactions |
|-----------------|-------------|-------------------|
| Travel          | 792.00      | 2                 |
| Office Supplies | 309.50      | 2                 |
| Marketing       | 300.00      | 1                 |
| Software        | 153.99      | 2                 |
| Utilities       | 150.00      | 1                 |

## Security note
Database credentials are stored in a `.env` file (excluded from version control via `.gitignore`).
