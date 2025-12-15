from sqlalchemy.ext.asyncio import AsyncConnection
from sqlmodel import Session
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy import create_engine, Column, Integer, Float, select, func, RowMapping
from app.models.database_models import MetricItem
from app.models.metrics_models import MetricsInputModel, MetricModel
from app.services.metrics_dao import MetricsDAO
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy import text
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from sqlalchemy.engine import Engine


@dataclass
class MetricsFacade:
    metrics_dao: MetricsDAO

    def get_metrics(self, event: MetricsInputModel) -> list[MetricModel]:
        result = []

        for metric in event.metrics:
            result.extend(
                [MetricModel(**row_to_dict(row) | {"start_date": event.start_date,
                                                   "end_date": event.end_date,
                                                   "statistic": event.statistic}) for row in
                 self.metrics_dao.get_metric(event, metric)])

        return result


def row_to_dict(row: RowMapping):
    result = {}
    for key, value in row.items():
        result[key] = value
    return result

