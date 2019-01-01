import requests
import pymongo
import os
from hashlib import md5 
from bs4 import BeautifulSoup
import re
from lxml import etree
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_onepage_url(start_url):
    response = requests.get(start_url).text
    return response

def parse_one_page(html, a):   
    pattern = re.compile('<tbody\sid="normalthread_(.*?)">', re.S)
    items = re.findall(pattern, html)
    for item in items:
        detail_url = 'https://54sadsad.com/thread-{}-1-{}.html'.format(item, a)
        urllist.append(detail_url)
    return urllist

def parse_detail_page(url):
    response_html = requests.get(url).text
    soup = BeautifulSoup(response_html, 'lxml')
    item1 = soup.find_all('span', id="thread_subject")
    item2 = soup.find('td', class_="t_f")
    item3 = soup.find_all('div', class_="blockcode")
    img_url = item2.img['file']

    pattern1 = ('>(.*?)</span>')
    pattern2 = ('<li>(.*?)</li>')
    pattern3 = re.compile('出演者：(.*?)<br/>', re.S)
    
    magnets = re.findall(pattern2, str(item3))
    titles = re.findall(pattern1, str(item1))
    descriptions = re.findall(pattern3, str(item2))

    magnet = magnets[0].replace('<br/>', '')
    Actress = "".join(descriptions[0].split())
    print(Actress)
    imgtrueurl = str(img_url)
    content = requests.get(imgtrueurl).content

    file_path = '{0}/{1}.{2}'.format(os.getcwd(), titles[0], 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

    content = {
               "title":titles[0],
               "magnet":magnet,
               "Actress":Actress
           }
    return content

    



def save_to_mongo(content):
    if db[MONGO_TABLE].insert(content):
        print('Save to MongoDB successfully!', content)
        return True
    return False


urllist = []

def main():
    start_urls =['https://54sadsad.com/forum-37-{}.html'.format(i) for i in range(1,2)]
    a = 0
    for start_url in start_urls:
        a = a + 1
        html = get_onepage_url(start_url)
        parse_one_page(html, a)
    for url in urllist:
        content = parse_detail_page(url)
        save_to_mongo(content)

if __name__ == '__main__':
    main()
    