import scrapy


class NamesSpider(scrapy.Spider):
    name = "Names"
    start_urls = ["https://www.ssa.gov/oact/babynames/decades/century.html"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 " \
                 "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def parse(self, response):
        data = response.css('td::text').getall()
        for item in data:
            is_name = True
            for char in item:
                if char.isdigit():
                    is_name = False
            if is_name:
                print(type(item))
                yield {'name': item}
