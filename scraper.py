# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 01:12:08 2019

@author: SNIGDHA S
"""

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import lxml
import pandas as pd

my_url = 'https://karki23.github.io/Weather-Data/assignment.html'

# opening connection
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# lxml parser
page_soup = soup(page_html,'lxml')

# extracting city links from homepage
city_url = []
for link in page_soup.find_all('a'):
    city_url.append('https://karki23.github.io/Weather-Data/'+ link.get('href'))	

# scraping each city table
for city in city_url :

	uCity = uReq(city)
	city_html = uCity.read()
	uCity.close()
	
	city_soup = soup(city_html,'lxml')
		
	table = city_soup.find('table')
	rows = table.find_all('tr')
	columns = [v.text.replace('\n','') for v in rows[0].find_all('th')]
		
	df = pd.DataFrame(columns = columns)
		
	for i in range(1,len(rows)):
		td = rows[i].find_all('td')
		values = [td.text for td in td]
		df = df.append(pd.Series(values,index=columns),ignore_index=True)
			
		df.to_csv('C:\SNIGDHA\PESU\Summer 2019\PESU-IO-SUMMER\FINAL ASSIGNMENT\\'+ values[1] + '.csv',index = False)
			
		
