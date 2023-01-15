# /project/main.py

from fastapi import FastAPI

from endpoints.school_endpoints import school_router
from endpoints.process_endpoints import process_router
from endpoints.user_endpoints import user_router, privileged_user_router, super_privileged_user_router

app = FastAPI()

app.include_router(school_router, tags=['Schools'])
app.include_router(process_router, tags=['Processes'])
app.include_router(user_router, tags=['Users'])
app.include_router(privileged_user_router, tags=['Staff'])
app.include_router(super_privileged_user_router, tags=['Admin'])

@app.get("/")
def root():
    return {'message': "hello world"}

# def create_db_and_tables(): 
#     SQLModel.metadata.create_all(engine)  


# if __name__ == "__main__": 
#     create_db_and_tables()