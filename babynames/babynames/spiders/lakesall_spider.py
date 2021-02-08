import scrapy

next_letter = "A"


class LakesAllSpider(scrapy.Spider):
    name = "LakesAll"
    start_urls = ["https://wldb.ilec.or.jp/Search/Lakename/A"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 " \
                 "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def parse(self, response):
        global next_letter
        iterator = -1
        for row in response.xpath('//*[@class="list"]//tbody//tr'):
            iterator += 1
            if iterator == 0:
                continue

            lake_name = row.xpath('td[2]//text()').extract_first()
            yield {
                'lake_name': lake_name,
            }
        next_letter = chr(ord(next_letter) + 1)
        path_str = '//option[text()="' + next_letter + '"]//@value'
        next_page = response.xpath(path_str).get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


