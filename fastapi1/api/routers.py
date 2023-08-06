from fastapi import FastAPI

from .routes import dishes, menu, submenu


def include_routers(app: FastAPI):
    prefix = '/api/v1'
    app.include_router(menu.router, prefix=prefix)
    app.include_router(submenu.router, prefix=prefix)
    app.include_router(dishes.router, prefix=prefix)
