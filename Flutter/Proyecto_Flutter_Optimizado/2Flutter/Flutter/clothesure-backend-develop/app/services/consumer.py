"""
Módulo para consumo de mensajes de RabbitMQ (CloudAMQP)
"""

import json
import logging
import threading
import time
from typing import Callable, Optional, Dict, Any
from app.core.connection import RabbitMQConnection

logger = logging.getLogger(__name__)


class MessageConsumer:
    def __init__(self, connection: RabbitMQConnection):
        self.connection = connection
        self._consuming = False
        self._consumer_threads = {}
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

    def _create_callback_wrapper(self, callback: Callable, queue_name: str) -> Callable:
        def wrapped_callback(ch, method, properties, body):
            try:
                message_str = body.decode('utf-8')
                try:
                    message_data = json.loads(message_str)
                except json.JSONDecodeError:
                    message_data = message_str

                logger.debug(f"📨 Mensaje recibido en '{queue_name}': {message_data}")

                callback(message_data, method, properties)
                ch.basic_ack(delivery_tag=method.delivery_tag)

            except Exception as e:
                logger.error(f"❌ Error procesando mensaje en '{queue_name}': {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        return wrapped_callback

    def start_consuming(self, queue_name: str, callback: Callable, auto_ack: bool = False) -> bool:
        try:
            if queue_name in self._consumer_threads:
                logger.warning(f"⚠️ Ya se está consumiendo la cola '{queue_name}'")
                return False

            wrapped_callback = self._create_callback_wrapper(callback, queue_name)
            consumer_thread = threading.Thread(
                target=self._consume_queue,
                args=(queue_name, wrapped_callback, auto_ack),
                daemon=True
            )
            consumer_thread.start()
            self._consumer_threads[queue_name] = consumer_thread

            logger.info(f"🎧 Iniciando consumo de la cola '{queue_name}'")
            return True

        except Exception as e:
            logger.error(f"❌ Error al iniciar consumo de '{queue_name}': {e}")
            return False

    def _consume_queue(self, queue_name: str, callback: Callable, auto_ack: bool):
        while self._consuming:
            try:
                channel = self.connection.get_channel()
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=auto_ack)

                logger.info(f"🎧 Escuchando mensajes en la cola '{queue_name}'...")
                channel.start_consuming()

            except Exception as e:
                logger.error(f"❌ Error en consumo de '{queue_name}': {e}")
                if not self.connection.ensure_connection():
                    logger.warning(f"⚠️ No se pudo reconectar para '{queue_name}', reintentando en 5 segundos...")
                    time.sleep(5)

    def stop_consuming(self, queue_name: Optional[str] = None):
        if queue_name:
            if queue_name in self._consumer_threads:
                del self._consumer_threads[queue_name]
                logger.info(f"⏹️ Deteniendo consumo de la cola '{queue_name}'")
        else:
            self._consuming = False
            self._consumer_threads.clear()
            logger.info("⏹️ Deteniendo todos los consumos")

    def start_all_consuming(self):
        self._consuming = True
        self.start_consuming('reacciones_cola', self._default_reaction_callback)
        self.start_consuming('persistencia_cola', self._default_persistence_callback)
        logger.info("🚀 Iniciando consumo de todas las colas")

    def stop_all_consuming(self):
        """Detiene el consumo de todas las colas"""
        self.stop_consuming()
        logger.info("🛑 Deteniendo consumo de todas las colas")

    def _default_reaction_callback(self, message_data: Any, method, properties):
        logger.info(f"🔥 [REACCIONES] Procesando: {message_data}")
        if isinstance(message_data, dict) and message_data.get('tipo') == 'reaccion':
            user_id = message_data.get('usuario_id')
            outfit_id = message_data.get('outfit_id')
            action = message_data.get('accion')
            logger.info(f"👤 Usuario {user_id} {action} outfit {outfit_id}")

    def _default_persistence_callback(self, message_data: Any, method, properties):
        logger.info(f"💾 [PERSISTENCIA] Procesando: {message_data}")
        if isinstance(message_data, dict) and message_data.get('tipo') == 'persistencia':
            event_type = message_data.get('evento')
            data = message_data.get('datos')
            logger.info(f"📊 Evento de persistencia: {event_type} - {data}")

    def get_queue_info(self, queue_name: str) -> Optional[Dict[str, Any]]:
        try:
            channel = self.connection.get_channel()
            method = channel.queue_declare(queue=queue_name, passive=True)
            return {
                'queue': queue_name,
                'message_count': method.method.message_count,
                'consumer_count': method.method.consumer_count
            }
        except Exception as e:
            logger.error(f"❌ Error obteniendo info de cola '{queue_name}': {e}")
            return None

    def purge_queue(self, queue_name: str) -> bool:
        try:
            channel = self.connection.get_channel()
            method = channel.queue_purge(queue=queue_name)
            logger.info(f"🧹 Cola '{queue_name}' limpiada: {method.method.message_count} mensajes eliminados")
            return True
        except Exception as e:
            logger.error(f"❌ Error limpiando cola '{queue_name}': {e}")
            return False