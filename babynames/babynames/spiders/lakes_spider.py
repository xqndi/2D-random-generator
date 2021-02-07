import scrapy


class LakesSpider(scrapy.Spider):
    name = "Lakes"
    start_urls = ["https://tpwd.texas.gov/fishboat/fish/recreational/lakes/lakelist.phtml"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 " \
                 "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def parse(self, response):
        for lake_name in response.xpath('//ul//li//a//text()').getall()[177:-40]:
            if lake_name[0] == " ":
                lake_name = lake_name[1:]
            if lake_name[-1] == " ":
                lake_name = lake_name[:-1]
            yield {
                'lake': lake_name,
            }
            print(lake_name)
