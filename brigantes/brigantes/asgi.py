import os
from dotenv import load_dotenv, dotenv_values
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
import socketio, asyncio, redis
from socketio import AsyncRedisManager
from asgiref.sync import sync_to_async
from brigantes.mqtt_client import MQTTClient

# --- Load environment ---
load_dotenv()
config = dotenv_values(".env")

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    config.get("DJANGO_SETTINGS_MODULE") or 'brigantes.settings.prod'
)

# --- Django ASGI App ---
django_asgi_app = get_asgi_application()

mqtt = MQTTClient()

rds = redis.Redis(host='localhost', port=6379, db=0)

redis_url = "redis://localhost:6379/0"
mgr = AsyncRedisManager(redis_url)

# --- Socket.IO setup ---
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*",
    client_manager=mgr
)

app = socketio.ASGIApp(sio, other_asgi_app=django_asgi_app)


periodic_tasks = {}

@sio.event
async def connect(sid, environ, auth):
    print(f"Client connected: {sid}")
    await sio.emit('sid-auth', sid, to=sid)

    # async def emit_every_5_seconds():
    #     try:
    #         while True:
    #             await sio.emit('message', {'user': username, 'msg': 'Hello every 5 seconds'}, to=sid)
    #             await asyncio.sleep(5)
    #     except asyncio.CancelledError:
    #         print(f"Stopped emitting to {sid}")
    #         pass

    # Start the background task and save it
    # task = asyncio.create_task(emit_every_5_seconds())
    # periodic_tasks[sid] = task


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    # Cancel the background task if it exists
    task = periodic_tasks.pop(sid, None)
    if task:
        task.cancel()
        print(f"Client disconnected: {sid}")

@sio.event
async def my_message(sid, data):
    await sio.emit('response', {'data': data}, room=sid)


# --- Application routing ---
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Let Django handle ALL HTTP paths (e.g. /admin/)
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("socket.io/", socketio.ASGIApp(sio)),  # Socket.IO handles WebSocket at /socket.io/
        ])
    ),
})
