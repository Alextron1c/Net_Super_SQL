import requests
import time
from bs4 import BeautifulSoup
import io
import sys
import csv
import mysql.connector

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
name_list=[]
price_list=[]
holder_list=[]
updated_data={}

parsing_list=["https://sm.rakuten.co.jp/search/110000?l-id=_leftnavi_110000&sort=",
            "https://sm.rakuten.co.jp/search/110013?l-id=_leftnavi_110013&sort=",
            "https://sm.rakuten.co.jp/search/110008?l-id=_leftnavi_110008&sort=",
            "https://sm.rakuten.co.jp/search/110001?l-id=_leftnavi_110001&sort=",
            "https://sm.rakuten.co.jp/search/110009?l-id=_leftnavi_110009&sort=",
            "https://sm.rakuten.co.jp/search/200773?l-id=_leftnavi_200773&sort=",
            "https://sm.rakuten.co.jp/search/200875?l-id=_leftnavi_200875&sort=",
            "https://sm.rakuten.co.jp/search/110002?l-id=_leftnavi_110002&sort=",
            "https://sm.rakuten.co.jp/search/110006?l-id=_leftnavi_110006&sort=",
            "https://sm.rakuten.co.jp/search/200884?l-id=_leftnavi_200884&sort=",
            "https://sm.rakuten.co.jp/search/200002?l-id=_leftnavi_200002&sort=",
            "https://sm.rakuten.co.jp/search/110007?l-id=_leftnavi_110007&sort=",
            "https://sm.rakuten.co.jp/search/200003?l-id=_leftnavi_200003&sort=",
            "https://sm.rakuten.co.jp/search/200830?l-id=_leftnavi_200830&sort=",
                ]
            
for url in parsing_list:
    website = requests.get(url+"1", headers=HEADERS) 
    website.encoding = 'UTF-8'
    time.sleep(1)  
    doc0 = BeautifulSoup(website.content, 'html.parser')

    pagelist = doc0.find("ul", class_="only-pc")
    if pagelist:
        fullpage_list = pagelist.find_all()[-1].text
        try:
            last_page_number = int(fullpage_list)
        except ValueError:
            last_page_number = 1  
        
        for y in range(1, last_page_number + 1):
            holder_list.append(url + f"{y}")
                


    
for items in holder_list:
    website = requests.get(items, headers=HEADERS)
    website.encoding = 'UTF-8'
    time.sleep(1)
    doc = BeautifulSoup(website.content, 'html.parser')

    name_list_elements = doc.find_all("span", class_="product-item-info-name")
    price_list_elements = doc.find_all("p", class_="product-item-info-price")

    
    for name_element, price_element in zip(name_list_elements, price_list_elements):
        name = name_element.text.strip()
        price = price_element.text.replace("¥", "").replace("円", "").replace(",", "").strip()
        updated_data[name]=price
            

mydb = mysql.connector.connect(
    host="",
    user="",
    password=""
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS whole_foods_s1")
cursor.close()
mydb.close()


mydb = mysql.connector.connect(
    host = "",
    user = "",
    password ="",
    database= "whole_foods_S1"
)
 
cursor = mydb.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    price INT(10)
)
""")

for name, price in updated_data.items():
    cursor.execute("INSERT INTO Item (name, price) VALUES (%s, %s)", (name, price))
    mydb.commit()  
cursor.close()
mydb.close()

