import unittest
from scrapy.http import HtmlResponse
from refly_scraper.items import ReferenceItem
from refly_spiders.dotnet import DotNetSpider

class DotNetParserTest(unittest.TestCase):
	def test_parse(self):
		test = 1
		test1 = './tests/data/dotnet_ienumerable.html'
		test2 = './tests/data/dotnet_references.html'
		if test == 1:
			url = test1
		else:
			url = test2              
		response = HtmlResponse(url='http://msdn.microsoft.com/en-us/library/gg145045(v=vs.110).aspx',
			body=open('./tests/data/dotnet_ienumerable.html').read())
		spider = DotNetSpider()
		result = spider.parse(response)

		item = result.next()
		#print '#########################' + unicode(item['path']) + '#####################################' 
                
                
 		if test == 1:
			
			self.assertEqual(item['name'], u'Comparer<T> Properties')
			self.assertEqual(item['url'], 'gg145045(v=vs.110).aspx')
			self.assertIsNotNone(item['content'])
			self.assertEqual(item['path'], [u'.NET Framework 4.5 and 4.6 Preview', u'.NET Framework Class Library', u'System.Collections Namespaces', u'System.Collections.Generic', u'Comparer(T) Class', u'Comparer(T) Properties'])
			#self.assertEqual(len(list(result)), 24)
		if test == 2:
			print '#########################' + unicode(item['name']) + '#####################################'
			self.assertEqual(item['name'], u'.NET Framework Class Library')
			self.assertEqual(item['url'], 'gg145045(v=vs.110).aspx')
			self.assertIsNotNone(item['content'])
			self.assertEqual(item['path'], [])
			#self.assertEqual(len(list(result)), 24)

