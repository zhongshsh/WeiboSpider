from proxypool.crawlers.base import BaseCrawler
from proxypool.schemas.proxy import Proxy
from pyquery import PyQuery as pq
import requests
from loguru import logger

BASE_URL = 'http://www.goubanjia.com/'
# <head><title>403 Forbidden</title></head>

class GoubanjiaCrawler(BaseCrawler):
    """
    http://www.goubanjia.com/
    """
    urls = [BASE_URL]

    def crawl(self):
        for url in self.urls:
            logger.info(f'fetching {url}')
            requests.packages.urllib3.disable_warnings()
            html = requests.get(url, verify=False).text
            print(html)
            doc = pq(html)
            trs = doc('.ip').items()
            # print(trs)
            for tr in trs:
                print(tr)
                # if (tr.attr("href").find("dayProxy")!=-1):
                #     url='https://www.zdaye.com'+tr.attr("href")
                #     print(url)
                #     html = requests.get(url, headers=self.headers, verify=False).text
                #     doc = pq(html)
                #     x=doc('.cont').text()
                #     ip_address = re.compile('\n(.*?):(.*?)@')
                #     re_ip_address = ip_address.findall(x)
                #     for address, port in re_ip_address:
                #         proxy = Proxy(host=address.strip(), port=int(port.strip()))
                #         yield proxy


if __name__ == '__main__':
    crawler = GoubanjiaCrawler()
    crawler.crawl()
    # for proxy in crawler.crawl():
    #     print(proxy)

