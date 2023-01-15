# project/repos/school_repos.py

from db.db import engine
from sqlmodel import Session, select

from models.school_models import School

def get_school_by_id( id: int):
    with Session(engine) as session:
        statement = select(School).where( School.id == id)
        school = session.exec(statement).first()
        return school

def get_school_by_name( name: str):
    with Session(engine) as session:
        statement = select(School).where( School.name == name)
        school = session.exec(statement).first()
        return school

def get_school_names():
    with Session( engine) as session:
        statement = select(School)
        schools = session.exec(statement).all()
        school_names = []
        for item in schools:
            school_names.append(item.name)
        return school_names