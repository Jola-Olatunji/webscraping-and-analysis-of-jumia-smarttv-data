import scrapy
from scrapy import Request
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess


class JumiaSpider2(scrapy.Spider):

    name = 'jumia2'

    def start_requests(self):

        url = 'https://www.jumia.com.ng/smart-tvs/' 

        yield scrapy.Request(url = url, callback = self.parse2)


    def parse2(self, response):


        # extract all the product links on current page
        link_path = '//*[@id="jm"]/main/div[2]/div[3]/section/div[1]//@href'
        links = response.xpath(link_path).extract()
        

        # follow the lnks to the next parser
        for url in links:



            yield response.follow(url = url, callback = self.parse_page,
                                  meta={'dont_merge_cookies': True,'dont_filter' : True})

        next_page_href = response.xpath('//div[@class="pg-w -ptm -pbxl"]/a[6]/@href')
        next_page_url = response.urljoin(next_page_href.extract_first())


        
        if next_page_href is not None:
            yield Request(next_page_url, callback = self.parse2, meta={'dont_merge_cookies': True, 
                                                                       'dont_filter' : True} )
    
    def parse_page(self, response):

        #extract product details
        yield {
            'name' : response.xpath('//div[@class = "-fs0 -pls -prl"]/h1/text()').extract_first(),
            'brand' : response.xpath('//div[@class = "-pvxs"]/a[1]/text()').extract_first(),
            'price' : response.xpath('//div[@class = "-phs"]/div[3]/div/span/text()').extract_first(),
            'ratings' : response.xpath('//div[@class = "stars _s _al"]/text()').extract_first(),
            'specification' : response.xpath('//div[@class = "card-b -fh"]/div/ul//li/text()').extract(),
            'Seller_name' : response.xpath('//div[@class = "-hr -pas"]/p/text()').extract_first(),
            'seller_rating' : response.xpath('//div[@class = "-hr -pas"]/div/div/p/bdo/text()').extract_first(),
            'url': response.url
        }
    
process = CrawlerProcess(settings ={
    "FEEDS": {
        "jumia_tv_catalogues.json":{"format" : "json"}
    }
})

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s', 'level': 'logging.DEBUG'  })

process.crawl(JumiaSpider2)
process.start()


