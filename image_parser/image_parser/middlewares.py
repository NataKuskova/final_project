from fake_useragent import UserAgent


class RandomUserAgentMiddleware(object):
    """
    Class for the substitution of a random user agent.
    """
    def __init__(self):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)
