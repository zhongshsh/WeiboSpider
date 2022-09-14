# 微博爬虫

无需登录，爬取 [手机版微博](https://m.weibo.cn/) 转发关系数据。爬取结果示例见 `./spider/data`.

过渡频繁访问会导致IP封号几个小时，本项目使用了几种方法缓解这一问题。

* proxyPool: 来自GitHub的proxyPool构建代码，主要增加了几个免费代理爬虫
* spider: 我们项目爬虫代码

## 1. 简介

通过微博的热搜 API 获取 #关键词#，通过【检索词+检索url】组装，得到【微博id】。通过【微博id+转发url】，爬取到转发关系。

优化：
- 通过python multiprocessing，多线程爬取的方式增加爬取速度
- 反爬

```
 - 使用python fake_useragent随机添加header
 - 使用python time sleep
 - 使用多个url爬取一类信息
 - [代理池](https://github.com/Python3WebSpider/ProxyPool)
```

## 2. 配置

```json
{
    "searchlist": ["新冠"],   // 爬取的关键词列表
    "expand_topic": false,    // 是否需要加载扩展的关键词
    "hot_dir": "./data/",     // 热搜词文件夹
    "repost_dir": "./data/",  // 转发关系文件夹
    "topic_dir": "./data/",   // tag 文件夹
    "log_dir": "./log/",      // 日志文件夹
    "process_num": 2,
    "use_proxy": false,       // 是否使用代理池
    "page_num": 1             // 爬取关键词下的微博页数
}
```

## 3. 执行指令

```shell
cd spider
python word_spider.py

```
