import uvicorn
from fastapi import FastAPI

from .api.routers import include_routers
from .db.migrations import init_db

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await init_db()

include_routers(app)
if __name__ == '__main__':

    uvicorn.run(app, host='localhost', port=8000)
