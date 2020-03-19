"""
创建一个工程：
    scrapy startproject 工程名
    cd 工程名
    scrapy genspider 爬虫名 网址
    scrapy crawl 爬虫名
    settings:
        不遵从robots协议
        UA伪装
        LOG_LEVEL = "ERROR"

scrapy的数据解析
scrapy的持久化存储
    基于终端指令
        只可以将parse方法的返回值存储到磁盘文件中
        scrapy crawl ssmy -o file.csv
    基于管道：pipelines.py
        编码流程：
            1. 解析数据
            2. 在item的类中定义相关的属性
            3. 将解析的数据存储封装到item类型的对象中
            4. 将item对象提交给管道
            5. 在管道类中接受item对象，然后对item进行任意形式的持久化存储
            6. 在配置文件中开启管道
        细节：
            将爬取的数据进行备份？
                一个管道对应一种平台的持久化存储
            有多个管道是否意味着多个管道类都可以接受爬虫文件提交的item？
                只有最高优先级的管道才可以接受item，剩下的管道来是需要从最高优先级的管道类中接受item

基于spider父类进行全站数据的爬取
    全站数据的爬取：将所有页码对应的页面数据进行爬取
    手动请求的发送（GET）：
        yield scrapy.Request(url, callback)   (用到yield的情况：相管道提交  手动请求)
    手动发动post请求
        yield scrapy.FormRequest(url, formdata, callback)  formdata是一个字典表示的是请求参数

scrapy五大核心组件


请求传参
    作用：实现深度爬取
    使用场景：如果使用scrapy爬取的数据没有在同一张页面中

提高效率：
    配置文件中进行一些操作即可

    DOWNLOAD_DELAY = 0   # 降低下载延迟

    CONCURRENT_REQUESTS = 100   # 开启的线程数量

    CONCURRENT_REQUESTS_PER_DOMAIN = 100  #　同多线程

    CONCURRENT_REQUESTS_PER_IP = 100　　　＃　同多线程

    COOKIES_ENABLED = False    # 禁止cookies

    RETRY_ENABLED = False   # 禁止对请求失败的目标再次请求

    DOWNLOAD_TIMEOUT = 3   # 设置下载时间 超过三秒不在需求

中间件
    爬虫中间件
    下载中间件：处于引擎和下载器之间
        作用：批量拦截所有的请求和响应
        为什么拦截请求：
            篡改请求的头信息 UA伪装
            篡改请求的url
            修改请求对应的ip 代理
        为什么拦截响应
            篡改响应数据，篡改响应对象
    爬取网易新闻的新闻标题内容
        分析：
            1.每一个板块对应的新闻数据都是动态加载出来的

图片懒加载
    应用到标签的伪属性，数据捕获的时候一定是基于伪属性进行
ImagePileline 专门用于二进制数据下载和持久化存储的管道类

CrawlSpider
    一种基于scrapy进行全站数据爬去的新的技术手段
    是spider的一个子类
        链接提取器：LinkExtractor
        规则解析器：Rule
    使用流程
        新建一个工程
        cd 工程中
        新建一个爬虫文件 scrapy genspider -t crawl 爬虫名 url

分布式
    概念：需要搭建一个分布式的机群，在机群的每一台电脑中执行同一组程序，让其对某一个网站的数据进行联合分布爬取
    原生的scrapy是不可以实现分布式的
        调度器不可以被共享
        管道不可以被共享
    如何实现
        scrapy + scrapy_redis实现分布式
    scrapy + scrapy_redis组件作用：
        可以提供可被共享的调度器和管道
        数据只可以存储在redis数据库
    分布式实现流程
        1.pip install scrapy-redis
        2.创建工程
        3.cd 工程
        4.创建爬虫文件  a.创建基于spider的爬虫文件  b.创建crawlspider的爬虫文件
        5.修改爬虫类
            5.1 from scrapy_redis.spiders import RedisCrawlSpider
            5.2 修改当前爬虫类的父类
            5.3 allowed_domains和start_urls删除掉
            5.4 添加一个新属性redis_key = "fbsQueue"，表示的是可以被共享的调度器队列的名称
            5.5 编写爬虫类的其他操作（常规操作）
        6.settings配置文件
            UA伪装
            Robots
            管道的指定
                ITEM_PIPELINES = {
                    'scrapy_redis.pipelines.RedisPipeline': 400,
                }
            制定调度器
                # 指定使用scrapy-redis的调度器
                SCHEDULER = "scrapy_redis.scheduler.Scheduler"

                # 指定使用scrapy-redis的去重
                DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

                # 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理redis queues
                SCHEDULER_PERSIST = True
            指定redis数据库
                REDIS_HOST = "127.0.0.1"
                REDIS_PORT = 6379
            redis配置文件进行配置redis.windows.conf
                关闭默认绑定 56行：# bind 127.0.0.1
                关闭保护模式 75行：protected-mode no
            启动redis服务端和客户端
                redis-server redis.windows.conf
                redis-cli
            启动程序
                scrapy runspider xx.py
                (base) C:\Users\acer\Desktop\AsyCra\fbsPro\fbsPro\spiders>scrapy runspider fbs.py
            向调度器的队列中扔入一个起始的URL：
                队列是存在于redis中的
                LPUSH fbsQueue http://wz.sun0769.com/index.php/question/questionType?type=4&page=

增量式
    概念：用于监测网站数据更新的情况
    核心机制：去重 redis的set实现去重
"""








