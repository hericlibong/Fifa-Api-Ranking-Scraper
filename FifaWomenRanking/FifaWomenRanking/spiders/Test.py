import scrapy
import json


class TestSpider(scrapy.Spider):
    name = "Test"
    allowed_domains = ["fifa.com"]
    start_urls = ["https://inside.fifa.com/fifa-world-ranking/women?dateId=ranking_20240614"]

    def parse(self, response):
        script_content = response.xpath("//script[contains(text(), 'date')]/text()").extract_first()
        date_list = json.loads(script_content)
        date_list = date_list['props']['pageProps']['pageData']['ranking']['dates']
        print(date_list)
