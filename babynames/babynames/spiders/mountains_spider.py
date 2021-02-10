import scrapy


class MountainsSpider(scrapy.Spider):
    name = "Mountains"
    start_urls = ["http://www.simonstewart.ie/list/irish_mountains_height.htm"]

    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 " \
                 "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def parse(self, response):

        for row in response.xpath('//table[@bgcolor="#E6DDDB"]//tbody//tr'):

            mountain_name = row.xpath('td[2]//text()').extract_first()
            if mountain_name is None:
                break

            yield {
                'mountain': mountain_name,
            }
