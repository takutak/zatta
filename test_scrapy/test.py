import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_wiki_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', {'class': 'firstHeading'}).text
    first_para = soup.find('div', {'class': 'mw-parser-output'}).find('p').text

    return title, first_para

# URLを指定（例：'https://ja.wikipedia.org/wiki/人工知能'）
url = 'https://ja.wikipedia.org/wiki/%E4%BA%AC%E9%83%BD%E5%A4%A7%E5%AD%A6'
title, first_para = scrape_wiki_page(url)

# 結果をCSVに保存
df = pd.DataFrame([[title, first_para]], columns=['instruct', 'output'])
df.to_csv('output.csv', index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')
