#python3.x
#date: 2018-4-11
# http://www.cnblogs.com/zhaof/p/7284312.html
# http://www.cnblogs.com/zhaof/category/858301.html

import re
import requests
from bs4 import BeautifulSoup
import xlwt


def get_github_html(url):
    '''
    这里用于获取登录页的html，以及cookie
    :param url: https://github.com/login
    :return: 登录页面的HTML,以及第一次的cooke
    '''

    response = requests.get(url)
    first_cookie = response.cookies.get_dict()
    return response.text, first_cookie


def get_token(html):
    '''
    处理登录后页面的html
    :param html:
    :return: 获取csrftoken
    '''

    soup = BeautifulSoup(html, 'lxml')
    res = soup.find('input',attrs={'name': 'authenticity_token'})
    token = res['value']
    return token

def github_login(url, token, cookie, username, password):
	data = {
		'commit': 'Sign in',
		'utf8': '✓',
		'authenticity_token': token,
		'login': username, 
		'password': password,
	}

	response = requests.post(url, data=data, cookies=cookie)
	# print(response.status_code)
	cookie = response.cookies.get_dict()
	return cookie

def get_repositories_by_regexp(url, cookie):
	response = requests.get(url, cookies=cookie)
	text = response.text
	pattern = re.compile('<div.*?class="listgroup.*?>.*?<a.*?class="mr-1".*?href=".*?">(.*?)</a>' +
						 '.*?<small>(.*?)</small>' + 
						 '.*?<span.*?Forked from.*?<a.*?href="(.*?)">(.*?)</a>', re.S
		)

	res = re.findall(pattern, text)
	result = []
	for item in res:
		name = item[0].split('/')[1]
		size = item[1]
		link = 'https://github.com' + item[2]
		# print( '{name}\t{size}\t{link}'.format(name=name, size=size, link=link) )
		result.append({'name': name, 'size': size, 'link': link})

	keys = ['name', 'size', 'link']
	return keys, result


def get_repositories_by_bs4(url, cookie):
	response = requests.get(url, cookies=cookie)
	text = response.text
	soup = BeautifulSoup(text, 'lxml')
	res = soup.find_all('div', attrs = {'class':'listgroup-item simple public fork js-collab-repo'})
	result = []
	for item in res:
		name = item.find('a', class_ = 'mr-1').text.split('/')[1]
		size = item.find('small').get_text()
		link = 'https://github.com' + item.find_all('a')[1]['href']
		# yield(name, size, link)
		# yield {
		# 	'name': name,
		# 	'size': size,
		# 	'link': link,
		# }
		result.append({'name': name, 'size': size, 'link': link})
	keys = ['name', 'size', 'link']
	result = sorted(result, key=lambda x: x.get('size'))
	return keys, result

def save_to_excel(keys, result, output):
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('repos')
	# head_style = xlwt.easyxf('font: blod on')
	head_style = xlwt.easyxf('font: bold on')
	nrows = len(result)  # 获取行数
	ncols = len(keys)  # 获取列数
	
	#写入表头
	for i in range(ncols):
		ws.write(0, i, keys[i], head_style)

	# 写入内容
	index = 1
	for item in result:
		for j in range(ncols):
			ws.write(index, j, item.get(keys[j]))
		index += 1

	try:
		wb.save(output)
	except:
		print('\n{0} 写入失败!'.format(output))
	else:
		print('\n{0} 写入成功!'.format(output))


def main():
	html, cookie = get_github_html(Base_URL)
	# print(cookie)
	token = get_token(html)

	cookie = github_login(Login_URL, token, cookie, username, password)
	# keys, res = get_repositories_by_regexp(Repositories_URL, cookie)

	for item in get_repositories_by_bs4(Repositories_URL, cookie)[1]:
		print(item)

	keys, result = get_repositories_by_bs4(Repositories_URL, cookie)
	save_to_excel(keys, result, output)

if __name__ == '__main__':
	username = '用户名'
	password = '密码'

	proxies = {
	    "https": "https://xxx.com:8080",
	    "http": "http://xxx:8080",
	}

	Base_URL = "https://github.com/login"
	Login_URL = "https://github.com/session"
	Repositories_URL = "https://github.com/settings/repositories"
	output = 'github_respos.xls'

	main()