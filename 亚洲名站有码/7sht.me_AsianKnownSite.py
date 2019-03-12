import requests
import re
import pymongo
from bs4 import BeautifulSoup
from config import *



client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

class TorrentSpider():
	def __init__(self):
		self.base_url = "https://www.dsndsht23.com/forum-104-{}.html"
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
		}
		
	def get_url_list(self):
		urllist = []
		for i in range(1,12):
			urllist.append(self.base_url.format(i))

		return urllist

	def parse_index_page(self, url):
		response = requests.get(url, headers=self.headers)
		if response.status_code == 200:
			html = response.text		
			soup = BeautifulSoup(html, "lxml")
			items = soup.find_all("tbody", attrs={"id":re.compile(r"normalthread_\d+")})
			
			urls = []
			for item in items:
				soup = BeautifulSoup(str(item), "lxml")
				url = "https://www.dsndsht23.com/" + soup.find("a", class_="s xst")["href"]
				urls.append(url)
			return urls
		else:
			print(response.status_code, " Failure to get index page.")

	def parse_detailed_page(self, one_url):
		response = requests.get(one_url,headers=self.headers)
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
			try:
				UUID = re.findall(patterns, description)[0]
			except:
				UUID = description
			elements = item.text.split('\n')
			pre_list = []
			for i in elements:
				try:
					if "影片名称"  in i:
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
				except:
					data = None
			print(data)
			return data

	def save_to_mongo(self, data):
		try:
			if db[MONGO_TABLE].insert(data):
				print(data)
				return True
			else:
				return False
		except:
			pass

	def run(self):
		urllist = self.get_url_list()
		for url in urllist:
			urls = self.parse_index_page(url)
			for one_url in urls:
				data = self.parse_detailed_page(one_url)
				self.save_to_mongo(data)



TorrentSpider().run()