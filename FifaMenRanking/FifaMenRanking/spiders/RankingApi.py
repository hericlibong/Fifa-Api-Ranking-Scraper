import scrapy
import json


class RankingapiSpider(scrapy.Spider):
    name = "RankingApi"
    allowed_domains = ["fifa.com"]
    start_urls = ["https://inside.fifa.com/api/ranking-overview?locale=en&dateId=id14443"]

    def parse(self, response):
        data = json.loads(response.body)
        base_url = "https://inside.fifa.com"
        for ranking_data in data['rankings']:
            yield {
                "country": ranking_data['rankingItem']['name'],
                "rank": ranking_data['rankingItem']['rank'],
                "previous_rank": ranking_data['rankingItem']['previousRank'],
                "total_points": ranking_data['rankingItem']['totalPoints'],
                "previous_points": ranking_data['previousPoints'], 
                "flagUrl": ranking_data['rankingItem']['flag']['src'],  
                "countryUrl": base_url + ranking_data['rankingItem']['countryURL'],
                "conf": ranking_data['tag']['text']      

            }



