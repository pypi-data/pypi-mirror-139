import requests
from settings import *
from helper_baza_gai import *
from dto import CarEntity


def search_gai_base_car_number(car_number: str):
    url = f"https://baza-gai.com.ua/nomer/{car_number}"
    r = requests.get(url, headers={"Accept": "application/json", "X-Api-Key": GAI_KEY})
    car_data = r.json()
    car_data['photo_url'] = fix_baza_gai_image_url(car_data['photo_url'])
    formatted_data = CarEntity(
        digits=car_data['digits'],
        vin=car_data['vin'],
        vendor=car_data['vendor'],
        model_year=car_data['model_year'],
        photo_url=car_data['photo_url'],
        is_stolen=car_data['is_stolen'],
    )
    return formatted_data
