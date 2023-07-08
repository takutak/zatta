import pandas as pd

print("###  ファイル名は拡張子まで含めて記述してください。  ###")
# csvファイルの名前のリストを作成
n = int(input("結合したいcsvファイルの個数を入力："))
csv_files = []  # ここに必要なcsvファイルの名前を記入
for i in range(n):
    input_file = input("csvファイルの名前を入力：")
    csv_files.append(input_file)

# すでに読み込んだ 'instruct' の値を保存するセット
seen_instructions = set()

output_file_name = input("出力するcsvファイルの名前を入力：")

# 結合後のデータを保存するデータフレーム
df_output = pd.DataFrame()

for file in csv_files:
    df = pd.read_csv(file, encoding='utf-8')

    if 'instruct' in df.columns:
        df = df[~df['instruct'].isin(seen_instructions)]
        seen_instructions.update(df['instruct'].tolist())

    df_output = pd.concat([df_output, df])

    print(f"{file}は正常に追加しました。")

df_output.to_csv(output_file_name, index=False, encoding='utf-8')
