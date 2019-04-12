import requests
import re
import pymongo
from hashlib import md5
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from config import *


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_onepage(mainurl):
	response = requests.get(mainurl)
	if response.status_code == 200:
		return response.text

def parse_onepage(html):
	soup = BeautifulSoup(html, "lxml")
	items = soup.find_all("tbody", attrs={"id":re.compile(r"normalthread_\d+")})
	urls = []
	for item in items:
		soup = BeautifulSoup(str(item), "lxml")
		url = soup.find("a", class_="s xst")["href"]
		urls.append(url)
	return urls

#下载图片
def get_img(url,UUID):
    response = requests.get(url)
    html = response.text
    pattern = re.compile('class="zoom"\sfile="(.*?)"', re.S)
    items = re.findall(pattern, html)
    for item in items:
        r = requests.get(str(item))
        if r.status_code == 200:
            open(UUID,'wb').write(r.content)

def generate_dict(url):
	response = requests.get(url)
	if response.status_code == 200:
		html = response.text
		soup = BeautifulSoup(html, "lxml")
		item = soup.find("td", class_="t_f")
		try:
			magnet = soup.find("ol").text
		except:
			magnet = None
		description = soup.find("span", id="thread_subject").text
		patterns = re.compile('(.*?)\s')
		UUID = re.findall(patterns, description)[0]
		elements = item.text.split('\n')
		pre_list = []
		for i in elements:
			if "影片名称" in i:
				pre_list.append(i.lstrip("【影片名称】：").strip("\r"))
			if "出演女优" in i:
				pre_list.append(i.lstrip("【出演女优】：").strip("\r"))
			if "影片大小" in i:
				pre_list.append(i.lstrip("【影片大小】：").strip("\r"))
			if "是否有码" in i:
				pre_list.append(i.lstrip("【是否有码】").lstrip("：").strip("\r"))
		data = {
			"Title":pre_list[0],
			"UUID":UUID,
			"Actress":pre_list[1],
			"Size":pre_list[2],
			"Censored or not":pre_list[3],
			"Magnet":magnet
			}
		return data
	
	else:
		print(response.status_code, "\s", "error.")


def save_to_mongo(data):
	if db[MONGO_TABLE].insert(content):
		print('Save to MongoDB successfully!', content)
		return True
	else:
		return False


def main():
	dict_list = []
	startpage = input("startpage:")
	lastpage = input("lastpage:")
	for i in range(int(startpage), int(lastpage)+1):
		mainurl = 'https://www.dsndsht23.com/forum-103-{}.html'.format(i)
		get_onepage(mainurl)
		html = get_onepage(mainurl)
		urls = parse_onepage(html)
		for url in urls:
			url = "https://www.dsndsht23.com/" + url
			data = generate_dict(url)
			print(data["UUID"], "is down.")
			dict_list.append(data)
	return dict_list
       
if __name__ == '__main__':
	contents = main()
	for content in contents:
		save_to_mongo(contents)