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
	url_matcher = re.compile('^https:\/\/www\.zara\.com\/us\/en\/') 
	# Create a set that'll keep track of ids we've crawled
	crawled_ids = set()
	def start_requests(self):
		url = "https://www.zara.com/us/en/man-jeans-slim-l675.html?v1=1079309"
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
		id = int(url.split('/')[-2].split('-')[-1]) 
		if id not in Bot.crawled_ids:
			Bot.crawled_ids.add(id) 
			return False
		return True

	def parse(self, response): 
		body = Selector(text=response.body) 
		images = body.css('img.image-section__image').extract() 
		# body.css().extract() returns a list which might be empty 
		for image in images: 
			img_url = Bot.src_extractor.findall(image)[0] 
			tags = [tag.replace(',', '').lower() 
			for tag in Bot.tags_extractor.findall(image)[0].split(' ')] 
			print img_url, tags 
		link_extractor = LinkExtractor(allow=Bot.url_matcher) 
		next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)] 
		# Crawl the filtered links 
		for link in next_links: 
			yield scrapy.Request(link, self.parse)

