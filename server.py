#!/usr/bin/env python3

import importlib, inspect
import logging
import sys
import traceback
import os
import socketio
from aiohttp import web
from aiohttp_index import IndexMiddleware
from src.attacks import attacks
from src.database import Database

logger = logging.getLogger('traffic-player')

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
    sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/config'))
    db_config = importlib.import_module('config')
    db = Database(db_config.db_cfg, 'log_kzh')
    args = [db]
    for a in attacks:
        if a.__name__ == name:
            for k in inspect.getfullargspec(a.__init__)[0][2:]:
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

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    web.run_app(app)

