from aiohttp import client_exceptions

from .errors import RequestError
from .const import BASE_URL


async def get_json(websession, path, params=None):
    url = '{}{}'.format(BASE_URL, path)
    try:
        async with websession.get(url, params=params) as res:
            return await res.json(content_type='application/json')
    except client_exceptions.ClientError as err:
        raise RequestError(
            'Error requesting data from {}: {}'.format(url, err)
        ) from None
