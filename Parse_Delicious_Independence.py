import pandas as pd
import sys

# указать нужный путь
new_delicious_path = r"C:\Users\User\Desktop\вкусы.xlsx"
path_to_save = r"C:\Users\User\Desktop"

del_need_parse = pd.read_excel(new_delicious_path)

del_good = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name='вкусы')

del_need_parse = del_need_parse.drop_duplicates()

del_need_parse['low_symbols'] = del_need_parse['Бренд-Вкус'].str.lower()
del_need_parse['low_symbols'] = del_need_parse['low_symbols'].replace('black burn', 'blackburn')

del_need_parse['low_symbols'] = del_need_parse['low_symbols'].replace('burn black', 'blackburn')

del_need_parse['low_symbols'] = del_need_parse['low_symbols'].replace('peter ralf', 'peterralf')

del_need_parse['low_symbols2'] = del_need_parse['low_symbols']

del_need_parse['low_symbols'] = del_need_parse['low_symbols'].replace(r'\s+','',regex=True)

del_good['вкус_подготовленный'] = del_good['Вкус'].str.lower().str.split('(').str[0]

del_good['бренд_подготовленный'] = del_good['Бренд'].str.lower()

del_good['бренд_подготовленный'] = del_good['бренд_подготовленный'].str.strip()

del_good['бренд_подготовленный'] = del_good['бренд_подготовленный'].replace('peter ralf', 'peterralf')

del_good['вкус_подготовленный'] = del_good['вкус_подготовленный'].str.strip()

del_good['вкус_подготовленный2'] = del_good['вкус_подготовленный']

del_good['вкус_подготовленный'] = del_good['вкус_подготовленный'].replace(r'\s+','',regex=True)

for index1, row1 in del_need_parse.iterrows():
    for index2, row2 in del_good.iterrows():
        if row2['вкус_подготовленный'] in row1['low_symbols'] and row2['бренд_подготовленный'] in row1['low_symbols']:
            del_need_parse.at[index1, 'Код'] = row2['Код']
            del_need_parse.at[index1, 'Новый вкус'] = row2['Вкус']

del_need_parse = del_need_parse.drop(columns={'low_symbols', 'low_symbols2'})

del_need_parse.to_excel(path_to_save + "/new_delicious.xlsx", index=False)