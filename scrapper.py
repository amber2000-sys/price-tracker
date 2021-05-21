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


def Scrap_flipkart(url):
    data = getData(url)
    soup = getSoup(data)
    # print(soup)
    details = {}
    details['name'] = soup.find('span', {'class': 'B_NuCI'}).text
    details['price'] = soup.find('div', {'class': '_30jeq3'}).text

    return details


def Scrap_Amazon(url):
    data = getData()
    soup = getSoup(data.text)
