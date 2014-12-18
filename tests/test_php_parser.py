import unittest
from scrapy.http import HtmlResponse
from refly_scraper.items import ReferenceItem
from refly_spiders.php import PhpSpider

class PhpParserTest(unittest.TestCase):
	def test_parse(self):
		response = HtmlResponse(url='http://php.net/manual/en/language.basic-syntax.php',
			body=open('./tests/data/php_removeanchor.html').read())
		spider = PhpSpider()
		result = spider.parse(response)

		item = result.next()
		print unicode(item['content'])
		self.assertEqual(item['name'], 'Basic syntax')
		self.assertEqual(item['url'], 'language.basic-syntax.php')
		self.assertIsNotNone(item['content'])
		self.assertEqual(item['path'], [])
		self.assertEqual(len(list(result)), 24)
