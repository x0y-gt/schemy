import asyncio
import json

from schemy.httpclient import HttpClient
from ..transport import Transport


class HttpTransport(Transport):
    """This is a wrapper to send data using the http client to a defined url"""

    def __init__(self, url, method, **kwargs):
        self.client = HttpClient(url)
        self.method = method
        self.kwargs = kwargs


    async def send(self, message):
        """Returns an aiohttp.ClientResponse"""

        payload, instructions = Transport.get_payload(message)
        kwargs = {**self.kwargs, **instructions}

        # verify if the intention is to send json data
        if ('headers' in kwargs and
                'Content-Type' in kwargs['headers'] and
                kwargs['headers']['Content-Type'].lower() == 'application/json'):
            kwargs['json'] = json.dumps(payload)
        else:
            kwargs['data'] = payload

        # verify if we need to add a path to the route
        path = None
        if 'path' in kwargs:
            path = kwargs['path']
            del kwargs['path']

        async with self.client.request(
            self.method,
            path,
            **kwargs
        ) as response:
            await response.read()
            if response.status >= 400:
                raise Exception(await response.text())

            return response
