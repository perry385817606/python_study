import json
import requests
from bs4 import BeautifulSoup

def get_repositories_by_bs4(url, cookie):
	response = requests.get(url, cookies=cookie)
	text = response.text
	soup = BeautifulSoup(text, 'lxml')
	res = soup.find_all('div', attrs = {'class': 'listgroup-item simple public fork js-collab-repo'})
	result = []
	for item in res:
		name = item.find('a', class_ = 'mr-1').text.split('/')[1]
		size = item.find('small').get_text()
		link = 'https://github.com' + item.find_all('a')[1]['href']
		# yield(name, size, link)
		yield {
			'name': name,
			'size': size,
			'link': link,
		}

if __name__ == '__main__':
	f = open('cookie.txt')
	cookie = json.loads(f.read())
	print(cookie)
	Repositories_URL = "https://github.com/settings/repositories"
	for item in get_repositories_by_bs4(Repositories_URL, cookie):
		print(item)
