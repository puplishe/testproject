from .api.routers import include_routers
from .db.database import Base, engine, SessionLocal, get_db
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session
from .models import models
from fastapi.responses import JSONResponse
import uvicorn

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

include_routers(app)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)