import unittest
from scrapy.http import HtmlResponse
import re
from refly_scraper.items import ReferenceItem
from refly_spiders.dotnet import DotNetSpider
import html2text as html2text_orig
class DotNetParserTest(unittest.TestCase):
    def test_parse(self):
        test = 5
        test1 = u'./tests/data/dotnet_ienumerable.html'
        test2 = u'./tests/data/dotnet_references.html'
        test3 = u'./tests/data/dotnet_framework4.6.html'
        test4 = u'./tests/data/dotnet_language_selector.html'
        url1 = u'gg145045(v=vs.110).aspx'
        url2 = u'gg145045(v=vs.110).aspx'
        url3 = u'w0x726c2(v=vs.110).aspx'
        url4 = u'system.object.gettype(v=vs.110).aspx';
        if test == 1:
            bodyfile = test1
            url = url1
        elif test == 2:
            bodyfile = test2
            url = url2
        elif test == 3:
            bodyfile = test3
            url = url3
        elif test == 4:
            bodyfile = test4
            url = url4
        elif test == 5:
            bodyfile = test1
            url = url1

        response = HtmlResponse(url='http://msdn.microsoft.com/en-us/library/' + url,
                        body=open(bodyfile).read())
        spider = DotNetSpider()
        result = spider.parse(response)
        item = result.next()
        if test == 1:
            self.assertEqual(item['name'], u'Comparer<T> Properties')
            self.assertEqual(item['url'], 'gg145045(v=vs.110).aspx')
            self.assertIsNotNone(item['content'])
            self.assertEqual(item['path'], [u'.NET Framework 4.5 and 4.6 Preview', u'.NET Framework Class Library', u'System.Collections Namespaces', u'System.Collections.Generic', u'Comparer(T) Class', u'Comparer(T) Properties'])
        elif test == 2:
            print '#########################' + unicode(item['content']) + '#####################################'
            self.assertEqual(item['name'], u'.NET Framework Class Library')
            self.assertEqual(item['url'], 'gg145045(v=vs.110).aspx')
            self.assertIsNotNone(item['content'])
            self.assertEqual(item['path'], [])
        elif test == 3:
            print '######################### path: ' + unicode(item['path']) + '#####################################'
            self.assertEqual(item['name'], u'.NET Framework 4.5 and 4.6 Preview')
            self.assertEqual(item['url'], 'w0x726c2(v=vs.110).aspx')
            self.assertIsNotNone(item['content'])
            self.assertEqual(item['path'], [])
        elif test == 4:
            print '######################### content: ' + unicode(item['content']) + '#####################################'
            self.assertEqual(item['name'], u'Comparer<T> Properties')
            self.assertEqual(item['url'], 'gg145045(v=vs.110).aspx')
            self.assertIsNotNone(item['content'])
            self.assertEqual(item['path'], [u'.NET Framework Class Library', u'System', u'Object Class'])
        elif test == 5:
            item['content'] = self.html2text(item['content'])
            print '######################### content: ' + unicode(item['content']) + '#####################################'
            self.assertEqual(item['name'], u'Object.GetType Method')
            self.assertEqual(item['url'], 'gg145045(v=vs.110).aspx')
            self.assertIsNotNone(item['content'])
            self.assertEqual(item['path'], [u'.NET Framework Class Library', u'System', u'Object Class'])


    def html2text(self, html):
        """use html2text but repair newlines cutting urls and fix errors in links with code inside"""
        html = self.MarkTables(html)
        h = html2text_orig.HTML2Text()
        h.inline_links = False
        h.bypass_tables = False
        txt = h.handle(html).replace('`[', '[`')
        txt = self.RestoreTables(txt)

        return txt

    def MarkTables(self,txt):
        txt = txt.replace('\n','')
        td_re = re.compile("<td.*?>(.*?)<\/td>")
        for td in td_re.findall(txt):
            txt = txt.replace(td, '<td>;begin_td;' + td + ';end_td;</td>')
        return txt

    def RestoreTables(self,txt):
        td_re = re.compile(";begin_td;(.*?);end_td;")
        for td in td_re.findall(txt):
            td_correct = td.replace('\n', '')
            txt = txt.replace(td, td_correct)
        txt = txt.replace(';begin_td;','').replace(';end_td;','')
        return txt
