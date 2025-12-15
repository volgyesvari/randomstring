from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.database_models import Base

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(engine)