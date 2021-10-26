# 微博爬虫

无需登录，但是过渡频繁访问会导致IP封号几个小时，项目中使用了几种方法缓解这一问题。

## 1. 前言

完整项目请转[Weibo_RepostRelationship_Visualization_Platform](https://github.com/WIN0624/Weibo_RepostRelationship_Visualization_Platform)，此部分为项目的爬虫模块，爬虫的任务是爬取[手机版微博](https://m.weibo.cn/)数据。

## 2. 思路

### 2.1 数据组织方式

HTTP网络传输中的数据组织方式有三种方式：

* HTML方式
* XML方式
* JSON方式

打开[手机版微博](https://m.weibo.cn/)首页，按下F12，选择【网络】-【XHR】，可以看到接收到如下数据：

<img src="https://github.com/zhongshsh/Images/blob/main/1635230542661.png" alt="1635230542661" style="zoom:50%;" />

因此确定微博的数据组织方式为JSON。

### 2.2 爬取目标数据

我们想要构建微博转发关系图谱，并在图谱上展示用户具体数据。因此，所需的核心实体为【发表的微博】。发现微博的途径一般为【在搜索框进行关键词检索-检索出与检索词相关的微博网页】，因此，我以倒推的方式分析如何爬取到【发表的微博】。

#### 2.2.1 检索结果页

先分析【检索结果页】，如下所示：

<img src="https://github.com/zhongshsh/Images/blob/main/1635230892352.png" alt="1635230892352" style="zoom:50%;" />

<img src="https://github.com/zhongshsh/Images/blob/main/1635231244505.png" alt="1635231244505" style="zoom:50%;" />

点击链接，跳到数据页面：

<img src="https://github.com/zhongshsh/Images/blob/main/1635231309006.png" alt="1635231309006" style="zoom:50%;" />

可以看到访问的链接带有我们的检索关键词【新冠疫情】，到这一步我们已经get到检索的地址。

将进度条往下拉，可以看到数据有出现了page=2，说明微博是实时拉取数据的，新数据的地址以page值的形式进行更新。

<img src="https://github.com/zhongshsh/Images/blob/main/1635231425980.png" alt="1635231425980" style="zoom:50%;" />

到此，检索页已经分析完毕。

#### 2.2.2 微博内容页

预览检索页内容，我们可以发现检索页提供了很多信息：

<img src="https://github.com/zhongshsh/Images/blob/main/1635231642037.png" alt="1635231642037" style="zoom:50%;" />

这里的0~9共十条微博就是展示在检索结果页的【发表的微博】的【简要信息】，具体大家见网页。但是我们还需要爬取每一条微博的转发关系，所以我点击进入微博详情页：

<img src="https://github.com/zhongshsh/Images/blob/main/1635231830101.png" alt="1635231830101" style="zoom:50%;" />

可以看到repost【转发】信息的访问地址，这里的id是被转发微博的id，可以在【检索结果页】中获取。至此，爬取分析完毕。

#### 2.2.3 总结

通过【检索词+检索url】组装，得到【微博id】。通过【微博id+转发url】，爬取到转发关系。



### 2.3 全站爬取

上述爬取只能爬取到【具体关键词】下的【微博转发关系】，那么如何实现全站微博数据的爬取呢？

#### 2.3.1 如何实现全站微博数据的爬取

微博有个热搜数据的API，每隔一段时间更新一次。而每一个热搜都以tag【#文本#】的形式组织，其下有许多的相关微博。不断使用【热搜+检索url】的形式进行爬取，即能不断获得数据。

此外，在爬取热搜过程中，不断收集爬取到的微博的tag信息，然后更新到tag库中，对这些tag进行检索和数据爬取。

#### 2.3.2 如何避免数据重新爬取

微博的数据更新很快，一条微博的前后两天转发量差距可能很大，需要不断重新爬取同一条微博的转发数据。那么如何确定当前转发关系是否已被爬取呢？主要通过【时间】。当前转发博文的发表时间如果在上一次爬取时间内，那么不再对当前转发关系进行保存。

#### 2.3.3 如何提升爬取速度

主要通过python multiprocessing，多线程爬取的方式增加爬取速度。

#### 2.3.4 如何解决反爬

基础配置：

* 使用python fake_useragent随机添加header，但这个库不是很稳定，有时候会报些错，最好自己把header数据下载到本地，自己编写个函数，随机初始化header。
* 使用python time sleep，控制爬虫。
* 使用多个url爬取一类信息。相同的信息【例如用户粉丝数据】往往在不同的url中出现。

终极配置：主要使用的是GitHub上的这个[代理池](https://github.com/Python3WebSpider/PorxyPool)。我们在这个代理池的基础上添加了几个爬虫。很重要的一点是，http的网页需要https的代理ip，https的网页需要http的代理ip。经过我的测试，从免费代理中爬取到的ip基本上是失效的……所以，可以尝试花点小钱~~

