"""
Servidor Socket.IO para The Clothesure 2.0
Integra el frontend React con RabbitMQ a través de eventos Socket.IO
"""

import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import socketio
from aiohttp import web

# Agregar la raíz del proyecto al path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from connection import RabbitMQConnection
from publisher import MessagePublisher
from consumer import MessageConsumer
from config import LoggingConfig

load_dotenv() 
# Configurar logging
LoggingConfig.setup_logging(level='INFO')
logger = logging.getLogger(__name__)


class ClothesureSocketIOServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port

        # Inicializar Socket.IO server
        self.sio = socketio.AsyncServer(
            async_mode='aiohttp',
            cors_allowed_origins='*',
            ping_interval=20,
            ping_timeout=10
        )
        self.app = web.Application()
        self.sio.attach(self.app, socketio_path='socket.io')

        # Inicializar RabbitMQ
        self.rabbitmq_connection: Optional[RabbitMQConnection] = None
        self.publisher: Optional[MessagePublisher] = None
        self.consumer: Optional[MessageConsumer] = None

        # Eventos Socket.IO
        @self.sio.event
        async def connect(sid, environ):
            logger.info(f"🔌 Cliente conectado: {sid}")

        @self.sio.event
        async def disconnect(sid):
            logger.info(f"👋 Cliente desconectado: {sid}")

        @self.sio.event
        async def join_room(sid, data):
            room = data.get('room')
            if room:
                self.sio.enter_room(sid, room)
                logger.info(f"🎯 {sid} entró a room {room}")

        @self.sio.event
        async def leave_room(sid, data):
            room = data.get('room')
            if room:
                self.sio.leave_room(sid, room)
                logger.info(f"🎯 {sid} salió de room {room}")

        @self.sio.event
        async def like(sid, data):
            await self._handle_like_unlike(sid, data, action='like')

        @self.sio.event
        async def unlike(sid, data):
            await self._handle_like_unlike(sid, data, action='unlike')

    async def _handle_like_unlike(self, sid, data, action: str):
        try:
            user_id = data.get('userId') or data.get('user_id')
            outfit_id = data.get('outfitId') or data.get('outfit_id')
            if not user_id or not outfit_id:
                await self.sio.emit('error', {'message': 'userId y outfitId son requeridos'}, to=sid)
                return
            if self.publisher:
                self.publisher.publish_reaction(
                    user_id=user_id,
                    outfit_id=outfit_id,
                    action=action,
                    metadata={
                        'source': 'socketio',
                        'timestamp': data.get('timestamp'),
                        'likes_count': data.get('likes_count')
                    }
                )
            payload = {
                'outfit_id': outfit_id,
                'likes_count': data.get('likes_count'),
                'action': action,
                'user_id': user_id
            }
            await self.emit_event('like_update', payload, room=f'outfit_{outfit_id}')
        except Exception as e:
            logger.error(f"❌ Error en evento {action}: {e}")

    async def setup_rabbitmq(self):
        try:
            logger.info("🔌 Configurando conexión a RabbitMQ desde RABBITMQ_URL...")

            
            rabbitmq_url = os.getenv('CLOUDAMQP_URL')
            if not rabbitmq_url:
                logger.error("❌ No se encontró la variable de entorno CLOUDAMQP_URL")
                return False

        
            self.rabbitmq_connection = RabbitMQConnection(url=rabbitmq_url)

            if self.rabbitmq_connection.connect():
                logger.info("✅ Conexión a RabbitMQ establecida")
                self.publisher = MessagePublisher(self.rabbitmq_connection)
                self.consumer = MessageConsumer(self.rabbitmq_connection)
                self.consumer.start_consuming('reacciones_cola', self.handle_rabbitmq_message)
                self.consumer.start_consuming('persistencia_cola', self.handle_rabbitmq_message)
                return True
            logger.error("❌ No se pudo conectar a RabbitMQ")
            return False
        except Exception as e:
            logger.error(f"❌ Error configurando RabbitMQ: {e}")
            return False

    def handle_rabbitmq_message(self, message_data: Dict[str, Any], method, properties):
        try:
            logger.info(f"📨 RabbitMQ: {message_data}")
            event_name, payload, room = None, None, None
            if isinstance(message_data, dict):
                tipo = message_data.get('tipo')
                if tipo == 'reaccion':
                    event_name = 'like_update'
                    payload = {
                        'outfit_id': message_data.get('outfit_id'),
                        'likes_count': message_data.get('metadata', {}).get('likes_count'),
                        'action': message_data.get('accion'),
                        'user_id': message_data.get('usuario_id')
                    }
                    room = f"outfit_{payload.get('outfit_id')}" if payload.get('outfit_id') else None
                elif tipo in ('notificacion', 'notification'):
                    event_name = 'notification'
                    payload = message_data.get('data') or message_data

            if event_name:
                asyncio.create_task(self.emit_event(event_name, payload, room))
            else:
                asyncio.create_task(self.emit_event('message', message_data))
        except Exception as e:
            logger.error(f"❌ Error procesando mensaje RabbitMQ: {e}")

    async def emit_event(self, event: str, data: Dict[str, Any], room: Optional[str] = None):
        try:
            if room:
                await self.sio.emit(event, data, room=room)
            else:
                await self.sio.emit(event, data)
            logger.debug(f"📤 Emitido evento '{event}' room={room}: {str(data)[:120]}")
        except Exception as e:
            logger.error(f"❌ Error emitiendo evento '{event}': {e}")

    async def start(self):
        logger.info(f"🚀 Iniciando Socket.IO en http://{self.host}:{self.port} (path=/socket.io)")
        if not await self.setup_rabbitmq():
            logger.warning("⚠️ RabbitMQ no disponible. Servidor iniciará en modo sin colas.")

        # Ruta de salud
        async def health(_request):
            return web.json_response({"status": "ok"})

        self.app.router.add_get('/health', health)

        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        while True:
            await asyncio.sleep(3600)

    def cleanup(self):
        if self.rabbitmq_connection:
            self.rabbitmq_connection.disconnect()
            logger.info("🔌 Conexión RabbitMQ cerrada")


async def main():
    server = ClothesureSocketIOServer()
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("👋 Deteniendo servidor...")
    except Exception as e:
        logger.error(f"❌ Error en servidor: {e}")
    finally:
        server.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
