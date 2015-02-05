# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor
import urlparse
import re
import HTMLParser
from refly_scraper.items import ReferenceItem
from spiderbase import SpiderBase



class DotNetSpider(SpiderBase):
 
    name = '.NET'
    excluded_path = [u'MSDN Library', u'.NET Development', u'.NET Framework 4.5 and 4.6 Preview']
    allowed_domains = ['microsoft.com']
    rules = (Rule(LinkExtractor(allow_domains=allowed_domains,allow = (r'\/en-us\/library\/.*\(v\=vs\.110\)\.aspx'), restrict_xpaths='//*[@class="toclevel2"]'), callback='parse_item', follow=True),)

    baseuri = '/dotnet/'
    xpathalias = ''

    xpathname = [
        {'filter': u'//div[@class="toclevel1 current"]/a[1]', 'extract': u'/text()'},
        {'filter': u'//h1[@class="title"]', 'extract': u''}]
    xpathcontent = [
        {'filter': u'//div[@id="mainBody"]','extract': u''}
        ]
    xpathpath = '//div[@id="tocnav"]/div[@data-toclevel<1]/a/text()'

    start_urls = (
        'http://msdn.microsoft.com/en-us/library/gg145045(v=vs.110).aspx',
    )

    def __init__(self, *a, **kw):
      super(DotNetSpider, self).__init__(*a, **kw)


    #Overwrites
    def getUrl(self, response):
        return urlparse.urlsplit(response.url)[2].split('/').pop().decode('utf-8')

    #Overwrites
    def getContent(self, response, xpathpattern):
        return  self.TransformLinks(self.removeTabs(response, self.getExistingNode(response,xpathpattern)),response)


    def resolveType(self, url, name):
        strtype = name.split(' ').pop()
        if strtype == 'Library':
          return 'guide'
        elif strtype == 'Methods' or strtype=='Method':
          return 'method'
        elif strtype == 'Property':
          return 'property'
        elif strtype == 'NameSpaces':
          return 'namespace'
        else:
          return 'class'


    def removeTabs(self,response,content):
        for tabs in response.xpath('//div[@class="codeSnippetContainerTabs"]').extract():
            content = content.replace(tabs, '')
        return content

    def unescape(self,htmltext):
        htmltext = htmltext.replace(u'&lt;', u'<')
        htmltext = htmltext.replace(u'&gt;', u'>')
        htmltext = htmltext.replace(u'&amp;', u'and')
        return htmltext.strip()

    def TransformLinks(self,content,response):
        validlink = re.compile(u'https:\/\/msdn\.microsoft\.com\/en-us\/library\/(.*\(v=vs\.110\)\.aspx)')
        links = response.xpath('//a/@href').extract()
        for link in links:
            match = validlink.match(link)
            if match:
                content = content.replace('"' + link + '"', '"' + match.group(1) + '"',1)

        return content

