import scrapy


class SlovakdictSpider(scrapy.Spider):
    name = "slovakdict"

    def start_requests(self):
        yield scrapy.Request(url='https://slovnik.aktuality.sk/pravopis/vsetky/a/1/', callback=self.parse)

    def parse(self, response):
        next_page_url = response.css("#nav a.sipkar::attr(href)").get()

        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
        else:
            next_letter_url = response.css("a.vybrane + *::attr(href)").get()
            yield scrapy.Request(response.urljoin(next_letter_url))

        words = dict()
        for idx, word in enumerate(response.css('#reg-zoznam li > a::text').getall()):
            words[idx] = word

        yield words
