import json

import aiohttp

from .http import HttpTransport

MAIL_GUN_API = 'https://api.mailgun.net/v3/'


class MailGunTransport(HttpTransport):
    """Transport to make request to mailgun using their API"""

    def __init__(self, mailgun_domain, apikey):
        url = MAIL_GUN_API + mailgun_domain
        super().__init__(url, 'post', auth=aiohttp.BasicAuth('api', apikey))

    async def send(self, message):
        response = await super().send(message)
        payload = await response.text()
        if response.status == 200:
            return json.loads(payload)

        return payload
