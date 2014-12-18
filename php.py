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
        {'filter': '//li[@class="current"]/a/','extract': '/text()'}
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
        reference['content'] = self.TransformLinks(self.getExistingNode(response,self.filterscontent))
        reference['path'] = [p for p in response.xpath('//*[@id="breadcrumbs-inner"]//li/a/text()').extract() if p not in self.excluded_path]

        yield reference

        urls = [self.visit(urlparse.urljoin(response.url, url)) for url in response.xpath('//a[re:test(@href, "^((?!\/).)*\.php$")]/@href').extract() if urlparse.urljoin(response.url, url) not in self.visited]

        for i in urls:
            yield i

    def visit(self, url):
        self.visited.append(url)
        return scrapy.Request(url, callback=self.parse)

    def resolveType(self, url, name):
        if re.search(r'^.*language.types\.(.*).*$',url)!=None:
            return 'type'
        elif re.search(r'^.*language.pseudo-types\.(.*).*$',url)!=None:
            return 'type'
        elif re.search(r'^.*language.variables\.(.*).*$',url)!=None:
            return 'variable'
        elif re.search(r'^.*language.constants\.(.*).*$',url)!=None:
            return 'constant'
        elif re.search(r'^.*language.expressions\.(.*).*$',url)!=None:
            return 'expression'
        elif re.search(r'^.*language.operators\.(.*).*$',url)!=None:
            return 'operators'
        elif re.search(r'^.*control-structures\.(.*).*$',url)!=None:
            return 'control structures'
        if re.search(r'^.*function\.(.*).*$',url)!=None:
            return 'function'
        elif re.search(r'^.*language.oop5\.(.*).*$',url)!=None:
            return 'class'
        elif re.search(r'^.*class\.(.*).*$',url)!=None:
            return 'class'
        elif re.search(r'^.*language.namespaces\.(.*).*$',url)!=None:
            return 'namespaces'
        elif re.search(r'^.*language.exceptions\.(.*).*$',url)!=None:
            return 'exceptions'
        elif re.search(r'^.*language.generators\.(.*).*$',url)!=None:
            return 'generators'
        elif re.search(r'^.*language.references\.(.*).*$',url)!=None:
            return 'references'
        elif re.search(r'^.*reserved.variables\.(.*).*$',url)!=None:
            return 'predefined variables'
        elif re.search(r'^.*context\.(.*).*$',url)!=None:
            return 'context'
        elif re.search(r'^.*wrappers\.(.*).*$',url)!=None:
            return 'wrappers'
        else:
            return "others";

    def getSlashUrl(self,path, name):
        if name!='':
          if len(path)>0:
            return (u'/php/'+('/'.join(path)+'/'+name)).replace('"','').replace("'","").replace(' ', '_').lower()
          else:
            return u'/php/' + name.lower().replace('"','').replace("'","").replace(' ', '_').lower()
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

    def TransformLinks(self,content):
        content = re.sub(r'"(.*).php#(.*)"', r'"\1.php"', content)
        return content

