# /project/endpoints/school_endpoints.py

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from sqlmodel import select

from models.school_models import School, SchoolPatch
from models.user_models import UserTypes
from db.db import session
from repos.school_repos import get_school_names
from endpoints.user_endpoints import auth_handler

school_router = APIRouter(prefix="/schools")

@school_router.get('/list')
def get_all_school_names():
    return get_school_names()
    

@school_router.get('/')
def get_all_schools():
    statement = select(School)
    schools = session.exec(statement).all()
    return schools

@school_router.get('/{id}', response_model=School)
def get_school(id: int):
    school_found = session.get(School, id)
    if not school_found:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content=school_found)
    return school_found
        
@school_router.post('/')
def create_school( school: School, user=Depends(auth_handler.get_current_user)):
    if user.user_type != UserTypes.ADMIN:
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={'error' : 'user is restricted'})
    new_school =  School( name=school.name, address=school.address, description=school.description, is_available=school.is_available)
    session.add( new_school)
    session.commit()
    return school

@school_router.put('/{id}', response_model=School)
def replace_school(id: int, school: School, user=Depends(auth_handler.get_current_user)):
    if user.user_type != UserTypes.ADMIN:
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={'error' : 'user is restricted'})
    school_found = session.get( School, id)
    if not school_found:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content=school_found)
    update_item_encoded = jsonable_encoder(school)
    update_item_encoded.pop('id', None)
    for key, val in update_item_encoded.items():
        school_found.__setattr__(key, val)
    session.commit()
    return school_found

@school_router.patch('/{id}', response_model=School)
def patch_school( id: int, school: SchoolPatch, user=Depends(auth_handler.get_current_user)):
    if user.user_type != UserTypes.ADMIN:
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={'error' : 'user is restricted'})
    school_found = session.get( School, id)
    if not school_found:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content=school_found)
    update_data = school.dict(exclude_unset=True)
    update_data.pop('id', None)
    for key, val in update_data.items():
        school_found.__setattr__(key, val)
    session.commit()
    return school_found

@school_router.delete('/{id}')
def delete_school( id:int, user=Depends(auth_handler.get_current_user)):
    if user.user_type != UserTypes.ADMIN:
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={'error' : 'user is restricted'})
    school_found = session.get( School, id)
    if not school_found:
        return JSONResponse( status_code=HTTP_404_NOT_FOUND, content=school_found)
    session.delete( school_found)
    session.commit()
    return {'message': 'school deleted'}


    
