from bs4 import BeautifulSoup
import requests


def getData(url):
    try:
        data = requests.get(url)
        return data
    except Exception as e:
        print('could not get data')
        print(e)


def getSoup(data):
    try:
        soup = BeautifulSoup(data.text)
        return soup
    except Exception as e:
        print('could not create soup')
        print(e)


def Scrap_flipkart(q):
    url = 'https://www.flipkart.com/search?q='+'+'.join(q.split())

    print('url', url)
