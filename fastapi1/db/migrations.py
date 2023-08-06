from ..models import models
from .database import engine


def migrations():
    models.Base.metadata.create_all(bind=engine)
