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
			'cookie': 'u=2kcjfp1o.ct1d8o.1lq7pnsr89500; buyer_selected_search_radius4=0_general; _ym_d=1603402841; _ym_uid=1592672365425194758; _ga=GA1.2.1546958479.1603402842; _fbp=fb.1.1603402842266.542066452; _gid=GA1.2.940613621.1605900214; showedStoryIds=51-50-49-48-47-46-45-43-41-42-39-32-30-25; lastViewingTime=1605902764969; __gads=ID=ab8a31d6bc70c8ba:T=1605902765:S=ALNI_MY792JBnBc7gDYRn-pikF0t1cJEJA; isCriteoSetNew=true; buyer_selected_search_radius2=0_job; __cfduid=d5c7264063ebc3eb54397647923cbc2021606045219; sessid=b100d8ad87e2e638db1a6ec03717086f.1606045219; _ym_isad=2; f=5.10a94bb89dd075604b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8b175a5db148b56e9bcc8809df8ce07f640e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0ac91e52da22a560f550df103df0c26013a7b0d53c7afc06d0bba0ac8037e2b74f92da10fb74cac1eab71e7cb57bbcb8e0f71e7cb57bbcb8e0f71e7cb57bbcb8e0f0df103df0c26013a93e76904ac7560d30c79affd4e5f1d11162fe9fd7c8e976756d999b8eea7c59691a22177a7e2e7505e61d702b2ac73f7cdd7d7007065d4e04e0f80e5b86a5ca5577c150a38e7a983979b78d3d9e0e11cc772035eab81f5e146b8ae4e81acb9fa46b8ae4e81acb9faf5b8e78c6f0f62a372f07604be87ef73dbdbb8e64632d0122da10fb74cac1eab2da10fb74cac1eabc98d1c3ab1f148dc193cc3161054d47da6ef565a9fc26059; _gcl_au=1.1.765876914.1606045273; buyer_laas_location=653240; buyer_selected_search_radius0=200; no-ssr=1; v=1606073192; _ym_visorc_34241905=b; _ym_visorc_419506=w; _ym_visorc_188382=w; buyer_location_id=653240; luri=sankt-peterburg; sx=H4sIAAAAAAACA52VzZaiShCE38X1LBIqgXTeRhJIsJQSC6y258y7T1TP0dvc5bhwocVX%2BRMR%2FDqUmxbiaC47zyTeKEa1FFI8%2FPx1eBx%2BHnoZtvL22fVkMYiKBWHyShJMSOzw49AffhY11UV1bKT8%2FePQrvU2yr164gkKZqYqIXD0L2R36zsO8dp%2B%2BKAmuDFQ0GBs5DnwN6Qraj4CWZy3y6krinMVLCZVnxgfMvonZF1kpH1M7TQ9w%2BXMpKZknCI6%2Bjdkk6ssC%2F98tvFI21UoGc5HSeTl3Xg7DWGM63Vy3qsI2jBJPmCM5hPRHikCZK96DNxv8w3FeeaYoqlF1n9BNuSAHPim6zRcryMeMCZii4LdvhsfXem7pRiec0zEWLf4PB%2FWlM%2FaHlkykNzQGuqqeFBIiSPEkQRno72Qy6X60Es5XcqIEtXnobBGkQgd%2BbRDSklZRFKcI41DUYqJZWrABjS%2BdblUVXFep3n1FkFR80IsBLElhjy%2BI0t2NZDyuVb3slzSYIGUclMs9m3j9VXLxmiZ87pZVQMT5oODBP2GHdKVWUTlqZ01POg0Jm8%2BxsghQCP%2B3XhRL6GIReeegZLCP0pwAsAasak9kr%2FW4641fyxde79vmYUyWNC8hhdytvZ8Km98nmK2IAcv8C36UBwKe%2BRfQ7piubnr%2Bd486oiVYkjeVCDOF5KXYXnEz88kuApbTgb15npV2Ef9jnRlXeX1FNTX59OxaWIeevQGmSA%2F0gs5rA2HWs99qwldMw5oJLMEo5HfVem4zI33H%2BvU1%2BYgXvNZQTlj8HlXOV79tNT9uBhlxRJzwggRWcIBl%2ByQRdMAWVc4V4TBwzVJEV8C%2FwRwX0g%2FdfXleHuuiDSyRFiMBxcO8nn%2FOyTKzBsvq62ny%2FjxgMtCDqGIviDPF%2FIsF%2FHt3XSDBQKBCij%2Bz4mFH%2FaN%2F0UOs8a5vT5nweXoKWWzsb09fh9pCevqTx368BEy94RvRRrDZN%2BrrKmSL0Om27DKhbdigsoD9u0lKdjvKls7PYfxcrwgU5DpACOnAwQgiOyde1z1tR7uxVVdf8QqPc57CmIwMr3dc%2BpP7Jqn9Y5znCD6EUJZbflm2c2yKr9iwz2xuLWaB39VBAJwmlPzP6VXw9nN%2Bjzd8kwiLs5vEkzc4Iv0P6LLcSnHtaH5weOGLXrcnsef8LZ6IW3je%2FfYZnQJVI6pJJy%2BZhm87voW1%2BS%2Bq2lpxuLh4hgJAoeO8wPq36Hu6HTsjl1Xt1XZDUdpq34oeqmpH4ae6rZou1PrpPnG5toR%2Ff79B3BGvNt%2BBwAA; dfp_group=13; abp=0; _ym_visorc_106253=w; buyer_from_page=main',
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