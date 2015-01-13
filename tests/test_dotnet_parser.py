import unittest
from scrapy.http import HtmlResponse
from refly_scraper.items import ReferenceItem
from refly_spiders.dotnet import DotNetSpider
from bs4 import BeautifulSoup

class DotNetParserTest(unittest.TestCase):
    def test_parse(self):
        test = 5
        test1 = u'./tests/data/dotnet_ienumerable.html'
        test2 = u'./tests/data/dotnet_references.html'
        test3 = u'./tests/data/dotnet_framework4.6.html'
        test4 = u'./tests/data/dotnet_language_selector.html'
        test5 = u'./tests/data/dotnet_class_library.html'
        url1 = u'gg145045(v=vs.110).aspx'
        url2 = u'gg145045(v=vs.110).aspx'
        url3 = u'w0x726c2(v=vs.110).aspx'
        url4 = u'system.object.gettype(v=vs.110).aspx';
        url5 = u'gg145045(v=vs.110).aspx';
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
            bodyfile = test5
            url = url5

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
            #soup = BeautifulSoup(item['content'])
            #print '###################' + soup.get_text() + '############################'
            print '######################### content: ' + unicode(item['content']) + '#####################################'
            self.assertEqual(item['name'], u'.NET Framework Class Library')
            self.assertEqual(item['url'], 'gg145045(v=vs.110).aspx_fallo')
            self.assertIsNotNone(item['content'])
            self.assertEqual(item['path'], [])

