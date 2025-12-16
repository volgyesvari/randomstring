from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.services.metrics_service import MetricsFacade
from app.services.metrics_dao import MetricsDAO
from app.database.database import engine


def get_metrics_facade() -> MetricsFacade:
    return MetricsFacade(MetricsDAO(async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)))