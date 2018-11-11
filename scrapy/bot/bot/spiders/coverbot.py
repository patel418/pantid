'''from bot.items import BotItem
import datetime
import scrapy
import re

class Bot(scrapy.Spider):
	name = "pant-pic-find"
	def start_requests(self):
		urls = [
		"https://www.zara.com/us/en/man-jeans-slim-l675.html?v1=1079309",
		#"https://www.zara.com/us/en/man-jeans-regular-l671.html?v1=1079307",
		#"https://www.zara.com/us/en/man-jeans-skinny-l673.html?v1=1079308"
		#http://quotes.toscrape.com/page/1/'
		]
		for url in urls:
            		yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		print response.url, response.body
		#url = response.css("div.refineCol ul li").xpath("a[contains(., 'TIME U.S.')]")
'''

import scrapy
import re
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector 
class Bot(scrapy.Spider): 
	name = "pant-pic-find" 
	src_extractor = re.compile('src="([^"]*)"')
	tags_extractor = re.compile('alt="([^"]*)"')
	# Define the regex we'll need to filter the returned links
	url_matcher = re.compile('^https:\/\/www\.zara\.com\/us/en') 
	# Create a set that'll keep track of ids we've crawled
	crawled_ids = set()
	def start_requests(self):
		url = "https://www.zara.com/us/en/man-jeans-slim-l675.html?v1=1079309"
		#url = "https://www.pexels.com/"
		yield scrapy.Request(url, self.parse)

	'''def parse(self, response):
		body = Selector(text=response.body) 
		link_extractor = LinkExtractor(allow=PexelsScraper.url_matcher) 
		next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]
		# Crawl the filtered links 
		for link in next_links:
			yield scrapy.Request(link, self.parse)'''
	def is_extracted(self, url):
	# Image urls are of type: https://www.pexels.com/photo/asphalt-blur-clouds-dawn-392010/
		#print ("***url about to be split: %s " % (url))
		#print url.split('/')
		#print ("THIS IS THE ID: %s" % (((url.split('/')[-1]).split('-')[-1]).split('.')[0]))
		
		id1 = ((url.split('/')[-1]).split('-'))#[-1]).split('.')[0]))
		#print id1
		#What i am doing wrong is that it is coming in one at a time so i must filter first and take it only if it is man and jeans
		
		#id1 = id1[-1].split('.')[0]
		if id1[0] == "man" and id1[1] == "jeans":
			#print id1
			id1 = id1[-1].split('.')[0]
			if id1 not in Bot.crawled_ids:
				Bot.crawled_ids.add(id1)
				return False
		return True

	def parse(self, response): 
		body = Selector(text=response.body) 
		print ("body: %s" % (body))
		images = body.css('img.product-media _img_imageLoaded').extract() 
		
		print ("images: %s" % (images))
		
		# body.css().extract() returns a list which might be empty 

		for image in images: 
			img_url = Bot.src_extractor.findall(image)[0] 
			tags = [tag.replace(',', '').lower() 
			for tag in Bot.tags_extractor.findall(image)[0].split(' ')] 
			print img_url, tags 
			print "hello"
		link_extractor = LinkExtractor(allow=Bot.url_matcher) 
		next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)] 
		# Crawl the filtered links 
		for link in next_links: 
			yield scrapy.Request(link, self.parse)
	'''
	def start_requests(self):
        	urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        	]
        	for url in urls:
            		yield scrapy.Request(url=url, callback=self.parse)

    	def parse(self, response):
       		print ("response url: %s " % (response.url))
		page = response.url.split("/")#[-2]
        	print page
		#print ("page: %s" % (page))
		filename = 'quotes-%s.html' % page
        	with open(filename, 'wb') as f:
            		f.write(response.body)
        	self.log('Saved file %s' % filename)'''
