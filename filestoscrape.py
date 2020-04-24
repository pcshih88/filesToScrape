import scrapy
from scrapy.loader import ItemLoader
from course2_projects.books_to_scrape.books_to_scrape.items import FilesToScrapeItem

class FilestoscrapeSpider(scrapy.Spider):
    name = 'filestoscrape'
    allowed_domains = ['bitsavers.org']
    start_urls = ['http://bitsavers.org/pdf/sony/floppy']

    def parse(self, response):
        for pdffile in response.css('a[href$=".pdf"]'):
            loader = ItemLoader(item=FilesToScrapeItem(), selector=pdffile)
            relative_url = pdffile.xpath('.//@href').get()
            absolute_url = response.urljoin(relative_url)
            loader.add_value('file_urls', absolute_url)
            loader.add_xpath('file_name', './/text()')
            yield loader.load_item()