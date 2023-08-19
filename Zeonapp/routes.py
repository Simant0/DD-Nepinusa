from fastapi import APIRouter, Depends
from typing import Annotated

## local imports
from db import ping_db
from models import User, UserModify, Files, SelectedServices, SelectedUniversities
from helpers import retrieve_all_users, add_user, retrieve_one_user, modify_user, remove_user, add_file, add_service, add_university
from auth import get_current_user, AuthUser

user_router = APIRouter( prefix="/users", tags=['ADMINS'])
student_router = APIRouter( prefix="/student", tags=['STUDENT'])

### Endpoint Routes------------------------------------------------------------

# app home api
# @user_router.get("/")
# async def app_home():
#     return {'message': 'Hello, This is User Server'}

# database connection check
@user_router.get("/db_check/")
async def check_db_connection():
    return ping_db()
    
# get all users
@user_router.get("/")
async def get_users(
    current_user: Annotated[AuthUser, Depends( get_current_user)]
):
    if current_user["user_type"] == 'GOD' or current_user["user_type"] == 'ADMIN':
        users = retrieve_all_users()
        if users:
            return users
        else:
            return None
    return None

# add an user
@user_router.post("/")
async def create_user( user: User):
    user_created = add_user( user)
    if user_created:
        return user_created
    else:
        return {'error': 'cannot create account'}

# get one users
@user_router.get("/{user_id}")
def get_one_user( user_id: str, current_user: Annotated[AuthUser, Depends( get_current_user)]):
    if current_user["user_type"] == 'GOD' or current_user["user_type"] == 'ADMIN':
        users = retrieve_one_user( user_id)
        if users:
            return users
        else:
            return None
    return None

# update user
@user_router.patch("/{user_id}")
def update_user( user_id: str, user_updated: UserModify, current_user: Annotated[AuthUser, Depends( get_current_user)]):
    if current_user["user_type"] == 'GOD' or current_user["user_type"] == 'ADMIN':
        user = modify_user( user_id, user_updated)
        return user
    return None

# delete user
@user_router.delete("/{user_id}")
def delete_user( user_id: str, current_user: Annotated[AuthUser, Depends( get_current_user)]):
    if current_user["user_type"] == 'GOD':
        return remove_user( user_id)
    return None

# add files for user
@user_router.post("/files/{user_id}")
def upload_files(user_id: str, file: Files, current_user: Annotated[AuthUser, Depends( get_current_user)]):
    if current_user["user_type"] == 'GOD' or current_user["user_type"] == 'ADMIN':
        file = dict( file)
        user = add_file( user_id, file)
        return user
    return None

# add services for user
@user_router.post("/services/{user_id}")
def add_more_service(user_id: str, service: SelectedServices, current_user: Annotated[AuthUser, Depends( get_current_user)]):
    if current_user["user_type"] == 'GOD' or current_user["user_type"] == 'ADMIN':
        service = dict( service)
        user = add_service( user_id, service)
        return user
    return None

# add university for user
@user_router.post("/university/{user_id}")
def add_more_university(user_id: str, university: SelectedUniversities,current_user: Annotated[AuthUser, Depends( get_current_user)]):
    if current_user["user_type"] == 'GOD' or current_user["user_type"] == 'ADMIN':
        university = dict( university)
        user = add_university( user_id, university)
        return user
    return None

@user_router.get("/usersMe/")
def get_users_my_details(
    current_user: Annotated[AuthUser, Depends( get_current_user)]
):
    print(current_user["username"])
    return {'usr': current_user["username"]}

###---------------------------------------------------------------------

### Students Purposes Routes---------------------------------------------------------
@student_router.get("/my_details")
def get_my_details_student(
    current_user: Annotated[AuthUser, Depends( get_current_user)]
):
    if current_user["user_type"] == 'STUDENT':
        user = retrieve_one_user( current_user["id"])
        return user["user_details"]
    return None

@student_router.patch("/my_details")
def update_user( user_updated: UserModify, current_user: Annotated[AuthUser, Depends( get_current_user)]):
    if current_user["user_type"] == 'STUDENT':
        user = modify_user( current_user["id"], user_updated)
        return user
    return None

@student_router.post("/my_files")
def add_my_files( file: Files, current_user: Annotated[AuthUser, Depends( get_current_user)] ):
    if current_user["user_type"] == 'STUDENT':
        file = dict( file)
        add_file( current_user["id"], file)
        return {"File added"}
    return None

@student_router.post("/my_services")
def add_my_service( service: SelectedServices, current_user: Annotated[AuthUser, Depends( get_current_user)] ):
    if current_user["user_type"] == 'STUDENT':
        service = dict( service)
        add_more_service( current_user["id"], service)
        return {"Service added"}
    return None

@student_router.post("/my_universities")
def add_my_university( university: SelectedUniversities, current_user: Annotated[AuthUser, Depends( get_current_user)] ):
    if current_user["user_type"] == 'STUDENT':
        university = dict( university)
        add_more_university( current_user["id"], university)
        return {"University added"}
    return None


###----------------------------------------------------------------------------------