from enum import Enum as PyNum


class Mode(str, PyNum):
    FBA = "FBA"
    EASY_SHIP = "Easy Ship"
    SELF_SHIP = "Self Ship"


class ServiceLevel(str, PyNum):
    PREMIUM = "premium"
    ADVNACED = "advanced"
    STANDARD = "standard"
    ECONOMY = "economy"


class Size(str, PyNum):
    STANDARD = "Standard"
    HEAVY_AND_BULKY = "Heavy Bulky"


class Location(str, PyNum):
    LOCAL = "local"
    REGIONAL = "regional"
    NATIONAL = "national"
