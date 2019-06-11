# -*- coding: utf-8 -*-
import scrapy
import re
from downloadbook.items import DownloadBookItem
import requests
from lxml import etree

class JjshuSpider(scrapy.Spider):
    name = 'jjshu'
    allowed_domains = ['jjshu.net']
    start_urls = ['https://www.jjshu.net/0/74/index.html']
    
# 新建main.py，调试该文件，并在parse函数内打断点，就会进入到该断点。    
# scrapy框架库是异步获取数据模式，所以对于需要同步获取数据的方式不适用。
# xpath表达式可以通过chrome开发者工具可以看到具体的元素顺序和属性，具体方法：打开网页，按F12，用箭头工具查看标签，右键选择copy，选择xpath就可以了
# yield 是python的关键字，相当于return，但是返回的是迭代器，对于还有next send 功能函数，next是获取下一个值，send是设置值，并next
# 对于scrapy框架中，如果想使用item通过pipelines保存数据，需要在spider中返回item，并且配置settings，就会自动调用对应数据库保存类。

    def parse(self, response):
        readerlist = response.xpath('//div[@id="maininfo"]/div[@id="readerlist"]/ul/li/a[@href]').extract()
        # <li><a href="/0/74/8426142.html">第01章 玄字一号监</a></li>
        for node in readerlist:
            matchObj = re.match(r'.*<a href=\"(.*)\">(.*)</a>.*', node)
            url='https://www.jjshu.net' + matchObj.group(1)
            title = matchObj.group(2)

            print(title)
            print(url)
            if title[0] == '第' :
                content = requests.get(url).content #获取 url 网页源码
                html = etree.HTML(content) #将网页源码转换为 XPath 可以解析的格式
                contentList = html.xpath('//*[@id="content"]/text()') #可能为列表或节点
                with open("夜天子.txt", 'a') as f:
                    f.write(title)
                    for content in contentList:
                        if content == '\r\n':
                            continue
                        f.write(content)
                    f.flush()

                # yield item
        #     yield scrapy.Request(url, callback=self.parse_content)

        pass

    # def parse_content(self, response):
    #     title = response.xpath('//*[@id="center"]/div[1]/h1/text()').extract()[0].replace('章节目录 ', '', 1)
    #     contentList = response.xpath('//*[@id="content"]/text()').extract()
    #     print(title)
    #     print(contentList)
    #     with open("夜天子.txt", 'a') as f:
    #         f.write(title)
    #         for content in contentList:
    #             if content == '\r\n':
    #                 continue
    #             f.write(content)
    #         f.flush()
