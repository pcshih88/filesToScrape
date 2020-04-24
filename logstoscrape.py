import scrapy
from scrapy.loader import ItemLoader
from course2_projects.books_to_scrape.books_to_scrape.items import FilesToScrapeItem

class LogstoscrapeSpider(scrapy.Spider):
    name = 'logstoscrape'
    allowed_domains = ['lit-thicket-55904.herokuapp.com']
    start_urls = ['https://lit-thicket-55904.herokuapp.com/logs/default/gdp_debt_xpth']

    def parse(self, response):
        for logentry in response.xpath('//td/a'):
            loader = ItemLoader(item=FilesToScrapeItem(), selector=logentry)
            relative_url = logentry.xpath('.//@href').get()
            # print("The relative url is: " + relative_url)
            absolute_url = response.urljoin(relative_url)
            # print("The absolute url is: "+ absolute_url )
            loader.add_value('file_urls', absolute_url)
            loader.add_xpath('file_name', './/text()')
            yield loader.load_item()