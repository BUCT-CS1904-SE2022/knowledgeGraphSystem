from urllib.request import urlopen, Request
import urllib3
from bs4 import BeautifulSoup
from pandas import DataFrame
import os
import requests
import random

# encoding:utf-8


    
            
  
def get_photo(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    ret = Request(url, headers=headers)
    res = urlopen(ret)
    contents = res.read()
    soup = BeautifulSoup(contents, "html.parser")


    tag6 = soup.find('div', class_ = 'group-left')    
    if tag6.find('a') == None:
        m_photo = 'unknown'
    else:
        m_photo = tag6.find('a').get('href')

    if m_photo != 'unknown':
        
        filename0 = m_photo.split('/')[-5]
        m_photo_name = filename0[:4]+ '_' + filename0[5:]+ '.jpg'
    else:
        m_photo_name = '0'
    

    tag5 = soup.find('div', class_ = 'group-right')
    tag7 = tag5.find('div', class_ = 'field field-name-field-provenance field-type-text-long field-label-inline clearfix')
    if tag7 == None:
        m_details = 'unknown'
    else:
        m_details = tag7.find('p').get_text()

    tag10 = tag5.find('div', class_ = 'field field-name-field-dimensions field-type-text field-label-hidden')
    m_dimension = identify(tag10)

    return m_photo, m_details, m_dimension, m_photo_name


def identify(tag):
    if tag != None:
        m = tag.find('div', class_ = 'field-item even').get_text()
    else:
        m = 'unknown'
    m.replace(u'\xa0', u' ')
    return m



def this_page(url, count, df_ret):
   
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    ret = Request(url, headers=headers)
    res = urlopen(ret)
    contents = res.read()
    soup = BeautifulSoup(contents, "html.parser")
    

    for tag in soup.find_all('div', class_='ds-3col node node-collections-object view-mode-search_result clearfix'):

        ptag = tag.find('div', class_='group-right')
        if ptag.find('div', class_='photo-wrapper') == None:
            break;

        tag1 = tag.find('div', class_ = 'field field-name-title field-type-ds field-label-hidden')
        m_name = tag1.find('a').get_text()


        tag2 = tag.find('div', class_='field field-name-field-dated field-type-text field-label-inline clearfix')
        tag4 = tag.find('div', class_='field field-name-field-period field-type-text field-label-inline clearfix')
        if tag2 != None:
            m_date = tag2.find('div', class_ = 'field-item even').get_text()
        elif tag4 != None:
            m_date = tag4.find('div', class_ = 'field-item even').get_text()   
        else:
            m_date = 'unknown'
        m_date.replace(u'\xa0', u' ')
            

        tag3 = tag.find('div', class_='field field-name-field-medium field-type-text-long field-label-inline clearfix')
        m_medium = identify(tag3)
        


        tag8 = tag.find('div', class_ = 'field field-name-field-classification field-type-text field-label-inline clearfix')
        m_classification = identify(tag8)

        tag9 = tag.find('div', class_ = 'field field-name-field-artist field-type-text field-label-inline clearfix')
        m_artist = identify(tag9)

        tag11 = tag.find('div', class_ = 'field field-name-object-location field-type-ds field-label-inline clearfix')
        m_location = identify(tag11).strip()+',Yale University Art Gallery'


        m_details_url = tag1.find('a').get('href')
        liststr = ['https://artgallery.yale.edu', m_details_url]
        m_details_url = ''.join(liststr)

        m_photo, m_details, m_dimension, m_photo_name = get_photo(m_details_url)

        if m_photo != 'unknown':
            print(m_name + "        " + m_date + "           " + m_medium + "    " +  m_classification + "    " +  m_dimension + "    "+  m_artist + "    " +  m_location + "    " +  m_details + "    "+ m_details_url+ "    " + m_photo + "    " +m_photo_name)
            df_ret.loc[count] = [m_name, m_date, m_medium, m_classification, m_dimension, m_artist, m_location, m_details, m_details_url, m_photo, m_photo_name]
            count = count +1
        df_ret.to_csv('24-884.csv', encoding= 'utf_8')
      
    

    pcxt=soup.find('div',{'class':'item-list'})
    pcxt1=pcxt.find('li',{'class':'pager-next'})
    if pcxt1!=None:
        link1=pcxt1.find('a').get('href')
        liststr = ['https://artgallery.yale.edu', link1]
        link = ''.join(liststr) 
        this_page(link, count, df_ret)
    else:
        print("爬取完成")
        
        
        
        


if __name__ == '__main__':
    
    os.makedirs('./image', exist_ok=True)
    url = 'https://artgallery.yale.edu/collection/search/China?page=884'
    df_ret = DataFrame(columns=[" name", "time", "medium", "classification", "dimension", "artist", "location", "details", "detail_url ","photo_url", "photo_name"])
    #url = "https://artgallery.yale.edu/collection/search/China"
    this_page(url, 0, df_ret)
    
