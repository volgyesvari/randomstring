from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.database.database import engine
from app.services.measurement_service import MeasurementFacade


def get_measurement_facade():
    return MeasurementFacade(async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession))