import unittest
from scrapy.http import HtmlResponse
from refly_scraper.items import ReferenceItem
from refly_spiders.js import JsSpider

    
class JavaScriptParserTest(unittest.TestCase):
    def test_parse(self):
        response = HtmlResponse(url='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference', 
        	body=open('./tests/data/javascript_json.parse.html').read())
        spider = JsSpider()

        result = spider.parse(response)
        item = result.next()
        self.assertEqual(item['name'], 'JSON.parse()')
        self.assertEqual(item['url'], '/en-US/docs/Web/JavaScript/Reference')
        self.assertIsNotNone(item['content'])
        self.assertEqual(item['path'], [u'JavaScript', u'JavaScript reference', u'Standard built-in objects', u'JSON'])

    def test_getSlashUrl(self):
        pass

    def test_resolveType(self):
        pass

        
