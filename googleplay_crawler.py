import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# local path
#path = '/Users/charlie/Desktop/GooglePlay/'

# Install latest Chrome driver:
# https://sites.google.com/a/chromium.org/chromedriver/downloads
driver = webdriver.Chrome('./chromedriver')
# Page url
driver.get('https://play.google.com/store/search?q=%EB%A9%94%EC%8B%A0%EC%A0%80&c=apps')

# crawl until the end page
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
	lastCount = lenOfPage
	time.sleep(3)
	lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	if lastCount==lenOfPage:
		match=True


soup = BeautifulSoup(driver.page_source, 'html.parser',from_encoding='utf-8')
domain = 'https://play.google.com'
url = []
app = []
org = []
desc = []
star = []

for element in soup.find_all('div', {'class':'card-content id-track-click id-track-impression'}):
	url.append(domain+element.find('a', {"class": "title"}).get('href'))
	app.append(element.find('a', {"class": "title"}).get('title'))
	org.append(element.find('a', {"class": "subtitle"}).get('title'))
	desc.append(element.find('div', {"class": "description"}).text)
	star.append(element.find('div', {"class": "tiny-star star-rating-non-editable-container"}).get('aria-label').split()[1])

df = pd.DataFrame({'url':url, 'app':app, 'org':org, 'desc':desc, 'star':star})

print(len(df))
df.to_csv('./App.csv', index=False, encoding='utf-8')
driver.close()
