from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute

from .configuration.database import SessionLocal, Base, engine
from .controller import base, user, document

FASTAPI_CFG = {
    'debug': True,
    'version': 0.1
}

APP = FastAPI(**FASTAPI_CFG)


# register startup event
@APP.on_event('startup')
async def start_app():
    # create database
    Base.metadata.create_all(engine)

    APP.include_router(base.ROUTER, tags=["base"])
    APP.include_router(user.ROUTER, prefix="/api/user", tags=["user"], )
    APP.include_router(document.ROUTER, prefix="/api/document", tags=["document"], )

    # dump routers
    for route in APP.routes:
        if isinstance(route, Route):
            print('http router %s: %s %s' %
                  (route.name, route.path, route.methods))
        elif isinstance(route, WebSocketRoute):
            print('websocket router %s: %s ' %
                  (route.name, route.path))
    # middlewares
    APP.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
    )


@APP.get("/")
async def root():
    return {"message": "Hello World"}


@APP.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# register shutdown event
@APP.on_event('shutdown')
async def shutdown_app():
    print('shutdown fastapi application...')
