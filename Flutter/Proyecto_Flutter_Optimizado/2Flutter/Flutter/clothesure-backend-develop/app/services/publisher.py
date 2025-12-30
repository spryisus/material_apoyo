import json
import logging
from typing import Any, Dict, Optional
from app.core.connection import RabbitMQConnection
import time
import pika

logger = logging.getLogger(__name__)
class MessagePublisher:

    def __init__(self, connection: RabbitMQConnection):
        self.connection = connection
        self._setup_exchanges_and_queues()

    def _setup_exchanges_and_queues(self):
        try:
            channel = self.connection.get_channel()

            # Declarar el exchange principal
            channel.exchange_declare(
                exchange='events_exchange',
                exchange_type='fanout',
                durable=True
            )

            # Declarar las colas con sus parámetros
            channel.queue_declare(
                queue='reacciones_cola',
                durable=True,
                arguments={
                    'x-message-ttl': 10000,
                    'x-max-length': 5000
                }
            )

            channel.queue_declare(
                queue='persistencia_cola',
                durable=True,
                arguments={
                    'x-dead-letter-exchange': 'x-dead-letter-exchange'
                }
            )

            # Hacer binding de las colas al exchange
            channel.queue_bind(exchange='events_exchange', queue='reacciones_cola')
            channel.queue_bind(exchange='events_exchange', queue='persistencia_cola')

            logger.info("✅ Exchanges y colas configurados correctamente")

        except Exception as e:
            logger.error(f"❌ Error al configurar exchanges y colas: {e}")
            raise

    def publish_message(
        self,
        message: Any,
        exchange: str = 'events_exchange',
        routing_key: str = '',
        persistent: bool = True
    ) -> bool:
        """
        Publica un mensaje en el exchange especificado
        """
        try:
            if isinstance(message, dict):
                message_body = json.dumps(message, ensure_ascii=False)
            elif isinstance(message, str):
                message_body = message
            else:
                message_body = json.dumps(message, ensure_ascii=False, default=str)

            channel = self.connection.get_channel()

            properties = pika.BasicProperties(
                delivery_mode=2 if persistent else 1,
                content_type='application/json',
                content_encoding='utf-8'
            )

            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=message_body,
                properties=properties
            )

            logger.info(f"✅ Mensaje publicado en exchange '{exchange}': {message_body[:100]}...")
            return True

        except Exception as e:
            logger.error(f"❌ Error al publicar mensaje: {e}")
            return False

    def publish_reaction(
        self,
        user_id: str,
        outfit_id: str,
        action: str = 'like',
        metadata: Optional[Dict] = None
    ) -> bool:
        message = {
            'tipo': 'reaccion',
            'usuario_id': user_id,
            'outfit_id': outfit_id,
            'accion': action,
            'timestamp': time.time(),
            'metadata': metadata or {}
        }
        return self.publish_message(message)

    def publish_persistence_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        metadata: Optional[Dict] = None
    ) -> bool:
        message = {
            'tipo': 'persistencia',
            'evento': event_type,
            'datos': data,
            'timestamp': time.time(),
            'metadata': metadata or {}
        }
        return self.publish_message(message)

    def publish_user_event(
        self,
        user_id: str,
        event_type: str,
        data: Dict[str, Any]
    ) -> bool:
        message = {
            'tipo': 'usuario',
            'usuario_id': user_id,
            'evento': event_type,
            'datos': data,
            'timestamp': time.time()
        }
        return self.publish_message(message)

    def publish_outfit_event(
        self,
        outfit_id: str,
        event_type: str,
        data: Dict[str, Any]
    ) -> bool:
        message = {
            'tipo': 'outfit',
            'outfit_id': outfit_id,
            'evento': event_type,
            'datos': data,
            'timestamp': time.time()
        }
        return self.publish_message(message)

    def publish_batch_messages(self, messages: list) -> Dict[str, int]:
        success_count = 0
        failed_count = 0

        for message in messages:
            if self.publish_message(message):
                success_count += 1
            else:
                failed_count += 1

        logger.info(f"📊 Lote procesado: {success_count} exitosos, {failed_count} fallidos")
        return {
            'success': success_count,
            'failed': failed_count
        }