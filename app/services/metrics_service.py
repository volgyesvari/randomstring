from sqlalchemy import RowMapping
from app.models.metrics_models import MetricsInputModel, MetricModel
from app.services.metrics_dao import MetricsDAO
from pydantic.dataclasses import dataclass
import asyncio


@dataclass
class MetricsFacade:
    metrics_dao: MetricsDAO

    async def get_metrics(self, event: MetricsInputModel) -> list[MetricModel]:
        result = []
        tasks = []

        for metric in event.metrics:
            task = self.metrics_dao.get_metric(event, metric)
            tasks.append(task)

        all_metric_results = await asyncio.gather(*tasks)

        for metric_rows in all_metric_results:
            for row in metric_rows:
                result.append(MetricModel(**row_to_dict(row) | {
                    "start_date": event.start_date,
                    "end_date": event.end_date,
                    "statistic": event.statistic
                }))

        return result


def row_to_dict(row: RowMapping) -> dict:
    result = {}
    for key, value in row.items():
        result[key] = value
    return result

