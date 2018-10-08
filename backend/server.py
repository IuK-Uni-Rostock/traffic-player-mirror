import socketio
from aiohttp import web
from aiohttp_index import IndexMiddleware
from src.attacks import attacks

sio = socketio.AsyncServer()
app = web.Application(middlewares=[IndexMiddleware()])
sio.attach(app)


async def index(request):
    """Serve the client-side application."""
    with open('./frontend/dist/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('connect')
def connect(sid, environ):
    print("Client connected ", sid)


@sio.on('get attacks')
async def send_attacks(sid, *args):
    await sio.emit('attacks', data=[a.get_attack_info() for a in attacks])


@sio.on('disconnect')
def disconnect(sid):
    print('Client disconnected ', sid)


app.router.add_get('/', index)
app.router.add_static('/', './frontend/dist/')

