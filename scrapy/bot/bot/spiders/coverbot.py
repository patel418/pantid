import scrapy
import re
from scrapy.item import Item
from bot.items import ImgData
from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector 
class Bot(scrapy.Spider): 
	name = "pant-pic-find" 
	# Define the regex we'll need to filter the returned links
	# Create a set that'll keep track of ids we've crawled
	crawled_ids = set()
	def start_requests(self):
		url = "https://www.lordandtaylor.com/Men/Clothing/Jeans/Straight-Jeans/shop/_/N-4ztf5k?FOLDER%3C%3Efolder_id=2534374302023928&Nao=60"
		yield scrapy.Request(url, self.parse)

	
	
	def parse(self, response): 
		count = 0
		for image in response.css("body div#saksContainer div#saksBody div#product-container a img::attr(src)").extract():
			count = count+1
			print image
			print count
			yield ImgData(image_urls=[image])
