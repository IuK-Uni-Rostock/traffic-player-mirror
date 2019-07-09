#!/usr/bin/env python3

import asyncio
import importlib
import inspect
import logging
import os
import sys
import traceback

import socketio
from aiohttp import web
from aiohttp_index import IndexMiddleware

from src.attacks import attacks
from src.database import Database

sio = socketio.AsyncServer()
running_attacks = []

async def index(request):
    """Serve the client-side application."""
    with open('./frontend/dist/index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('connect')
def connect(sid, environ):
    print("Client connected", sid)


async def error(msg):
    print("Error:", msg)
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
                running_attacks.append((name, app.loop.create_task(attack.start(on_progress))))
            except:
                await error(traceback.format_exc())
            return
    await error("Unknown attack type: {}".format(name))


@sio.on("stop attack")
async def stop_attack(sid, name):
    print("Stopping attack", name)
    for attack in [a for a in running_attacks if a[0] == name]:
        attack[1].cancel()
        running_attacks.remove(attack)


@sio.on("stop all attacks")
async def stop_attack(sid):
    print("Stopping all attacks")
    for attack in running_attacks:
        attack[1].cancel()
        running_attacks.remove(attack)


@sio.on('get attacks')
async def send_attacks(sid, *args):
    await sio.emit('attacks', data=[a.get_attack_info() for a in attacks])


@sio.on('disconnect')
def disconnect(sid):
    print("Client disconnected", sid)


async def create_app():
    app = web.Application(middlewares=[IndexMiddleware()])
    sio.attach(app)
    app.router.add_get('/', index)
    app.router.add_static('/', './frontend/dist/')
    return app


async def cleanup(app):
    for attack in running_attacks:
        attack[1].cancel()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    app.on_cleanup.append(cleanup)
    web.run_app(app)
