import logging
import traceback

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


async def error(msg):
    logging.error(msg)
    await sio.emit("error", msg)


@sio.on('start attack')
async def start_attack(sid, name, params):
    print("Starting attack", name, params)
    db = None # TODO
    args = [db]
    for a in attacks:
        if a.__name__ == name:
            for k, t in a.__init__.__annotations__.items():
                try:
                    args.append(params[k])
                except KeyError:
                    args.append(None)
            try:
                attack = a(*args)
                attack.prepare()

                async def on_progress(p):
                    await sio.emit("attack status", {"name": name, "status": p})
                attack.start(on_progress)
                await sio.emit("attack status", {"name": name, "status": 1})
            except:
                await error(traceback.format_exc())
            return
    await error("Unknown attack type: {}".format(name))


@sio.on("stop attack")
async def stop_attack(sid, name):
    pass  # TODO


@sio.on('get attacks')
async def send_attacks(sid, *args):
    await sio.emit('attacks', data=[a.get_attack_info() for a in attacks])


@sio.on('disconnect')
def disconnect(sid):
    print('Client disconnected ', sid)


app.router.add_get('/', index)
app.router.add_static('/', './frontend/dist/')

