# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
import HTMLParser
from refly_scraper.items import ReferenceItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from spiderbase import SpiderBase


class PhpSpider(SpiderBase):
    name = 'PHP'
    excluded_path = ['PHP Manual', 'Language Reference', 'Table of Contents']
    allowed_domains = ['php.net']
    rules = (Rule(LinkExtractor(allow_domains=allowed_domains,deny=(r'.*\.php\.net'),  allow = (r'\/manual\/en\/.*\.php')) , callback = 'parse_item', follow = True),
            )

    start_urls = (
        'http://php.net/manual/en/index.php',
    )
    
    def __init__(self, *a, **kw):
      super(PhpSpider, self).__init__(*a, **kw)
      
    baseuri = '/php/'

    xpathalias = [
        {'filter': '//li[@class="current"]/a','extract': '/text()'}
      ] 
    xpathname = [
        {'filter': u'//div[@class="reference"]//h1[@class="title"]', 'extract': u''},
        {'filter': u'//h1[@class="refname"]','extract': u''},
	{'filter': u'//h2[@class="title"]','extract': u''},
	{'filter': u'//div[@class="section"]//h2[@class="title"]','extract': u''},
	{'filter': u'//div[@class="sect1"]//h2[@class="title"]','extract': u''},
        {'filter': u'//div[@class="reference"]//h1[@class="title"]','extract': u''},
        {'filter': u'//table[@class="doctable table"]//caption//strong','extract': u''},
        {'filter': u'//div[@class="chapter"]//h1','extract': u''},
        {'filter': u'//div[@class="sect1"]//h2[@class="title"]','extract': u''},
        {'filter': u'//h1','extract': u''},
        {'filter': u'//h2','extract': u''},
        {'filter': u'//h4[@class="title"]','extract': u''},
        {'filter': u'//h1[@class="title"]', 'extract': u''},
        {'filter': u'//h1[@class="title"]','extract': u''},
        {'filter': u'//h2[@class="title"]','extract': u''}]
    xpathcontent = [
        {'filter': '//div[@id="legalnotice"]','extract': ''},
        {'filter': '//div[@class="refentry"]','extract': ''},
        {'filter': '//div[@class="sect1"]','extract': ''},
        {'filter': '//div[@class="reference"]','extract': ''},
        {'filter': '//div[@class="book"]','extract': ''},
        {'filter': '//div[@class="chapter"]','extract': ''},
        {'filter': '//div[@class="appendix"]','extract': ''},
        {'filter': '//div[@class="preface"]','extract': ''},
        {'filter': '//div[@class="section"]','extract': ''},
        {'filter': '//div[@class="article"]','extract': ''},
        {'filter': '//div[@class="part"]','extract': ''},
        {'filter': '//div[@class="set"]','extract': ''}]

    xpathalias = '//li[@class="current"]/a/text()'
    
    xpathpath = '//*[@id="breadcrumbs-inner"]//li/a/text()'
    
    #Overwrites
    def getUrl(self, response):
        return urlparse.urlsplit(response.url)[2].split('/').pop()

    #Overwrites
    def getName(self, response, xpathpattern):
        self.fullname = self.getExistingNode(response,xpathpattern)
        return self.remove_tags(self.fullname)

    def getContent(self, response, xpathpattern):
        return  self.MarkSourceCode(self.RemoveTitle(self.getExistingNode(response,xpathpattern),self.fullname),response)


    def resolveType(self, url, name):
        if re.search(r'^.*types.*$',url)!=None:
            return 'type'
        elif re.search(r'^.*interface.*$',name.lower())!=None:
            return 'interface'
        elif re.search(r'^.*variables.*$',url)!=None:
            return 'variable'
        elif re.search(r'^.*language.constants.*$',url)!=None:
            return 'constant'
        elif re.search(r'^.*appendices.*$',name.lower())!=None:
            return 'interface'
        elif re.search(r'^.*migration.*$',name.lower())!=None:
            return 'guide'
        elif re.search(r'^faq.*$',name.lower())!=None:
            return 'guide'
        elif re.search(r'^.*install.*$',url)!=None:
            return 'guide'
        elif re.search(r'^.*basic.*$',url)!=None:
            return 'guide'
        elif re.search(r'^.*language.expressions.*$',url)!=None:
            return 'guide'
        elif re.search(r'^.*language.operators.*$',url)!=None:
            return 'guide'
        elif re.search(r'^.*control-structures.*$',url)!=None:
            return 'function'
        elif re.search(r'^.*funcs.*$',url)!=None:
            return 'function'
        elif re.search(r'^cairocontext.*$',url)!=None:
            return 'function'
        elif re.search(r'^.*function.*$',url)!=None:
            return 'function'
        elif re.search(r'^.*language.oop5.*$',url)!=None:
            return 'class'
        elif re.search(r'^.*class.*$',url)!=None:
            return 'class'
        elif re.search(r'^.*language.namespaces.*$',url)!=None:
            return 'namespace'
        elif re.search(r'^.*language.exceptions.*$',url)!=None:
            return 'class'
        elif re.search(r'^.*language.references.*$',url)!=None:
            return 'guide'
        elif re.search(r'^.*operators.*$',name.lower())!=None:
            return 'variable'
        elif re.search(r'^.*context\.(.*).*$',url)!=None:
            return 'guide'
        elif re.search(r'^.*::.*$',name)!=None:
            return 'method'
        elif re.search(r'^.*wrappers\.(.*).*$',url)!=None:
            return 'class'
        else:
            return "others";

    def RemoveTitle(self,content,title):
        return content.replace(title, '')

    def MarkSourceCode(self, content, response):
        snipetsmethod = response.xpath('//div[@class="methodsynopsis dc-description"]').extract()
        snipetsclass = response.xpath('//div[@class="classsynopsis"]').extract()
        """ this case is particular because of codec issue"""
        content = content.replace('<div class="phpcode"><code>','<pre><code>').replace('</code></div>','</code></pre>')
        snipets = snipetsmethod + snipetsclass   
        for snipet in snipets:
            content = content.replace(snipet, '<pre><code>' + snipet + '</code></pre>')
        return content

