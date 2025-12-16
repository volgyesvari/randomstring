from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.ioc.measurement_service_ioc import get_measurement_facade

from app.models.measurement_input_model import MeasurementInputModel
from app.services.measurement_service import MeasurementFacade

measurement_router = APIRouter()


@measurement_router.post("/measurement")
async def create_measurement_item(event: MeasurementInputModel,
                                  measurement_facade: MeasurementFacade = Depends(get_measurement_facade)
                                  ) -> JSONResponse:
    await measurement_facade.create_item(event)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=event.model_dump())
