import requests

headers = {
	'authority': 'www.flightradar24.com',
	'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Yandex";v="22"',
	'dnt': '1',
	'sec-ch-ua-mobile': '?0',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.3.850 Yowser/2.5 Safari/537.36',
	'sec-ch-ua-platform': '"Windows"',
	'accept': '*/*',
	'sec-fetch-site': 'same-origin',
	'sec-fetch-mode': 'cors',
	'sec-fetch-dest': 'empty',
	'referer': 'https://www.flightradar24.com/1059/2ad69e49',
	'accept-language': 'ru,en;q=0.9'
}

def request(endpoint, params = None, proxies = None):
	return requests.get(endpoint, headers = headers, proxies = proxies, params = params)