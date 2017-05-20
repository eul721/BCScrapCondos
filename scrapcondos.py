import scrapy
import pipelines

class BCCondosScrapper(scrapy.Spider):
    name = 'condospider'
    custom_settings = {
        'ITEM_PIPELINES' : {
            'pipelines.JsonWithEncodingPipeline': 1
        }
    }

    start_urls = ['http://bccondos.net/buildingcondoscity-VVW']

    def parse(self, response):
        for url in response.css('div.module table td a::attr(href)'):
            yield scrapy.Request(response.urljoin(url.extract()), self.parse_condos)

    def parse_condos(self, response):
        address = response.css('div.building-summary div.bld_des h2.bld-address::text').extract_first().strip()
        description = response.css('div.mainCol_div div.module p::text').extract_first().strip()
        neighborhood = response.css('div.building-summary div.bld_des h2.bld-address a.bld-number::text').extract_first().strip()

        yield {
            'addr' : address,
            'desc' : description,
            'neighborhood' : neighborhood
        }
