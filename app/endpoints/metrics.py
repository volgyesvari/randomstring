from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated

from app.models.metrics_models import MetricsInputModel
from app.services.metrics_service import MetricsFacade
from app.ioc.metrics_service_ioc import get_metrics_facade

metrics_router = APIRouter()

@metrics_router.get("/metrics")
async def get_metrics(event: Annotated[MetricsInputModel, Depends()] ,
                      metrics_facade: MetricsFacade = Depends(get_metrics_facade)):

    return [metric.model_dump(by_alias=True) for metric in metrics_facade.get_metrics(event)]