# /project/endpoints/processs_endpoints.py

from fastapi import APIRouter,Depends
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from sqlmodel import select

from models.process_models import Process, ProcessPatch
from models.school_models import School
from models.user_models import UserTypes, User
from db.db import session
from endpoints.user_endpoints import auth_handler

from repos.school_repos import get_school_by_id, get_school_by_name
from repos.process_repos import get_all_processes, get_my_processes, get_process

import datetime

process_router = APIRouter(prefix="/processes")

@process_router.get('/')
def get_all_process( user: User=Depends(auth_handler.get_current_user)):
    if user.user_type == UserTypes.STUDENT:
        my_processes = get_my_processes( user.id)
        return {'processes': my_processes} 
    else:
        processes = get_all_processes()
        return {'processes': processes}

@process_router.get('/{id}')
def get_process_by_id(id: int, user: User=Depends(auth_handler.get_current_user)):
    if user.user_type == UserTypes.STUDENT:
        my_processes = get_my_processes( user.id)
        for p in my_processes:
            if p["Process"].id == id:
                return{'process': p}   
    else:
        process = get_process(id)
        if not process:
            return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'process not found'})
        return {'processes': process}        

@process_router.post('/')
def create_process( process: Process, school_name:str, user: User=Depends(auth_handler.get_current_user)):
    if user.user_type == UserTypes.STUDENT:
        school = get_school_by_name( school_name)
        if not school:
            return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'school not found'})
        new_process =  Process( title=process.title, process_type=process.process_type, status=process.status, notes=process.notes, school=school, school_id=school.id, student_id=user.id, student=user)
        session.add( new_process)
        session.commit()
        return process
    else:
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'only for students'})

@process_router.put('/{id}', response_model=Process)
def replace_process(id: int, process: ProcessPatch, user: User=Depends(auth_handler.get_current_user)):
    if user.user_type == UserTypes.STUDENT:
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'not authorized'})
    process_found = session.get( Process, id)
    if not process_found:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'process not found'})
    update_item_encoded = jsonable_encoder(process)
    update_item_encoded.pop('id', None)
    for key, val in update_item_encoded.items():
        process_found.__setattr__(key, val)
    last_modified = datetime.datetime.now()
    process_found.__setattr__('last_modified', last_modified)
    session.commit()
    return process_found

@process_router.patch('/{id}', response_model=Process)
def patch_process( id: int, process: ProcessPatch, user: User=Depends(auth_handler.get_current_user)):
    if user.user_type == UserTypes.STUDENT:
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'not authorized'})
    process_found = session.get( Process, id)
    if not process_found:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'process not found'})
    update_data = process.dict(exclude_unset=True)
    update_data.pop('id', None)
    for key, val in update_data.items():
        process_found.__setattr__(key, val)
    last_modified = datetime.datetime.now()
    process_found.__setattr__('last_modified', last_modified)
    session.commit()
    return process_found

@process_router.delete('/{id}')
def delete_process( id:int, user: User=Depends(auth_handler.get_current_user)):
    if user.user_type == UserTypes.STUDENT:
        return JSONResponse( status_code=HTTP_401_UNAUTHORIZED, content={'error': 'not authorized'})
    process_found = session.get( Process, id)
    if not process_found:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content={'error': 'process not found'})
    session.delete( process_found)
    session.commit()
    return {'message': 'process deleted'}


    
