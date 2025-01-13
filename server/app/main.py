from http import HTTPStatus
from fastapi import FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.services import price_calculator_service as pc_service
from app.schemas.request_schema import ProfitabilityCalculatorRequest
from app.schemas.data_response_dto import GenericResponse, ErrorResponse
from app.schemas.response_schema import ProfitabilityCalculatorResponse
from app.middlewares import middleware
from loguru import logger

app = FastAPI(
    title=settings.APP_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}


@app.post(
    "/api/v1/profitability-calculator",
    response_model=GenericResponse[ProfitabilityCalculatorResponse],
)
@middleware.router_exception_handler
async def profitability_calculator(request: ProfitabilityCalculatorRequest):
    """
    Request Body:
        category: str
        price: int
        weight: float
        mode: Mode
        service_level: ServiceLevel
        size: Size
    """
    try:
        data = await pc_service.calculate_profitability(request)
        return GenericResponse(data=data)
    except Exception as e:
        logger.error(e)
        response = GenericResponse(
            error=ErrorResponse(
                message="Some error occurred!",
                code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        )
        return response
