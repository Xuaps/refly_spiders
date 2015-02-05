# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from refly_scraper.items import ReferenceItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class SpiderBase(CrawlSpider):
    excluded_path = ['MDN', 'Web technology for developers']
    allowed_domains = ['mozilla.org']
    rules = ()
    start_urls = ()

    def __init__(self, *a, **kw):
        super(SpiderBase, self).__init__(*a, **kw)

    def parse_start_url(self, response):
        return list(self.parse_item(response))


    def parse_item(self, response):
        reference = ReferenceItem()
        reference['name'] = self.getName(response,self.xpathname) 
        reference['alias'] = self.getAlias(response, self.xpathalias)
        if reference['alias'] == '':
            reference['alias'] = reference['name']
        reference['url'] = self.getUrl(response)
        reference['content'] = self.getContent(response, self.xpathcontent)
        reference['path'] = self.getPath(response, self.xpathpath)

        yield reference

    def getName(self, response, xpathpattern):
        return self.remove_tags(self.getExistingNode(response,xpathpattern).decode('utf-8'))

    def getAlias(self, response, xpathpattern):
        try:
            xpathpattern
        except NameError:
            xpathpattern = ''
        if xpathpattern != '':
            return self.getExistingNode(response,xpathpattern)
        else:
            return ''
  
    def getUrl(self, response):
        return urlparse.urlsplit(response.url)[2].decode('utf-8')
  

    def getContent(self, response, xpathpattern):
        return  self.getExistingNode(response,xpathpattern).decode('utf-8')
  

    def getPath(self, response, xpathpattern):
        return [p.replace(u'\\',u'-').replace(u'/',u'-') for p in response.xpath(xpathpattern).extract() if p not in self.excluded_path]

    def resolveType(self, url, name):
        if re.search(r'^.*Statements\/((?!\/).)*$',url)!=None:
            return u'statement'
        elif re.search(r'^.*Operators\/((?!\/).)*$',url)!=None:
            return u'expression'
        elif re.search(r'^.*Global_Objects\/.*(?=\/).*$',url)!=None and re.search(r'^.*(?=\)$)',name)!=None:
            return u'method'
        elif re.search(r'^.*Global_Objects\/.*(?=\/).*$',url)!=None and re.search(r'^((?!\().)*$',name)!=None:
            return u'property'
        elif re.search(r'^.*Global_Objects\/((?!\/).)*$',url)!=None and re.search(r'^[A-Z]((?!\().)*$',name)!=None:
            return u'class'
        elif re.search(r'^.*Global_Objects\/((?!\/).)*$',url)!=None and re.search(r'^.*(?=\)$)',name)!=None:
            return u'function'
        elif re.search(r'^.*Global_Objects\/((?!\/).)*$',url)!=None and re.search(r'^[a-z]((?!\().)*$', name)!=None:
            return u'object'
    
        return u'others';

    def getSlashUrl(self,path, name): 
        if self.baseuri == '':
            self.baseuri = '/'
        if name!='':
            return unicode(self.baseuri) + (u'/'.join(path)+u'/'+name.replace(u'\\',u'-').replace(u'/',u'-')).replace(u'"',u'').replace(u"'",u"").lower().replace(u' ', u'_').replace(u'[', u'.').replace(u']', u'')
        else:
            if len(path)>1:
                return unicode(self.baseuri) + (u'/'.join(path)).lower().replace(u'"',u'').replace(u"'",u"").replace(u' ', u'_').replace(u'[', u'.').replace(u']', u'')
            else:
                return None


    def getExistingNode(self, response, criteria):
        if isinstance(criteria, list):
            for composedcriteria in criteria:
                filtercriteria = composedcriteria['filter']
                fullcriteria = filtercriteria + composedcriteria['extract']
                if len(response.xpath(fullcriteria).extract())>0:
                    returnedvalue = response.xpath(fullcriteria).extract()[0]
                    return self.filter_Chars(returnedvalue)
        else:
                if len(response.xpath(criteria).extract())>0:
                    return self.filter_Chars(response.xpath(criteria).extract()[0])
        return u''

    def remove_tags(self,text):
        return re.sub('<[^>]*>', '', text)

    def filter_Chars(self, text):
        return text.replace(u'\u200b', u'').replace(u'\u00a0',u'').replace(u'\xa0',u'').replace(u'\xb6',u'').replace(u'\u2014',u'-')

