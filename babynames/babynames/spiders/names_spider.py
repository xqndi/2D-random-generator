import scrapy

name_counter = 0


class NamesSpider(scrapy.Spider):
    name = "Names"
    start_urls = ["https://www.verywellfamily.com/top-1000-baby-boy-names-2757618"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 " \
                 "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def parse(self, response):
        global name_counter
        name_data = response.xpath('//ol//li//text()').getall()
        for item in name_data:
            name_counter += 1
            yield {
                'name': item
            }
        next_page = response.xpath('//div//a[@id="mntl-sc-block-featuredlink__link_1-0-1"]//@href').get()

        if next_page is not None and next_page != self.start_urls[0]:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        print(name_counter)
