from bs4 import BeautifulSoup
from selenium import webdriver
from openpyxl import Workbook


driver = webdriver.Chrome('chromedriver')

url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=추석"

driver.get(url)
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')
wb = Workbook()
ws1 = wb.active
ws1.title = "articles"

articles = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li')
ws1.append(["제목", "링크", "신문사", "썸네일"])

for article in articles:
    title = article.select_one('dl > dt > a').text
    url = article.select_one('dl > dt > a')['href']
    thumbnail = article.select_one('div > a')['href']
    broadCast = article.select_one('span._sp_each_source')
    final = broadCast.text.split(' ')[0].replace('언론사', ' ')
    ws1.append([title, url, final, thumbnail])
    
wb.save(filename='articles.xlsx')

driver.quit()
