# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 11:19:01 2024

@author: USER
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time


def fetch_data():
    url="https://www.104.com.tw/jobs/search/?ro=1&kwop=7&keyword=Python%20Machine%20Learning&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000%2C6001005000%2C6001006000&order=14&asc=0&sctp=M&scmin=40000&scstrict=1&scneg=0&page=1&mode=s&jobsource=tab_cs_to_job&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"
    response = requests.get(url)#可直接用request函式並在參數內選擇方法(get,post)
    soup = BeautifulSoup(response.text,"html.parser")
    # print(soup)
    page = 1
    aa = soup.find_all('article', class_="b-block--top-bord job-list-item b-clearfix js-job-item")
    # print(aa[3])

    data_list = []      
    while soup.find_all('article', class_="b-block--top-bord job-list-item b-clearfix js-job-item"):
        for item in soup.find_all('article', class_="b-block--top-bord job-list-item b-clearfix js-job-item"):
            data = {}
            job_name = item.get('data-job-name')
            data['職缺'] = job_name
            company_name = item.get('data-cust-name')
            data['公司'] = company_name
        
            place = item.find("ul", class_="b-list-inline b-clearfix job-list-intro b-content" )
            if place and place.li:
                place = place.li.text
            else:
                place = 'N/A'    
            data['地點'] = place
            
            salary = item.find("span", class_="b-tag--default" )
            if salary :
                salary = salary.text
            else:
                salary = 'N/A'    
            data['薪水'] = salary
            
            organization = item.find("a", class_="b-tag--default" )
            if organization :
                organization = organization.text
            else:
                organization = 'N/A'    
            data['員工數'] = organization
            
            data_list.append(data)
            
        page += 1
        response = requests.get(f'https://www.104.com.tw/jobs/search/?ro=1&kwop=7&keyword=Python%20Machine%20Learning&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area=6001001000%2C6001002000%2C6001005000%2C6001006000&order=14&asc=0&sctp=M&scmin=40000&scstrict=1&scneg=0&page={page}&mode=s&jobsource=tab_cs_to_job&langFlag=0&langStatus=0&recommendJob=1&hotJob=1')
        soup = BeautifulSoup(response.text, "html.parser")
        print(f"正在爬取:{page}")
        
        if page >= 55:
            break
    return data_list

if __name__ == "__main__":
    data_list = fetch_data()
    
    
    
df = pd.DataFrame(data_list)
df.to_excel("北.xlsx",index=False, engine="openpyxl")

