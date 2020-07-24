from fastapi import FastAPI
from .models import db
import logging
from importlib import import_module

logger = logging.getLogger(__name__)

ROUTES = ['users']


def load_modules(app=None):
    for route in ROUTES:
        logger.info("Loading module: %s", route)
        module = import_module(f'src.crm.views.{route}')
        if app:
            module.init_app(app)


def get_app():
    app = FastAPI(title="BALOON-CRM")
    db.init_app(app)
    load_modules(app)
    return app
