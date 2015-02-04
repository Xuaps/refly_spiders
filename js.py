# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from refly_scraper.items import ReferenceItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class JsSpider(SpiderBase):
    name = 'JavaScript'
    excluded_path = ['MDN', 'Web technology for developers']
    allowed_domains = ['mozilla.org']
    rules = (Rule(LinkExtractor(allow_domains=allowed_domains, deny=(r".*\$.*"), allow = ("\/en-US\/docs\/Web\/JavaScript\/Reference\/[\w\*\/]*")) , callback = 'parse_item', follow = True), 
            )
    start_urls = (
        'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference',
    )

    author_info = u'<p>© 2015 Mozilla Contributors.<br />Licensed under the Creative Commons Attribution-ShareAlike License v2.5 or later.<br/>{link}</p>'
    baseuri = '/'
    xpathname = '//h1/text()'
    xpathalias = ''
    xpathcontent = '//article'
    xpathpath = '//nav[@class="crumbs"]//a/text()'

    def __init__(self, *a, **kw):
        super(JsSpider, self).__init__(*a, **kw)


    def getContent(self, response, xpathpattern):
        return  self.appendAuthorInfo(self.TransformLinks(self.getExistingNode(response,xpathpattern),response),response.url)

    def appendAuthorInfo(self, content,url):
        content += self.author_info.replace('{link}','<a href="' + url + '">'+ url +'</a>')
        return content

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
