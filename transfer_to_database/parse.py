import requests
import re
from bs4 import BeautifulSoup

url = "https://www.dsndsht23.com/thread-86279-1-1.html"
def generate_dict():
	response = requests.get(url)
	if response.status_code == 200:
		html = response.text
		soup = BeautifulSoup(html, "lxml")
		item = soup.find("td", class_="t_f")
		magnet = soup.find("ol").text
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
			"UUID": UUID,
			"Atress":pre_list[1],
			"Size":pre_list[2],
			"Censored or not":pre_list[3],
			"Magnet":magnet
			}
		print(data)
	else:
		print(response.status_code, "\s", "error.")

generate_dict()