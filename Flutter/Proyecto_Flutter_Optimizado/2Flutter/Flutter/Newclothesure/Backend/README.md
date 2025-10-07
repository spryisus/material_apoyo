# Backend Package - The Clothesure 2.0

Paquete Python para el manejo de colas RabbitMQ con reconexión automática para The Clothesure 2.0.

## Características

- ✅ Conexión SSL/TLS a Amazon MQ (RabbitMQ)
- ✅ Reconexión automática con backoff exponencial
- ✅ Manejo de errores robusto
- ✅ Logging estructurado
- ✅ Separación de responsabilidades (conexión, publicación, consumo)
- ✅ Callbacks personalizables
- ✅ Soporte para múltiples tipos de mensajes

## Estructura del Paquete

```
backend/
├── __init__.py          # Inicialización del paquete
├── connection.py        # Manejo de conexión y reconexión
├── publisher.py         # Publicación de mensajes
├── consumer.py          # Consumo de mensajes
├── example.py          # Ejemplo de uso
├── requirements.txt    # Dependencias
└── README.md          # Documentación
```

## Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt
```

## Uso Básico

### 1. Conexión

```python
from backend import RabbitMQConnection

# Crear conexión
connection = RabbitMQConnection(
    host="tu-host.amazonaws.com",
    port=5671,
    username="tu-usuario",
    password="tu-password",
    ssl_enabled=True,
    max_retries=5,
    retry_delay=2.0
)

# Conectar
if connection.connect():
    print("✅ Conectado exitosamente")
```

### 2. Publicación de Mensajes

```python
from backend import MessagePublisher

# Crear publisher
publisher = MessagePublisher(connection)

# Publicar reacción
publisher.publish_reaction(
    user_id="usuario123",
    outfit_id="outfit456",
    action="like"
)

# Publicar evento de persistencia
publisher.publish_persistence_event(
    event_type="user_registration",
    data={"user_id": "usuario123", "email": "test@example.com"}
)
```

### 3. Consumo de Mensajes

```python
from backend import MessageConsumer

# Crear consumer
consumer = MessageConsumer(connection)

# Callback personalizado
def mi_callback(message_data, method, properties):
    print(f"Mensaje recibido: {message_data}")

# Iniciar consumo
consumer.start_consuming('reacciones_cola', mi_callback)
```

## Tipos de Mensajes

### Reacciones
```python
{
    "tipo": "reaccion",
    "usuario_id": "usuario123",
    "outfit_id": "outfit456",
    "accion": "like",  # o "unlike"
    "timestamp": 1234567890.123,
    "metadata": {}
}
```

### Persistencia
```python
{
    "tipo": "persistencia",
    "evento": "user_registration",
    "datos": {"user_id": "usuario123", "email": "test@example.com"},
    "timestamp": 1234567890.123,
    "metadata": {}
}
```

### Usuario
```python
{
    "tipo": "usuario",
    "usuario_id": "usuario123",
    "evento": "profile_update",
    "datos": {"field": "bio", "old_value": "", "new_value": "Fashion lover"},
    "timestamp": 1234567890.123
}
```

### Outfit
```python
{
    "tipo": "outfit",
    "outfit_id": "outfit456",
    "evento": "view",
    "datos": {"user_id": "usuario123", "duration": 5.2},
    "timestamp": 1234567890.123
}
```

## Configuración de Colas

### reacciones_cola
- **TTL**: 10 segundos
- **Máximo**: 5000 mensajes
- **Propósito**: Mensajes de likes/unlikes en tiempo real

### persistencia_cola
- **Dead Letter Exchange**: x-dead-letter-exchange
- **Propósito**: Eventos que requieren persistencia en base de datos

## Manejo de Errores

El paquete incluye manejo robusto de errores:

- **Reconexión automática**: Si se pierde la conexión, se reintenta automáticamente
- **Backoff exponencial**: Los reintentos aumentan el delay progresivamente
- **Logging detallado**: Todos los eventos se registran con diferentes niveles
- **Callbacks de error**: Puedes configurar callbacks para eventos de conexión

## Context Manager

```python
from backend import RabbitMQConnection, MessagePublisher

# Usar como context manager
with RabbitMQConnection(host="...", username="...", password="...") as conn:
    publisher = MessagePublisher(conn)
    publisher.publish_reaction("user123", "outfit456", "like")
    # La conexión se cierra automáticamente
```

## Logging

El paquete usa el módulo `logging` estándar de Python:

```python
import logging

# Configurar nivel de logging
logging.basicConfig(level=logging.INFO)

# Los logs incluyen:
# - Conexiones y desconexiones
# - Publicación de mensajes
# - Consumo de mensajes
# - Errores y reconexiones
```

## Ejemplo Completo

Ver `example.py` para un ejemplo completo que incluye:

- Configuración de conexión
- Publicación de diferentes tipos de mensajes
- Consumo con callbacks personalizados
- Manejo de errores
- Limpieza de recursos

## Monitoreo

### Información de Colas
```python
# Obtener información de una cola
info = consumer.get_queue_info('reacciones_cola')
print(f"Mensajes en cola: {info['message_count']}")
print(f"Consumidores activos: {info['consumer_count']}")
```

### Limpiar Colas
```python
# Limpiar todos los mensajes de una cola
consumer.purge_queue('reacciones_cola')
```

## Mejores Prácticas

1. **Siempre usar context managers** para asegurar que las conexiones se cierren
2. **Configurar callbacks de error** para manejar desconexiones
3. **Usar logging apropiado** para monitorear el sistema
4. **Manejar excepciones** en los callbacks de consumo
5. **No bloquear** en los callbacks de consumo
6. **Usar QoS** para controlar el flujo de mensajes

## Troubleshooting

### Error de Conexión
- Verificar credenciales
- Verificar configuración SSL
- Verificar conectividad de red

### Mensajes No Llegan
- Verificar que las colas estén declaradas
- Verificar que el exchange esté configurado
- Verificar que los bindings estén correctos

### Reconexión Falla
- Verificar configuración de reintentos
- Verificar logs para errores específicos
- Verificar estado del servidor RabbitMQ

