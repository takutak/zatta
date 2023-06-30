# 必要なライブラリをインポートします
from bs4 import BeautifulSoup
import requests

# スクレイピングしたいサイトのURLを定義します
url = 'https://en.wikipedia.org/wiki/Fine-tuning_(machine_learning)'

# サイトにリクエストを送ります
r = requests.get(url)

# BeautifulSoupでページをパースします
soup = BeautifulSoup(r.text, 'html.parser')

# ページ上の見出しを探します（通常は<h1>, <h2>, <h3>タグで見つかります）
headlines = soup.find_all(['h1', 'h2', 'h3'])

# 各見出しを出力します
for headline in headlines:
    print(headline.text.strip())
