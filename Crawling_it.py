# 크롤링 후 해시태그들을 taglist폴더에 번호순대로 저장

from bs4 import BeautifulSoup
import requests
import os
import datetime

soup = ''
def writeHashtag(category, n):
    filepath = "./taglist/"+str(n)+".txt"
    li_tag = soup.find('h3', id=category).find_next('ul')
    li_list = li_tag.find_all('li')
    if os.path.exists(filepath):
        os.remove(filepath)
    file = open(filepath, 'w')    
    for li in li_list[:-1]:
        file.write(li.string+"\n")
    file.close() 

def run():
    global soup
    url = 'https://www.tomoson.com/blog/most-popular-hashtags-by-category/'

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        print("Crawling Data Updated =>", datetime.datetime.now())

        writeHashtag('holidays', 1)
        writeHashtag('beauty', 2)
        writeHashtag('couples', 3)
        writeHashtag('fashion', 4)
        writeHashtag('pets', 5)
        writeHashtag('food', 6)
        writeHashtag('travel', 7)
        writeHashtag('fitness', 9)

    else : 
        print(response.status_code)

