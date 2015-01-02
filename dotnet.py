# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import urlparse
import re
import HTMLParser
from refly_scraper.items import ReferenceItem


class DotNetSpider(scrapy.Spider):
    name = '.NET'
    excluded_path = [u'MSDN Library', u'.NET Development', u'.NET Framework 4.5 and 4.6 Preview']
    allowed_domains = ['microsoft.com']
    visited = ['http://msdn.microsoft.com/en-us/library/ff361664(v=vs.110).aspx',
              'http://msdn.microsoft.com/en-us/library/w0x726c2(v=vs.110).aspx',
              ]
    filterscontent = []
    filtersname = []
    filtersalias = []
    start_urls = (
        'http://msdn.microsoft.com/en-us/library/gg145045(v=vs.110).aspx',
    )

    def __init__(self):
      #scrapy.log.start(self.name+'.log',scrapy.log.CRITICAL, False)
      self.filtersname = [
        {'filter': u'//h1[@class="title"]', 'extract': u''}]
      self.filterscontent = [
        {'filter': u'//div[@class="topic"]','extract': u''}
        ]

    def parse(self, response):
        self.__init__()
        reference = ReferenceItem()
        reference['name'] = self.unescape(re.sub(u'<[^>]*>', u'', self.getExistingNode(response,self.filtersname))).decode('utf-8')
        if self.resolveType(self,reference['name'])=='namespace':
                reference['alias'] = reference['name'].split(' ')[:-1]
        else:
                reference['alias'] = reference['name']
        reference['url'] = urlparse.urlsplit(response.url)[2].split('/').pop().decode('utf-8')
        reference['content'] = self.getExistingNode(response,self.filterscontent)
        reference['path'] = [p for p in response.xpath('//div[@id="tocnav"]/div[@data-toclevel<1]/a/text()').extract() if p not in self.excluded_path]
        yield reference

        #urls = [self.visit(urlparse.urljoin(response.url, url)) for url in self.filterLink(response,'//div[@class="tocnav"]//a/@href','(\/en-us\/library\/.*\(v=vs\.110\).aspx)') if urlparse.urljoin(response.url, url) not in self.visited]
        urls = [self.visit(urlparse.urljoin(response.url, url)) for url in response.xpath('//a[re:test(@href, "^\/en-us\/library\/.*\(v=vs\.110\).aspx$")]/@href').extract() if urlparse.urljoin(response.url, url) not in self.visited]



        for i in urls:
           
            yield i

    def visit(self, url):
        self.visited.append(url)
        return scrapy.Request(url, callback=self.parse)

    def resolveType(self, url, name):
        strtype = name.split(' ').pop()
        if strtype == 'Library':
          return 'others'
        elif strtype == 'Methods' or strtype=='Method':
          return 'method'
        else:
          return strtype.lower()

    def getSlashUrl(self,path, name):
        if name!='':
          if len(path)>0:
            return unicode(u'/dotnet/'+('/'.join(path) + '/' + name)).replace('"','').replace("'","").replace(' ', '_').lower()
          else:
            return u'/dotnet/' + name.lower().replace('"','').replace("'","").replace(' ', '_').lower()
        else:
          if len(path)>0:
            return unicode(u'/dotnet/'+('/'.join(path))).replace('"','').replace("'","").replace(' ', '_').lower()
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

    def unescape(self,htmltext):
        htmltext = htmltext.replace(u'&lt;', u'<')
        htmltext = htmltext.replace(u'&gt;', u'>')
        htmltext = htmltext.replace(u'&amp;', u'and')
        return htmltext.strip()


    def filterLink(self,response,xpathexp, regexp):
         hrefs = response.xpath(xpathexp).extract()
         regex = re.compile(regexp)
         newhrefs = []
         for a in hrefs:
             if regex.match(a):
                 a.split('?')[:-1]
                 if a not in newhrefs:
                     newhrefs.append(a)
         return newhrefs
