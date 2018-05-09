import scrapy
import json
from scrapy.selector import Selector

class newsSpider(scrapy.Spider):
	name= "news"
	def start_requests(self):
		start_url= [
			'http://cafebiz.vn/vao-cptpp-nguoi-viet-se-duoc-mua-sua-ngoai-gia-re-20180314082932836.chn'
		]
		for url in start_url:
			yield scrapy.Request(url= url, callback= self.parse)


	def parse(self,response):
		contents=[]
		contents= response.css('div.detail-content *::text').extract()
		j=i=0
		while i < len(contents):
			print i
			print len(contents)
			print contents[i]
			contents[i] = contents[i].strip('\r\n')
			if contents[i].strip()=='':
				del contents[i]
				i-=1
			i+=1
		data = yield {
			'origin': 'group 9',
			'url': response.request.url,
			'title': response.css("h1.title::text").extract_first().strip('\r\n'),
			'category': response.css("span.cat a::text").extract_first().strip('\r\n'),
			'description': response.css("h2.sapo::text").extract_first().strip('\r\n'),
			'content': contents,
			'author': response.css("strong.detail-author::text").extract_first().strip('\r\n'),
			'date': response.css("div.timeandcatdetail span.time::text").extract_first().strip('\r\n'),
		}
		next_pages =response.css('ul.tinlienquan li a::attr(href)').extract()
		for next_page in next_pages:
			next_page = 'http://cafebiz.vn' + str(next_page) 
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)



		