import requests
from requests.exceptions import RequestException
import re
from bs4 import BeautifulSoup



def get_onepage(mainurl):

    response = requests.get(mainurl)
    if response.status_code == 200:
        return response.text

def parse_onepage(html):
    pattern = re.compile('有码</a>\]</em>\s<a href="(.*?)".*?class="s xst">(.*?)\[高清中文字幕\]', re.S)
    items = re.findall(pattern, html)
    return items
        
def get_magnet_page(url):
    response = requests.get(url)
    html1 = response.text
    return html1

def get_img(url,UUID):
    response = requests.get(url)
    html = response.text
    pattern = re.compile('class="zoom"\sfile="(.*?)"', re.S)
    items = re.findall(pattern, html)
    for item in items:
        r = requests.get(str(item))
        if r.status_code == 200:
            open(UUID,'wb').write(r.content)


def parse_magnet_page(html1):
    pattern = re.compile('磁力链接.*?<ol><li>(.*?)</ol>', re.S)
    items = re.findall(pattern, html1)
    return items

def main():
    mainurl = 'https://54sadsad.com/forum-103-1.html'
    get_onepage(mainurl)
    html = get_onepage(mainurl)
    parse_onepage(html)
    for item in parse_onepage(html):
        UUID = item[1]
        print(UUID)
        url = 'https://54sadsad.com/' + item[0]
        html1 = get_magnet_page(url)
        parse_magnet_page(html1)
        get_img(url, UUID)
        for item in parse_magnet_page(html1):
           print(item)
       
if __name__ == '__main__':
    main()
