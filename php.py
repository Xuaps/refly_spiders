# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
import HTMLParser
from refly_scraper.items import ReferenceItem


class PhpSpider(scrapy.Spider):
    name = 'PHP'
    excluded_path = ['PHP Manual', 'Language Reference', 'Table of Contents']
    allowed_domains = ['php.net']
    visited = []
    filterscontent = []
    filtersname = []
    filtersalias = []
    start_urls = (
        'http://php.net/manual/en/index.php',
    )

    def __init__(self):
      #scrapy.log.start(self.name+'.log',scrapy.log.CRITICAL, False)
      self.filtersalias = [
        {'filter': '//li[@class="current"]/a','extract': '/text()'}
      ]
      self.filtersname = [
        {'filter': u'//div[@class="reference"]//h1[@class="title"]', 'extract': u''},
        {'filter': u'//h1[@class="refname"]','extract': u''},
		{'filter': u'//h2[@class="title"]/em','extract': u'/text()'},
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
      self.filterscontent = [
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

    def parse(self, response):
        self.__init__()
        reference = ReferenceItem()
        reference['name'] = re.sub('<[^>]*>', '', self.getExistingNode(response,self.filtersname))
        reference['alias'] = self.getExistingNode(response,self.filtersalias)
        if reference['alias'] == u'':
          reference['alias'] = reference['name']
        reference['type'] = u''
        reference['url'] = urlparse.urlsplit(response.url)[2].split('/').pop()
        reference['content'] = self.RemoveTitle(self.getExistingNode(response,self.filterscontent),reference['name'])
        reference['path'] = [p for p in response.xpath('//*[@id="breadcrumbs-inner"]//li/a/text()').extract() if p not in self.excluded_path]

        yield reference

        urls = [self.visit(urlparse.urljoin(response.url, url)) for url in response.xpath('//a[re:test(@href, "^((?!\/).)*\.php$")]/@href').extract() if urlparse.urljoin(response.url, url) not in self.visited]

        for i in urls:
            yield i

    def visit(self, url):
        self.visited.append(url)
        return scrapy.Request(url, callback=self.parse)

    def resolveType(self, url, name):
        if re.search(r'^.*types.*$',url)!=None:
            return 'type'
        elif re.search(r'^.*interface.*$',name.lower())!=None:
            return 'interface'
        elif re.search(r'^.*variables.*$',url)!=None:
            return 'variable'
        elif re.search(r'^.*language.constants.*$',url)!=None:
            return 'constant'
        elif re.search(r'^.*language.expressions.*$',url)!=None:
            return 'guide'
        elif re.search(r'^.*language.operators.*$',url)!=None:
            return 'guide'
        elif re.search(r'^.*control-structures.*$',url)!=None:
            return 'guide'
        if re.search(r'^.*function.*$',url)!=None:
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

    def getSlashUrl(self,path, name):
        path = [item.replace('/','-') for item in path]
        if name!='':
          if len(path)>0:
            return (u'/php/'+('/'.join(path)+'/'+name.replace('\\', '-'))).replace('"','').replace("'","").replace(' ', '_').lower()
          else:
            return u'/php/' + name.replace('\\', '-').lower().replace('"','').replace("'","").replace(' ', '_').lower()
        else:
          if len(path)>0:
            return (u'/php/'+('/'.join(path))).replace('"','').replace("'","").replace(' ', '_').lower()
          else:
            return None

    def getExistingNode(self, response, criteria):
        if isinstance(criteria, list):
            for composedcriteria in criteria:
                filtercriteria = composedcriteria['filter']
                fullcriteria = filtercriteria + composedcriteria['extract']
                
                if len(response.xpath(fullcriteria).extract())>0:
                    returnedvalue = response.xpath(fullcriteria).extract()[0]
                    return returnedvalue.replace(u'\u200b', u'')
        else:
            return response.xpath(criteria).extract()[0]
        return u''

    def RemoveTitle(self,content,title):
        content = re.sub(r'<([\w]+)[^>]*>' + title + '<\/\1>', r'', content)
        return content

