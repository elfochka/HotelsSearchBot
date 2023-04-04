import requests
from typing import Any
from requests import HTTPError
from hotlog import hotels_log
from backoff import on_exception, expo
from config_data import config


@on_exception(expo, (ConnectionError, TimeoutError, HTTPError), max_tries=3)
def check_city(city: str) -> str | Any:
    """
        Проверка по Списку городов
        :param city:
        :return: (region_id | None), id региона поиска или ничего
        """
    try:
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": city, "locale": "ru_RU"}
        headers = {
            'x-rapidapi-key': config.RAPID_API_KEY,
            'x-rapidapi-host': "hotels4.p.rapidapi.com"
        }

        response = requests.request("GET", url,
                                    headers=headers,
                                    params=querystring)
        response_data = response.json()

        try:
            region_id = response_data['sr'][0]['gaiaId']

            return region_id
        except Exception as e:
            hotels_log.logger.exception(e)
            return None

    except Exception as e:
        hotels_log.logger.exception(e)
        return None
