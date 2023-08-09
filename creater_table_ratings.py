import pandas as pd
import pathlib as pathlib
from tkinter import Tk, messagebox, filedialog
import os

def show_notification(text):
    root = Tk()
    root.withdraw()  # Скрыть основное окно приложения
    messagebox.showinfo("Внимание", text)
    root.destroy()

# Получаем путь к папке, содержащей скрипт
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# все файлы прочитать
# s2b = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Санкт Петербург S2B ИП Дрига\Sell_Out_Санкт_Петербург_S2B.xlsx")
# smokelab = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Санкт-Петербург СмокЛаб\Sell_Out_Санкт_Петербург_СмокЛаб.xlsx")
# osh = pd.read_csv(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Москва OSHISHA\Sell_out_Москва_OSHISHA_2023.csv")
# nizhniy_par = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Нижний Новгород Пармаркет\Sell_Out_Нижний_Новгород_Пар_Маркет.xlsx")
# ekb_ural = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Екатеринбург Урал табак\Sell_Out_Екатеринбург_Уралтабак.xlsx")
# kazan_best = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Казань Best Shop\Sell_Out_Казань_Best_Shop.xlsx")
# barnaul_hookah_people = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Барнаул Hookah People\Sell_out_Барнаул_Hookah_People.xlsx")
# krasnodar_sklad = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Краснодар Склад\Sell_Out_Краснодар_Склад.xlsx")
# novosib_ugli = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Новосибирск Поставь Угли\Sell_Out_Новосибирск_Поставь_угли (только Новосибирск).xlsx")
# novosib_bs = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Новосибирск БС-Трейд\Sell_Out_Новосибирск_БС_Трейд.xlsx")
# novosib_filial = pd.read_excel(r"D:\Analysis Burn\Дистрибьютеры отчетность\Source\Отчеты\Новосибирск Филиал\sell_out_новосибирск_филиал.xlsx")

# собрать в одну
# osh = pd.concat([
#     s2b,
#     smokelab,
#     osh,
#     nizhniy_par,
#     ekb_ural,
#     kazan_best,
#     barnaul_hookah_people,
#     krasnodar_sklad,
#     novosib_ugli,
#     novosib_bs,
#     novosib_filial
# ])

# Отображаем диалоговое окно выбора продаж
sell_out_path = filedialog.askopenfilename(title="Выберите файл продаж для создания отчета SKU")

# сделать как путь
name_temp = pathlib.WindowsPath(sell_out_path)

name = name_temp.name

# убрать расширение
name = name.replace('.csv','')

name = name + "_SKU.xlsx"

osh = pd.read_excel(sell_out_path)


osh['Торговый представитель'] = osh['Торговый представитель'].str.lower()
osh['Код клиента'] = osh['Код клиента'].str.lower()
osh['Сегмент'] = osh['Сегмент'].str.lower()
osh['Клиент'] = osh['Клиент'].str.title()
osh['Адрес доставки'] = osh['Адрес доставки'].str.lower()
osh['Бренд'] = osh['Бренд'].str.title()
osh['Группа'] = osh['Группа'].str.title()
osh['Вкус'] = osh['Вкус'].str.title()

# преобразование типа в дату
def convert_date(date_series):
    if date_series[0:4].isdigit():
        # Попытка преобразования с yearfirst=True
        converted_dates = pd.to_datetime(date_series, yearfirst=True)
    else:
        # Если возникла ошибка, пробуем преобразовать с dayfirst=True
        converted_dates = pd.to_datetime(date_series, dayfirst=True)
    return converted_dates


if osh['Дата отгрузки'].dtypes != '<M8[ns]':
    osh['Дата отгрузки'] = osh['Дата отгрузки'].apply(convert_date)


osh["Год"] = osh["Дата отгрузки"].dt.year
osh["Месяц"] = osh["Дата отгрузки"].dt.month


osh_2 = osh.copy(deep=True)

osh_2.loc[:, 'Месяц название'] = osh_2.loc[:,'Год'].astype(str) + '-' + osh_2.loc[:, 'Месяц'].astype(str)


pivot_table = osh_2.pivot_table(values='ВЕС',
                             index=['Дистрибьютор','Клиент', 'Бренд', 'Вкус', 'Группа'],
                             columns='Месяц название',
                             aggfunc=lambda x: 1 if sum(x) > 0 else 0,
                             fill_value=0).reset_index()

pivot_table['Общая сумма'] = pivot_table.iloc[:, 5:].sum(axis=1)

pivot_table3 = osh_2.pivot_table(values='ВЕС',
                             index=['Дистрибьютор','Клиент', 'Бренд', 'Вкус'],
                             columns='Месяц название',
                             aggfunc=lambda x: 1 if sum(x) > 0 else 0,
                             fill_value=0).reset_index()

# здесь править цифру в iloc
pivot_table3['Общая сумма'] = pivot_table3.iloc[:, 4:].sum(axis=1)

pivot_table2 = pivot_table3.pivot_table(values='Клиент',
                             index=['Дистрибьютор','Бренд', 'Вкус'],
                             columns='Общая сумма',
                             aggfunc=pd.Series.count,
                             fill_value=0,
                             margins=False).reset_index()

columns = pivot_table.columns.values

pivot_table['Клиент_2'] = pd.NaT

# Добавление колонки 'Клиент1'
new_column = 'Клиент_2'
columns = [new_column] + [col for col in columns if col != new_column]

pivot_table = pivot_table[columns]


# загрузить файл дистрибьюторы где есть код
partners = pd.read_excel(r"D:\Analysis Burn\Дистрибьюторы Burn.xlsx", sheet_name='Дистрибьюторы')
#
#  правильное расположение колонок у первой таблицы
# 
columns = pivot_table.columns.values

pivot_table['Клиент_2'] = pd.NaT

# Добавление колонки 'Клиент1'
columns = ['Дистрибьютор'] + ['Клиент_2'] + [col for col in columns if col != 'Клиент_2' and col != 'Дистрибьютор']

pivot_table = pivot_table[columns]

pivot_table = pivot_table.merge(partners[['Город', 'Партнер', 'Уникальный идентификатор']], how='left', left_on= 'Дистрибьютор', right_on='Уникальный идентификатор')

columns = ['Город'] + ['Партнер'] + [col for col in columns if col != 'Дистрибьютор']

pivot_table = pivot_table[columns]

# 
# правильное расположение колонок у второй таблицы
# 
columns2 = pivot_table2.columns.values

pivot_table2 = pivot_table2.merge(partners[['Город', 'Партнер', 'Уникальный идентификатор']], how='left', left_on= 'Дистрибьютор', right_on='Уникальный идентификатор')

columns2 = ['Город'] + ['Партнер'] + [col for col in columns2 if col != 'Дистрибьютор']
pivot_table2 = pivot_table2[columns2]

# 
# 

# условное форматирование
pivot_table = pivot_table.style.background_gradient(subset=['Общая сумма'],cmap='YlGn')

with pd.ExcelWriter(r"C:\Users\User\Desktop" + "\\" + name) as writer:  
    pivot_table2.to_excel(writer, sheet_name='1', index=False)  
    pivot_table.to_excel(writer, sheet_name='2', index=False)