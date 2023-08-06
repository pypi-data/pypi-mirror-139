from http.client import NOT_FOUND
from .exceptions import BGExceptions as BGExc
from .exceptions import TelegramExceptions as TExc
from .apps.baza_gai import search_gai_base_car_number


class PBAClient:
    def __init__(self, host: str, api_key: str):
        self.host = host
        self.api_key = api_key

    def search_car_number(self, car_number: str):
        data = search_gai_base_car_number(car_number)

        if not data:
            return BGExc.prepare_error_message(
                msg="Invalid car number",
                status_code=NOT_FOUND,
            )
        return data







