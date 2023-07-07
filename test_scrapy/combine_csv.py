import csv
print("###  ファイル名は拡張子まで含めて記述してください。  ###")
# csvファイルの名前のリストを作成
n = int(input("結合したいcsvファイルの個数を入力："))
csv_files = []  # ここに必要なcsvファイルの名前を記入
for i in range(n):
    input_file = input("csvファイルの名前を入力：")
    csv_files.append(input_file)

# すでに見た 'instruction' の値を保存するセット
seen_instructions = set()

output_file_name = input("出力するcsvファイルの名前を入力：")
# 出力用のCSVファイルを開く
with open(output_file_name, 'w', newline='', encoding='utf-8') as outfile:  # ここで 'utf-8' を指定
    writer = csv.writer(outfile)

    for file in csv_files:
        with open(file, 'r', encoding='utf-8') as infile:  # ここでも 'utf-8' を指定
            reader = csv.reader(infile)

            # header 行を処理
            if file == csv_files[0]:
                header = next(reader)
                writer.writerow(header)
            else:
                # header 行をスキップ
                next(reader)

            for row in reader:
                instruction = row[0]  # 'instruction' 列が最初であると仮定

                if instruction not in seen_instructions:
                    writer.writerow(row)
                    seen_instructions.add(instruction)
        print(f"{file}は正常に追加しました。")
