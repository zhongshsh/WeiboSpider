from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from loguru import logger


BASE_URL = 'http://www.66ip.cn/areaindex_{page}/1.html'
MAX_PAGE = 34


class Daili66Crawler(BaseCrawler):
    """
    daili66 crawler, http://www.66ip.cn/1.html
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]
    
    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        for url in self.urls:
            logger.info(f'fetching {url}')
            html = self.fetch(url)
            doc = pq(html)
            trs = doc('tr').items()
            for tr in trs:
                host = tr.find('td:nth-child(1)').text()
                port = tr.find('td:nth-child(2)').text()
                if (str(host).find('.')!=-1):
                    yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = Daili66Crawler()
    for proxy in crawler.crawl():
        print(proxy)
