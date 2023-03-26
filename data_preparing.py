import numpy as np
import pandas as pd
import os

df = pd.read_csv("C:/py_projects/stats_hotel/data_files/main", header=[0, 1], index_col=0)
month_var = input('type filename from data_files folder without extansion: ')
month = pd.read_excel(f'C:/py_projects/stats_hotel/data_files/{month_var}.xlsx', index_col='Показатель')

def group_rows(x):
    name = x.index[0]
    x = x.iloc[1:]
    x.index = pd.MultiIndex.from_product([[name], x.index])
    return x

month.index = month.index.str.strip()

rows_to_exclude = ["Доход за период", "Pechory Apartment (Gagarina 1 room)", "Доход по еде и напиткам (F&B)",
                   "Доходы прочие", "Заказано допуслуг на сумму"]

month = month[~month.index.isin(rows_to_exclude)]

month = month.rename(index={'Процент загрузки отеля': 'load_percent', 'Средняя стоимость номера за сутки (ADR)':'room_coast_mean', 
                        'Средний доход на номер (RevPar)': 'room_profit_mean', 'Забронировано номеров/день': 'rooms_per_day',
                             '2-х комнатные Апартаменты с 1 спальней': '2_rooms', '3-х комнатные апартаменты с 2-я спальнями':
                             '3_rooms', 'Апартаменты с 1-й спальней': '1_room', '2-х комнатные апартаменты': 'P2_rooms',
                             'Доход за проживание': 'profit', 'Количество гостей': 'guests'})

month = month.rename(columns={'Значение за период': f'{month_var}'})

for c1 in month.columns:
    v = month[c1]
    month[c1] = v.str.replace(",", ".", regex=False)


for c1 in month.columns:
    v = month[c1]
    month[c1] = v.str.replace("[\s, %, R, U, B]", "", regex=True).astype(float)

month = month.groupby(np.arange(len(month)) // 5, group_keys=False).apply(group_rows).T

frames = [df, month]
result = pd.concat(frames)
result.to_csv('C:/py_projects/stats_hotel/data_files/main')
os.remove(f'C:/py_projects/stats_hotel/data_files/{month_var}.xlsx')

print(f'main is extended by {month_var}')
print('initial scale: ', df.shape)
print('finite scale: ', result.shape)
print(result.index)

