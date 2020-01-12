from django.shortcuts import render
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup

# Create your views here.
def scrape():
    #create a session#
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
    url = 'https://www.theonion.com/'
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content , "html.parser")
    posts = soup.find_all('div', {'class':'curation-module__item'})#return a list#

    for i in posts:
        link = i.find_all('section',{'class':'content-meta__headline__wrapper'})[1]
        image_source = i.find('img', {'class':'dv4r5q-2 iaqrWM'})['src']
        print(link.text)
        print(image_source)


scrape()