import time
import logging
from app.core.connection import RabbitMQConnection
from app.services.consumer import MessageConsumer
from app.services.publisher import MessagePublisher
from app.core.config import RabbitMQConfig, LoggingConfig

# Configurar logging
LoggingConfig.setup_logging(level='INFO')
logger = logging.getLogger(__name__)

def main():
    # Crear conexión a RabbitMQ
    rabbit_conn = RabbitMQConnection(url=RabbitMQConfig.get_config()['url'])
    consumer = MessageConsumer(rabbit_conn)
    publisher = MessagePublisher(rabbit_conn)  # Opcional, si necesitas republicar

    # Conectar y arrancar consumidores
    if rabbit_conn.connect():
        consumer.start_all_consuming()
        logger.info("🚀 Consumidores iniciados, escuchando colas...")
    else:
        logger.error("❌ No se pudo conectar a RabbitMQ. Saliendo...")
        return

    # Mantener el proceso vivo
    try:
        while True:
            time.sleep(3600)  # Mantener hilo principal vivo
    except KeyboardInterrupt:
        logger.info("👋 Deteniendo consumidores...")
        consumer.stop_all_consuming()
        rabbit_conn.disconnect()
        logger.info("🛑 Worker detenido")

if __name__ == "__main__":
    main()
