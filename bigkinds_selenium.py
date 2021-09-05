from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from requests.api import options
from selenium import webdriver
import pandas as pd
import time
from tqdm import tqdm

NUM_NEWS = 3
TIMESLEEP = 3  # seconds

# selenium에서 사용할 웹 드라이버 절대 경로 정보
chromedriver = 'C:/Users/soomn/Desktop/ds_TermProject/chromedriver.exe'
# option 적용
# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
# selenum의 webdriver에 앞서 설치한 chromedirver를 연동한다.
driver = webdriver.Chrome(chromedriver, options=options)  # option 적용
# url에 접근한다.
driver.get('https://www.bigkinds.or.kr/v2/news/weekendNews.do')

# 로그인 버튼을 눌러주자.
driver.find_element_by_xpath(
    '//*[@id="header"]/div[1]/div/div/button[1]').click()
time.sleep(TIMESLEEP)
# 아이디/비밀번호를 입력해준다.
driver.find_element_by_id('login-user-id').send_keys('sumini02@naver.com')
time.sleep(TIMESLEEP)
driver.find_element_by_id('login-user-password').send_keys('bigkinds1234!!')


# 로그인 버튼을 눌러주자.
driver.find_element_by_xpath('//*[@id="login-btn"]').click()


article_list = []

for i in tqdm(range(NUM_NEWS)):

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    date = soup.select(
        '#weekend-news-result > ul > li:nth-of-type(1) > div > div.title')

    news = soup.select(
        '#weekend-news-result > ul > li:nth-of-type(1) > div > div > ul > li > a > span')

    howmany = soup.select(
        '#weekend-news-result > ul > li:nth-of-type(1) > div > div > ul > li > a > i')
    date_text = soup.find("div", {"class": "title"}).text.strip()

    for n in zip(howmany, news):
        article_list.append(
            {
                'count': n[0].text.strip(),
                'title': n[1].text.strip(),
                'date': date_text
            }
        )
    # 전날 뉴스(이전) 버튼을 눌러주자.
    time.sleep(TIMESLEEP)
    driver.find_element_by_xpath('//*[@id="prev-date-btn"]').click()
    time.sleep(TIMESLEEP)
    # print(article_list[-1]) # check

data = pd.DataFrame(article_list)
data.to_csv('article_bigkinds_{}.csv'.format(str(NUM_NEWS)), mode='w',
            encoding='utf-8-sig', header=True, index=True)

driver.quit()
