from app.services.metrics_service import MetricsFacade
from app.services.metrics_dao import MetricsDAO
from app.database.database import DATABASE_URL
from sqlalchemy.engine import create_engine


def get_metrics_facade() -> MetricsFacade:
    return MetricsFacade(metrics_dao=MetricsDAO(engine=create_engine(DATABASE_URL)))