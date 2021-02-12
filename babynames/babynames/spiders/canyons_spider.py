import scrapy

# globals for debugging
a = 0
b = 0
c = 0
d = 0
e = 0


class CanyonsSpider(scrapy.Spider):
    name = "Canyons"
    start_urls = ["https://www.math.utah.edu/~sfolias/canyontales/canyonames/"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 " \
                 "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    def parse(self, response):
        global a, b, c, d, e
        for canyon_name in response.xpath(
                '//table[@class="cyname"]//tr//td[1]//text()').getall()[:-75]:
            canyon_name = canyon_name.strip()
            if canyon_name == 'AKA':
                b += 1
                continue
            if canyon_name == '&':
                c += 1
                continue
            if canyon_name == '':
                d += 1
                continue
            if canyon_name[-1] == ',':
                a += 1
                continue
            if canyon_name[0].isalpha() and canyon_name[0].islower():
                e += 1
                continue
            yield {
                'canyon': canyon_name,
            }
        print(a, b, c, d, e)
