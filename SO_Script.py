import pandas as pd
import numpy as np
from dateutil.parser import parse
import subprocess
from tkinter import Tk, messagebox, filedialog
import sys
import os

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

# идентификатор что всё норм по колонкам
all_nice_in_table = True

# Получаем путь к папке, содержащей скрипт
script_dir = folder_path_full

# # Отображаем диалоговое окно выбора папки с промежуточными файлами
# file_path = filedialog.askdirectory(title="Выберите папку где будут промежуточные файлы и итоговый", initialdir=script_dir)
# path_for_news = file_path

# Отображаем диалоговое окно выбора продаж
sell_out_path = filedialog.askopenfilename(title="Выберите подготовленный для обработки файл продаж")


file_path = os.path.dirname(sell_out_path)
path_for_news = file_path

## Чтение нужных файлов

brands = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name="варианты брендов")

groups = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name="варианты групп")

delicious = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name="варианты вкусов")

gramming = pd.read_excel(r"D:\Analysis Burn\Продукция Burn.xlsx", sheet_name="варианты граммовок")



sell_out = pd.read_excel(sell_out_path)


## Преобразование в UPPERCASE колонок

sell_out['Бренд'] = sell_out['Бренд'].str.strip()
sell_out['Бренд'] = sell_out['Бренд'].str.upper()

sell_out['Группа'] = sell_out['Группа'].str.strip()
sell_out['Группа'] = sell_out['Группа'].str.upper()

sell_out['Вкус'] = sell_out['Вкус'].str.strip()
sell_out['Вкус'] = sell_out['Вкус'].str.upper()

# Определение функции для применения str.strip().upper() только к строкам
def strip_string(x):
    if isinstance(x, str):  # Проверка, является ли значение строкой
        return x.strip().upper()
    return x
# Применение функции к каждому элементу Series
sell_out['Граммовка'] = sell_out['Граммовка'].apply(strip_string)


# Определение функции для преобразования кривых чисел
def int_type(x):
    if isinstance(x, str):  # Проверка, является ли значение строкой
        return int(float(x.replace("\xa0","").replace(",",".")))
    return x
# Применение функции к каждому элементу Series
sell_out['стоимость'] = sell_out['стоимость'].apply(int_type)

