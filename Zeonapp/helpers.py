
from bson.objectid import ObjectId
import datetime

# local imports
from db import users_db
from models import UserDetails

### Mongo to api( bson to json)----------------------------------------
# def user_details_serializer( user_details)

# def user_serializer( user) -> dict:
#     return{
#         "id": str(user["_id"]),
#         "name": str(user["name"]),
#         "user_type": user["user_type"],
#         "user_details": user["user_details"],  
#         "created_at": str(user["created_at"]),
#     }

def user_serializer( user) -> dict:
    if user:
        user["_id"] = str( user["_id"])
        return dict( user)
    else:
        return {}

def users_list_serializer( users) -> list:
    users_list = []
    for user in users:
        users_list.append( user_serializer( user))
    return users_list
###--------------------------------------------------------------------

###Helper functions-----------------------------------------------------

# add an user
def add_user( user):
    
    if users_db.find_one({"email": user.email}):
        return None
    
    if users_db.find_one({"username": user.username}):
        return None
    
    # change Enums into strings
    user.user_type = str(user.user_type)
    user.user_details.personal.gender = str(user.user_details.personal.gender)
    
    # now add into database
    user = users_db.insert_one(user.dict())
    user = users_db.find_one({"_id": ObjectId( user.inserted_id)})
    user = user_serializer( user)
    return user

# get one user
def retrieve_one_user( user_id):
    user = users_db.find_one({"_id": ObjectId( user_id)})
    user = user_serializer( user)
    return user

# modify one user
def modify_user( user_id, updated_user):
    user_dict = {}
    
    ## type convert manually                   
    if updated_user.user_details:
        if updated_user.user_details.personal:
            if updated_user.user_details.personal.gender:
                updated_user.user_details.personal.gender = str( updated_user.user_details.personal.gender)
            if updated_user.user_details.personal.profile_picture:
                updated_user.user_details.personal.profile_picture = dict( updated_user.user_details.personal.profile_picture)
            updated_user.user_details.personal = dict( updated_user.user_details.personal)
        if updated_user.user_details.contact:
            updated_user.user_details.contact = dict(updated_user.user_details.contact)
        
        if updated_user.user_details.address:
            updated_user.user_details.address = dict(updated_user.user_details.address)
        if updated_user.user_details.application:
            updated_user.user_details.application = dict(updated_user.user_details.application)        
        # if updated_user.user_details.files:
        #     for i in range( len(updated_user.user_details.files)):
        #         updated_user.user_details.files[i] = dict(updated_user.user_details.files[i])
        # if updated_user.user_details.universities:
        #     for i in range( len(updated_user.user_details.universities)):
        #         updated_user.user_details.universities[i] = dict(updated_user.user_details.universities[i])
        # if updated_user.user_details.services:
        #     for i in range( len(updated_user.user_details.services)):
        #         updated_user.user_details.services[i] = dict(updated_user.user_details.services[i])
        
        updated_user.user_details = dict( updated_user.user_details)
        
    for k, v in updated_user:
        if v != None:
            user_dict.update({k: v})
    
    try:
        personal_details = user_dict['user_details']['personal']
    except:
        personal_details = None
    try:
        contact_details = user_dict['user_details']['contact']
    except:
        contact_details = None
    try:
        address_details = user_dict['user_details']['address']
    except:
        address_details = None
    try:
        application_details = user_dict['user_details']['application']
    except:
        application_details = None
    
    if personal_details:
        users_db.find_one_and_update({"_id": ObjectId( user_id)},{"$set": {'user_details.personal': personal_details}})
    if contact_details:
        users_db.find_one_and_update({"_id": ObjectId( user_id)},{"$set": {'user_details.contact': contact_details}})
    if address_details:
        users_db.find_one_and_update({"_id": ObjectId( user_id)},{"$set": {'user_details.address': address_details}})
    if application_details:
        users_db.find_one_and_update({"_id": ObjectId( user_id)},{"$set": {'user_details.application': application_details}})
    # print (user_dict['user_details']['personal'])
    # users_db.find_one_and_update({"_id": ObjectId( user_id)},{"$set": user_dict})
    user = users_db.find_one({"_id": ObjectId( user_id)})
    user = user_serializer( user)
    return user

# delete user
def remove_user( user_id):
    users_db.find_one_and_delete( {"_id": ObjectId( user_id)})
    return {'message': 'User deleted'}    

# get all users
def retrieve_all_users():
    users = users_db.find()
    if users:
        users = users_list_serializer( users)
        return users
    return None  

# # add files
def add_file( user_id, file):
     # upload files function
    user = users_db.find_one( {"_id": ObjectId( user_id)})
    if user:
        # print (user)
        try:
            files_list = user['user_details']['files']
            files_list = list( files_list)
        except:
            files_list = []
        files_list.append( file)
        users_db.find_one_and_update({"_id": ObjectId( user_id)},{"$set": {"user_details.files": files_list}})
    user = users_db.find_one( {"_id": ObjectId( user_id)})
    user = user_serializer( user)
    return user

# # add services
def add_service( user_id, service):
     # add services function
    user = users_db.find_one( {"_id": ObjectId( user_id)})
    if user:
        # print (user)
        try:
            services_list = user['user_details']['services']
            services_list = list( services_list)
        except:
            services_list = []
        services_list.append( service)
        users_db.find_one_and_update({"_id": ObjectId( user_id)},{"$set": {"user_details.services": services_list}})
    user = users_db.find_one( {"_id": ObjectId( user_id)})
    user = user_serializer( user)
    return user

# # add universities
def add_university( user_id, university):
     # add university function
    user = users_db.find_one( {"_id": ObjectId( user_id)})
    if user:
        # print (user)
        try:
            universities_list = user['user_details']['universities']
            universities_list = list( universities_list)
        except:
            universities_list = []
        universities_list.append( university)
        users_db.find_one_and_update({"_id": ObjectId( user_id)},{"$set": {"user_details.universities": universities_list}})
    user = users_db.find_one( {"_id": ObjectId( user_id)})
    user = user_serializer( user)
    return user

###-----------------------------------------------------------------------------