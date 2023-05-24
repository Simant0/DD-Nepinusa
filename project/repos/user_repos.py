# /project/repos/user_repos.py

from db.db import engine
from sqlmodel import Session, select
from models.user_models import User, UserDetails

def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res

# def find_user(name: str):
#     with Session(engine) as session:
#         statement = select(User).where(User.username == name)
#         res = session.exec(statement).first()
#         return res

def find_user_email( email: str):
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        res = session.exec(statement).first()
        return res

def find_user_by_id(id: int):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        res = session.exec(statement).first()
        return res

def find_user_details( user_id: int):
    with Session(engine) as session:
        statement = select(UserDetails).where(UserDetails.user_id == user_id)
        res = session.exec(statement).first()
        return res