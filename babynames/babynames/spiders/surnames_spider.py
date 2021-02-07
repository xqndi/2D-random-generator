import scrapy


class SurnamesSpider(scrapy.Spider):
    name = "Surnames"
    start_urls = ["https://www.nrscotland.gov.uk/statistics-and-data/"
                  "statistics/statistics-by-theme/vital-events/births/"
                  "popular-names/archive/100-most-common-surnames"]

    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 " \
                 "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def parse(self, response):
        iterator = -1
        for row in response.xpath('//*[@class="no-border"]//tbody/tr'):
            iterator += 1
            if iterator == 0:
                continue

            name_one_raw = row.xpath('td[2]//text()').extract_first()
            name_two_raw = row.xpath('td[6]//text()').extract_first()

            name_one_cleaned = name_one_raw[5:]
            name_two_cleaned = name_two_raw[5:]
            yield {
                'surname': name_one_cleaned,
            }
            yield {
                'surname': name_two_cleaned,
            }
            print(iterator)
            # get the first 50 name-pairs
            if iterator == 50:
                return
