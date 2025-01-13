import csv
from pydantic import BaseModel
import re


class ReferralCsvRow(BaseModel):
    category: str
    price_range: str
    referral_fee_percentage: str


FILE_PATH = "/Users/adi790u/Desktop/pricing-calculator/server/Amazon marketplace - Referral fees.csv"  # noqa


def process_amazon_market_place_csv():
    mapping = {}
    with open(
        FILE_PATH,
        "r",
    ) as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            if not index:
                continue

            csv_row = ReferralCsvRow(
                category=row[0],
                price_range=row[1],
                referral_fee_percentage=row[2],
            )
            if csv_row.category not in mapping:
                mapping[csv_row.category] = []
            min_val, max_val = parse_ranges(csv_row.price_range)

            mapping[csv_row.category].append(
                {
                    "min_val": min_val,
                    "max_val": max_val,
                    "referral_fee_percentage": csv_row.referral_fee_percentage,
                }
            )
    return mapping


def parse_ranges(range_string):

    range_string = range_string.strip()
    if "<=" in range_string and ">" in range_string:
        match = re.search(r"> (\d+) and <= (\d+)", range_string)
        if match:
            min_val = int(match.group(1)) + 1
            max_val = int(match.group(2))

            return min_val, max_val
    elif "<=" in range_string:
        match = re.search(r"<= (\d+)", range_string)
        if match:
            max_val = int(match.group(1))
            return None, max_val
    elif ">" in range_string:
        match = re.search(r"> (\d+)", range_string)
        if match:
            min_val = int(match.group(1)) + 1
            return min_val, None
    else:
        return None, None
