
from selenium.webdriver.common.keys import Keys    #模仿键盘,操作下拉框的
from selenium import webdriver    #模仿浏览器的
from urllib.request import urlopen, Request
import urllib3
from bs4 import BeautifulSoup
from pandas import DataFrame
import os
import requests
import random
import time
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
count  = 0
df_ret = DataFrame(columns=[" name", "time", "medium", "classification", "dimension", "artist", "location", "details", "detail_url ","photo_url", "photo_name"])
#m_name, m_date, m_medium, m_classification, m_dimension, m_artist, m_location, m_details, url, m_photo, m_photo_name
# encoding:utf-8
  


def details_page(url):    
    ret = Request(url, headers=headers)
    res = urlopen(ret)
    contents = res.read()
    soup = BeautifulSoup(contents, "html.parser")
   
    ptag = soup.find('div', style="max-height:nullpx; max-width:500px;")
    if ptag != None:
        m_photo = ptag.find('img').get('src')
        m_photo = 'https://allenartcollection.oberlin.edu' + m_photo
        m_photo_name = m_photo.split('/')[-2] + '/preview'
        
    else:
        return

    m_name = soup.find('div', class_='detailField titleField').find('h1').get_text()
    m_artist = soup.find('div', class_='detailField peopleField')
    if m_artist == None:
        m_artist = 'unknown'
    else:
        m_artist = m_artist.find('span', property="name").get_text()

    m_date = soup.find('div', class_='detailField displayDateField')
    if m_date == None:
        m_date = 'unknown'
    else:
        m_date = m_date.find('span', property="dateCreated").get_text()

    m_medium = soup.find('div', class_='detailField mediumField')
    if m_medium == None:
        m_medium = 'unknown'
    else:
        m_medium = m_medium.find('span', property="artMedium").get_text()

    m_dimension = soup.find('div', class_='detailField dimensionsField')
    if m_dimension == None:
        m_dimension = 'unknown'
    else:
        m_dimension = m_dimension.find('span', class_="detailFieldValue").get_text()

    m_location = soup.find('div', class_='detailField onviewField').find('span').get_text() + ',Allen Memorial Art Museum'   
    m_classification = 'unknown'
    m_details = soup.find('div', class_ = 'detailFieldValue')
    if m_details == None:
        m_details = 'unknown'
    else:
        m_details = m_details.get_text()

    global df_ret
    #print(m_name + "        " + m_date + "           " + m_medium + "    " +  m_classification + "    " +  m_dimension + "    "+  m_artist + "    " +  m_location + "    " +  m_details + "    "+ url+ "    " + m_photo + "    " +m_photo_name)
    global count
    print(url, "ok")
    df_ret.loc[count] = [m_name, m_date, m_medium, m_classification, m_dimension, m_artist, m_location, m_details, url, m_photo, m_photo_name]
    count = count +1        
    df_ret.to_csv('15new.csv', encoding= 'utf_8')  


if __name__ == '__main__':

    url = "https://allenartcollection.oberlin.edu/search/Chinese"
    option = webdriver.ChromeOptions() # 不打印无用的日志
    option.add_experimental_option("excludeSwitches", ['enable-automation','enable-logging'])
    browser = webdriver.Chrome(options=option)#创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
    browser.get(url) 
    for i in range(300): 
        print(i)
        browser.execute_script("window.scrollTo(0,document.body.clientHeight)")         # 将滚动条调整至页面底部循环三次
        time.sleep(2)
    response = browser.page_source                      # 获取页面源码
    soup = BeautifulSoup(response, 'lxml')
    
    for tag in soup.find_all('div', class_ = 'title text-wrap'):
        u = tag.find('a', class_ = '').get('href')
        detail_url = 'https://allenartcollection.oberlin.edu/objects/' + u.split('/')[2]
        details_page(detail_url)

    
