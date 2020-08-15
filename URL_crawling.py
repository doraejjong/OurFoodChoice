from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

client = MongoClient('localhost', 27017)
db = client.dbsparta

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')

driver = webdriver.Chrome('/Users/John/Desktop/sparta/test/chromedriver', options=options)

driver.get('https://store.naver.com/restaurants/list?bounds=127.0983469%3B37.3923675%3B127.1240103%3B37.4045388&filterId=s20543619&query=%ED%8C%90%EA%B5%90%EC%97%AD%20%EB%A7%9B%EC%A7%91&sessionid=DXh8oq%2FHmrvdZ35b0zc6jQ%3D%3D')

page = 1
all_List = []
while True:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    list = soup.select('div.tit > span')

    for data in list:
        for detail_url in data.find_all('a', attrs=True):
            if detail_url is None:
                pass
            else:
                url = detail_url.attrs['href']
                all_List.append(url)

    page = page + 1
    try:

        if page % 5 == 1:
            driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/div/div[2]/div/div[2]/a[7]').click()
        else:
            driver.find_element_by_xpath('//a[text()=' + str(page) + ']').click()
    except:
        break
    sleep(5)

doc = {
    'url': all_List
}

db.all_urls.insert_one(doc)








