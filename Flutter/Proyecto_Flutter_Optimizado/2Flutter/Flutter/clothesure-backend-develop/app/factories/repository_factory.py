import os
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.interfaces.i_carros_repository import ICarrosRepository
from app.repositories.carros_repository import CarrosRepository 
from app.services.carros_service import CarrosService
from app.interfaces.photo_repository import IPhotoRepository
from app.repositories.photo_repository import PhotoModel
from app.services.photo_service import PhotoService
from app.interfaces.post_repository import IPostRepository
from app.repositories.post_repository import PostModel
from app.services.post_service import PostService
from app.interfaces.user_repository import IUserRepository
from app.repositories.user_repository import UserModel
from app.services.user_service import UserService
from app.interfaces.user_preference_repository import IUserPreferenceRepository
from app.repositories.user_preference_repository import UserPreferenceRepository
from app.services.user_preference_service import UserPreferenceService
from app.interfaces.preference_options_repository import IPreferenceOptionRepository
from app.repositories.preference_options_repository import PreferenceOptionsRepository
from app.services.preference_options_service import PreferenceOptionService
from app.interfaces.preference_questions_repository import IPreferenceQuestionRepository
from app.repositories.preference_questions_repository import PreferenceQuestionsRepository
from app.services.preference_questions_service import PreferenceOptionService
from app.interfaces.user_device_repository import IUserDeviceRepository
from app.repositories.user_device_repository import UserDeviceModel
from app.services.user_device_service import UserDeviceService


DB_SCHEMA = os.getenv("DB_SCHEMA")
#Cuando se agreguen más repositorios, se puede usar este factory method para elegir entre ellos
def factory_method(func):
    use_Dynamo = os.getenv("USE_DYNAMO", "false").lower() == "true"
    db_engine = os.getenv("DB_ENGINE", "POSTGRES").upper()
    if use_Dynamo or db_engine == "DYNAMODB":
        return None  # Placeholder for DynamoDB repository if implemented
    if func is None:
        raise ValueError("Invalid database session provided for Postgres repository.")
    
def set_search_schema(db: Session | None):
    if db is None:
        raise ValueError("Invalid database session provided for Postgres repository.")
    print(f"Setting search path to {DB_SCHEMA}")
    db.execute(text(f"SET search_path TO {DB_SCHEMA}"))

def get_carros_repository(db: Session) -> ICarrosRepository:
    #se podría agregar lógica para elegir entre diferentes repositorios
    return CarrosRepository(db)

def get_carros_service(db: Session) -> CarrosService:
    repository = get_carros_repository(db)
    return CarrosService(repository, db)

def get_photo_repository(db: Session | None) -> IPhotoRepository:
    use_dynamo = os.getenv("USE_DYNAMO", "false").lower() == "true"
    db_engine = os.getenv("DB_ENGINE", "POSTGRES").upper()

    if use_dynamo or db_engine == "DYNAMODB":
        return None  # Placeholder for DynamoDB repository if implemented

    if db is None:
        raise ValueError("Invalid database session provided for Postgres repository.")
    
    
    return PhotoModel(db) 

def get_photo_service(db: Session | None) -> PhotoService:
    repo = get_photo_repository(db)
    return PhotoService(repo)


def get_post_repository(db: Session | None) -> IPostRepository:
    use_dynamo = os.getenv("USE_DYNAMO", "false").lower() == "true"
    db_engine = os.getenv("DB_ENGINE", "POSTGRES").upper()

    if use_dynamo or db_engine == "DYNAMODB":
        return None  # Placeholder for DynamoDB repository if implemented

    if db is None:
        raise ValueError("Invalid database session provided for Postgres repository.")
    
    
    return PostModel(db) 

def get_post_service(db: Session | None) -> PostService:
    repo = get_post_repository(db)
    return PostService(repo)

def get_user_repository(db: Session | None) -> IUserRepository:
    use_dynamo = os.getenv("USE_DYNAMO", "false").lower() == "true"
    db_engine = os.getenv("DB_ENGINE", "POSTGRES").upper()

    if use_dynamo or db_engine == "DYNAMODB":
        return None  # Placeholder for DynamoDB repository if implemented

    if db is None:
        raise ValueError("Invalid database session provided for Postgres repository.")
    
    
    return UserModel(db) 

def get_user_service(db: Session | None) -> UserService:
    repo = get_user_repository(db)
    return UserService(repo)

def get_user_device_repository(db: Session | None) -> IUserDeviceRepository:
    use_dynamo = os.getenv("USE_DYNAMO", "false").lower() == "true"
    db_engine = os.getenv("DB_ENGINE", "POSTGRES").upper()

    if use_dynamo or db_engine == "DYNAMODB":
        return None  # Placeholder for DynamoDB repository if implemented

    if db is None:
        raise ValueError("Invalid database session provided for Postgres repository.")
    
    
    return UserDeviceModel(db)

def get_user_device_service(db: Session | None) -> UserDeviceService:
    repo = get_user_device_repository(db)
    return UserDeviceService(repo)


def get_user_preference_repository(db: Session | None) -> IUserPreferenceRepository:
    use_dynamo = os.getenv("USE_DYNAMO", "false").lower() == "true"
    db_engine = os.getenv("DB_ENGINE", "POSTGRES").upper()

    if use_dynamo or db_engine == "DYNAMODB":
        return None  # Placeholder for DynamoDB repository if implemented

    if db is None:
        raise ValueError("Invalid database session provided for Postgres repository.")
    
    
    return UserPreferenceRepository(db)

def get_user_preference_service(db: Session | None) -> UserPreferenceService:
    repo = get_user_preference_repository(db)
    return UserPreferenceService(repo)

def get_preference_options_repository(db: Session | None) -> IPreferenceOptionRepository:
    use_dynamo = os.getenv("USE_DYNAMO", "false").lower() == "true"
    db_engine = os.getenv("DB_ENGINE", "POSTGRES").upper()

    if use_dynamo or db_engine == "DYNAMODB":
        return None  # Placeholder for DynamoDB repository if implemented

    if db is None:
        raise ValueError("Invalid database session provided for Postgres repository.")
    
    
    return PreferenceOptionsRepository(db)

def get_preference_options_service(db: Session | None) -> PreferenceOptionService:
    repo = get_preference_options_repository(db)
    return PreferenceOptionService(repo)

def get_preference_question_repository(db: Session | None) -> IPreferenceQuestionRepository:
    use_dynamo = os.getenv("USE_DYNAMO", "false").lower() == "true"
    db_engine = os.getenv("DB_ENGINE", "POSTGRES").upper()

    if use_dynamo or db_engine == "DYNAMODB":
        return None  # Placeholder for DynamoDB repository if implemented

    if db is None:
        raise ValueError("Invalid database session provided for Postgres repository.")
    
    
    return PreferenceQuestionsRepository(db)

def get_preference_question_service(db: Session | None) -> PreferenceOptionService:
    repo = get_preference_question_repository(db)
    return PreferenceOptionService(repo)

