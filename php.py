# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
import HTMLParser
from refly_scraper.items import ReferenceItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class PhpSpider(CrawlSpider):
    name = 'PHP'
    excluded_path = ['PHP Manual', 'Language Reference', 'Table of Contents']
    allowed_domains = ['php.net']
    rules = (Rule(LinkExtractor(allow_domains=allowed_domains,deny=(r'.*\.php\.net'),  allow = (r'\/manual\/en\/.*\.php')) , callback = 'parse_item', follow = True),
            )

    start_urls = (
        'http://php.net/manual/en/index.php',
    )
    
    def __init__(self, *a, **kw):
      scrapy.log.start(self.name+'.log',scrapy.log.INFO, False)
      super(PhpSpider, self).__init__(*a, **kw)
      
      
      self.filtersalias = [
        {'filter': '//li[@class="current"]/a','extract': '/text()'}
      ] 
      self.filtersname = [
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

    def parse_start_url(self, response):
        return list(self.parse_item(response))

    def parse_item(self, response):
        self.__init__()
        reference = ReferenceItem()
        fullname =  self.getExistingNode(response,self.filtersname)
        reference['name'] = self.remove_tags(fullname)
        reference['alias'] = self.getExistingNode(response,self.filtersalias)
        if reference['alias'] == u'':
            reference['alias'] = reference['name']
        reference['type'] = u''
        reference['url'] = urlparse.urlsplit(response.url)[2].split('/').pop()
        reference['content'] = self.MarkSourceCode(self.RemoveTitle(self.getExistingNode(response,self.filterscontent),fullname),response)
        reference['path'] = [p for p in response.xpath('//*[@id="breadcrumbs-inner"]//li/a/text()').extract() if p not in self.excluded_path]

        return reference

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

    def getSlashUrl(self,path, name):
        path = [item.replace('/','-') for item in path]
        if name!='':
          if len(path)>0:
            return (u'/php/'+('/'.join(path)+'/'+name.replace('/', '-').replace('\\', '-'))).replace('"','').replace("'","").replace(' ', '_').lower()
          else:
            return u'/php/' + name.replace('\\', '-').replace('/', '-').lower().replace('"','').replace("'","").replace(' ', '_').lower()
        else:
          if len(path)>0:
            return (u'/php/'+('/'.join(path))).replace('\\', '-').lower().replace('"','').replace("'","").replace(' ', '_').lower()
          else:
            return None

    def getExistingNode(self, response, criteria):
        if isinstance(criteria, list):
            for composedcriteria in criteria:
                filtercriteria = composedcriteria['filter']
                fullcriteria = filtercriteria + composedcriteria['extract']
                print str(response)
                if len(response.xpath(fullcriteria).extract())>0:
                    returnedvalue = response.xpath(fullcriteria).extract()[0]
                    return returnedvalue.replace(u'\u200b', u'').replace(u'\u00a0',u'').replace(u'\xa0','')
        else:
                if len(response.xpath(criteria).extract())>0:
                    return response.xpath(criteria).extract()[0]
        return u''

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

    def remove_tags(self,text):
        return re.sub('<[^>]*>', '', text)
