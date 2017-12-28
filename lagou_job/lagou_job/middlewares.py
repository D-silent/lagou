from random import choice
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RandomUserAgentMiddleware(UserAgentMiddleware):
    agents = open("agent.dat").readlines()

    def process_request(self, request, spider):
        agent = choice(self.agents).strip()
        request.headers["User-Agent"] = agent
        request.headers["Connection"] = "close"

    def process_response(self, request, response, spider):
        if response.status != 200:
            agent = choice(self.agents).strip()
            request.headers["User-Agent"] = agent
            return request
        return response


class ProxyMiddleware:
    proxies = open("proxy.dat").readlines()

    def get_proxy(self):
        proxy = choice(self.proxies).strip()
        return proxy

    def process_request(self, request, spider):
        request.meta['proxy'] = self.get_proxy()

    def process_response(self, request, response, spider):
        if response.status != 200:
            request.meta['proxy'] = self.get_proxy()
            return request
        return response
