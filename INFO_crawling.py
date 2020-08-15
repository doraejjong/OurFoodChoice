from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('disable-gpu')


client = MongoClient('localhost', 27017)
db = client.dbsparta

driver = webdriver.Chrome('/Users/John/Desktop/sparta/test/chromedriver', options=options)

urls = list(db.all_urls.find({}))
url_list = (urls[0]['url'])
all_info = []
for i in url_list:
    driver.get(i)
    sleep(3)
    driver.find_element_by_xpath('//*[@id="tab02"]').click()

    sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    all_List = []
    menus = []

    title_table = soup.select('#container')
    for title_info in title_table:
        title = title_info.select_one('div > div.biz_name_area > strong').text
        category = title_info.select_one('div > div.biz_name_area > span').text
        phone = title_info.select_one('div > div.bizinfo_area > div > div.list_item.list_item_biztel > div').text
        address = title_info.select_one(
            'div > div.bizinfo_area > div > div.list_item.list_item_address > div > ul > li > span').text
        book_review_count = title_info.select_one('div > div.biz_name_area > div > div > a').text

        title_info_doc = {
            'title': title,
            'category': category,
            'phone': phone,
            'address': address,
            'book_review_count': book_review_count,
        }
        all_List.append(title_info_doc)

    image_menu_table = soup.select('#panel02 >div > div>div.image_menu_area > div > a > div.info_area')
    for menu_info in image_menu_table:
        image_menu_menu = menu_info.select_one('div.tit').text
        image_menu_price = menu_info.select_one('div.price').text

        image_menu = {
            'menu': image_menu_menu,
            'price': image_menu_price,
        }
        menus.append(image_menu)
        sleep(0.5)

    menu_table = soup.select('#panel02 >div > div> div.txt_menu_area > ul')

    for txt_menu_info in menu_table:
        txt_menu = txt_menu_info.select_one('li> div > div.tit_area > div.tit').text
        if txt_menu_info.select_one('li> div > div.price') is None:
            pass
        else:
            txt_price = txt_menu_info.select_one('li> div > div.price').text

        txt_menu_info = {
            'menu': txt_menu,
            'price': txt_price,
        }
        menus.append(txt_menu_info)

    shop_info = {
            'title_info': all_List,
            'menu_info': menus
        }
    db.all_shops_info.insert_one(shop_info)

driver.close()
