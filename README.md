# Scraping Fifa men’s ranking with Scrapy and hidden API


## Collect the 1992–2023 Fifa rankings in seconds using the internal API of the Fifa website


![fifa picture](asset/fifa_picture.webp)


### Presentation

This repo proposes an approach to retrieving the Fifa men ranking using the hidden API of the Fifa website.
It is also an update of an article published on [Medium in April 2023](https://medium.com/@rico69/scraping-fifa-mens-ranking-with-scrapy-and-hidden-api-7799570b7737).

This script uses [Scrapy](https://scrapy.org/) and allows you to retrieve both the current ranking and the history in just a few seconds.

The Python version used is 3.12, but the program can run with at least 3.9


### Installation and use

#### Clone the Repository

First, clone the repository to your local machine:

```
git clone https://github.com/hericlibong/HIDDEN_API_FIFA_RANKING_MEN_SCRAPING.git
cd HIDDEN_API_FIFA_RANKING_MEN_SCRAPING

```

Set Up a Virtual Environment
Create a virtual environment to manage the dependencies:

### For Unix or MacOS

```
python3 -m venv venv
source venv/bin/activate
```

### For Windows

```
python -m venv venv
venv\Scripts\activate
```


### Install the Dependencies
### Install the required Python packages using pip:

```
pip install -r requirements.txt
```


### Run the Scrapy Spider
To start the scraping process, run the Scrapy spider:

```
scrapy crawl RankingApi -o fifa_rankings.json
scrapy crawl RankingApi -o fifa_rankings.csv
```







