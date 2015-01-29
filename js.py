# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from refly_scraper.items import ReferenceItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class JsSpider(CrawlSpider):
    name = 'JavaScript'
    excluded_path = ['MDN', 'Web technology for developers']
    allowed_domains = ['mozilla.org']
    rules = (Rule(LinkExtractor(allow_domains=allowed_domains, deny=(r".*\$.*"), allow = ("\/en-US\/docs\/Web\/JavaScript\/Reference\/[\w\*\/]*")) , callback = 'parse_item', follow = True), 
            )
    start_urls = (
        'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference',
    )


    def __init__(self, *a, **kw):
        super(JsSpider, self).__init__(*a, **kw)

    def parse_start_url(self, response):
        return list(self.parse_item(response))


    def parse_item(self, response):
        reference = ReferenceItem()
        reference['name'] = response.xpath('//h1/text()').extract()[0]
        reference['alias'] = reference['name']
        reference['url'] = urlparse.urlsplit(response.url)[2]
        reference['content'] = self.TransformLinks(response.xpath('//article').extract()[0],response)
        reference['path'] = [p for p in response.css('.crumbs').xpath('.//a/text()').extract() if p not in self.excluded_path]

        yield reference

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
            return u'/'+('/'.join(path)+'/'+name).lower().replace(u' ', u'_').replace('[', '.').replace(']', '')
        else:
            if len(path)>1:
                return u'/'+('/'.join(path)).lower().replace(u' ', u'_').replace('[', '.').replace(']', '')
            else:
                return None

    def TransformLinks(self,content,response):
        validlink = re.compile(u'(\/en-US\/docs\/Web\/JavaScript\/Reference.*)')
        links = response.xpath('//a/@href').extract()
        for link in links:
            if validlink.match(link) is None:
                if urlparse.urlparse(link).scheme=='':
                    content = content.replace('"' + link + '"', '"' + urlparse.urljoin('https://developer.mozilla.org', link) + '"',1)
        return content
