from fastapi import FastAPI
from app.core.db import Base, engine
from app.routes import carros_handler, user_handler, photo_handler, post_handler,preference_question_handler,preference_options_handler,user_preference_handler, preferences_handler
from app.services.publisher import MessagePublisher
from app.core.connection import RabbitMQConnection
from app.core.config import RabbitMQConfig
import logging
from app.models.preference_questions_model import PreferenceQuestion
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)

app = FastAPI(title="CRUD genérico implementado a Carros")

origins = [
    "http://localhost:60492",  
    "http://127.0.0.1:60492",
    "http://localhost:8000",   
    "*",                        
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(carros_handler.router)
app.include_router(user_handler.router)
app.include_router(photo_handler.router)
app.include_router(post_handler.router)
app.include_router(preference_question_handler.router)
app.include_router(preferences_handler.router, prefix="/api/preferences", tags=["preferences"])


@app.on_event("startup")
async def startup_event():
    app.state.rabbit_conn = RabbitMQConnection(url=RabbitMQConfig.get_config()['url'])
    if app.state.rabbit_conn.connect():
        logger.info("Conexión a RabbitMQ establecida para la API")
        app.state.publisher = MessagePublisher(app.state.rabbit_conn)
    else:
        logger.error("No se pudo conectar a RabbitMQ en la API")

@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state, "rabbit_conn"):
        app.state.rabbit_conn.disconnect()
        logger.info("🔌 Conexión a RabbitMQ cerrada en la API")