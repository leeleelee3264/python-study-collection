import dload
from bs4 import BeautifulSoup
from selenium import webdriver
import time


driver = webdriver.Chrome('chromedriver')  # 웹드라이버 파일의 경로
driver.get("https://search.daum.net/search?nil_suggest=btn&w=img&DA=SBC&q=%EB%94%94%EC%95%84%EB%B8%94%EB%A1%9C")
time.sleep(5)  # 5초 동안 페이지 로딩 기다리기

req = driver.page_source
# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(req, 'html.parser')

###################################
# 이제 여기에 코딩을 하면 됩니다!
###################################
# imgList > div:nth-child(1) > a > img

thumbNails = soup.select('#imgList > div > a > img')
n = 0
for thumbNail in thumbNails:
    n += 1
    img = thumbNail['src']
    dload.save(img, f'img/{n}.jpg')
driver.quit()
