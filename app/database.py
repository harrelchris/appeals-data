from sqlalchemy import create_engine

from app.models import *
from app.settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
