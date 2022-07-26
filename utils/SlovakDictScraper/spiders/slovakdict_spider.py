import scrapy
import re


class SlovakdictSpider(scrapy.Spider):
    name = "slovakdict"

    def start_requests(self):
        yield scrapy.Request(url='https://slovnik.aktuality.sk/pravopis/vsetky/a/1/', callback=self.parse)

    def parse(self, response):
        filename = 'slovakdict.txt'
        words = list(filter(lambda word: re.search("^[^-().’! ]*$", word) and len(word) == 5,
                     response.css('#reg-zoznam li > a::text').getall()))

        fd = open(filename, "a", encoding="utf-8")
        for word in words:
            fd.write(f"{word}\n")
        fd.close()

        next_page_url = response.css("#nav a.sipkar::attr(href)").get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
        else:
            next_letter_url = response.css("a.vybrane + *::attr(href)").get()
            yield scrapy.Request(response.urljoin(next_letter_url))
