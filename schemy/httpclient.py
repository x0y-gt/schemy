import aiohttp
import urllib.parse


class HttpClient:
    """Http client using the ClientSession class from aiohttp"""

    methods = ['get', 'post', 'put', 'delete', 'head', 'options', 'patch']

    def __init__(self, host: str, headers=None):
        self.host = host
        self.headers = [] if not headers else headers

    def __getattr__(self, name):
        """Catcher for all the http methods"""

        def request_handler(*args, **kwargs):
            if name not in self.methods:
                raise Exception('Undefined method %s in HttpClient' % name)

            url = urllib.parse.urljoin(self.host, args[0])
            return aiohttp.request(name, url, **kwargs)

        return request_handler
