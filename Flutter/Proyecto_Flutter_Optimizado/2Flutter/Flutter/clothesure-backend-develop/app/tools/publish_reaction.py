"""
Script de utilidad: publica un mensaje de reacción (like/unlike) en RabbitMQ
Usa la misma conexión que el backend.

Uso:
  python -m backend.tools.publish_reaction --user user_1 --outfit outfit_1 --action like
"""

import argparse
import time
import sys
import os

# Asegurar imports del paquete backend
PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = os.path.dirname(PACKAGE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from backend.connection import RabbitMQConnection  # type: ignore
from backend.publisher import MessagePublisher     # type: ignore


def main():
    parser = argparse.ArgumentParser(description="Publicar reacción en RabbitMQ")
    parser.add_argument('--user', required=True, help='ID de usuario')
    parser.add_argument('--outfit', required=True, help='ID del outfit')
    parser.add_argument('--action', choices=['like', 'unlike'], default='like', help='Acción')
    args = parser.parse_args()

    # Conexión centralizada (CLOUDAMQP_URL o variables de entorno)
    conn = RabbitMQConnection()

    if not conn.connect():
        print("❌ No se pudo conectar a RabbitMQ")
        sys.exit(1)

    pub = MessagePublisher(conn)

    ok = pub.publish_reaction(
        user_id=args.user,
        outfit_id=args.outfit,
        action=args.action,
        metadata={
            'source': 'cli',
            'timestamp': time.time(),
        }
    )

    if ok:
        print("✅ Mensaje publicado en exchange 'events_exchange' → cola 'reacciones_cola'")
    else:
        print("❌ Error publicando mensaje")


if __name__ == '__main__':
    main()