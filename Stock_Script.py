import pandas as pd
from tkinter import Tk, messagebox, filedialog
import sys

def show_notification(text):
    root = Tk()
    root.withdraw()  # Скрыть основное окно приложения
    messagebox.showinfo("Внимание", text)
    root.destroy()

# получить доступ к переменной, которую передал скрипт с продажами
if len(sys.argv) == 1:
    folder_path_full = sys.argv[0]
else:
    folder_path_full = sys.argv[1]

# Получаем путь к папке, содержащей скрипт
script_dir = folder_path_full

# Отображаем диалоговое окно выбора папки с промежуточными файлами
file_path = filedialog.askdirectory(title="Выберите папку где будут промежуточные файлы и итоговый", initialdir=script_dir)
path_for_news = file_path

# Отображаем диалоговое окно выбора продаж
sell_out_path = filedialog.askopenfilename(title="Выберите файл продаж, который соответствует шаблону")

## Чтение нужных файлов

brands = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name="варианты брендов")

groups = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name="варианты групп")

delicious = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name="варианты вкусов")

gramming = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name="варианты граммовок")

price = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name = "Цены", usecols={'Наименование', 'дистр'})

sell_out = pd.read_excel(sell_out_path)


sell_out.columns = sell_out.columns.str.strip()

## Преобразование в UPPERCASE колонок

sell_out['Бренд'] = sell_out['Бренд'].str.strip()
sell_out['Бренд'] = sell_out['Бренд'].str.upper()

sell_out['Группа'] = sell_out['Группа'].str.strip()
sell_out['Группа'] = sell_out['Группа'].str.upper()

sell_out['Вкус'] = sell_out['Вкус'].str.strip()
sell_out['Вкус'] = sell_out['Вкус'].str.upper()

try:
    sell_out['Граммовка'] = sell_out['Граммовка'].str.strip()
    sell_out['Граммовка'] = sell_out['Граммовка'].str.upper()

except:
    print("Граммовки не строки и преобразования для них не работают")

else:
    pass

# Выгрузка не найденных в справочнике значений

## Получить не найденые бренды

new_brands = sell_out.merge(brands, left_on = 'Бренд', how='outer', right_on = 'Бренд (исходный)',indicator=True)

new_brands = new_brands.loc[new_brands['_merge'] == 'left_only']

new_brands = new_brands['Бренд_x']
new_brands = new_brands.drop_duplicates()

check_new_brands = new_brands.empty

if check_new_brands == False:
    show_notification("Найдены не существующие бренды в справочнике, добавьте и запустите заново")  
    new_brands.to_excel(path_for_news + "/new_brands.xlsx", index=False)


# Добавить правильный бренд

sell_out = sell_out.merge(brands, how="left", left_on="Бренд", right_on="Бренд (исходный)" )

sell_out = sell_out.drop(columns=['Бренд_x', 'Бренд (исходный)'])
sell_out = sell_out.rename(columns={'Бренд_y':'Бренд'})

## Получить не найденые группы

new_groups = sell_out.merge(groups, left_on = 'Группа', how='outer', right_on = 'Исходная группа',indicator=True)

new_groups = new_groups.loc[new_groups['_merge'] == 'left_only']

new_groups = new_groups['Группа_x']
new_groups = new_groups.drop_duplicates()

check_new_groups = new_groups.empty
if check_new_groups == False:
    show_notification("Найдены не существующие группы в справочнике, добавьте и запустите заново") 
    new_groups.to_excel(path_for_news + "/new_groups.xlsx", index=False)

## Получить не найденые вкусы

sell_out['Бренд-Вкус'] = sell_out['Бренд'] + sell_out['Вкус']

sell_out['Бренд-Вкус'] = sell_out['Бренд-Вкус'].str.upper()

new_delicious = sell_out.merge(delicious, left_on = 'Бренд-Вкус', how='outer', right_on = 'Исходный вкус',indicator=True)

new_delicious = new_delicious.loc[new_delicious['_merge'] == 'left_only']

