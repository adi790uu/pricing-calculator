# flake8: noqa

from app.core.utils import process_amazon_market_place_csv
import math
from app.core.data import weight_handling_fees, closing_fees, other_fees


class PriceCalculator:
    def calculate_referral_fee(self, category: str, price: int):
        category_mapping = process_amazon_market_place_csv()
        category_array = category_mapping[category]

        for item in category_array:
            if item["min_val"] is None and item["max_val"] and price <= item["max_val"]:
                return float(item["referral_fee_percentage"].strip("%")) / 100 * price
            elif (
                item["min_val"]
                and item["max_val"]
                and item["min_val"] <= price <= item["max_val"]
            ):
                return float(item["referral_fee_percentage"].strip("%")) / 100 * price

            elif (
                item["min_val"] and item["max_val"] is None and price > item["min_val"]
            ):
                return float(item["referral_fee_percentage"].strip("%")) / 100 * price

        raise ValueError(
            f"No matching price range found for category {category} and price {price}"
        )

    def calculate_weight_handling_fee(
        self, mode: str, weight: float, service_level: str, location: str, size: str
    ) -> float:
        """
        mode: 'Easy Ship' or 'FBA'
        weight: Weight in kg
        service_level: 'premium', 'standard', 'advanced' or 'basic'
        location: 'local', 'regional', or 'national'
        size: 'Standard' or 'Heavy Bulky'

        """

        if mode == "Easy Ship":
            fees = weight_handling_fees["easyShip"]
            size_fees = fees["standard"] if size == "Standard" else fees["heavyBulky"]
            location = location.lower()

            if size == "Standard":
                if weight <= 0.5:
                    return size_fees["first500g"][location]
                elif weight <= 1:
                    return (
                        size_fees["first500g"][location]
                        + size_fees["additional500gUpTo1kg"][location]
                    )
                elif weight <= 5:
                    return (
                        size_fees["first500g"][location]
                        + size_fees["additional500gUpTo1kg"][location]
                        + (
                            math.ceil(weight - 1)
                            * size_fees["additionalKgAfter1kg"][location]
                        )
                    )
                else:
                    return (
                        size_fees["first500g"][location]
                        + size_fees["additional500gUpTo1kg"][location]
                        + (4 * size_fees["additionalKgAfter1kg"][location])
                        + (
                            math.ceil(weight - 5)
                            * size_fees["additionalKgAfter5kg"][location]
                        )
                    )
            else:
                if weight <= 12:
                    return size_fees["first12kg"][location]
                else:
                    return size_fees["first12kg"][location] + (
                        math.ceil(weight - 12)
                        * size_fees["additionalKgAfter12kg"][location]
                    )

        if mode == "FBA":
            fees = weight_handling_fees["fba"]["standard"][service_level.lower()]
            if weight <= 0.5:
                return fees["first500g"]
            if weight <= 1:
                return fees["first500g"] + fees["additional500gUpTo1kg"]
            if weight <= 5:
                return (
                    fees["first500g"]
                    + fees["additional500gUpTo1kg"]
                    + (math.ceil(weight - 1) * fees["additionalKgAfter1kg"])
                )

            return (
                fees["first500g"]
                + fees["additional500gUpTo1kg"]
                + (4 * fees["additionalKgAfter1kg"])
                + (math.ceil(weight - 5) * fees["additionalKgAfter5kg"])
            )

        return 0

    def calculate_closing_fee(self, mode: str, price: float) -> float:
        """
        mode: 'FBA', 'Easy Ship', or 'Self Ship'
        price: Price of the item

        """

        range_key = self._get_fee_range(price)

        if mode == "FBA":
            return closing_fees["fba"]["normal"][range_key]
        elif mode == "Easy Ship":
            return closing_fees["easyShip"]["standard"][range_key]
        elif mode == "Self Ship":
            return closing_fees["selfShip"][range_key]

        return 0

    def pick_and_pack_fee(self, mode: str, size: str) -> float:
        """
        mode: 'FBA', 'Easy Ship', or 'Self Ship'
        size: 'Standard' or 'Heavy Bulky'

        """
        if mode != "FBA":
            return 0

        return (
            other_fees["pickAndPack"]["standard"]
            if size == "Standard"
            else other_fees["pickAndPack"]["oversizeHeavyBulky"]
        )

    def total_fees_and_net_profit(
        self,
        referral_fee: float,
        weight_handling_fee: float,
        closing_fee: float,
        pick_and_pack_fee: float,
        price: float,
    ):
        total_fee = referral_fee + weight_handling_fee + closing_fee + pick_and_pack_fee
        net_earnings = price - total_fee
        return total_fee, net_earnings

    def _get_fee_range(self, price: float) -> str:
        if price <= 250:
            return "upTo250"
        if price <= 500:
            return "upTo500"
        if price <= 1000:
            return "upTo1000"
        return "above1000"
