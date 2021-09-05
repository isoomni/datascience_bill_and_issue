import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm
import time

DETAIL_LINK = 'http://likms.assembly.go.kr/bill/main.do'
TIMESLEEP = 3

suggest_raw = pd.read_csv('C:/Users/soomn/Desktop/ds_TermProject/open/suggest.csv')

suggest = suggest_raw.copy()
suggest['BILL_TEXT'] = ''

driver = webdriver.Chrome('C:/Users/soomn/Desktop/ds_TermProject/chromedriver.exe')

for i in tqdm(range(len(suggest))):
    driver.get(suggest['DETAIL_LINK'][i]);
    try:
        time.sleep(TIMESLEEP)
        driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/button[1]').click()
        time.sleep(TIMESLEEP)
        text = driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/div[3]/div[2]')
        suggest['BILL_TEXT'][i] = text.text
    except NoSuchElementException:
        suggest['BILL_TEXT'][i] = ""   
        
    if i % 1000 == 0:
        file_name="congrass_selenium/suggest_bill_text" + "_" + str(i) + ".csv"
        suggest.to_csv(file_name, index = False, encoding = 'utf-8-sig')
        print(i)

suggest.to_csv('congrass_selenium/suggest_bill_text.csv', index = False, encoding = 'utf-8-sig')