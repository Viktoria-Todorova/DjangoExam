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
# Maps to Django model choices
GENRE_TRANSLATION = {
    'фентъзи': 'FANTASY',
    'роман': 'NOVEL',
    'научна фантастика': 'SCIENCE_FICTION',
    'трилър': 'THRILLER',
    'криминале': 'CRIME',
    'романтика': 'ROMANCE',
    'ужаси': 'HORROR',
    'мистерия': 'MYSTERY',
    'драма': 'DRAMA',
    'биография / мемоари': 'BIOGRAPHY_MEMOIR',
    'мемоари': 'BIOGRAPHY_MEMOIR',
    'самоусъвършенстване': 'SELF_IMPROVEMENT',
    'българска класика': 'BULGARIAN_CLASSICS',
    'класика': 'BULGARIAN_CLASSICS',
    'поезия': 'POETRY',
    'лгбт литература': 'LGBT_LITERATURE',
    'учебник': 'TEXTBOOK',
    'езотерика': 'ESOTERIC',
    'готварски': 'COOKBOOKS',
    'приключения': 'ADVENTURE',
    'разкази': 'SHORT_STORIES',
    'антология': 'ANTHOLOGY',
    'научно-популярна': 'POPULAR_SCIENCE',
    'исторически' : 'HISTORY',
    'none': 'NONE',
}


def translate_genre(genre_value):
    """Translate Bulgarian genre to English"""
    if pd.isna(genre_value):
        return 'NONE'

    genre_str = str(genre_value).strip().lower()

    if genre_str in GENRE_TRANSLATION:
        return GENRE_TRANSLATION[genre_str]

    return genre_value.strip().title()

def import_excel(path):
    raw_data = pd.read_excel(path)
    raw_data.columns = raw_data.columns.str.strip().str.lower().str.replace(' ', '_')
    raw_data['writer'] = raw_data['writer'].fillna('Unknown Author')
    raw_data['genre'] = raw_data['genre'].fillna('NONE')
    raw_data['genre'] = raw_data['genre'].apply(translate_genre)
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