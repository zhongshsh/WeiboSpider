from proxypool.crawlers.base import BaseCrawler
from proxypool.schemas.proxy import Proxy
import re
from pyquery import PyQuery as pq

BASE_URL = 'http://www.kxdaili.com/dailiip/1/{page}.html'


class KxdailiCrawler(BaseCrawler):
    """
    kuaidaili crawler, http://www.kxdaili.com/dailiip/1/1.html
    """
    urls = [BASE_URL.format(page=page) for page in range(1, 10)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        for item in doc('tr').items():
            td_ip = item.find('td:first-child').text()
            td_port = item.find('td:nth-child(2)').text()
            if len(td_ip)>4 and td_port:
                yield Proxy(host=td_ip, port=td_port)


if __name__ == '__main__':
    crawler = KxdailiCrawler()
    for proxy in crawler.crawl():
        print(proxy)
