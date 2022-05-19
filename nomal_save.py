import csv
from selenium.webdriver.common.keys import Keys    #模仿键盘,操作下拉框的
from selenium.webdriver.common.by import By 
from selenium import webdriver    #模仿浏览器的
from urllib.request import urlopen, Request
import urllib3
from bs4 import BeautifulSoup
from pandas import DataFrame
import os
import requests
import random
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait




def save(url,name):
    
    res = requests.get(url)   
    with open(name,"wb") as f :
        f.write(res.content)
        f.close()
    time.sleep(2)



def read_csv(name):
    with open(name,"r", encoding = 'utf-8') as f:
        csv_reder=csv.reader(f)
        data=[]
        for i in csv_reder:
            data.append(i)
        data=data[1:]
    temp=[]
    for index in range(0,len(data)):
        temp.append(data[index][11])
    return temp


if __name__=="__main__":
    #path = "C:\\Users\\hp\\Desktop\博物馆数据\save_image\img_4"
    #filelist = os.listdir(path)
    data=read_csv("5.csv")    
    s = 0
    n = set()
    for i in range(0,len(data)):
        if data.count(data[i]) != 1:
            n.add(data[i])
            print(i, data[i], data.count(data[i]))
            s += 1
    print(len(n), s)
        #save(data[i][0],"img_test/"+data[i][1])
        #print(i, data[i][1]," OK")



 
 

