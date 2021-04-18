from Avito.celery import app
from .models import *
import requests
import cfscrape
from bs4 import BeautifulSoup as bs
def get_html(region: str, query: str) -> int:

	url = 'https://www.avito.ru/{0}?q={1}'.format(region, query)

	session = requests.Session()
	session.headers = {
			'scheme': 'https',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
			'cache-control': 'max-age=0',
			'sec-fetch-dest': 'document',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-site': 'none',
			'sec-fetch-user': '?1',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
		}
	result = cfscrape.create_scraper(sess=session)
	response = result.get(url)
	if response.status_code == 404:
		return 0
	else:
		sp = bs(response.text, 'html.parser')
		div_class = sp.find('div', class_='page-title-root-3uh27 js-page-title')
		count = div_class.find('span', class_='page-title-count-1oJOc')
		return int(count.string.replace(' ', ''))

@app.task
def counter():
	for i in Query.objects.all():
		count = get_html(i.region, i.search_query)
		temp = Time(count=count, query=i)
		temp.save()
		i.qr.add(temp)
