from dotenv import load_dotenv
import os
import logging
from typing import Generator, Optional

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()

DB_ENGINE = os.getenv("DB_ENGINE", "POSTGRES").upper()
USE_DYNAMO = os.getenv("USE_DYNAMO", "false").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "")
DB_SCHEMA = os.getenv("DB_SCHEMA", "test")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
Base = declarative_base()

DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 50)) 
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 10))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", 30))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", 1800))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("db")
if not USE_DYNAMO and DB_ENGINE == "POSTGRES":
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set. Please set it in your environment variables.")

    engine = create_engine(
        DATABASE_URL,
        pool_size=DB_POOL_SIZE,
        max_overflow=DB_MAX_OVERFLOW,
        pool_timeout=DB_POOL_TIMEOUT,
        pool_recycle=DB_POOL_RECYCLE,
        connect_args={"options": f"-c search_path={DB_SCHEMA}"},
        echo_pool=True,
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db() -> Generator[Session, None, None]:
        db: Optional[Session] = SessionLocal()
        logger.info(f"🔵 Nueva sesión abierta: id={id(db)}")
        try:
            yield db
            db.commit()
            logger.info(f"Sesión commit y cerrada correctamente: id={id(db)}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error en sesión {id(db)} -> rollback ({e})")
            raise
        finally:
            db.close()
            logger.info(f"Sesión cerrada (finally): id={id(db)}")

    @event.listens_for(engine, "connect")
    def connect_listener(dbapi_connection, connection_record):
        logger.info("Nueva conexión establecida con la base de datos.")

    @event.listens_for(engine, "checkout")
    def checkout_listener(dbapi_connection, connection_record, connection_proxy):
        logger.info("Conexión tomada del pool.")

    @event.listens_for(engine, "checkin")
    def checkin_listener(dbapi_connection, connection_record):
        logger.info("Conexión devuelta al pool.")

else:
    SessionLocal = None

    def get_db() -> Generator[None, None, None]:
        yield None
