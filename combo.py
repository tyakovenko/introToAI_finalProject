import pandas as pd

df1 = pd.read_csv('fogsmog.csv')
df2 = pd.read_csv('rain.csv')
df3 = pd.read_csv('sandstorm.csv')

df_combined = pd.concat([df1, df2, df3], ignore_index=True)
df_combined.to_csv('all224.csv', index=False)

print(df_combined)