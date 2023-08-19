# for fastapi
from fastapi import FastAPI
from routes import user_router, student_router
from auth import auth_router

## local imports
from db import ping_db, close_connection

# fastapi app 
app = FastAPI()

app.include_router( user_router)
app.include_router( auth_router)
app.include_router( student_router)

@app.on_event("startup")
def check_db():
    ping_db()
    

@app.on_event("shutdown")
def end_connection():
    close_connection()
    