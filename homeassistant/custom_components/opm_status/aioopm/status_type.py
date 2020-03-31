from aiohttp import client_exceptions

from .api import get_json

import uuid


async def get_status_types(websession):
    response = await get_json(websession, '/statustypes.json')
    return [StatusType(s) for s in response['OperatingStatusTypes']]

class StatusType:
    """Operating status type"""

    def __init__(self, raw):
        self.raw = raw

    @property
    def id(self):
        return self.raw['Id']

    @property
    def name(self):
        return self.raw['Name']

    @property
    def icon(self):
        return self.raw['Icon']

    @property
    def abbreviation(self):
        return self.raw['Abbreviation']

    @property
    def default(self):
        return self.raw['Default']
