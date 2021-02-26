import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import SabankItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class SabankSpider(scrapy.Spider):
	name = 'sabank'
	start_urls = ['https://www.sabank.hr/obavijesti']

	def parse(self, response):
		post_links = response.xpath('//div[@class="col-sm-9"]//p[@class="paragrav-poslovnice"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):

		date = "Not stated"
		title = response.xpath('//h1//text()').get()
		content = response.xpath('//div[@class="col-sm-12"]/p//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=SabankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
