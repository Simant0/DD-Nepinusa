# /project/repos/process_repos

from db.db import engine
from sqlmodel import Session, select
from models.process_models import Process
from models.school_models import School

def get_all_processes():
    with Session(engine) as session:
        statement = select(Process, School).join(School)
        res = session.exec(statement).all()
        return res

def get_process( id: int):
    with Session(engine) as session:
        statement = select(Process, School).where(Process.id == id).join(School)
        res = session.exec(statement).first()
        return res

def get_my_processes( id: int):
     with Session(engine) as session:
        statement = select(Process, School).where(Process.student_id == id).join(School)
        res = session.exec(statement).all()
        return res