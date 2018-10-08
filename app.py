import logging
from aiohttp import web

from backend.server import app

logger = logging.getLogger('traffic-player')

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    web.run_app(app)