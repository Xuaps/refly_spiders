Collaborate
===========
You can collaborate creating new spiders for reference not included in refly.


*Creating your own spider*

All the spiders are based on [Scrapy](http://doc.scrapy.org/) crawling framework, specifically, inheriting from [scrapy.crawler](http://doc.scrapy.org/en/latest/topics/api.html?highlight=crawler#module-scrapy.crawler).Using [xpath](http://www.w3schools.com/xpath/xpath_functions.asp) to extract info from documentation

**Understanding the spider**

The structure of every reference is the following:

* _name_
* _docset_ (name of the documentation to scrape, PHP, JavaScript, Ruby, etc...)
* _type_ (function, method, constant, etc...)
* _content_
* _parent_(reference parent, path)
* _uri_, a friendly url composed by docset + parent + name


**Creating a class:**
import spiderbase.py and make your class inherit from spiderbase


**Configure the spider:**

Add the following global configuration to your spider.

* _name_, the name of the reference to import (Javascript, Ruby, PHP, etc)
* _excluded_path_  a list of items that will be ignore from the path
* _rules_, a set of rules, for defining the links to be processed through [LinkExtractor](http://doc.scrapy.org/en/latest/topics/link-extractors.html) class
* _start_urls_, the initial urls.
* _author_info_, the information in html format about the original author of the documentation. it will be append at the end every reference.
* _baseuri_, the root uri of the processed references (if path does not contain docset, it shoud be added here)
* _xpathname_, xpath expression to extract the title of the reference, tipically, “Printf”, “Math.sqrt”, etc.
* _xpathalias_, name of the reference that will be used in the path(in most cases it matches with the name of the reference)
* _xpathcontent_, the content of the reference.
* _xpathpath_, to extract the path to the parent reference

It is necessary to define a method call _resolveType_ which extract the type from the reference.

At least, call the __init__ of SpiderBase.


SpiderBase contains five methods to extract the different piece of information from the document. It is possible and in fact must be overwritten those method that require some special process beyond the simple extraction from the document with xpath.

* _getName_
* _getAlias_
* _getUrl_
* _getContent_
* _getPath_
* _appendAuthorInfo_


Inform about Issues
===================

We appreciate a lot that Chineese invent powder, however we never remember those who tried to put fire on it, simply to see the result, and that was a task as important as the invention itself. That's why we appreciate so much your collaboration in the form of try and inform about the result. You can do it through [refly_spiders issues](https://github.com/Xuaps/refly_spiders/issues)
