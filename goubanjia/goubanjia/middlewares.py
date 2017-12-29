from random import choice
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RandomUserAgentMiddleware(UserAgentMiddleware):
    agents = open("agent.dat").readlines()

    def process_request(self, request, spider):
        agent = choice(self.agents).strip()
        request.headers["User-Agent"] = agent

    def process_response(self, request, response, spider):
        if response.status != 200:
            agent = choice(self.agents).strip()
            request.headers["User-Agent"] = agent
            return request
        return response
