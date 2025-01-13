from pydantic import BaseModel, field_validator
from app.core.enums import Mode, ServiceLevel, Size, Location


class ProfitabilityCalculatorRequest(BaseModel):
    category: str
    price: int
    weight: float
    mode: Mode
    service_level: ServiceLevel
    size: Size
    location: Location

    @field_validator(
        "category",
        "mode",
        "service_level",
        "size",
        mode="before",
    )
    def validate_non_empty_fields(cls, value: str, field_name: str):
        if not value:
            raise ValueError(f"{field_name} must not be empty")
        return value

    @field_validator("price", "weight", mode="before")
    def validate_positive_numbers(cls, value: str, field_name: str):
        try:
            value = float(value)
        except ValueError:
            raise ValueError(f"{field_name} must be a valid number")

        if value <= 0:
            raise ValueError(f"{field_name} must be greater than 0")
        return value
