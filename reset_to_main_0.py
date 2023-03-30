import pandas as pd
df = pd.read_csv('C:/py_projects/stats_hotel/data_files/main_0', header=[0,1], index_col=0)
df.to_csv('C:/py_projects/stats_hotel/data_files/main')
print(df.tail())

print(df.shape)
print(df.index)