# удаление мерча
sell_out = sell_out.loc[ sell_out['Группа'].str.contains('мерч',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Бренд'].str.contains('мерч',case=False) == False ]

sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('уголь',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('свитшот',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('футболка',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('мундштук',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('шелфтокер',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('воблер',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('наклейк',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('ремувк',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('ПОДСТАВКА',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('СВЕТЯЩИЙСЯ ЛОГОТИП',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('ТЕЙБЛТЕНТ',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('ЛИСТОВКА',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Вкус'].str.contains('ЧАША ПРЯМОТОК',case=False) == False ]
sell_out = sell_out.loc[ sell_out['Бренд'].str.contains('Кальян ',case=False) == False ]

# если группа = БЕЗ МРК, то писать в группу и в бренд вкус
sell_out.loc[sell_out['Группа'] == 'БЕЗ МРК', ['Группа', 'Бренд']] = sell_out['Вкус']

# если граммовка = 0, то писать вкус
sell_out.loc[sell_out['Граммовка'] == 0, 'Граммовка'] = sell_out['Вкус']

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
    exit()


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
    all_nice_in_table = False

## Получить не найденые вкусы

sell_out['Бренд-Вкус'] = sell_out['Бренд'] + sell_out['Вкус']

sell_out['Бренд-Вкус'] = sell_out['Бренд-Вкус'].str.upper()

new_delicious = sell_out.merge(delicious, left_on = 'Бренд-Вкус', how='outer', right_on = 'Исходный вкус',indicator=True)

new_delicious = new_delicious.loc[new_delicious['_merge'] == 'left_only']

new_delicious = new_delicious['Бренд-Вкус']
new_delicious = new_delicious.drop_duplicates()

# убрать те, в которых написано не указан
new_delicious = new_delicious.loc[~new_delicious.str.match(r".*НЕ УКАЗАН")]

check_new_delicious = new_delicious.empty



if check_new_delicious == False:
    # здесь добавить появление информационного окна    
    show_notification("Найдены не существующие вкусы в справочнике, добавьте и запустите заново")
    all_nice_in_table = False
    # вызвать скрипт для полной обработки

    new_delicious.to_excel(path_for_news + "/new_delicious.xlsx", index=False)

    new_delicious_path = path_for_news + "/new_delicious.xlsx"

    # запуск отдельного скрипта
    subprocess.call(["python", "D:\Analysis Burn\Scripts\ParseDelicious_Script.py", new_delicious_path, path_for_news])

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
    all_nice_in_table = False
    exit()

# Добавление правильных признаков

## Добавить правильный группу

sell_out = sell_out.merge(groups, how="left", left_on="Группа", right_on="Исходная группа" )

sell_out = sell_out.drop(columns=['Группа_x', 'Граммовка_x', 'Исходная группа', 'Brand'])
sell_out = sell_out.rename(columns={'Группа_y':'Группа', 'Граммовка_y':'Граммовка'})

## Добавить правильный вкус

sell_out = sell_out.merge(delicious, how="left", left_on="Бренд-Вкус", right_on="Исходный вкус" )

sell_out = sell_out.drop(columns=['Вкус_x', 'Бренд-Вкус', 'Исходный вкус', 'Код'])
sell_out = sell_out.rename(columns={'Вкус_y':'Вкус'})
sell_out['Вкус'].fillna('не указан', inplace=True)

## Добавить правильный граммовку

sell_out = sell_out.merge(gramming, how="left", left_on="Граммовка", right_on="Исходная граммовка" )

sell_out = sell_out.drop(columns=['Граммовка_x', 'Исходная граммовка'])
sell_out = sell_out.rename(columns={'Граммовка_y':'Граммовка'})

# правильное расположение колонок
sell_out = sell_out[['Торговый представитель','Код клиента','Сегмент','Клиент','Адрес доставки', 'Дата отгрузки', 'Бренд', 'Группа', 'Вкус', 'Граммовка', 'Количество шт', 'ВЕС', 'Цена', 'стоимость', 'Дистрибьютор']]

# преобразование типа в дату
def convert_date(date_series):
    if date_series[0:4].isdigit():
        # Попытка преобразования с yearfirst=True
        converted_dates = pd.to_datetime(date_series, yearfirst=True)
    else:
        # Если возникла ошибка, пробуем преобразовать с dayfirst=True
        converted_dates = pd.to_datetime(date_series, dayfirst=True)
    return converted_dates


if sell_out['Дата отгрузки'].dtypes != '<M8[ns]':
    sell_out['Дата отгрузки'] = sell_out['Дата отгрузки'].apply(convert_date)

if sell_out.isna().sum().any():
    show_notification("Есть пустые значения в колонках, необходимо проверить")
    exit()


# если ВЕС = 0, то граммовку разделить на 1000 и умножить на количество
sell_out.loc[sell_out['ВЕС'] == 0, 'ВЕС'] = (sell_out['Граммовка']/1000) * sell_out['Количество шт']

# если стоимость = 0, то цену умножить на количество
sell_out.loc[sell_out['стоимость'] == 0, 'стоимость'] = sell_out['Цена'] * sell_out['Количество шт']

# если цена = 0, то стоимость разделить на количество
sell_out.loc[sell_out['Цена'] == 0, 'Цена'] = sell_out['стоимость'] / sell_out['Количество шт']

sell_out['Торговый представитель'] = sell_out['Торговый представитель'].str.lower()

sell_out['Код клиента'] = sell_out['Код клиента'].astype(str)
sell_out['Код клиента'] = sell_out['Код клиента'].str.lower()


sell_out['Сегмент'] = sell_out['Сегмент'].str.lower()
sell_out['Клиент'] = sell_out['Клиент'].str.capitalize()
sell_out['Адрес доставки'] = sell_out['Адрес доставки'].str.capitalize()
sell_out['Бренд'] = sell_out['Бренд'].str.capitalize()
sell_out['Группа'] = sell_out['Группа'].str.capitalize()
sell_out['Вкус'] = sell_out['Вкус'].str.capitalize()


# спросить путь для общего файла
sell_out_path_for_good_file = filedialog.askopenfilename(title="Выберите файл продаж готовый куда добавятся данные, если всё хорошо")
# если указан путь для общего то загрузить его


### чтение общего файла продаж в зависимости от типа
# чтение если csv
if sell_out_path_for_good_file.endswith(".csv"):
    is_csv = True
    if sell_out_path_for_good_file != '':
        good_sell_out = pd.read_csv(sell_out_path_for_good_file)
# чтение если excel
if sell_out_path_for_good_file.endswith(".xlsx"):
    is_csv = False
    if sell_out_path_for_good_file != '':
        good_sell_out = pd.read_excel(sell_out_path_for_good_file)

# проверка идентичности заголовков общего и подготовленного
if sell_out_path_for_good_file != '':
    if good_sell_out.columns.equals(sell_out.columns) == False:
        show_notification("Что-то не так с заголовками проверьте файл вручную")  
        sys.exit()

# проверка отсутствия дубликатов дат
if sell_out_path_for_good_file != '':
    if sell_out['Дата отгрузки'].isin(good_sell_out['Дата отгрузки']).any():
        show_notification("Даты дублируются, соединить нельзя, только сохранить отдельно в sell_out")  
        if all_nice_in_table == True:
            sell_out.to_excel(path_for_news + "/sell_out.xlsx", index=False)
        sys.exit()



if all_nice_in_table == True:
    if sell_out_path_for_good_file != '':
        all = pd.concat(
            [good_sell_out, sell_out]
        )
        sell_out.to_excel(path_for_news + "/sell_out.xlsx", index=False)

        if is_csv == False:
            all.to_excel(sell_out_path_for_good_file, index=False)
        if is_csv == True:
            all.to_csv(sell_out_path_for_good_file, index=False)
    else:
        sell_out.to_excel(path_for_news + "/sell_out.xlsx", index=False)
        show_notification("Вы не выбрали общих Sell_Out дистрибьютора, поэтому сохранился отдельный файл и не добавился в общие Sell_Out дистра")