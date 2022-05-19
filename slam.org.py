
from urllib.request import urlopen, Request
import urllib3
from bs4 import BeautifulSoup
from pandas import DataFrame
import os
import requests
import random
import json
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
count  = 0
df_ret = DataFrame(columns=[" name", "time", "medium", "classification", "dimension", "artist", "location", "details", "detail_url ","photo_url", "photo_name"])
#m_name, m_date, m_medium, m_classification, m_dimension, m_artist, m_location, m_details, url, m_photo, m_photo_name
# encoding:utf-8
  


def details_page(url, str):
    
    ret = Request(url, headers=headers)
    res = urlopen(ret)
    contents = res.read()
    soup = BeautifulSoup(contents, "html.parser")
    
    ptag = soup.find('div', class_ = 'viewer-download-buttons mb-3')
    if ptag != None:
        m_photo = ptag.find('a').get('href')
        filename0 = m_photo.split('&')[-1]
        m_photo_name = filename0[2:]
    else:
        return
 
    

    tag1 = soup.find('div', class_ = 'container bb-2')
    m_name = tag1.find('h1',  class_ = 'pb-sm-4 pb-3').get_text()

    flag = 1
    for tag2 in soup.find_all('div', class_=str):
        flag = 0
        m = tag2.find('dt', class_='label label--no-spacing').get_text()
        
        if m == 'Artist Culture' or m == 'Artist':
            m_artist = tag2.find('dd').get_text()
        elif m == 'Date':
            m_date = tag2.find('dd').get_text()
        elif m == 'Classification' :
            m_classification = tag2.find('dd').get_text()
        elif m == 'Material' :
            m_medium = tag2.find('dd').get_text()
        elif m == 'Dimensions' :
            m_dimension = tag2.find('dd').get_text()
        elif m == 'Current Location' :
            m_location = tag2.find('dd').get_text().strip() + ',Saint Louis Art Museum'
   
    if flag == 1:
        details_page(url, 'col-sm-4 mb-4')
        return
    
    tag3 = soup.find('div', class_ = 'actwork-notes')
    if tag3 != None:
        m_details = tag3.get_text()
    else: 
        m_details = 'unknown'
    

    global df_ret
    #print(m_name + "        " + m_date + "           " + m_medium + "    " +  m_classification + "    " +  m_dimension + "    "+  m_artist + "    " +  m_location + "    " +  m_details + "    "+ url+ "    " + m_photo + "    " +m_photo_name)
    global count
    print(url, "ok")
    df_ret.loc[count] = [m_name, m_date, m_medium, m_classification, m_dimension, m_artist, m_location, m_details, url, m_photo, m_photo_name]
    count = count +1
        
    df_ret.to_csv('28.csv', encoding= 'utf_8')  


def single_page(url):
    
    r = requests.get(url,headers=headers)
    data=json.loads(r.text)
 
    for t in data:   
        print(url)
        details_url = t.get('url')# json文件中的列表
        details_page(details_url, 'col-sm-6 mb-4')



if __name__ == '__main__':
    for i in range(1, 6):
        liststr = ['https://www.slam.org/wp-json/slam/v1/objects/?se=chinese&paged=', repr(i), '&show_on_view=true&featured_objects=false&order=ASC&orderby=title&sortBy=TitleAsc']
        next_url = ''.join(liststr)
        print("page = ", i)
        single_page(next_url)
    else:
        print("爬取完成")
    
