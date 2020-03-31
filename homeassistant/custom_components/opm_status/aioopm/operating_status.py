from aiohttp import client_exceptions

from .api import get_json

import uuid
from datetime import datetime, timezone


DEFAULT_PARAMS = {'useutc': 'true'}


async def current_operating_status(websession):
    return OperatingStatus(await get_json(websession, '/operatingstatus.json', DEFAULT_PARAMS))

def _convert_timestamp(value):
    if value:
        ts = float(value[value.find("(")+1:value.find(")")])
        return datetime.fromtimestamp(ts / 1000.0, timezone.utc)
    return None


class OperatingStatus:
    """The federal government's operating status"""

    def __init__(self, raw):
        self.raw = raw

    @property
    def id(self):
        return self.raw['Id']

    @property
    def title(self):
        return self.raw['Title']

    @property
    def location(self):
        return self.raw['Location']

    @property
    def status_summary(self):
        return self.raw['StatusSummary']

    @property
    def status_web_page(self):
        return self.raw['StatusWebPage']

    @property
    def short_status_message(self):
        return self.raw['ShortStatusMessage']

    @property
    def long_status_message(self):
        return self.raw['LongStatusMessage']

    @property
    def extended_information(self):
        return self.raw['ExtendedInformation']

    @property
    def date_status_posted(self):
        return _convert_timestamp(self.raw['DateStatusPosted'])

    @property
    def current_date(self):
        return _convert_timestamp(self.raw['CurrentDate'])

    @property
    def date_status_complete(self):
        return _convert_timestamp(self.raw['DateStatusComplete'])

    @property
    def applies_to(self):
        return self.raw['AppliesTo']

    @property
    def icon(self):
        return self.raw['Icon']

    @property
    def status_type(self):
        return self.raw['StatusType']

    @property
    def status_type_guid(self):
        return uuid.UUID(self.raw['StatusTypeGuid'])

    @property
    def url(self):
        return self.raw['Url']
