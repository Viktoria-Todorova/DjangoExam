import pandas as pd
from sqlalchemy import create_engine

"""
Excel to PostgreSQL Import Script
==================================

This script imports book data from an Excel file into a Django PostgreSQL database.

Requirements:
-------------
pip install pandas openpyxl django sqlalchemy
"""

def import_excel(path):
    raw_data = pd.read_excel(path)
    raw_data.columns = raw_data.columns.str.strip().str.lower().str.replace(' ', '_')
    raw_data['writer'] = raw_data['writer'].fillna('Unknown Author')
    raw_data['genre'] = raw_data['genre'].fillna('NONE')
    raw_data['quantity'] = raw_data['quantity'].fillna(0)
    raw_data['quantity'] = raw_data['quantity'].astype(int)
    return raw_data

DATABASE_URL = "postgresql://tori:123456@localhost:5432/library_db"
engine = create_engine(DATABASE_URL)

path = r"D:\SoftUni\DjangoExam\extra\LibraryDataSet.xlsx"
data =import_excel(path)

table_name = 'catalog_catalog'
data.to_sql(table_name, engine, if_exists='append', index=False)
print(f"✓ Successfully imported {len(data)} rows into {table_name}")