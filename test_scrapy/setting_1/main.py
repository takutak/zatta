import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

#scrape_wiki_page(url)：指定されたWikipediaページのURLを引数として受け取る。この関数はHTTPリクエストを行い、ページのHTMLをパース（解析）します。
# タイトルと最初の段落のテキストを抽出。タイトルや最初の段落が存在しない場合、対応する変数はNoneとなります。
def scrape_wiki_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('h1', {'class': 'firstHeading'})
    first_para_tag = soup.find('div', {'class': 'mw-parser-output'}).find('p')

    title = title_tag.text if title_tag else None
    first_para = first_para_tag.text.strip() if first_para_tag and first_para_tag.text.strip() != "" else None

    #first_para = first_para_tag.text if first_para_tag else None

    return title, first_para, soup


#find_links(soup, base_url)：BeautifulSoupオブジェクト（解析されたHTML）と基本URLを引数として受け取る。
#HTML内のすべてのリンクを探し、そのリンクが特定のパターン（Wikipediaの記事ページを指すもの）に一致するかどうかを確認
#一致するリンクが見つかれば、そのリンクのURLを抽出し、リストに追加

def find_links(soup, base_url):
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/') and not href.startswith(("/wiki/Wikipedia:", "/wiki/%E7%89%B9%E5%88%A5:", "/wiki/Help:", "/wiki/File:", "/wiki/Portal:", "/wiki/%E3%83%8E%E3%83%BC%E3%83%88:")) and not '.svg' in href and not '.jpeg' in href and not '.jpg' in href and not href == "/wiki/%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9A%E3%83%BC%E3%82%B8":
            links.append(base_url + href)
    return links



# 開始URLを指定（例：'https://ja.wikipedia.org/wiki/人工知能'）
start_url = input("wikipediaのURLを入力してください。：")
base_url = 'https://ja.wikipedia.org'

visited = set()
to_visit = [start_url]
df = pd.DataFrame(columns=['instruct', 'output'])

#max_pagesでアクセスするサイトの上限を管理
page_count = 0
max_pages = int(input("何件のサイトを巡回しますか："))

while to_visit and page_count < max_pages:
    url = to_visit.pop(0)
    if url not in visited:
        visited.add(url)
        try:
            title, first_para, soup = scrape_wiki_page(url)
            if title and first_para:  # Both title and first paragraph should exist
                df = pd.concat([df, pd.DataFrame({'instruct': [title], 'output': [first_para]})], ignore_index=True)
                page_count += 1
            links = find_links(soup, base_url)
            to_visit.extend(links)
        except Exception as e:
            print(f"Error on page {url}: {e}")

# 結果をCSVに保存
output_name = input("保存するcsvファイルの名前を入力してください（csvまでつけてください）：")
df.to_csv(output_name, index=False, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8-sig')

