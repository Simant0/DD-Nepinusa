# /projects/endpoints/user_endpoints.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from sqlmodel import select

from auth.auth import AuthHandler
from db.db import session
from models.user_models import UserInput, User, UserLogin, UserDetails, UserTypes
from repos.user_repos import select_all_users, find_user_email , find_user_details, find_user_by_id

user_router = APIRouter()

# for admins and staffs
privileged_user_router = APIRouter()

# for admins
super_privileged_user_router = APIRouter()
auth_handler = AuthHandler()


@user_router.post('/registration', status_code=201,description='Register new user')
def register(user: UserInput):
    # user_found  = find_user(user.username)
    # if user_found:
    #     raise HTTPException(status_code=400, detail='Username is taken')
    user_found = find_user_email(user.email)
    if user_found:
        raise HTTPException(status_code=400, detail='E-mail is already used to create an account')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(first_name=user.first_name,last_name=user.last_name, password=hashed_pwd, email=user.email, user_type=user.user_type, password2=user.password2)
    session.add(u)
    session.commit()
    return {'message' : 'user created'}


@user_router.post('/login')
def login(user: UserLogin):
    # user_found = find_user(user.username)
    # if not user_found:
    user_found = find_user_email( user.email)
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid email and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid email and/or password')
    token = auth_handler.encode_token(user_found.email)
    return {'token': token}


@user_router.get('/me')
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user

@user_router.get('/user_details')
def get_user_details(user: User = Depends(auth_handler.get_current_user)):
    return find_user_details( user.id)

@user_router.post('/user_details')
def add_user_details( user_details: UserDetails, user:User = Depends(auth_handler.get_current_user)):
    user_details_found = find_user_details( user.id)
    if user_details_found:
        return{ 'message': 'user details already exists'}
    new_user_details = UserDetails( first_name=user_details.first_name, last_name=user_details.last_name, middle_name=user_details.middle_name, address= user_details.address, phone=user_details.phone, user = user, user_id=user.id)
    session.add( new_user_details)
    session.commit()
    return { 'user_details': new_user_details}

@user_router.put('/user_details')
def replace_user_details( user_details: UserDetails, user: User = Depends( auth_handler.get_current_user)):
    user_d = find_user_details( user.id)
    if not user_d:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error':'user details not found'})
    user_details_found = session.get(UserDetails, user_d.id)
    update_data = jsonable_encoder( user_details)
    update_data.pop('id', None)
    update_data.pop('user_id', None)
    update_data.pop('user', None)
    for key,val in update_data.items():
        user_details_found.__setattr__(key, val)
    session.commit()
    return { 'user_details': user_details_found}

@user_router.patch('/user_details')
def replace_user_details( user_details: UserDetails, user: User = Depends( auth_handler.get_current_user)):
    user_d = find_user_details( user.id)
    if not user_d:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error':'user details not found'})
    user_details_found = session.get(UserDetails, user_d.id)
    update_data = user_details.dict(exclude_unset=True)
    update_data.pop('id', None)
    update_data.pop('user_id', None)
    update_data.pop('user', None)
    for key,val in update_data.items():
        user_details_found.__setattr__(key, val)
    session.commit()
    return { 'user_details': user_details_found}


## Privileged routes
## ****(O O)****
##      III
## for admin and staff controls
@privileged_user_router.get('/p1/students')
def privileged_get_all_students( user:User = Depends( auth_handler.get_current_user)):
    if (user.user_type != UserTypes.ADMIN) and (user.user_type != UserTypes.STAFF):
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'not authorized', 'user': user.user_type._name_})
    users_found = select_all_users()
    students = []
    for u in users_found:
        if u.user_type == UserTypes.STUDENT:
            students.append(u)
    return {'students': students}

@privileged_user_router.get('/p1/students/{id}')
def privileged_get_student_detail( id: int, user:User = Depends( auth_handler.get_current_user)):
    if (user.user_type != UserTypes.ADMIN) and (user.user_type != UserTypes.STAFF):
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'not authorized'}) 
    student = find_user_by_id( id)
    if not student or student.user_type != UserTypes.STUDENT:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'student not found'})
    student_details = find_user_details( id)
    return {'student': student, 'details': student_details}

@privileged_user_router.delete('/p1/students/details/{id}/')
def privileged_delete_student_details( id: int, user:User = Depends( auth_handler.get_current_user)):
    if user.user_type != UserTypes.ADMIN and user.user_type != UserTypes.STAFF:
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'not authorized'}) 
    student = find_user_by_id( id)
    if not student:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'student not found'})
    student_details = find_user_details( id)
    if not student_details:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'student details not found'})
    student_details_found = session.get( UserDetails, student_details.id)
    session.delete( student_details_found)
    session.commit()
    return{'message': 'student details deleted'}

## Super Privileged routes
## ****(O O)****
## xxxx III xxxx
## for admin controls    
@super_privileged_user_router.delete('/p2/users/{id}')
def super_priviliged_delete_user( id: int, user: User= Depends( auth_handler.get_current_user)):
    if user.user_type != UserTypes.ADMIN :
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'not authorized'})
    user_details = find_user_details( id)
    if not user:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'student details not found'})
    user_details_found = session.get( UserDetails, user_details.id)
    session.delete( user_details_found)
    user_found = session.get(User, id)
    session.delete( user_found)
    session.commit()
    return{'message': 'user deleted'}

@super_privileged_user_router.get('/p2/users')
def super_privileged_get_all_users( user: User = Depends( auth_handler.get_current_user)):
    if user.user_type != UserTypes.ADMIN :
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'not authorized'})
    users = select_all_users()
    return {'users': users}

@super_privileged_user_router.get('/p2/users/{id}')
def super_privileged_get_user( id: int, user: User = Depends( auth_handler.get_current_user)):
    if user.user_type != UserTypes.ADMIN :
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'not authorized'})
    user_found = session.get( User, id)
    if not user_found:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'not authorized'})
    return {'user': user_found}


    
    