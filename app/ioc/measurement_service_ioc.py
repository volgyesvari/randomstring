from sqlalchemy import create_engine
from app.database.database import DATABASE_URL
from app.services.measurement_service import MeasurementFacade


def get_measurement_facade():
    return MeasurementFacade(create_engine(DATABASE_URL))