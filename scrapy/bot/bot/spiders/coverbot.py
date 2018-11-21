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
		#url = "https://www2.hm.com/en_us/men/products/jeans/skinny.html?sort=stock&image-size=small&image=model&offset=0&page-size=72"
		#url = "https://www2.hm.com/en_us/men/products/jeans/super-skinny.html?sort=stock&image-size=small&image=stillLife&offset=0&page-size=36"
		#url = "https://www2.hm.com/en_us/men/products/jeans/straight-leg.html"
		url = "https://www.kohls.com/catalog/mens-straight-jeans-bottoms-clothing.jsp?CN=4294723349+4294737080+4294719454+4294719807+4294719810&icid=menjeans-VN1-straight&pfm=browse-pdp-breadcrumb%20p13n_control%20visual%20nav&kls_sbp=77952038899920252860576992828139209166"

		yield scrapy.Request(url, self.parse)

	
	
	def parse(self, response): 
		count = 0
		#for image in response.css('body main div.sidebar-plus-content ul img::attr(data-altimage)').extract():	
		for image in response.css("body div.pmpSearch_rightPanel ul a img::attr(src)").extract():
			count = count+1
			if (count % 2 != 0):
				add = "https:"
				image = add + image
				print image
				print count
				yield ImgData(image_urls=[image])
