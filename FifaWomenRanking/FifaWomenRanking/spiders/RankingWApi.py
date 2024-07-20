import scrapy
import json
from datetime import datetime


class RankingwapiSpider(scrapy.Spider):
    name = "RankingWApi"
    allowed_domains = ["fifa.com"]
    start_urls = ["https://inside.fifa.com/fifa-world-ranking/women?dateId=ranking_20240614"]

    def parse(self, response):
        script_content = response.xpath("//script[contains(text(), 'date')]/text()").extract_first()
        if script_content:
            try :
                date_list = json.loads(script_content)
                date_list = date_list['props']['pageProps']['pageData']['ranking']['dates']
                for year_date in date_list:
                    for date_item in year_date['dates']:
                        url = f"https://inside.fifa.com/api/ranking-overview?locale=en&dateId={date_item['id']}"
                        date_iso = date_item['iso']
                        date_formatted = datetime.strptime(date_iso, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                        yield scrapy.Request(url=url, callback=self.parse_ranking, meta={'date': date_formatted})
            except(ValueError, KeyError) as e:
                self.logger.error(f"Erreur lors de l'analyse des dates: {e}")
        else:
            self.logger.warning("Pas de contenu script trouvé")        

    def parse_ranking(self, response):
        try:
            data = json.loads(response.body)
            base_url = "https://inside.fifa.com"
            for ranking_data in data['rankings']:
                yield {
                    "date": response.meta['date'],
                    "country": ranking_data['rankingItem']['name'],
                    "rank":ranking_data['rankingItem']['rank'],
                    "total_points": ranking_data['rankingItem']['totalPoints'],
                    "previous_points": ranking_data['previousPoints'],
                    "flagUrl": ranking_data['rankingItem']['flag']['src'],
                    "countryUrl": base_url + ranking_data['rankingItem']['countryURL'],
                    "conf": ranking_data['tag']['text'],
                }
        except(ValueError, KeyError) as e:
            self.logger.error(f"Erreur lors de l'analyse du classement: {e}")
