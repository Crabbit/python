# 迷你定向网页抓取器 - mini_spider

在调研过程中，经常需要对一些网站进行定向抓取。由于python包含各种强大的库，使用python做定向抓取比较简单。请使用python开发一个迷你定向抓取器mini_spider.py，实现对种子链接的抓取，并把URL长相符合特定pattern的网页保存到磁盘上。
程序运行:
> python mini_spider.py -c spider.conf 

配置文件spider.conf:
```vim
[spider] 
url_list_file: ./urls ; 种子文件路径 
output_directory: ./output ; 抓取结果存储目录 
max_depth: 1 ; 最大抓取深度(种子为0级) 
crawl_interval: 1 ; 抓取间隔. 单位: 秒 
crawl_timeout: 1 ; 抓取超时. 单位: 秒 
target_url: .*.(htm|html)$ ; 需要存储的目标网页URL pattern(正则表达式) 
thread_count: 8 ; 抓取线程数 
```

种子文件每行一条链接，例如: 
> http://www.baidu.com</br>
> http://www.sina.com.cn</br>

- 要求和注意事项:
1. 需要支持命令行参数处理。具体包含: -h(帮助)、-v(版本)、-c(配置文件)
2. 单个网页抓取或解析失败，不能导致整个程序退出。需要在日志中记录下错误原因并继续。
3. 当程序完成所有抓取任务后，必须优雅退出。
4. 从HTML提取链接时需要处理相对路径和绝对路径。
5. 需要能够处理不同字符编码的网页(例如utf-8或gbk)。
6. 网页存储时每个网页单独存为一个文件，以URL为文件名。注意对URL中的特殊字符，需要做转义。
7. 要求支持多线程并行抓取。
8. 代码严格遵守百度python编码规范
9. 代码的可读性和可维护性好。注意模块、类、函数的设计和划分
10. 完成相应的单元测试和使用demo。你的demo必须可运行，单元测试有效而且通过
11. 注意控制抓取间隔和总量，避免对方网站封禁IP。

***

提示(下面的python库可能对你完成测试题有帮助):

> re(正则表达式)
>> 参考: http://docs.python.org/2/library/re.html</br>
>> 参考: http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html</br>
>> 参考: http://blog.csdn.net/jgood/article/details/4277902</br>

> gevent/threading(多线程)
>> 参考: http://docs.python.org/2/library/threading.html</br>
>> 参考: http://www.cnblogs.com/huxi/archive/2010/06/26/1765808.html</br>

> docopt/getopt/argparse(命令行参数处理)
>> 参考: https://github.com/docopt/docopt</br>
>> 参考: http://docs.python.org/2/library/getopt.html</br>
>> 参考: http://andylin02.iteye.com/blog/845355</br>
>> 参考: http://docs.python.org/2/howto/argparse.html</br>
>> 参考: http://www.cnblogs.com/jianboqi/archive/2013/01/10/2854726.html</br>

> ConfigParser(配置文件读取)
>> 参考: http://docs.python.org/2/library/configparser.html</br>
>> 参考: http://blog.chinaunix.net/uid-25890465-id-3312861.html</br>

> urllib/urllib2/httplib(网页下载)
>> 参考: http://docs.python.org/2/library/urllib2.html</br>
>> 参考: http://blog.csdn.net/wklken/article/details/7364328</br>
>> 参考: http://www.nowamagic.net/academy/detail/1302872</br>

> pyquery/beautifulsoup4/HTMLParser/SGMLParser(HTML解析)
>> 参考: http://docs.python.org/2/library/htmlparser.html</br>
>> 参考: http://cloudaice.com/yong-pythonde-htmlparserfen-xi-htmlye-mian/</br>
>> 参考: http://docs.python.org/2/library/sgmllib.html</br>
>> 参考: http://pako.iteye.com/blog/592009</br>

> urlparse(URL解析处理)
>> 参考: http://docs.python.org/2/library/urlparse.html</br>
>> 参考: http://blog.sina.com.cn/s/blog_5ff7f94f0100qr3c.html</br>

> logging(日志处理)
>> 参考: http://docs.python.org/2/library/logging.html
>> 参考: http://kenby.iteye.com/blog/1162698
>> 参考: http://my.oschina.net/leejun2005/blog/126713
