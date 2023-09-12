import pandas as pd

df = pd.read_csv('input.csv')
new_df = pd.DataFrame()
new_df['id'] = df['id']
questions = set(col.split('_')[0] for col in df.columns if '_' in col)

for question in questions:
    # 各問題に対する列を取得
    cols = [f"{question}_{i:02}" for i in range(1, 6)]
    
    # 評価を取得
    new_df[question] = df[cols].idxmax(axis=1).str[-2:].astype(int)

# 新しいCSVファイルとして保存
new_df.to_csv('output.csv', index=False)
