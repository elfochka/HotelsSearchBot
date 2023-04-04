from typing import Any
import api
from hotlog import hotels_log


def general(data: dict) -> list[dict[str, str | list | Any]] | None:
    """
        Командный пункт по запросам API
        :param data:
        :return: (hotels_list), список отелей по запросу
        """
    try:
        region_id = api.check_city.check_city(data['city'])
        hotels_list = api.selection_hotels.selection_hotels(region_id, data)
        return hotels_list
    except Exception as e:
        hotels_log.logger.exception(e)
