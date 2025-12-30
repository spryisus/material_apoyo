"""
Paquete backend para The Clothesure 2.0
Manejo de colas RabbitMQ con reconexión automática
"""
from app.core.connection import RabbitMQConnection
from app.services.publisher import MessagePublisher
from app.services.consumer import MessageConsumer
from app.core.config import RabbitMQConfig, QueueConfig, LoggingConfig

__version__ = "1.0.0"
__author__ = "The Clothesure Team"

__all__ = [
    "RabbitMQConnection",
    "MessagePublisher", 
    "MessageConsumer",
    "RabbitMQConfig",
    "QueueConfig",
    "LoggingConfig"
]