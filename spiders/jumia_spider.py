import scrapy
from pathlib import Path


class JumiaSpider(scrapy.Spider):
    name = "jumia"

    def start_requests(self):

        url = "https://www.jumia.com.ng/smart-tvs/hisense/"
        
        yield scrapy.Request(url = url, callback = self.parse)
    
    def parse(self, response):

        self.logger.debug(response.url)

        
        links = response.xpath('//*[@id="jm"]/main/div[2]/div[3]/section/div[1]//@href').extract()
        filename = 'jumia_hisenses.html'
        with open (filename, 'w') as f:
           for link in links:
               f.write('{} \n'.format(link))
