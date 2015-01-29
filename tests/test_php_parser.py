import unittest
from scrapy.http import HtmlResponse
from refly_scraper.items import ReferenceItem
from refly_spiders.php import PhpSpider

class PhpParserTest(unittest.TestCase):
    def test_parse(self):
        response = HtmlResponse(url='http://php.net/manual/en/faq.php',
                   body=open('./tests/data/php_faq.html').read())
        spider = PhpSpider()
        result = spider.parse(response)
        
        item = result.next()
        #print '##########' + item['content'] + '#############'
        self.assertEqual(item['name'], 'FAQ: Frequently Asked Questions')
        self.assertEqual(item['url'], 'faq.php')
        self.assertIsNotNone(item['content'])
        self.assertEqual(item['path'], [])
