"""
Paquete backend para The Clothesure 2.0
Manejo de colas RabbitMQ con reconexión automática
"""
from connection import RabbitMQConnection
from publisher import MessagePublisher
from consumer import MessageConsumer
from config import RabbitMQConfig, QueueConfig, LoggingConfig

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
