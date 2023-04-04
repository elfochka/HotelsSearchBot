import requests
from backoff import on_exception, expo
from requests import HTTPError
from config_data import config
from typing import Any
from hotlog import hotels_log


@on_exception(expo, (ConnectionError, TimeoutError, HTTPError), max_tries=3)
def selection_hotels(region_id, input_data) -> \
        list[dict[str, str | list | Any]] | None:
    """
    Подборка отелей по заданным параметрам
    :param region_id:
    :param input_data:
    :return: (hotels_list | None), список отелей или ничего
    """
    try:
        currency = "USD"
        adults = 1

        check_in = input_data['check_in'].split('-')
        check_out = input_data['check_out'].split('-')

        for i in range(len(check_in)):
            if check_in[i][0] == '0':
                check_in[i] = check_in[i][1:]

        for i in range(len(check_out)):
            if check_out[i][0] == '0':
                check_out[i] = check_out[i][1:]

        in_day = int(check_in[2])
        in_month = int(check_in[1])
        in_year = int(check_in[0])

        out_day = int(check_out[2])
        out_month = int(check_out[1])
        out_year = int(check_out[0])

        if input_data['command'] == '/lowprice':
            sort_order = "PRICE_LOW_TO_HIGH"
        elif input_data['command'] == '/highprice':
            sort_order = "PRICE_HIGH_TO_LOW"
        else:
            sort_order = "DISTANCE_FROM_LANDMARK"

        url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        payload = {
            "currency": currency,
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {"regionId": region_id},
            "checkInDate": {
                "day": in_day,
                "month": in_month,
                "year": in_year
            },
            "checkOutDate": {
                "day": out_day,
                "month": out_month,
                "year": out_year
            },
            "rooms": [{"adults": adults}],
            "resultsStartingIndex": 0,
            "resultsSize": input_data['number_hotels'],
            "sort": sort_order,
            "filters": {"availableFilter": "SHOW_AVAILABLE_ONLY"}
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": config.RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        response_data = response.json()

        hotels_list = []
        for hotel in response_data['data']['propertySearch']['properties']:
            name = hotel['name']
            price = hotel['price']['lead']['formatted']
            total_price = hotel['price']['displayMessages'][1][
                'lineItems'][0]['value']
            total_price = str(total_price).split(' ')[0]
            rating = hotel['reviews']['score']
            preview_photo = hotel['propertyImage']['image']['url']
            hotel_id = hotel['id']

            detail_url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
            detail_payload = {
                "currency": currency,
                "eapid": 1,
                "locale": "ru_RU",
                "siteId": 300000001,
                "propertyId": hotel_id
            }
            detail_response = requests.request("POST", detail_url,
                                               json=detail_payload,
                                               headers=headers)
            detail_data = detail_response.json()

            address = detail_data['data']['propertyInfo']['summary'][
                'location']['address']['addressLine']
            photos = []

            for i in range(1, input_data['number_photos']):
                try:
                    photos.append(detail_data['data']['propertyInfo'][
                                      'propertyGallery']['images'][i]['image'][
                                      'url'])
                except Exception as e:
                    hotels_log.logger.exception(e)
            hotel_info = {'name': name, 'hotel_id': hotel_id,
                          'price': price, 'total_price': total_price,
                          'rating': rating, 'preview_photo': preview_photo,
                          'address': address, 'photos': photos}
            hotels_list.append(hotel_info)

        return hotels_list

    except Exception as e:
        hotels_log.logger.exception(e)
