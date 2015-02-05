# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from refly_scraper.items import ReferenceItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from spiderbase import SpiderBase

class JsSpider(SpiderBase):
    name = 'JavaScript'
    excluded_path = ['MDN', 'Web technology for developers']
    allowed_domains = ['mozilla.org']
    rules = (Rule(LinkExtractor(allow_domains=allowed_domains, deny=(r".*\$.*"), allow = ("\/en-US\/docs\/Web\/JavaScript\/Reference\/[\w\*\/]*")) , callback = 'parse_item', follow = True), 
            )

    start_urls = (
        'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference',
    )
    
    baseuri = '/'
    xpathname = '//h1/text()'
    xpathalias = ''
    xpathcontent = '//article'
    xpathpath = '//nav[@class="crumbs"]//a/text()'

    def __init__(self, *a, **kw):
        super(JsSpider, self).__init__(*a, **kw)

    def getContent(self, response, xpathpattern):
        return  self.TransformLinks(self.getExistingNode(response,xpathpattern),response)

    def resolveType(self, url, name):
        if re.search(r'^.*Statements\/((?!\/).)*$',url)!=None:
            return 'statement'
        elif re.search(r'^.*Operators\/((?!\/).)*$',url)!=None:
            return 'expression'
        elif re.search(r'^.*Global_Objects\/.*(?=\/).*$',url)!=None and re.search(r'^.*(?=\)$)',name)!=None:
            return 'method'
        elif re.search(r'^.*Global_Objects\/.*(?=\/).*$',url)!=None and re.search(r'^((?!\().)*$',name)!=None:
            return 'property'
        elif re.search(r'^.*Global_Objects\/((?!\/).)*$',url)!=None and re.search(r'^[A-Z]((?!\().)*$',name)!=None:
            return 'class'
        elif re.search(r'^.*Global_Objects\/((?!\/).)*$',url)!=None and re.search(r'^.*(?=\)$)',name)!=None:
            return 'function'
        elif re.search(r'^.*Global_Objects\/((?!\/).)*$',url)!=None and re.search(r'^[a-z]((?!\().)*$', name)!=None:
            return 'object'
    
        return "others";

    def getSlashUrl(self,path, name):
        if name!='':
