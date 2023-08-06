from dataclasses import dataclass


@dataclass
class CarEntity:
    digits: str
    vin: str
    vendor: str
    model_year: str
    photo_url: str
    is_stolen: bool
