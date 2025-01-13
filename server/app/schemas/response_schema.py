from pydantic import BaseModel


class Breakdown(BaseModel):
    referralFee: float
    weightHandlingFee: float
    closingFee: float
    pickAndPackFee: float


class ProfitabilityCalculatorResponse(BaseModel):
    breakdown: Breakdown
    totalFees: float
    netEarnings: float
