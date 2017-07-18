#!/usr/bin/python
# -*- coding: UTF-8 -*-

from coolscrapy.items import XiaoHuaItem
import scrapy
from scrapy.http import Request
import re

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['mmonly.cc']
    # start_urls = [
    #     'http://www.mmonly.cc/tag/',
    # ]
    def start_requests(self):
        url = 'https://www.mmonly.cc/tag/'
        yield Request(url, callback=self.parse)


    def parse(self, response):
          # filename = 'quotes3.html'
          # with open(filename, 'wb') as f:
          #    f.write(response.body)

          item01 = []
          item02 = []
          item03 = []
          tags_item02 = []
          pattern = re.compile(r'<h2>(.*?)</h2>', re.S)
          item01 = re.findall(pattern, response.text)   #一级标签内容


          for tags in response.css("div.TagList"):
              item02.append(tags.css("a::attr(href)").extract())    #二级标签地址
              item03.append(tags.css("a::attr(title)").extract())   #二级标签内容
          # str_tmp = str(item03).replace('u\'', '\'')
          # item00 = str_tmp.decode('unicode-escape')    #转换成中文！
          # for i in range(0, len(item03)):
          #     for j in range(0, len(item03[i])):
          #         item04.append(item03[i][j])

          for i in range(0, len(item02)):
              for j in range(0, len(item02[i])):
                  tags_item02.append(item02[i][j])
          #print tags_item02
          items = XiaoHuaItem()
          items['pre_tags'] = item01
          items['tags'] = tags_item02


          count = 0
          # for i in range(0, len(item04)):
          #     print i, '-', item04[i]

          for i in range(0, len(item03)):
              print ''
              print 'tag', i, ':', item01[i]
              for j in range(0, len(item03[i])):
                  print count, '-', item03[i][j],
                  print '  ',
                  count = count + 1
          print ''
          print '**************************************************'
          print 'scrapy框架爬取图片(version1.0)'
          print '作者： jiushizheyang'
          print '参考： https://zhuanlan.zhihu.com/p/26419110'
          print '目标站点：https://www.mmonly.cc/'


          while True:
              print '输入标签对应的数字( 范围 0 ——', len(tags_item02) - 1, '):'
              tag_id = raw_input()
              try:
                  tag_id = int(tag_id)
              except ValueError:
                  print '请输入正确数字!!!'
                  continue
              else:
                  break

          yield Request(url='https://www.mmonly.cc'+items['tags'][tag_id], meta={'items1': items, 'items2':tag_id}, callback=self.parse2)


    def parse2(self,response):    #分页处理
          items = response.meta['items1']
          tag_id = response.meta['items2']
          #print items['tags'][tag_id]
          item3_tmp=[]
          item3 = [items['tags'][tag_id]+'1.html']   #构造pages的第一页
          for pages in response.css("div.pages"):
             item3_tmp.append(pages.css("a::attr(href)").extract())  # 这里返回的是pages第二页往后的列表
          for item in item3_tmp[0]:
             item3.append(item)
          #print item3
          items['pages']=item3
          if  len(item3)==1:
              pagesNum = len(item3)
          else:
              pagesNum = len(item3)-2
          for i in range (0, pagesNum):
              yield Request(url='https://www.mmonly.cc'+items['pages'][i], meta={'items1': items}, callback=self.parse3)

    def parse3(self, response):
          items = response.meta['items1']
          item1 = []
          item2 = []
          for img in response.css("div.item_t"):
              item1.append(img.css("div.ABox a").extract_first())
              item2.append(img.css('div.ABox a img::attr(src)').extract_first())

          items['text'] = item1
          items['image_urls'] = item2
          yield items
