from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGO_DETAILS')

### Database connect---------------------------------------------------
# connection details
# uri = "mongodb+srv://sim4nt:HANUman123@devcluster00.huotq7z.mongodb.net/?retryWrites=true&w=majority"

# database client and engine to connect with mongodb
client = MongoClient( uri, server_api=ServerApi('1'))
# database name in monogodb
db = client["test-users"]
users_db = db.users

# ping database
def ping_db():
    try:
        client.admin.command('ping')
        print("mongodb connected successfully")
        return {'message': 'Sucessfully connected to database'}
    except Exception as e:
        return {'error': e}

# close client
def close_connection():
    print(" closing mongodb client")
    client.close()

###---------------------------------------------------------------------