new_delicious = new_delicious['Бренд-Вкус']
new_delicious = new_delicious.drop_duplicates()

check_new_delicious = new_delicious.empty

if check_new_delicious == False:
    # здесь добавить появление информационного окна    
    show_notification("Найдены не существующие вкусы в справочнике, добавьте и запустите заново")
    new_delicious.to_excel(path_for_news + "/new_delicious.xlsx", index=False)

## Получить не найденые граммовки

new_gramming = sell_out.merge(gramming, left_on = 'Граммовка', how='outer', right_on = 'Исходная граммовка',indicator=True)


new_gramming = new_gramming.loc[new_gramming['_merge'] == 'left_only']

new_gramming = new_gramming['Граммовка_x']
new_gramming = new_gramming.drop_duplicates()

check_new_gramming = new_gramming.empty

if check_new_gramming == False:
    # здесь добаваить появление информационного окна    
    show_notification("Найдены не существующие граммовки в справочнике, добавьте и запустите заново")
    new_gramming.to_excel(path_for_news + "/new_gramming.xlsx", index=False)

# Добавление правильных признаков

## Добавить правильный группу

sell_out = sell_out.merge(groups, how="left", left_on="Группа", right_on="Исходная группа" )

sell_out = sell_out.drop(columns=['Группа_x', 'Граммовка_x', 'Исходная группа', 'Brand'])
sell_out = sell_out.rename(columns={'Группа_y':'Группа', 'Граммовка_y':'Граммовка'})

## Добавить правильный вкус

sell_out = sell_out.merge(delicious, how="left", left_on="Бренд-Вкус", right_on="Исходный вкус" )

sell_out = sell_out.drop(columns=['Вкус_x', 'Бренд-Вкус', 'Исходный вкус', 'Код'])
sell_out = sell_out.rename(columns={'Вкус_y':'Вкус'})

## Добавить правильную граммовку

sell_out = sell_out.merge(gramming, how="left", left_on="Граммовка", right_on="Исходная граммовка" )

sell_out = sell_out.drop(columns=['Граммовка_x', 'Исходная граммовка'])
sell_out = sell_out.rename(columns={'Граммовка_y':'Граммовка'})

if 'ВЕС кг' in sell_out.columns:
    sell_out = sell_out.rename(columns={'ВЕС кг':'ВEC'})

## добавить правильные цены и стоимость и вес если отсутствует
with_price = sell_out.loc[sell_out['Цена'].notna()]
with_no_price = sell_out.loc[sell_out['Цена'].isna()]

a = pd.merge(with_no_price, price, how='outer', left_on='Группа', right_on='Наименование', indicator=True)

a = a.loc[a['_merge'] == 'left_only']

a = a['Группа']
a = a.drop_duplicates()

a = a.empty

if a == False:
    # здесь добавить появление информационного окна    
    show_notification("Найдены не существующие группы в справочнике, добавьте и запустите заново")
    a.to_excel(path_for_news + "/new_groups_with_price.xlsx", index=False)

with_no_price = with_no_price.merge(price, how='left', left_on='Группа', right_on='Наименование')

with_no_price = with_no_price.drop(columns={'Цена', 'Наименование'})
with_no_price = with_no_price.rename(columns={'дистр':'Цена'})

with_no_price['ВЕС'] = (with_no_price['Граммовка']/1000) * with_no_price['Количество шт']
with_no_price['стоимость'] = with_no_price['Цена'] * with_no_price['Количество шт']

with_no_price = with_no_price[['Бренд', 'Группа', 'Вкус', 'Граммовка', 'Количество шт', 'ВЕС', 'Цена', 'стоимость', 'Дистрибьютор', 'Дата' ]]

sell_out = pd.concat([with_price, with_no_price])

# 
sell_out = sell_out[['Бренд', 'Группа', 'Вкус', 'Граммовка', 'Количество шт', 'ВЕС', 'Цена', 'стоимость', 'Дистрибьютор', 'Дата' ]]




sell_out.to_excel(path_for_news + "/stock.xlsx", index=False)