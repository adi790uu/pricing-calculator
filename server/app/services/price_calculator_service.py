from app.core.calculator import PriceCalculator
from app.schemas.request_schema import ProfitabilityCalculatorRequest
from loguru import logger
from app.schemas.response_schema import (
    ProfitabilityCalculatorResponse,
    Breakdown,
)  # noqa


async def calculate_profitability(request: ProfitabilityCalculatorRequest):
    try:
        price_calculator = PriceCalculator()
        referral_fee = price_calculator.calculate_referral_fee(
            category=request.category,
            price=request.price,
        )
        weight_handling_fee = price_calculator.calculate_weight_handling_fee(
            location=request.location,
            mode=request.mode,
            weight=request.weight,
            service_level=request.service_level,
            size=request.size,
        )

        closing_fee = price_calculator.calculate_closing_fee(
            mode=request.mode, price=request.price
        )

        pick_and_pack_fee = price_calculator.pick_and_pack_fee(
            mode=request.mode, size=request.size
        )

        total_fee, net_earnings = price_calculator.total_fees_and_net_profit(
            referral_fee,
            weight_handling_fee,
            closing_fee,
            pick_and_pack_fee,
            request.price,
        )

        response = ProfitabilityCalculatorResponse(
            breakdown=Breakdown(
                referralFee=referral_fee,
                weightHandlingFee=weight_handling_fee,
                closingFee=closing_fee,
                pickAndPackFee=pick_and_pack_fee,
            ),
            netEarnings=net_earnings,
            totalFees=total_fee,
        )

        return response
    except Exception as e:
        logger.info(e)
        raise Exception("An error occurred during profitability calculation") from e
