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
		#url = "https://www.levi.com/US/en_US/clothing/men/jeans/c/levi_clothing_men_jeans/facets/feature-fit/straight"
		url = "https://www.buckle.com/mens/jeans/leg-opening:bootcut?page=6"
		yield scrapy.Request(url, self.parse)

	
	
	def parse(self, response): 
		count = 0
		#for image in response.css("body div#root div.row_Z2vyUxT div.block_19rjgc img::attr(src)").extract():
		for image in response.css("body div#wrapper main#content div.bottom-section a img::attr(src)").extract():
			count = count+1
			#if (count % 2 != 0):
				#add = "https:"
				#image = add + image
			print image
			print count
			yield ImgData(image_urls=[image])
