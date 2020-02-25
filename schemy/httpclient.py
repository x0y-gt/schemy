import aiohttp


class HttpClient:
    """It's a simple wrapper do make http requests
    using the Request method from aiohttp"""

    methods = ['get', 'post', 'put', 'delete', 'head', 'options', 'patch']

    def __init__(self, base: str, headers=None):
        self.base = base
        self.headers = [] if not headers else headers

    def __getattr__(self, name):
        """Catcher for all the http methods"""

        def request_handler(path, **kwargs):
            if name not in self.methods:
                raise Exception('Undefined method %s in HttpClient' % name)

            return self.request(name, path, **kwargs)

        return request_handler

    def request(self, method, path, **kwargs):
        """Low level api to do the requests
        return: aiohttp.ClientResponse"""
        url = HttpClient.join_url(self.base, path)

        return aiohttp.request(method, url, **kwargs)

    @classmethod
    def join_url(cls, base, path):
        """Joins a host base with a path"""

        if not base or not path:
            url = base if not path else path
        elif base[-1] == '/' and path[0] == '/':
            url = base + path[1:]
        elif base[-1] == '/' or path[0] == '/':
            url = base + path[0]
        else:
            url = base + '/' + path[0]

        return url
