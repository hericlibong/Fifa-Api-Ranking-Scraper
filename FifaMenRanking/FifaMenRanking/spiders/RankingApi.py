import scrapy
import json
from datetime import datetime


class RankingapiSpider(scrapy.Spider):
    name = "RankingApi"
    allowed_domains = ["fifa.com"]
    start_urls = ["https://inside.fifa.com/fifa-world-ranking/men?dateId=id14443"]

    def parse(self, response):
        script_content = response.xpath("//script[contains(text(), 'date')]/text()").extract_first()
        if script_content:
            try :
                date_list = json.loads(script_content)
                date_list = date_list['props']['pageProps']['pageData']['ranking']['dates']
                for year_data in date_list:
                    for date_item in year_data['dates']:
                        url = f"https://inside.fifa.com/api/ranking-overview?locale=en&dateId={date_item['id']}"
                        date_iso = date_item ['iso']
                        date_formatted = datetime.strptime(date_iso, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                        yield scrapy.Request(url=url, callback=self.parse_ranking_data, meta={'date':date_formatted})
            except(ValueError, KeyError) as e:
                self.logger.error(f"Erreur lors de l'analyse des dates: {e}")
        else:
            self.logger.warning("Script content est vide ou non trouvé")

    def parse_ranking_data(self, response):
        try:
            data = json.loads(response.body)
            base_url = "https://inside.fifa.com"
            for ranking_data in data['rankings']:
                yield {
                    "date": response.meta['date'],
                    "country": ranking_data['rankingItem']['name'],
                    "rank": ranking_data['rankingItem']['rank'],
                    "previous_rank": ranking_data['rankingItem']['previousRank'],
                    "total_points": ranking_data['rankingItem']['totalPoints'],
                    "previous_points": ranking_data['previousPoints'], 
                    "flagUrl": ranking_data['rankingItem']['flag']['src'],  
                    "countryUrl": base_url + ranking_data['rankingItem']['countryURL'],
                    "conf": ranking_data['tag']['text']      
                }
        except(ValueError, KeyError) as e:
            self.logger.error(f"Erreur lors de l'analyse des données de classement: {e}")



