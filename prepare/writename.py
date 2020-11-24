import pandas as pd

df = pd.read_json('books.json')

n=len(df)
with open('name.txt','w',encoding='utf-8') as f:
    for i in range(n):
        f.write(df['title'][i]+'\n')
