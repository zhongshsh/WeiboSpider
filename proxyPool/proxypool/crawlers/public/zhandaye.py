from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from loguru import logger
import requests
import re


BASE_URL = 'https://www.zdaye.com/dayProxy/{page}.html'
MAX_PAGE = 1000 #1637

class ZhandayeCrawler(BaseCrawler):
    """
    zhandaye crawler, https://www.zdaye.com/dayProxy/
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE)]
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

    def crawl(self):
        for url in self.urls:
            logger.info(f'fetching {url}')
            requests.packages.urllib3.disable_warnings()
            html = requests.get(url, headers=self.headers, verify=False).text
            doc = pq(html)
            trs = doc('h3 a').items()
            # print(trs)
            for tr in trs:
                if (tr.attr("href").find("dayProxy")!=-1):
                    url='https://www.zdaye.com'+tr.attr("href")
                    print(url)
                    html = requests.get(url, headers=self.headers, verify=False).text
                    doc = pq(html)
                    x=doc('.cont').text()
                    ip_address = re.compile('\n(.*?):(.*?)@')
                    re_ip_address = ip_address.findall(x)
                    for address, port in re_ip_address:
                        proxy = Proxy(host=address.strip(), port=int(port.strip()))
                        yield proxy


if __name__ == '__main__':
    crawler = ZhandayeCrawler()
    # crawler.crawl()
    for proxy in crawler.crawl():
        print(proxy)