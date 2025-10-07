import pika
import logging
import time
from typing import Optional, Callable
from pika.exceptions import AMQPConnectionError
import os
from dotenv import load_dotenv

load_dotenv() 
logger = logging.getLogger(__name__)

class RabbitMQConnection:  
    def __init__(
        self,
        url: str = None,
        max_retries: int = 5,
        retry_delay: float = 5.0,
        heartbeat: int = 600,
        blocked_connection_timeout: int = 300
    ):
        self.url = url or os.getenv('CLOUDAMQP_URL')
        if not self.url:
            raise ValueError("Debe proporcionarse la URL de CloudAMQP en `url` o `CLOUDAMQP_URL`")
        
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.heartbeat = heartbeat
        self.blocked_connection_timeout = blocked_connection_timeout
        
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        self._is_connected = False
        self._retry_count = 0
        
        self.on_connect_callback: Optional[Callable] = None
        self.on_disconnect_callback: Optional[Callable] = None
        self.on_reconnect_callback: Optional[Callable] = None
    
    def _create_connection_parameters(self) -> pika.URLParameters:
        params = pika.URLParameters(self.url)
        params.heartbeat = self.heartbeat
        params.blocked_connection_timeout = self.blocked_connection_timeout
        return params
    
    def connect(self) -> bool:
        try:
            logger.info(f"Conectando a RabbitMQ usando URL: {self.url}")
            
            params = self._create_connection_parameters()
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            
            self._is_connected = True
            self._retry_count = 0
            
            logger.info("✅ Conexión a RabbitMQ establecida exitosamente")
            
            if self.on_connect_callback:
                self.on_connect_callback()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al conectar a RabbitMQ: {e}")
            self._is_connected = False
            return False
    
    def disconnect(self):
        """Cierra la conexión a RabbitMQ"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
            
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            
            self._is_connected = False
            logger.info("🔌 Conexión a RabbitMQ cerrada")
            
            if self.on_disconnect_callback:
                self.on_disconnect_callback()
                
        except Exception as e:
            logger.error(f"Error al cerrar conexión: {e}")
    
    def reconnect(self) -> bool:
        """Reintenta la conexión con backoff exponencial"""
        if self._retry_count >= self.max_retries:
            logger.error(f"❌ Máximo número de reintentos ({self.max_retries}) alcanzado")
            return False
        
        self._retry_count += 1
        delay = self.retry_delay * (2 ** (self._retry_count - 1))
        logger.warning(f"🔄 Reintentando conexión en {delay:.1f} segundos (intento {self._retry_count}/{self.max_retries})")
        time.sleep(delay)
        
        self.disconnect()
        success = self.connect()
        
        if success and self.on_reconnect_callback:
            self.on_reconnect_callback()
        
        return success
    
    def ensure_connection(self) -> bool:
        """Asegura que la conexión esté activa, reintentando si es necesario"""
        if self.is_connected():
            return True
        
        logger.warning("⚠️ Conexión perdida, intentando reconectar...")
        return self.reconnect()
    
    def is_connected(self) -> bool:
        """Verifica si la conexión está activa"""
        try:
            return self.connection and self.connection.is_open and self.channel and self.channel.is_open
        except Exception:
            return False
    
    def get_channel(self):
        """Obtiene el canal de RabbitMQ"""
        if not self.ensure_connection():
            raise AMQPConnectionError("No se pudo establecer conexión con RabbitMQ")
        return self.channel
    
    def set_on_connect_callback(self, callback: Callable):
        self.on_connect_callback = callback
    
    def set_on_disconnect_callback(self, callback: Callable):
        self.on_disconnect_callback = callback
    
    def set_on_reconnect_callback(self, callback: Callable):
        self.on_reconnect_callback = callback
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()