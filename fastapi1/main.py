import uvicorn
from fastapi import FastAPI

from .api.routers import include_routers
from .db.migrations import migrations

migrations()
app = FastAPI()


include_routers(app)
if __name__ == '__main__':

    uvicorn.run(app, host='localhost', port=8000)
