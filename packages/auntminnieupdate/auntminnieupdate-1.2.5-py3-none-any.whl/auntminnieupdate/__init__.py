import os
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd


def info():
    print('how to use this package:')
    print('this package contains: recent news, conferences, and webinars')
    print('auntminnie.News() for recent news')
    print('auntminnie.Conferences() for recent conferences')
    print('auntminnie.Webinar() for recent conferences')
    print('.test for testing the web')
    print('.data for take a data from web')
    print('.createjson for show data & create file json')
    print('.excelcsv for show data & create file excel & csv')
    print('.run for run .test and .data')
    print('all exctract file in folder resultfile')
    print('.News & .Webinars have parameter for access custom page, default access page 1')


class Core:
    def __init__(self):
        self.url = 'https://www.auntminnie.com/index.aspx?'
        self.site = 'https://www.auntminnie.com'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
        self.newslist = []
        self.conlist = []
        self.weblist = []

        try:
            os.mkdir('resultfile')
        except FileExistsError:
            pass

    def test(self):
        pass

    def data(self):
        pass

    def createjson(self):
        pass

    def excelcsv(self):
        pass

    def run(self):
        self.test()
        self.data()
        self.createjson()
        self.excelcsv()


class News(Core):
    def __init__(self, page=None):
        super().__init__()
        params = {
            'sec': 'nws',
            'sub': 'rad',
            'pno': page
        }
        self.page = page
        self.newsweb = requests.get(self.url, params=params, headers=self.headers)
        self.newssoup = BeautifulSoup(self.newsweb.text, 'html.parser')
        if self.page is None:
            self.page = 1

    def data(self):
        print(f'This is the recent Radiology news in auntminnie on page {self.page}:')

        # scraping
        news = self.newssoup.find_all('div', 'MoreNewsItem')
        for i in news:
            title = i.find('span', 'Head').text
            date = i.find('span', 'maStartDate').text
            try:
                site = self.site + i.find('a')['href']
            except:
                site = 'sorry, the link for this aericle is not yet available'
            img = self.site + i.find('img', 'cntImgRightHeadline')['src']

            print(f"{title}. Published on {date.replace(' -- ', '')}. link: {site}. image:{img} ")

            # sorting & create json file
            newsdict = {
                'title': title,
                'date': date.replace(' -- ', ''),
                'site': site,
                'img': img
            }
            self.newslist.append(newsdict)

    def test(self):
        try:
            if self.newsweb.status_code == 200:
                print(f"{self.newssoup.find('div', 'siteSubHeader').text}is accsesable")
        except Exception:
            print("Can't accses web")

    def createjson(self):
        self.data()
        with open(f'resultfile/news_list page {self.page}.json', 'w+') as news_data:
            json.dump(self.newslist, news_data)
        print('json file created')

    def excelcsv(self):
        self.data()
        df = pd.DataFrame(self.newslist)
        df.to_csv(f'resultfile/news_csv page {self.page}.csv', index=False)
        df.to_excel(f'resultfile/news_excel page {self.page}.xlsx', index=False)
        print('excel & csv file created')


class Conferences(Core):
    def __init__(self):
        super().__init__()
        params = {'sec': 'def'}
        self.conreq = requests.get(self.url, params=params, headers=self.headers)
        self.consoup = BeautifulSoup(self.conreq.text, 'html.parser')

    def data(self):
        print('This is the recent Radiology Conferences:')

        # scraping
        con = self.consoup.find('div', 'supBoxLoopCtrl')
        con = con.findAll('span', 'supBoxHeadLnk')
        for i in con:
            title = i.find('a').text
            date = i.find('br').next_sibling
            try:
                site = i.find('a')['href']
            except:
                site = 'sorry, the link for this aericle is not yet available'

            print(f"{title}. held on {date}. link: {site}")

            # sorting & create json file
            condict = {
                'title': title,
                'date': date,
                'site': site
            }
            self.conlist.append(condict)

    def test(self):
        try:
            if self.conreq.status_code == 200:
                print(f"{self.consoup.find('title').string}is accsesable")
        except Exception:
            print("Can't accses web")

    def createjson(self):
        self.data()
        with open('json_result/conferences_list.json', 'w+') as con_data:
            json.dump(self.conlist, con_data)
        print('json file created')

    def excelcsv(self):
        self.data()
        df = pd.DataFrame(self.conlist)
        df.to_csv('resultfile/conferences_csv.csv', index=False)
        df.to_excel('resultfile/conferences_excel.xlsx', index=False)
        print('excel & csv file created')


class Webinar(Core):
    def __init__(self, page=None):
        super().__init__()
        params = {
            'sec': 'vendor',
            'sub': 'webinars',
            'pno': page
        }
        self.page = page
        self.webreq = requests.get(self.url, params=params, headers=self.headers)
        self.websoup = BeautifulSoup(self.webreq.text, 'html.parser')
        if self.page is None:
            self.page = 1

    def data(self):
        print(f'This is the recent Radiology Webinars in auntminnie on page {self.page}:')

        # scraping
        web = self.websoup.find_all('div', 'MoreNewsItem')
        for i in web:
            title = i.find('span', 'Head').text
            date = i.find('span', 'maStartDate').text
            try:
                site = self.site + i.find('a')['href']
            except:
                site = 'sorry, the link for this aericle is not yet available'
            img = self.site + i.find('img', 'cntImgRightHeadline')['src']

            print(f"{title}. held on {date.replace(' -- ', '')}. link: {site}. img: {img} ")

            # sorting & create json file
            webdict = {
                'title': title,
                'date': date.replace(' -- ', ''),
                'site': site,
                'img': img
            }
            self.weblist.append(webdict)

    def test(self):
        try:
            if self.webreq.status_code == 200:
                print(f"{self.websoup.find('div', 'siteSubHeader').text} is accsesable")
        except Exception:
            print("Can't accses web")

    def createjson(self):
        self.data()
        with open(f'json_result/webinars_list page {self.page}.json', 'w+') as web_data:
            json.dump(self.weblist, web_data)
        print('json file created')

    def excelcsv(self):
        self.data()
        df = pd.DataFrame(self.weblist)
        df.to_csv(f'resultfile/webinars_csv page {self.page}.csv', index=False)
        df.to_excel(f'resultfile/webinars_excel {self.page}.xlsx', index=False)
        print('excel & csv file created')

