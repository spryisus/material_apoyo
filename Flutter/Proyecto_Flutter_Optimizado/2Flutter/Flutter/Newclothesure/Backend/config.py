import os
from typing import Dict, Any
from dotenv import load_dotenv
import logging

load_dotenv() 
class RabbitMQConfig:
    """Configuración para RabbitMQ usando CloudAMQP"""
    
    
    DEFAULT_CONFIG = {
        'url': os.getenv('CLOUDAMQP_URL'),
        'max_retries': 5,
        'retry_delay': 2.0,
        'heartbeat': 600,
        'blocked_connection_timeout': 300
    }
    
    @classmethod
    def from_env(cls) -> Dict[str, Any]:
        config = cls.DEFAULT_CONFIG.copy()
        
        env_mapping = {
            'CLOUDAMQP_URL': 'url',
            'RABBITMQ_MAX_RETRIES': 'max_retries',
            'RABBITMQ_RETRY_DELAY': 'retry_delay',
            'RABBITMQ_HEARTBEAT': 'heartbeat',
            'RABBITMQ_BLOCKED_TIMEOUT': 'blocked_connection_timeout'
        }
        
        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convertir tipos según sea necesario
                if config_key in ['max_retries', 'heartbeat', 'blocked_connection_timeout']:
                    config[config_key] = int(value)
                elif config_key in ['retry_delay']:
                    config[config_key] = float(value)
                else:
                    config[config_key] = value
        
        return config
    
    @classmethod
    def get_config(cls, **overrides) -> Dict[str, Any]:
        config = cls.from_env()
        config.update(overrides)
        return config
class QueueConfig:
    QUEUES = {
        'reacciones_cola': {
            'durable': True,
            'arguments': {
                'x-message-ttl': 10000,  # 10 segundos
                'x-max-length': 5000     # Máximo 5000 mensajes
            }
        },
        'persistencia_cola': {
            'durable': True,
            'arguments': {
                'x-dead-letter-exchange': 'x-dead-letter-exchange'
            }
        }
    }
    
    # Configuración del exchange
    EXCHANGE = {
        'name': 'events_exchange',
        'type': 'fanout',
        'durable': True
    }
    
    @classmethod
    def get_queue_config(cls, queue_name: str) -> Dict[str, Any]:
        return cls.QUEUES.get(queue_name, {})
    
    @classmethod
    def get_exchange_config(cls) -> Dict[str, Any]:
        return cls.EXCHANGE.copy()


class LoggingConfig:
    DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def setup_logging(cls, level: str = 'INFO', format_string: str = None):
        format_string = format_string or cls.DEFAULT_FORMAT
        
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format=format_string
        )
        
        # Configurar logger específico para el paquete
        package_logger = logging.getLogger('backend')
        package_logger.setLevel(getattr(logging, level.upper()))


# Configuración por defecto
DEFAULT_RABBITMQ_CONFIG = RabbitMQConfig.get_config()
DEFAULT_QUEUE_CONFIG = QueueConfig.QUEUES
DEFAULT_EXCHANGE_CONFIG = QueueConfig.get_exchange_config()

