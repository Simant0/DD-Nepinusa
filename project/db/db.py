# /project/db/db.py

from sqlmodel import create_engine, Session

location = r'database.db'
sqlite_url = f'sqlite:///{location}'
engine = create_engine( sqlite_url, echo=True)
session = Session(bind=engine)