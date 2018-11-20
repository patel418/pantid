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
from scrapy.item import Item
from bot.items import ImgData
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector 
class Bot(scrapy.Spider): 
	name = "pant-pic-find" 
	#src_extractor = re.compile('src="([^"]*)"')
	tags_extractor = re.compile('alt="([^"]*)"')
	# Define the regex we'll need to filter the returned links
	url_matcher = re.compile('^https:\/\/www\.zara\.com\/us/en') 
	# Create a set that'll keep track of ids we've crawled
	crawled_ids = set()
	def start_requests(self):
		#url = "https://www.zara.com/us/en/man-jeans-slim-l675.html?v1=1079309"
		url = "https://www2.hm.com/en_us/men/products/jeans.html"
		#url = "https://www.pexels.com/"
		yield scrapy.Request(url, self.parse)

	
	
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
		count = 0
		for image in response.css('body main div.sidebar-plus-content ul img::attr(data-altimage)').extract():	
			count = count+1
			add = "https:"
			image = add + image
			print count
			yield ImgData(image_urls=[image])
