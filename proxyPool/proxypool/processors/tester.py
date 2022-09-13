import asyncio
import aiohttp
from aiohttp.client import request
from loguru import logger
from proxypool.schemas import Proxy
from proxypool.storages.redis import RedisClient
from proxypool.setting import TEST_TIMEOUT, TEST_BATCH, TEST_URL, TEST_VALID_STATUS
from aiohttp import (
    ClientProxyConnectionError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError,
)
from asyncio import TimeoutError
import requests

EXCEPTIONS = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError,
)


class Tester(object):
    """
    tester for testing proxies in queue
    """

    def __init__(self):
        """
        init redis
        """
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()

    async def test(self, proxy: Proxy):
        """
        test single proxy
        :param proxy: Proxy object
        :return:
        """
        try:
            se = requests.session()
            logger.debug(f"testing {proxy.string()}")
            response = se.get(
                TEST_URL, proxies={"https": proxy.string(), "http": proxy.string()}
            )
            if response.text != "请稍后访问":
                self.redis.max(proxy)
                logger.debug(f"proxy {proxy.string()} is valid, set max score")
            else:
                self.redis.decrease(proxy)
                logger.debug(f"proxy {proxy.string()} is invalid, decrease score")
        except:
            self.redis.decrease(proxy)
            logger.debug(f"proxy {proxy.string()} is invalid, decrease score")

    @logger.catch
    def run(self):
        """
        test main method
        :return:
        """
        # event loop of aiohttp
        logger.info("stating tester...")
        count = self.redis.count()
        logger.debug(f"{count} proxies to test")
        for i in range(0, count, TEST_BATCH):
            # start end end offset
            start, end = i, min(i + TEST_BATCH, count)
            logger.debug(f"testing proxies from {start} to {end} indices")
            proxies = self.redis.batch(start, end)
            tasks = [self.test(proxy) for proxy in proxies]
            # run tasks using event loop
            self.loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    tester = Tester()
    tester.run()
