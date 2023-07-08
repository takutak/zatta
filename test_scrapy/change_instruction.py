import pandas as pd
import random

# 日本語のランダムな語尾リスト
endings = ["って何?", "って何", "について教えて", "って何のこと", "とは"]

input_csv = input("成形するcsvファイルを入力：")
output_csv = input("出力するcsvの名前を入力：")

# csvファイルを読み込む
df = pd.read_csv(input_csv)

# 'instruct'列の各要素に対してランダムに語尾を追加
df['instruct'] = df['instruct'].apply(lambda x: str(x) + random.choice(endings))

# 変更を加えたデータフレームを新しいcsvファイルとして保存
df.to_csv(output_csv, index=False)
